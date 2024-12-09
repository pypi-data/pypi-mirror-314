from ctypes import cdll, CDLL, RTLD_GLOBAL
from ctypes import POINTER, byref, c_int, c_int64, c_int32, c_bool, c_char_p, c_double, c_void_p, CFUNCTYPE, py_object, cast, byref, Structure, string_at
import ctypes
import traceback
'''
CDLL(MPI.__file__, mode=RTLD_GLOBAL) is a workaround for a few MPICH bugs, including 
the bug with non-working MPI_IN_PLACE and 2-stage ELPA solver
https://bitbucket.org/mpi4py/mpi4py/issues/162/mpi4py-initialization-breaks-fortran
https://lists.mpich.org/pipermail/discuss/2020-July/006018.html
https://github.com/pmodels/mpich/issues/4130
'''
from mpi4py import MPI
CDLL(MPI.__file__, mode=RTLD_GLOBAL)

import numpy as np
from numpy.ctypeslib import ndpointer

import sys
from pathlib import Path
import os, shutil
from ase import units
from scalapack4py import ScaLAPACK4py
from scalapack4py.blacsdesc import ctypes2ndarray
from scipy.linalg import lapack

class ASI_matrix_descr(Structure):
    _fields_ = [("matrix_type", c_int),
                ("storage_type", c_int)]

dmhs_callback = CFUNCTYPE(None, c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_double), POINTER(ASI_matrix_descr))  # void(*)(void *aux_ptr, int iK, int iS, int *blacs_descr, void *blacs_data, ASI_matrix_descr_t *matrix_descr)
set_dmhs_callback = CFUNCTYPE(c_int, c_void_p, c_int, c_int, POINTER(c_int), POINTER(c_double), POINTER(ASI_matrix_descr))  # void(*)(void *aux_ptr, int iK, int iS, int *blacs_descr, void *blacs_data, ASI_matrix_descr_t *matrix_descr)
esp_callback = CFUNCTYPE(None, c_void_p, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double))   # void(*)(void *aux_ptr, int n, const double *coords, double *potential, double *potential_grad)

class ASI_basis_func_descr_generic(Structure):
  '''
     Generic basis function descriptior.
     Use basis_func_descr_type field to find actual structure type
     in basis_func_descr_ptr_types dict
  '''
  _fields_ = [("descr_size",c_int), ("basis_func_descr_type",c_int),]

class ASI_basis_func_descr_generic_local(Structure):
  _fields_ = [("descr_size",c_int), ("basis_func_descr_type",c_int), ("atom_index",c_int),]

class ASI_basis_func_descr_aims(Structure):
    _fields_ = [("descr_size",c_int), ("basis_func_descr_type",c_int), \
    ("atom_index",c_int),
    ("func_type_ptr", c_char_p),
    ("func_type_len", c_int),
    ("n_qn",c_int),
    ("l_qn",c_int),
    ("m_qn",c_int)]
    
    @property
    def func_type(self):
      return string_at(self.func_type_ptr,self.func_type_len).decode('utf-8')

basis_func_descr_types = {101:ASI_basis_func_descr_generic_local, 102:ASI_basis_func_descr_aims}


def triang2herm_inplace(X, uplo):
  indices_func = {"L":np.triu_indices, "U":np.tril_indices}[uplo]
  diag_shift = {"L":1, "U":-1}[uplo]
  i_upper = indices_func(X.shape[0], diag_shift)
  X[i_upper] = X.T[i_upper].conj()

def triang_packed2full_hermit(data, n, is_real, uplo):
  lapack_triang2full = lapack.dtpttr if is_real else lapack.ztpttr
  n_triang = (n + 1)*n//2
  data_packed_shape = (n_triang, ) if is_real else (n_triang*2, ) # 
  data_packed = np.ctypeslib.as_array(data, shape=data_packed_shape)
  if not is_real:
    data_packed = data_packed.view(np.complex128).reshape((n_triang,))

  data, info = lapack_triang2full(n, data_packed, uplo=uplo)
  triang2herm_inplace(data, uplo)
  return data
  
def HS_to_DM(H, S, nelectrons=None, fermi_level=None):
  '''
    Compute density matrix from Hamiltonian (H) and overlap (S) matrices
    via generalized eigenproblem solving. No smearing is used. Full spin-paired 
    occupancy is assumed.

    Parameters
    ----------
    H : Hamiltonian matrix
    S : Overlap matrix
    nelectrons : number of electrons 
    fermi_level : Fermi level to define number of electrons

    Returns
    -------
    DM : ndarray[n, n]
      Density matrix
  '''
  assert nelectrons is None or fermi_level is None
  from scipy.linalg import eigh
  w,v = eigh(H,S)

  occupancy_number = 2 # number of electrons per orbital - full spin-paired

  if nelectrons is None:
    if fermi_level is None:
      fermi_level = 0.0
    n_occ = np.sum(w < fermi_level) # number of occupied orbitals by energy
  else:
    n_occ = nelectrons // occupancy_number
    assert  nelectrons % occupancy_number == 0
  
  DM = v[:,:n_occ] @ (np.eye(n_occ) * occupancy_number )@ v[:,:n_occ].conj().T

  return DM

def matrix_asi_to_numpy(asi, descr, data, matrix_descr_ptr):
    #if (matrix_descr_ptr.contents.storage_type==0):
  if (matrix_descr_ptr.contents.storage_type not in {1,2}): # temporary workaround in aims implementation
    data = asi.scalapack.gather_numpy(descr, data, asi.matrix_shape)
  elif (matrix_descr_ptr.contents.storage_type in {1,2}): # ASI_STORAGE_TYPE_TRIL,ASI_STORAGE_TYPE_TRIU
    assert not descr, "default_saving_callback supports only dense full ScaLAPACK arrays"
    assert matrix_descr_ptr.contents.matrix_type == 1, "Triangular packed storage is supported only for hermitian matrices"
    uplo = {1:'L',2:'U'}[matrix_descr_ptr.contents.storage_type]
    data = triang_packed2full_hermit(data, asi.n_basis, asi.is_hamiltonian_real, uplo)
  else:
    assert False, f"Unsupported storage_type {matrix_descr_ptr.contents.storage_type}"
  return data

def default_saving_callback(aux, iK, iS, descr, data, matrix_descr_ptr):
  '''
     In this implementation of a callback the performace is sacrificed for universality
  '''
  try:
    label = 'no-label'
    asi, storage_dict, cnt_dict, keep_history, label = cast(aux, py_object).value
    data = matrix_asi_to_numpy(asi, descr, data, matrix_descr_ptr)

    if data is not None:
      assert len(data.shape) == 2
      data = data.copy()
      if asi.implementation == "DFTB+":
        triang2herm_inplace(data, 'L')
      if keep_history:
        if (iK, iS) not in storage_dict:
          storage_dict[(iK, iS)] = []
        storage_dict[(iK, iS)].append(data)
      else:
        storage_dict[(iK, iS)] = data
        triang2herm_inplace(storage_dict[(iK, iS)], 'U')
    cnt_dict[(iK, iS)] = cnt_dict.get((iK, iS), 0) + 1
  except Exception as eee:
    print (f"Something happened in ASI default_saving_callback {label}: {eee}\nAborting...")
    print ("T:", traceback.format_exc())
    MPI.COMM_WORLD.Abort(1)

def default_loading_callback(aux, iK, iS, descr, data, matrix_descr_ptr):
  try:
    label = 'no-label'
    asi, storage_dict, label = cast(aux, py_object).value
    m = storage_dict[(iK, iS)] if asi.scalapack.is_root(descr) else None
    assert m is None or (asi.n_basis == m.shape[0]) and (asi.n_basis == m.shape[1]), \
                     f"m.shape=={m.shape} != asi.n_basis=={asi.n_basis}"
    asi.scalapack.scatter_numpy(m, descr, data, asi.hamiltonian_dtype)
    return 1 # signal that  matrix has been loaded
  except Exception as eee:
    print (f"Something happened in ASI default_loading_callback {label}: {eee}\nAborting...")
    traceback = eee.__traceback__
    while traceback:
        print(f"{traceback.tb_frame.f_code.co_filename} : {traceback.tb_lineno}")
        traceback = traceback.tb_next
    MPI.COMM_WORLD.Abort(1)

class ASIlib:
  '''
    Python wrapper for dynamically loaded library with ASI API implementation
  '''
  def __init__(self, lib_file: str, initializer, mpi_comm=None, atoms=None, work_dir='asi.temp', logfile='asi.log'):
    '''
      Constructor for ASI library wrapper. Library itself is NOT loaded here.
      
      Parameters
      ----------
        lib_file : str 
          Path to the ASI-implementing shared object library
        initializer : function 
          Function or callable object that is supposed to create input files for the library in `work_dir`
        mpi_comm : int 
          MPI communicator, if is `None`, then `mpi4py.MPI.COMM_WORLD` will be used
        atoms : ase.Atoms
          ASE Atoms object for calculations. An internal copy will be created
        work_dir : str
          Working dir for `ASI_init()`, `ASI_run()`, and `ASI_finalize()` calls
        logfile : str 
          Log file for the ASI library
    '''
    self.lib_file = Path(lib_file).resolve()
    self.initializer = initializer
    if mpi_comm is not None:
      self.mpi_comm = mpi_comm
    else:
      from mpi4py import MPI
      self.mpi_comm = MPI.COMM_WORLD
    self.atoms = atoms.copy() if atoms is not None else None
    self.work_dir = Path(work_dir)
    self.work_dir.mkdir(parents=True, exist_ok=True)
    self.logfile = logfile

  def __enter__(self):
    return self.init()

  def __exit__(self, type, value, traceback):
    #Exception handling here
    #print ("__exit__: ", type, value, traceback)
    self.close()  

  def init(self):
    """
      Calls `self.initializer` (see __init__ argument of the same name), 
      load the ASI-implementing shared object library using `ctypes.CDLL`, and
      calls `ASI_init()`. All of the above is performed in `self.work_dir` as a current directory.
      
       No ASI calls are should be attempted before that function call.
    """
    curdir = os.getcwd()
    try:
      os.chdir(self.work_dir)
      
      if self.mpi_comm.Get_rank() == 0:
        self.initializer(self)
      self.mpi_comm.Barrier()
    
      # Load the FHI-aims library
      # mode=RTLD_GLOBAL is necessary to get rid of the error with MKL:
      # 		`INTEL MKL ERROR: /opt/intel/oneapi/mkl/2021.4.0/lib/intel64/libmkl_avx512.so.1: undefined symbol: mkl_sparse_optimize_bsr_trsm_i8.`
      # Details: https://bugs.launchpad.net/ubuntu/+source/intel-mkl/+bug/1947626
      self.lib = CDLL(self.lib_file, mode=RTLD_GLOBAL)
      self.scalapack = ScaLAPACK4py(self.lib)

      self.lib.ASI_n_atoms.restype = c_int
      self.lib.ASI_energy.restype = c_double
      self.lib.ASI_forces.restype = POINTER(c_double)
      if hasattr(self.lib, "ASI_stress"):
        self.lib.ASI_stress.restype = POINTER(c_double)
      self.lib.ASI_atomic_charges.restype = POINTER(c_double)
      self.lib.ASI_atomic_charges.argtypes  = [c_int,]
      self.lib.ASI_calc_esp.argtypes = [c_int, ndpointer(dtype=np.float64), ndpointer(dtype=np.float64), ndpointer(dtype=np.float64)]
      self.lib.ASI_register_dm_callback.argtypes = [dmhs_callback, c_void_p]
      self.lib.ASI_register_overlap_callback.argtypes = [dmhs_callback, c_void_p]
      self.lib.ASI_register_hamiltonian_callback.argtypes = [dmhs_callback, c_void_p]
      if hasattr(self.lib, "ASI_register_dm_init_callback"):
        self.lib.ASI_register_dm_init_callback.argtypes = [set_dmhs_callback, c_void_p]
      self.lib.ASI_register_external_potential.argtypes = [esp_callback, c_void_p];
      self.lib.ASI_is_hamiltonian_real.restype = c_bool
      self.lib.ASI_get_basis_size.restype = c_int
      if hasattr(self.lib, "ASI_get_basis_func_descr"):
        self.lib.ASI_get_basis_func_descr.restype = POINTER(ASI_basis_func_descr_generic)
        self.lib.ASI_get_basis_func_descr.argtypes = [c_int,]
      self.lib.ASI_get_nspin.restype = c_int
      self.lib.ASI_get_nkpts.restype = c_int
      self.lib.ASI_get_n_local_ks.restype = c_int
      self.lib.ASI_get_local_ks.restype = c_int
      self.lib.ASI_get_local_ks.argtypes = [ndpointer(dtype=np.int32),]
      if hasattr(self.lib, "ASI_is_scf_converged"):
        self.lib.ASI_is_scf_converged.restype = c_bool
      
      input_filename = {1:"dummy", 2:"dftb_in.hsd"}[self.lib.ASI_flavour()]
      self.lib.ASI_init(input_filename.encode('UTF-8'), self.logfile.encode('UTF-8'), c_int(self.mpi_comm.py2f()))
      if (self.lib.ASI_flavour() == 2):
        self.set_geometry() # DFTB+ ignores geometry from input files if used via API
      return self
    except Exception as err:
      print("Some error in ASIlib.init:", err)
      print ("traceback:\n", traceback.format_exc())
    finally:
      os.chdir(curdir)
  
  def close(self):
    '''
      Calls `ASI_finalize()`. No ASI calls are should be attempted after that function call.
    '''
    if not hasattr(self, 'lib'):
      return # allready closed

    curdir = os.getcwd()
    try:
      os.chdir(self.work_dir)
      self.lib.ASI_finalize()
      handle = self.lib._handle
      del self.lib
      if self.mpi_comm.Get_rank() == 0:
        os.system(f"cat {self.logfile} >> total.log")
    finally:
      os.chdir(curdir)
    
  def run(self):
    """
      Run calculation
      
      Calls `ASI_run()`
    """
    curdir = os.getcwd()
    try:
      os.chdir(self.work_dir)
      self.lib.ASI_run()
    except Exception as err:
      print(f"Exception, {err}")
    finally:
      os.chdir(curdir)

  def register_DM_init(self, dm_init_callback, dm_init_aux):
    """
      Register callback function to be called on Density Matrix initilaization before SCF loop
      
      Calls `ASI_register_dm_init_callback()`

      Parameters
      ----------
      dm_init_callback : dmhs_callback
        Callback function
      dm_init_aux : Object
        Auxiliary object for the callback
    """
    self.dm_init_callback = set_dmhs_callback(dm_init_callback)
    self.dm_init_aux = dm_init_aux
    self.lib.ASI_register_dm_init_callback(self.dm_init_callback, c_void_p.from_buffer(py_object(self.dm_init_aux)))

  def register_overlap_callback(self, overlap_callback, overlap_aux):
    """
      Register callback function to be called on overlap matrix calculation
      
      Calls `ASI_register_overlap_callback()`

      Parameters
      ----------
      overlap_callback : dmhs_callback
        Callback function
      overlap_aux : Object
        Auxiliary object for the callback
    """
    self.overlap_callback = dmhs_callback(overlap_callback)
    self.overlap_aux = overlap_aux
    self.lib.ASI_register_overlap_callback(self.overlap_callback, c_void_p.from_buffer(py_object(self.overlap_aux)))

  def register_hamiltonian_callback(self, hamiltonian_callback, hamiltonian_aux):
    """
      Register callback function to be called on hamiltonian matrix calculation
      
      Calls `ASI_register_hamiltonian_callback()`

      Parameters
      ----------
      hamiltonian_callback : dmhs_callback
        Callback function
      hamiltonian_aux : Object
        Auxiliary object for the callback
    """
    self.hamiltonian_callback = dmhs_callback(hamiltonian_callback)
    self.hamiltonian_aux = hamiltonian_aux
    self.lib.ASI_register_hamiltonian_callback(self.hamiltonian_callback, c_void_p.from_buffer(py_object(self.hamiltonian_aux)))

  def register_dm_callback(self, dm_callback, dm_aux):
    """
      Register callback function to be called on Density Matrix calculation
      
      Calls `ASI_register_dm_callback()`

      Parameters
      ----------
      dm_callback : dmhs_callback
        Callback function
      dm_aux : Object
        Auxiliary object for the callback
    """
    self.dm_callback = dmhs_callback(dm_callback)
    self.dm_aux = dm_aux
    self.lib.ASI_register_dm_callback(self.dm_callback, c_void_p.from_buffer(py_object(self.dm_aux)))

  def register_external_potential(self, ext_pot_func, ext_pot_aux_obj):
    """
      Register callback function for evaliation of external electrostatic potential
      
      Calls `ASI_register_external_potential()`

      Parameters
      ----------
      ext_pot_func : esp_callback
        Callback function
      ext_pot_aux_obj : Object
        Auxiliary object for the callback
    """
    self.ext_pot_func = esp_callback(ext_pot_func)
    self.ext_pot_aux_obj = ext_pot_aux_obj
    self.lib.ASI_register_external_potential(self.ext_pot_func, c_void_p.from_buffer(py_object(self.ext_pot_aux_obj)))

  def calc_esp(self, coords):
    """
      Compute electrostatic potential (ESP) and its gradient in arbitrary points
      
      Calls `ASI_calc_esp()`

      Parameters
      ----------
      coords : c_double[n, 3]
        Coordinates of points to compute ESP and its gradient
      
      Returns
      -------
      esp : c_double[n]
        ESP in corresponding points
      esp_grad : c_double[n, 3]
        ESP gradient in corresponding points
    """
    n = len(coords)
    esp = np.zeros((n,), dtype=c_double)
    esp_grad = np.zeros((n,3), dtype=c_double)
    self.lib.ASI_calc_esp(c_int(n), coords.ravel(), esp, esp_grad) 
    return esp, esp_grad

  @property
  def flavour(self):
    """
      int: ID of ASI implementation flavour
      
      Calls `ASI_flavour()`
    """
    return self.lib.ASI_flavour()
  
  @property
  def implementation(self):
    """
      str: Name of ASI implementation
      
      Calls `ASI_flavour()`
    """
    return {1:"FHI-AIMS", 2:"DFTB+"}[self.flavour]

  @property
  def n_atoms(self):
    """
      int: Number of atoms of the system

      Calls `ASI_n_atoms()`
    """
    return self.lib.ASI_n_atoms()

  @property
  def n_basis(self):
    """
      int: Number of basis functions

      Calls `ASI_get_basis_size()`
    """
    return self.lib.ASI_get_basis_size()
    
  @property
  def matrix_shape(self):
    '''
      int: Expected shape of H, S, or density matrices.
      
      (n_basis, n_basis) if matrices are real. (n_basis, n_basis, 2) if matrices are complex - last dimension is for Re/Im parts
    '''
    return (self.n_basis,self.n_basis) if self.is_hamiltonian_real else (self.n_basis,self.n_basis, 2) # resulting shape
  
  def get_basis_func_descr(self, bf_index):
    if not hasattr(self.lib, "ASI_get_basis_func_descr"):
      raise NotImplementedError("ASI_get_basis_func_descr not implemented in {self.lib_file}")
    
    descr_ptr = self.lib.ASI_get_basis_func_descr(bf_index)
    descr_ptr_specific = cast(descr_ptr, POINTER(basis_func_descr_types[descr_ptr.contents.basis_func_descr_type]))
    return descr_ptr_specific.contents

  @property
  def basis_atoms(self):
    """
      int[n_basis]: Atomic indices for each basis function

      Calls `ASI_get_basis_func_descr()` and `ASI_get_basis_size()`
    """
    return np.array([self.get_basis_func_descr(i).atom_index for i in range(self.n_basis)])

  @property
  def n_spin(self):
    """
      int: Number of spin channels

      Calls `ASI_get_nspin()`
    """
    return self.lib.ASI_get_nspin()

  @property
  def n_kpts(self):
    """
      int: Number of k-points

      Calls `ASI_get_nkpts()`
    """
    return self.lib.ASI_get_nkpts()

  @property
  def n_local_ks(self):
    """
      int: Number of pairs (k-point, spin-chanel-index) processed by current MPI process

      Calls `ASI_get_n_local_ks()`
    """
    return self.lib.ASI_get_n_local_ks()

  @property
  def local_ks(self):
    """
      int[n_local_ks * 2]: List of pairs (k-point, spin-chanel-index) processed by current MPI process

      Calls `ASI_get_local_ks()`
    """
    n = self.n_local_ks
    res = np.zeros((n*2,), dtype=c_int32)
    n2 =  self.lib.ASI_get_local_ks(res)
    assert n == n2
    return res.reshape((n, 2))

  @property
  def is_hamiltonian_real(self):
    """
      bool: `True`  if Hamiltonian of current system is real. `False` if Hamiltonian of current system is complex.
      
      Calls `ASI_is_hamiltonian_real()`
    """
    return self.lib.ASI_is_hamiltonian_real()

  @property
  def hamiltonian_dtype(self):
    """
      numpy.dtype: numpy.float64  if Hamiltonian of current system is real. numpy.complex128 if Hamiltonian of current system is complex.
      
      Calls `ASI_is_hamiltonian_real()`
    """
    return np.float64 if self.is_hamiltonian_real else np.complex128

  @property
  def is_scf_converged(self):
    """
      bool: `True`  if SCF loop is converged.
      
      Calls `ASI_is_scf_converged()`
    """
    return self.lib.ASI_is_scf_converged()

  @property
  def total_forces(self):
    """
      c_double[n_atoms, 3 ]: Total forces acting on system atoms.
      
      Calls `ASI_forces()`
    """
    forces_ptr = self.lib.ASI_forces()
    if forces_ptr:
      return np.ctypeslib.as_array(forces_ptr, shape=(self.n_atoms, 3))
    else:
      return None

  @property
  def stress(self):
    """
      c_double[3, 3 ]: Stress tensor of the periodic system
      
      Calls `ASI_stress()`
    """
    stress_ptr = self.lib.ASI_stress()
    if stress_ptr:
      return np.ctypeslib.as_array(stress_ptr, shape=(3, 3))
    else:
      return None

  @property
  def atomic_charges(self):
    """
      c_double[n_atoms]: Atomic charges. Default partitioning scheme is implementation-dependent
      
      Calls `ASI_atomic_charges(-1)` (`-1` for default partitioning scheme)
    """
    chg_ptr = self.lib.ASI_atomic_charges(-1)
    if chg_ptr:
      return np.ctypeslib.as_array(chg_ptr, shape=(self.n_atoms,)).copy()
    else:
      return None

  @property
  def total_energy(self):
    """
      c_double: Total energy of the system
      
      Calls `ASI_energy()`
    """
    return self.lib.ASI_energy()
  
  def set_geometry(self):
    coords_ptr = (self.atoms.positions / units.Bohr).ctypes.data_as(c_void_p)
    if any(self.atoms.pbc):
      lattice_ptr = (self.atoms.cell.ravel() / units.Bohr).ctypes.data_as(c_void_p)
      self.lib.ASI_set_geometry(coords_ptr, len(self.atoms), lattice_ptr)
    else:
      self.lib.ASI_set_atom_coords(coords_ptr, len(self.atoms))

  @property
  def keep_density_matrix(self):
    """
      bool : Flag to save Density Matrix in `self.dm_storage` dict and count number
        of the matrix calculations in `self.dm_calc_cnt` dict.
        The flag may be set to `True` to save only the last SCF interation matrix,
        or to `"history"` to save matrices for each SCF iteration.
        
        Dictionaries are indexed by (k-point, spin-chanel-index) pairs.
    """
    return hasattr(self, 'dm_callback')

  @keep_density_matrix.setter
  def keep_density_matrix(self, value):
    assert value, 'callback unsetting not implemented'
    if self.keep_density_matrix:
      self.dm_storage.clear()
      self.dm_calc_cnt.clear()
      return

    self.dm_storage = {}
    self.dm_calc_cnt = {}
    self.register_dm_callback(default_saving_callback, (self, self.dm_storage, self.dm_calc_cnt, value=='history', 'DM calc'))

  @property
  def keep_hamiltonian(self):
    """
      bool : Flag to save Hamiltonian matrix in `self.hamiltonian_storage` dict and count number
        of the matrix calculations in `self.hamiltonian_calc_cnt` dict.
        The flag may be set to `True` to save only the last SCF interation matrix,
        or to `"history"` to save matrices for each SCF iteration.
        
        Dictionaries are indexed by (k-point, spin-chanel-index) pairs.
    """
    return hasattr(self, 'hamiltonian_callback')

  @keep_hamiltonian.setter
  def keep_hamiltonian(self, value):
    assert value, 'callback unsetting not implemented'
    if self.keep_hamiltonian:
      self.hamiltonian_storage.clear()
      self.hamiltonian_calc_cnt.clear()
      return

    self.hamiltonian_storage = {}
    self.hamiltonian_calc_cnt = {}
    self.register_hamiltonian_callback(default_saving_callback, (self, self.hamiltonian_storage, self.hamiltonian_calc_cnt, value=='history', 'H calc'))

  @property
  def keep_overlap(self):
    """
      bool : Flag to save overlap matrix in `self.overlap_storage` dict and count number
        of the matrix calculations in `self.overlap_calc_cnt` dict.

        Dictionaries are indexed by (k-point, spin-chanel-index) pairs.
    """
    return hasattr(self, 'overlap_callback')

  @keep_overlap.setter
  def keep_overlap(self, value):
    assert value, 'callback unsetting not implemented'
    if self.keep_overlap:
      self.overlap_storage.clear()
      self.overlap_calc_cnt.clear()
      return

    self.overlap_storage = {}
    self.overlap_calc_cnt = {}
    self.register_overlap_callback(default_saving_callback, (self, self.overlap_storage, self.overlap_calc_cnt, False, 'S calc'))

  @property
  def init_density_matrix(self):
    """
      bool / c_double[n_basis, n_basis] : Set with a density matrix t be used for SCF loop initialization.
      Reading that property returns True if the density matrix initialization is enabled
    """
    return hasattr(self, 'dm_init_callback')
 
  @init_density_matrix.setter
  def init_density_matrix(self, value):
    self.dm_init_storage = value
    self.register_DM_init(default_loading_callback, (self, self.dm_init_storage, 'DM init'))

