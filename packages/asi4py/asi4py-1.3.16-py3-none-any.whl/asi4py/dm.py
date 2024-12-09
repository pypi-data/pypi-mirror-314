from ctypes import cdll, CDLL, RTLD_GLOBAL
from ctypes import POINTER, byref, c_int, c_int64, c_int32, c_bool, c_char_p, c_double, c_void_p, CFUNCTYPE, py_object, cast, byref, Structure
import ctypes

from scipy.linalg import block_diag
from ase.data import chemical_symbols
from ase.geometry import get_distances
import ase, os, warnings
import numpy as np
import numpy.typing as npt
from typing import List, Any
from scipy.io import netcdf_file
from asi4py.pyasi import matrix_asi_to_numpy
from scipy.optimize import LinearConstraint, minimize


def free_energy_fun(x, E, beta):
  '''
    Free energy
  '''
  return np.sum(x * (E*beta - np.log(x)))

def free_energy_jac(x, E, beta):
  '''
    Free energy gradient
  '''
  return E*beta - np.log(x)-1

def get_elems_ordered(atoms):
  '''
    List elements in the order of tiers.
    https://gitlab.com/ase/ase/-/commit/7b70eddd026154d636faf404cc2f8c7b08d89667
    https://mail.python.org/pipermail/python-dev/2017-December/151283.html
  '''
  return list(dict.fromkeys(atoms.symbols))

def split_dm(dm, magmom:float, iS:int):
  '''
    Split spin-paired density matrix into up/down spin-polarizes DM
  '''
  w,v = np.linalg.eigh(dm)
  w /= 2
  w_positive_indices = np.where(w>0)[0]
  E = -np.log(w[w_positive_indices])
  n_avg = np.sum(w)
  n_up   = n_avg + magmom/2
  n_down = n_avg - magmom/2
  b_eq = n_up if iS==1 else n_down
  w_new = minimize(lambda x: free_energy_fun(x, E, 0.1) , w[w_positive_indices], jac=lambda x: free_energy_jac(x, E, 0.1), bounds=[(1e-10, 1.0) for _ in E], constraints=[LinearConstraint(np.ones((1, len(E))), b_eq, b_eq), ] ).x
   
  w[w_positive_indices] = w_new
  return v @ np.diag(w) @ v.T

def build_dm_free_atoms(atoms, elem_dms, n_spin:int, iS:int):
  '''
    Build atoms density matrix from single-atomic matrices for each element
    :param n_spin: number of spin channels. 1 or 2.
    :param iS: index of the spin channel. 1 or 2.
  '''
  assert n_spin in [1,2], n_spin
  
  atomic_dms = [elem_dms[s] for s in atoms.symbols]
  if n_spin==2:
    atomic_dms = [split_dm(dm,magmom,iS) for dm,magmom in zip(atomic_dms, atoms.get_initial_magnetic_moments())]

  return np.asfortranarray(block_diag(*atomic_dms))

def load_atomic_dm(elem:str, path:str=None):
  if path is None:
    path = os.environ['ASI_FREE_ATOM_DMS']
  elemZ = chemical_symbols.index(elem)
  with netcdf_file(f'{path}/{elemZ:03d}_{elem}.ncdf', mmap=False) as f:
    return f.variables['DM'].data

def save_atomic_dm(dm, elem:str, path:str=None):
  '''
    Save density matrix for element `elem` into file `{path}/{elemZ:03d}_{elem}.ncdf`
    If `path` is `None` then it defaults to environment variable `ASI_FREE_ATOM_DMS`
    This files maybe used by :class:`PredictFreeAtoms` predictor
  '''
  if path is None:
    path = os.environ['ASI_FREE_ATOM_DMS']
  elemZ = chemical_symbols.index(elem)
  with netcdf_file(f'{path}/{elemZ:03d}_{elem}.ncdf','w', mmap=False) as f:
    f.createDimension('n_basis', dm.shape[0])
    f.createVariable('DM', dm.dtype, ('n_basis', 'n_basis'))[:,:] = dm

def bool2int_selector(atoms_selector):
  atoms_selector = np.array(atoms_selector)
  if np.issubdtype(atoms_selector.dtype, bool):
    atoms_selector = np.where(atoms_selector)[0]
  assert np.issubdtype(atoms_selector.dtype, np.integer)
  return atoms_selector

class PredictDMByAtoms:
  '''
    This is a base class for density matrix predictors. It is meant to be subclassed.
    Subclasses must overwrite the method :func:`PredictDMByAtoms.__call__` that takes :class:`ase.Atoms` object as argument
    and returns :class:`numpy.ndarray` with a density matrix guess.
  '''
  def __init__(self):
    pass
  
  def register_DM_init(self, asi):
    '''
      Register this density matrix predictor as an ASI callback for density matrix initialization
      
      :param asi: an instance of :class:`asi4py.pyasi.ASILib`
      
    '''
    self.asi = asi
    asi.register_DM_init(PredictDMByAtoms.dm_init_callback, self)

  def dm_init_callback(self, iK, iS, blacs_descr, data, matrix_descr_ptr):
    '''
      ASI DM init callback. Not to be invoked directly.
    '''
    self = cast(self, py_object).value
    n_basis = self.asi.n_basis
    m = self(self.asi.atoms, iK, iS) if self.asi.scalapack.is_root(blacs_descr) else None
    
    assert m is None or (m.shape == (n_basis, n_basis)), \
                     f"m.shape=={m.shape} != n_basis=={n_basis}"
    self.asi.scalapack.scatter_numpy(m, blacs_descr, data, self.asi.hamiltonian_dtype)
    return 1

  def __call__(self, atoms, iK:int=1, iS:int=1):
    '''
      This method is meant to be overwritten by derived classes.
    '''
    raise RuntimeError("Not implemented in base class")
    #return build_dm_free_atoms(atoms, self.elem_dms)

class PredictFreeAtoms(PredictDMByAtoms):
  '''
    Density matrix predictor that uses single-atomic density matrices for initialization.
    See :class:`PredictFreeAtoms.__init__` for details
  '''
  def __init__(self, elem_dms:dict[str, Any]=None, elem_dm_path:str=None,  n_spin:int=1, hamiltonian_dtype:np.dtype=np.float64):
    '''
      If ``elem_dms`` parameter is not ``None``, then ``elem_dm_path`` should be ``None`.
      If both ``elem_dms`` and ``elem_dm_path`` are ``None``, then  ``elem_dm_path` value
      defaults to the ``ASI_FREE_ATOM_DMS`` environment variable.
      
      :param elem_dms: a dictionary that maps chemical elements to its density matrices
      :param elem_dm_path: a path to a folder that contains `*.npz` files with density matrices of chemical elements
      :param n_spin:  number of spin channels, should be 2 if initial magnetic moment is specified
      :param hamiltonian_dtype: dtype of Hamiltonian and DM
    '''
    super().__init__()
    self.n_spin = n_spin
    self.hamiltonian_dtype = hamiltonian_dtype
    assert (elem_dms is None) or (elem_dm_path is None)
    self.elem_dms = elem_dms
    if self.elem_dms is None:
      self.elem_dm_path = elem_dm_path if elem_dm_path is not None else os.environ['ASI_FREE_ATOM_DMS']

  def __call__(self, atoms, iK:int=1, iS:int=1):
    if self.elem_dms is None:
      assert self.elem_dm_path is not None
      self.elem_dms = {elem:load_atomic_dm(elem, self.elem_dm_path) for elem in get_elems_ordered(atoms)}
    DM = build_dm_free_atoms(atoms, self.elem_dms, self.n_spin, iS)
    
    if iK != 1:
      DM = np.zeros(DM.shape, order='F')
    
    return DM.astype(self.hamiltonian_dtype)

class PredictConstAtoms(PredictDMByAtoms):
  '''
    Density matrix predictor that returns a density matrix passed to its constructor, independently from
    atomic coordinates.
  '''
  def __init__(self, const_atoms:ase.Atoms, const_dm:Any):
    '''
      :param const_atoms: :class:`ase.Atoms` object that is only used for checking order of chemical elements on density matrix prediction
      :param const_dm: a density matrix that will be returned as initial guess on SCF loop initialization
    '''
    super().__init__()
    self.const_atoms = const_atoms
    self.const_dm = const_dm

  def __call__(self, atoms, iK:int=1, iS:int=1):
    np.testing.assert_allclose(atoms.numbers, self.const_atoms.numbers)
    
    np.testing.assert_allclose(
      atoms.positions - atoms.get_center_of_mass(), 
      self.const_atoms.positions - self.const_atoms.get_center_of_mass(), 
      atol=1e-1, rtol=1e-1)
    
    if isinstance(self.const_dm, dict):
      DM = self.const_dm[(iK, iS)]
    else:
      DM = self.const_dm

    return DM

def select_basis_indices(all_basis_atoms, atoms_indices):
  '''
    Returns indices of basis functions for selected atoms.
    
    :param all_basis_atoms: atomic indices for all basis functions
    :param atoms_indices: indices of selected atoms
  '''
  return np.where(np.any(all_basis_atoms[None,:] == atoms_indices[:, None], axis=0))[0]

class PredictFrankensteinDM(PredictDMByAtoms):
  '''
    Density matrix predictor that "stitches" full density matrix prediction from 
    predictions of multiples predictors of smaller, possibly overlapping subsystems of the full system.
  '''
  def __init__(self, predictors_and_selectors:list[tuple[PredictDMByAtoms, list[int]]]):
    '''
      :param predictors_and_selectors: list of pairs. The first pair element is callable, that 
        should return predicted density matrix for a subsystem; it can be derived from :class:`PredictDMByAtoms`.
        The second pair element is the list of atomc that constitute the subsystem.
        
    '''
    # unzip https://stackoverflow.com/a/12974504/3213940
    self.predictors, atoms_selectors = list(zip(*predictors_and_selectors))
    self.atoms_groups_indices = list(map(bool2int_selector, atoms_selectors))

    if True: # extended assertion check
      all_selected_atoms_set = set().union(*self.atoms_groups_indices)
      max_range_atoms_set = set(range(max(all_selected_atoms_set) + 1))
      missed_atoms = max_range_atoms_set - all_selected_atoms_set
      # Heuristic check: doesn't guarantie full atoms coverage, because actual
      # number of atoms is not known here and max(all_selected_atoms_set) is 
      # just an heuristic
      assert len(missed_atoms) == 0, f"Missed atoms: {missed_atoms}"
  
  def register_DM_init(self, asi):
    super().register_DM_init(asi)
    self.init_basis_indices(asi)

  def init_basis_indices(self, asi):
    '''
      Loads indices of basis functions for subsystems from an ASI library.
      It should only be called if one is going to predict density matrix without registering 
      this predictor via :func:`PredictDMByAtoms.register_DM_init`
    '''
    all_basis_atoms = asi.basis_atoms
    self.basis_indices = [select_basis_indices(all_basis_atoms, atoms_group) for atoms_group in self.atoms_groups_indices]
    self.n_basis = asi.n_basis

    if True:
      all_selected_basis_indices = set().union(*self.basis_indices)
      total_basis_set = set(range(self.n_basis))
      missed_basis_functions = total_basis_set - all_selected_basis_indices
      assert len(missed_basis_functions) == 0, f'Basis functions missed from selection: {missed_basis_functions}'

  def __call__(self, atoms, iK:int=1, iS:int=1):
    assert len(self.predictors) == len(self.atoms_groups_indices)
    assert len(self.predictors) == len(self.basis_indices)

    total_dm = np.zeros((self.n_basis, self.n_basis), dtype=np.float64)
    total_dm_cnt = np.zeros(total_dm.shape, dtype=int)
    for predictor, atoms_group_indices, basis_group_indices in zip(self.predictors, self.atoms_groups_indices, self.basis_indices):
      total_dm[basis_group_indices[np.newaxis,:], basis_group_indices[:, np.newaxis]] += predictor(atoms[atoms_group_indices])
      total_dm_cnt[basis_group_indices[np.newaxis,:], basis_group_indices[:, np.newaxis]] += 1
    
    assert (total_dm[total_dm_cnt==0]==0).all()
    total_dm_cnt[total_dm_cnt==0] = 1 # to avoid division by zero

    return np.divide(total_dm, total_dm_cnt, order='F') # instead of  (total_dm / total_dm_cnt).T


def KR_predict(X, Y, x, alpha, kernel):
  '''
    KernelRidge regression with support of complex valued dependent variables Y
  '''
  from sklearn.kernel_ridge import KernelRidge

  with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="Ill-conditioned matrix")
    reg = KernelRidge(alpha=alpha, kernel=kernel)
    if Y.dtype!=np.complex128:
      reg.fit(X, Y)
      y = reg.predict(x)
    else:
      reg.fit(X, Y.real)
      y_real = reg.predict(x)
      reg = KernelRidge(alpha=alpha, kernel=kernel)
      reg.fit(X, Y.imag)
      y_imag = reg.predict(x)
      y = y_real + 1.0j*y_imag
    return y

class PredictSeqDM(PredictDMByAtoms):
  '''
    Extrapolates density matrix using kernel ridge regression from a few previous geometries.
    This predictor uses another predictor as a baseline and extrapolates only deviations of 
    baseline predictors from ground-state density matrices.
    The method :func:`PredictSeqDM.update_errs` should be invoked after SCF convergence to provide
    the predictor with ground-state density matrix, for extrapolation model adjustment.
    
  '''
  class PredictionSequence:
    '''
      This class stores sequences for DM predictions for a single (iK,iS) pair,
      and uses them to fit a KernelRidge model
    '''
    def __init__(self, baseline_as_feature:bool, alpha:float, rbf_length_scale:float):
      self.preds = []   # baseline predictions
      self.descrs = []  # structure descriptors
      self.errs = []    # differences between baseline predictions and ground state DMs
      self.predicted_errs = []  # FOR DEBUGGING ONLY: predicted differences between baseline predictions and ground state DMs
      self.baseline_as_feature=baseline_as_feature # use baseline prediction as independent variable for extrapolation
      self.alpha = alpha
      self.rbf_length_scale = rbf_length_scale

    def predict_err(self, predicted_dm, descr):
      from sklearn.gaussian_process.kernels import RBF
      k = len(self.preds)
      assert k == len(self.descrs), f'{k=} {len(self.descrs)=}'
      assert k == len(self.errs), f'{k=} {len(self.errs)=}'
      if k == 0:
        return np.zeros(predicted_dm.shape, order='F')

      X = [np.array(self.descrs).reshape((k, -1)), ]
      x = [descr.ravel(), ]
      if (self.baseline_as_feature):
        X = [np.array(self.preds).reshape((k, -1)), ] + X
        x = [predicted_dm.ravel(), ] + x

      X = np.hstack(X)
      x = np.hstack(x).reshape((1, -1))
      
      Y = np.array(self.errs).reshape((k, -1))

      X_mean = np.mean(X, axis=0)
      Y_mean = np.mean(Y, axis=0)
      
      X -= X_mean
      Y -= Y_mean
      x -= X_mean
      #------------------

      rbf_length_scale = np.sqrt(0.5*X.shape[1]) if self.rbf_length_scale is None else self.rbf_length_scale # equivalent of"rbf" by default
      y = KR_predict(X, Y, x, self.alpha, RBF(length_scale=rbf_length_scale)) 

      #------------------
      y += Y_mean
      P = np.asfortranarray(y.reshape(predicted_dm.shape))
      return P
      
  
  def __init__(self, base_predictor:PredictDMByAtoms, n_hist:int, baseline_as_feature=True ,alpha=1e-15, rbf_length_scale=None):
    '''
      :param base_predictor: Baseline predictor, for example :class:`PredictFreeAtoms` or :class:`PredictFrankensteinDM` 
      :param n_hist: history size for extrapolation
      :param baseline_as_feature: use baseline prediction as independent variable for extrapolation
      :param alpha: alpha parameter for sklearn.kernel_ridge.KernelRidge
      :param rbf_length_scale: length_scale parameter for sklearn.gaussian_process.kernels.RBF
    '''
    self.base_predictor = base_predictor
    self.predseq = {} # dict (iK,iS):PredictionSequence
    self.n_hist = n_hist
    self.baseline_as_feature = baseline_as_feature
    self.alpha = alpha
    self.rbf_length_scale = rbf_length_scale

  
  def __call__(self, atoms, iK:int=1, iS:int=1):
    predicted_dm = self.base_predictor(atoms, iK, iS)

    R,d = get_distances(atoms.positions, cell=atoms.cell, pbc=atoms.pbc)
    lowtri = np.tri(len(atoms), len(atoms), -1)==1
    invd = 1/d[lowtri]
    descr = invd
    #descr = atoms.positions
    #descr = atoms.calc.asi.overlap_storage[iK, iS].copy()

    if (iK, iS) not in self.predseq:
      self.predseq[(iK, iS)] = PredictSeqDM.PredictionSequence(self.baseline_as_feature, self.alpha, self.rbf_length_scale)

    predicted_err = self.predseq[(iK, iS)].predict_err(predicted_dm, descr)

    if len(self.predseq[(iK, iS)].preds) == self.n_hist:
      self.predseq[(iK, iS)].preds.pop(0)
      self.predseq[(iK, iS)].descrs.pop(0)
      self.predseq[(iK, iS)].errs.pop(0)
      self.predseq[(iK, iS)].predicted_errs.pop(0)
    self.predseq[(iK, iS)].preds.append(predicted_dm.copy())
    self.predseq[(iK, iS)].descrs.append(descr.copy())
    self.predseq[(iK, iS)].predicted_errs.append(predicted_err.copy())

    DM = np.subtract(predicted_dm, predicted_err, order='F')
    
    #print(f"predicted_err {iK=}", np.linalg.norm(predicted_err), f"base_predictor", np.linalg.norm(predicted_dm), "DM=", np.linalg.norm(DM))
    return DM

  def register_DM_init(self, asi):
    '''
      Register this density matrix predictor as an ASI callback for density matrix initialization,
      and registers itself to process DM evaluation callback for errors update.
      
      :param asi: an instance of :class:`asi4py.pyasi.ASILib`
      
    '''
    super().register_DM_init(asi)
    asi.dm_calc_cnt = {}
    asi.dm_storage = {}
    asi.register_dm_callback(PredictSeqDM._dm_callback, self)

  def _dm_callback(self, iK, iS, descr, data, matrix_descr_ptr):
    self = cast(self, py_object).value
    self.asi.dm_calc_cnt[(iK, iS)] = self.asi.dm_calc_cnt.get((iK, iS),0) + 1
    data = matrix_asi_to_numpy(self.asi, descr, data, matrix_descr_ptr)
    if data is not None:
      if (iK, iS) not in self.asi.dm_storage:
        self.asi.dm_storage[(iK, iS)] = []
      self.asi.dm_storage[(iK, iS)].append(data.copy())
  
  def update_errs(self):
    '''
      This method should be called after SCF convergence, to adjust extrapolation model.
    '''
    for (iK, iS),pred_item in self.predseq.items():
      assert len(pred_item.preds) == len(pred_item.errs) + 1
      pred_item.errs.append(pred_item.preds[-1] - self.asi.dm_storage[(iK, iS)][-1])
      #print(f"Error {iK=}", np.linalg.norm(pred_item.errs[-1] - pred_item.predicted_errs[-1]), np.linalg.norm(pred_item.preds[-1]), np.linalg.norm(self.asi.dm_storage[(iK, iS)]))
      self.asi.dm_calc_cnt[(iK, iS)] = 0
    
    self.register_DM_init(self.asi)
  




