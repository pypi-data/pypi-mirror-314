"""
A base class for global optimization including:

- WFS
- DFS
- QRS
"""
from __future__ import annotations
from multiprocessing import Pool

from concurrent.futures import TimeoutError
import signal

import logging
import os
from time import time
from typing import TYPE_CHECKING

import numpy as np
from pymatgen.analysis.structure_matcher import StructureMatcher
from numpy.random import Generator

from pyxtal.molecule import find_rotor_from_smile, pyxtal_molecule
from pyxtal.representation import representation
from pyxtal.util import new_struc
from pyxtal.optimize.common import optimizer, randomizer
from pyxtal.optimize.common import optimizer_par, optimizer_single
from pyxtal.lattice import Lattice
from pyxtal.symmetry import Group

def setup_worker_logger(log_file):
    """
    Set up the logger for each worker process.
    """
    logging.getLogger().handlers.clear()
    logging.basicConfig(format="%(asctime)s| %(message)s",
                        filename=log_file,
                        level=logging.INFO)


# Update run_optimizer_with_timeout to accept a logger
def run_optimizer_with_timeout(args, logger):
    """
    Run the optimizer with a timeout.
    This function will be executed by each process.
    """
    def handler(signum, frame):
        raise TimeoutError("Optimization timed out")

    # Set the timeout signal
    cwd = os.getcwd()
    timeout = int(args[-1])
    #logger.info(f"Rank-{args[-2]} entering optimizer_with_timeout")
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    #logger.info(f"Rank-{args[-2]} after signal")

    try:
        if args[-2] > 0:
            logger.info(f"Rank-{args[-2]} running optimizer_par for PID {os.getpid()}")
        result = optimizer_par(*args[:-2])
        if args[-2] > 0:
            logger.info(f"Rank-{args[-2]} finished optimizer_par for PID {os.getpid()}")
        signal.alarm(0)  # Disable the alarm
        return result
    except TimeoutError:
        logger.info(f"Rank-{args[-2]} Process {os.getpid()} timed out after {timeout} seconds.")
        os.chdir(cwd)
        return None  # or some other placeholder for timeout results

# Update process_task to accept a logger
def process_task(args):
    logger = logging.getLogger()
    #logger.info(f"Rank {args[-2]} start process_task.")
    result = run_optimizer_with_timeout(args, logger)
    return result

class GlobalOptimize:
    """
    Base-class for all global optimization methods

    Args:
        smiles (str): smiles string
        workdir (str): path of working directory
        sg (int or list): space group number or list of spg numbers
        tag (string): job prefix
        ff_opt (bool): activate on the fly FF mode
        ff_style (str): automated force style (`gaff` or `openff`)
        ff_parameters (str or list): ff parameter xml file or list
        reference_file (str): path of reference xml data for FF training
        N_cpu (int): number of cpus for parallel calculation (default: `1`)
        cif (str): cif file name to store all structure information
        block: block mode
        num_block: list of blocks
        compositions: list of composition, (default is [1]*Num_mol)
        lattice (bool): whether or not supply the lattice
        torsions: list of torsion angle
        molecules (list): list of pyxtal_molecule objects
        sites (list): list of wp sites, e.g., [['4a']]
        use_hall (bool): whether or not use hall number (default: False)
        skip_ani (bool): whether or not use ani or not (default: True)
        eng_cutoff (float): the cutoff energy for FF training
        E_max (float): maximum energy defined as an invalid structure
        matcher : structurematcher from pymatgen
        early_quit: whether quit the program early when the target is found
        pre_opt: whether pre_optimize the structure or not
    """

    def __init__(
        self,
        smiles: str,
        workdir: str,
        sg: int | list[int],
        tag: str,
        info: dict[any, any] | None = None,
        ff_opt: bool = False,
        ff_style: str = "openff",
        ff_parameters: str = "parameters.xml",
        reference_file: str = "references.xml",
        ref_criteria: dict[any, any] | None = None,
        N_cpu: int = 1,
        cif: str | None = None,
        block: list[any] | None = None,
        num_block: list[any] | None = None,
        composition: list[any] | None = None,
        lattice: Lattice | None = None,
        torsions: list[any] | None = None,
        molecules: list[pyxtal_molecule] | None = None,
        sites: list[any] | None = None,
        use_hall: bool = False,
        skip_ani: bool = True,
        factor: float = 1.1,
        eng_cutoff: float = 5.0,
        E_max: float = 1e10,
        random_state=None,
        max_time: float | None = None,
        matcher: StructureMatcher | None = None,
        early_quit: bool = True,
        check_stable: bool = False,
        use_mpi: bool = False,
        pre_opt: bool = False,
    ):

        self.ncpu = N_cpu
        self.use_mpi = use_mpi
        if self.use_mpi:
            from mpi4py import MPI
            self.comm = MPI.COMM_WORLD
            self.rank = self.comm.Get_rank()
            self.size = self.comm.Get_size()
        else:
            self.rank = 0
            self.size = self.ncpu

        # General information
        if isinstance(random_state, Generator):
            self.random_state = random_state.spawn(1)[0]
        else:
            self.random_state = np.random.default_rng(random_state)

        # Molecular information
        self.smile = smiles
        self.smiles = self.smile.split(".")  # list
        self.torsions = torsions
        self.molecules = molecules
        self.block = block
        self.num_block = num_block
        self.composition = [
            1] * len(self.smiles) if composition is None else composition
        self.N_torsion = 0
        for smi, comp in zip(self.smiles, self.composition):
            self.N_torsion += len(find_rotor_from_smile(smi)
                                  ) * int(max([comp, 1]))

        # Crystal information
        self.pre_opt = pre_opt
        self.sg = [sg] if isinstance(sg, (int, np.int64)) else sg
        self.use_hall = use_hall
        self.factor = factor
        self.sites = sites
        if lattice is None:
            self.lattice = lattice
        elif isinstance(lattice, Lattice):
            self.lattice = lattice
        else:
            ltype = Group(self.sg[0]).lattice_type
            if len(lattice) == 6:
                self.lattice = Lattice.from_para(lattice, ltype=ltype)
            else:
                raise ValueError("input lattice is invalid", lattice)
        self.opt_lat = self.lattice is None
        self.ref_criteria = ref_criteria
        self.eng_cutoff = eng_cutoff

        # Generation and Optimization
        self.workdir = workdir
        os.makedirs(self.workdir, exist_ok=True)
        self.log_file = self.workdir + "/loginfo"
        if self.rank > 0: self.log_file += f"-{self.rank}"

        self.skip_ani = skip_ani
        # self.randomizer = randomizer
        # self.optimizer = optimizer
        self.check_stable = check_stable
        if not self.opt_lat:
            self.check_stable = False
        # setup timeout for each optimization call
        if max_time is None:
            if not self.skip_ani:
                max_time = 300.0
            elif self.check_stable:
                max_time = 300.0
            else:
                max_time = 60.0
        self.timeout = max_time * self.N_pop / self.ncpu

        self.ff_opt = ff_opt
        self.ff_style = ff_style

        # Setup logger
        logging.getLogger().handlers.clear()
        logging.basicConfig(format="%(asctime)s| %(message)s",
                            filename=self.log_file, level=logging.INFO)
        self.logging = logging

        if info is not None:
            self.atom_info = info
            self.parameters = None
            self.ff_opt = False
        else:
            self.ff_parameters = self.workdir + "/" + ff_parameters
            self.reference_file = self.workdir + "/" + reference_file
            # Only call ForceFieldParameters once
            # No need to broadcast self.parameters?
            # Just broadcast atom_info should be fine
            # parameters = None
            atom_info = None
            if self.rank == 0:
                from pyocse.parameters import ForceFieldParameters
                self.parameters = ForceFieldParameters(
                    self.smiles, style=ff_style,
                    f_coef=1.0,
                    s_coef=1.0,
                    ref_evaluator='mace',
                    ncpu=self.ncpu)

                # Preload two set for FF parameters 1 for opt and 2 for refinement
                if isinstance(self.ff_parameters, list):
                    assert len(self.ff_parameters) == 2
                    for para_file in self.ff_parameters:
                        if not os.path.exists(para_file):
                            raise RuntimeError("File not found", para_file)
                    params0, dic = self.parameters.load_parameters(
                        self.ff_parameters[0])
                    if "ff_style" in dic:
                        assert dic["ff_style"] == self.ff_style
                    # print(params0)
                    params1, dic = self.parameters.load_parameters(
                        self.ff_parameters[1])
                    if "ff_style" in dic:
                        assert dic["ff_style"] == self.ff_style
                    # print(params1)
                    atom_info = self._prepare_chm_info(params0, params1)
                else:
                    if os.path.exists(self.ff_parameters):
                        self.print("Preload the existing FF parameters from",
                                   self.ff_parameters)
                        params0, _ = self.parameters.load_parameters(
                            self.ff_parameters)
                    else:
                        self.print(
                            "No FF parameter file exists, using the default setting",
                            ff_style,
                        )
                        params0 = self.parameters.params_init.copy()
                        self.parameters.export_parameters(self.ff_parameters, params0)
                    atom_info = self._prepare_chm_info(
                        params0, suffix='pyxtal')

            if self.use_mpi:
                # self.parameters = self.comm.bcast(parameters, root=0)
                self.atom_info = self.comm.bcast(atom_info, root=0)
            else:
                self.atom_info = atom_info

        # Structure matcher
        if matcher is None:
            self.matcher = StructureMatcher(ltol=0.3, stol=0.3, angle_tol=5)
        else:
            self.matcher = matcher

        # I/O stuff
        self.early_quit = early_quit
        self.N_min_matches = 10  # The min_num_matches for early termination
        self.E_max = E_max
        self.tag = tag.lower()
        self.suffix = f"{self.workdir:s}/{self.name:s}-{self.ff_style:s}"
        if self.rank == 0:
            if cif is None:
                self.cif = self.suffix + '.cif'
            else:
                self.cif = self.suffix + cif

            with open(self.cif, "w") as f:
                f.writelines(str(self))
            self.matched_cif = self.suffix + "-matched.cif"
            # print(self)

            # Some neccessary trackers
            self.matches = []
            self.best_reps = []
            self.reps = []
            self.engs = []

    def print(self, *args, **kwargs):
        """Utility method to print only from rank 0."""
        if self.rank == 0:
            print(*args, **kwargs)

    def __str__(self):
        s = "\n-------Global Crystal Structure Prediction------"
        s += f"\nsmile     : {self.smile:s}"
        s += f"\nZprime    : {self.composition!s:s}"
        s += f"\nN_torsion : {self.N_torsion:d}"
        s += f"\nsg        : {self.sg!s:s}"
        s += f"\nncpu      : {self.size:d}"
        s += f"\ndiretory  : {self.workdir:s}"
        s += f"\nopt_lat   : {self.opt_lat!s:s}"
        s += f"\nusp_mpi   : {self.use_mpi!s:s}\n"
        if self.early_quit:
            s += f"Mode      : Production\n"
        else:
            s += f"Mode      : Sampling\n"
        s += f"cif       : {self.cif:s}\n"
        if self.ff_opt:
            s += "forcefield: On-the-fly\n"
        else:
            s += "forcefield: Predefined\n"

        if self.parameters is not None:
            s += f"ff_style  : {self.ff_style:s}\n"
            if isinstance(self.ff_parameters, list):
                for para in self.ff_parameters:
                    s += f"ff_params : {para:s}\n"
            else:
                s += f"ff_params : {self.ff_parameters:s}\n"
            s += f"references: {self.reference_file:s}\n"
            s += str(self.parameters)

        return s

    def __repr__(self):
        return str(self)

    def new_struc(self, xtal, xtals):
        return new_struc(xtal, xtals)

    def run(self, ref_pmg=None, ref_pxrd=None):
        """
        The main code to run Sampling

        Args:
            ref_pmg: reference pmg structure
            ref_pxrd: reference pxrd profile in 2D array

        Returns:
            success_rate or None
        """
        t0 = time()

        if ref_pmg is not None:
            ref_pmg.remove_species("H")
        self.ref_pmg = ref_pmg
        self.ref_pxrd = ref_pxrd

        if self.ncpu > 1:
            pool = Pool(processes=self.ncpu, initializer=setup_worker_logger, initargs=(self.log_file,))
        else:
            pool = None

        results = self._run(pool)

        if self.rank == 0:
            t = (time() - t0)/60
            strs = f"{self.name:s} {self.workdir} COMPLETED "
            strs += f"in {t:.1f} mins {self.N_struc:d} strucs."
            print(strs)

        if self.use_mpi:
            self.comm.Barrier()
        return results

    def select_xtals(self, ref_xtals, ids, N_max):
        """
        Select only unique structures
        """
        xtals = []
        for id in ids:
            (xtal, _) = ref_xtals[id]
            if xtal.energy <= self.E_max and self.new_struc(xtal, xtals):
                xtals.append(xtal)  # .to_ase(resort=False))
            if len(xtals) == N_max:
                break
        # xtals = [xtal.to_ase(resort=False) for xtal in xtals]
        return xtals

    def count_pxrd_match(self, xtals, matches):
        """
        Wrap up the matched PXRD results

        Args:
            xtals: list of (xtal, tag) tuples
            matches (list): list of XRD matches

        """
        gen = self.generation
        for i, match in enumerate(matches):
            if match > 0.85:
                (xtal, tag) = xtals[i]
                with open(self.matched_cif, "a+") as f:
                    e = xtal.energy / sum(xtal.numMols)
                    try:
                        label = self.tag + "-g" + str(gen) + "-p" + str(i)
                        label += f"-e{e:.3f}-{tag:s}-{match:4.2f}"
                    except:
                        print("Error in e, tag, match", e, tag, match)
                    f.writelines(xtal.to_file(header=label))
                    self.matches.append((gen, i, xtal, e, match, tag))

    def success_count(self, xtals, matches):
        """
        Wrap up the matched results and count success rate.

        Args:
            xtals: list of (xtal, tag) tuples
            matches (list): list of matches [True, False, ..]

        Return:
            success_rate
        """
        gen = self.generation
        for i, match in enumerate(matches):
            if match:
                (xtal, tag) = xtals[i]
                with open(self.matched_cif, "a+") as f:
                    res = self._print_match(xtal, self.ref_pmg)
                    e, d1, d2 = xtal.energy/sum(xtal.numMols), res[0], res[1]
                    try:
                        label = self.tag + "-g" + str(gen) + "-p" + str(i)
                        label += f"-e{e:.3f}-{tag:s}-{d1:4.2f}-{d2:4.2f}"
                    except:
                        print("Error in e, tag, d1, d2", e, tag, d1, d2)
                    f.writelines(xtal.to_file(header=label))
                    self.matches.append((gen, i, xtal, e, d1, d2, tag))

        success_rate = len(self.matches) / self.N_struc * 100
        gen_out = f"Success rate @ Gen {gen:3d}: {success_rate:7.4f}%"
        self.logging.info(gen_out)
        print(gen_out)

        return success_rate

    def early_termination(self, success_rate):
        """
        Check if the calculation can be terminated early.
        """
        if success_rate > 0:
            if self.early_quit:
                msg = f"Early termination since a match is found"
                print(msg)
                self.logging.info(msg)
                return True

            elif success_rate > 2.5 or len(self.matches) >= self.N_min_matches:
                msg = f"Early termination with a high success rate"
                print(msg)
                self.logging.info(msg)
                return True
        return False

    def update_ff_paramters(self, xtals, engs, N_added):
        """
        Update the ff parameters

        Args:
            xtals: a list of pyxtals
            engs: a list of energies
            N_added (int): the number of structures that have been added
        """

        N_max = min([int(self.N_pop * 0.6), 50])
        ids = np.argsort(engs)
        _xtals = self.select_xtals(xtals, ids, N_max)
        print("Select structures for FF optimization", len(_xtals))

        return self.ff_optimization(_xtals, N_added)

    def ff_optimization(self, xtals, N_added, N_min=50, dE=2.5, FMSE=2.5):
        """
        Optimize the current FF based on newly explored data

        Args:
            xtals: list of xtals from the current gen
            N_added (int): the number of structures that have been added
            N_min (int): minimum number of configurations to trigger the FF training
            dE (float): the cutoff energy value
            FMSE (float): the cutoff Force MSE value
        """
        from pyocse.utils import reset_lammps_cell
        from pyocse.parameters import compute_r2, get_lmp_efs

        numMols = [xtal.numMols for xtal in xtals]
        xtals = [xtal.to_ase(resort=False) for xtal in xtals]

        gen = self.generation
        # Initialize ff parameters and references
        params_opt, err_dict = self.parameters.load_parameters(
            self.ff_parameters)
        if os.path.exists(self.reference_file):
            ref_dics = self.parameters.load_references(self.reference_file)
            if self.ref_criteria is not None:
                ref_dics = self.parameters.clean_ref_dics(
                    ref_dics, self.ref_criteria)
                ref_dics = self.parameters.cut_references_by_error(
                    ref_dics, params_opt, dE=dE, FMSE=FMSE)
            # self.parameters.generate_report(ref_dics, params_opt)
        else:
            ref_dics = []

        # Add references
        print("Current number of reference structures", len(ref_dics))
        t0 = time()
        if len(ref_dics) > 100:  # no fit if ref_dics is large
            # Here we find the lowest engs and select only low-E struc
            ref_engs = [ref_dic["energy"] / ref_dic["replicate"]
                        for ref_dic in ref_dics]
            ref_e2 = np.array(ref_engs).min()
            print("Min Reference Energy", ref_e2)

            if len(err_dict) == 0:
                # update the offset if necessary
                _, params_opt = self.parameters.optimize_offset(
                    ref_dics, params_opt)
                results = self.parameters.evaluate_multi_references(
                    ref_dics, params_opt, 1000, 1000)
                (ff_values, ref_values, rmse_values, r2_values) = results
                err_dict = {"rmse_values": rmse_values}

            _ref_dics = []
            rmse_values = err_dict["rmse_values"]
            lmp_in = self.parameters.ff.get_lammps_in()
            self.parameters.ase_templates = {}
            self.lmp_dat = {}
            ff_engs, ff_fors, ff_strs = [], [], []
            rf_engs, rf_fors, rf_strs = [], [], []

            for numMol, xtal in zip(numMols, xtals):
                struc = reset_lammps_cell(xtal)
                lmp_struc, lmp_dat = self.parameters.get_lmp_input_from_structure(
                    struc, numMol, set_template=False)
                replicate = len(lmp_struc.atoms) / \
                    self.parameters.natoms_per_unit

                try:
                    # ; print('Debug KONTIQ', struc, e1)
                    e1, f1, s1 = get_lmp_efs(lmp_struc, lmp_in, lmp_dat)
                except:
                    e1 = self.E_max

                # filter very high energy structures
                if e1 < 1000:
                    struc.set_calculator(self.parameters.calculator)
                    e2 = struc.get_potential_energy()
                    e2 /= replicate
                    # Ignore very high energy structures
                    if e2 < ref_e2 + self.eng_cutoff:
                        e1 /= replicate
                        f2 = struc.get_forces()
                        s2 = struc.get_stress()
                        struc.set_calculator()
                        e_err = abs(e1 - e2 + params_opt[-1])
                        f_err = np.sqrt(
                            ((f1.flatten() - f2.flatten()) ** 2).mean())
                        s_err = np.sqrt(((s1 - s2) ** 2).mean())
                        e_check = e_err < 0.5 * rmse_values[0]
                        f_check = f_err < 1.0 * rmse_values[1]
                        s_check = s_err < 1.0 * rmse_values[2]
                        strs = f"Errors of csp structure in gen{gen:3d} "
                        strs += f"{e_err:.4f} {f_err:.4f} {s_err:.4f} "
                        strs += f"{e1:8.4f} {e2:8.4f}"
                        print(strs, e_check, f_check, s_check)

                        # avoid very unphysical structures
                        if e_err < 4.0 and f_err < 4.0:
                            ff_engs.append(e1 + params_opt[-1])
                            rf_engs.append(e2)
                            ff_fors.extend(f1.flatten())
                            rf_fors.extend(f2.flatten())
                            ff_strs.extend(s1.flatten())
                            rf_strs.extend(s2.flatten())

                            if False in [e_check, f_check, s_check]:
                                _ref_dic = {
                                    "structure": struc,
                                    "energy": e2 * replicate,
                                    "forces": f2,
                                    "stress": s2,
                                    "replicate": replicate,
                                    "options": [True, not f_check, True],
                                    "tag": "CSP",
                                    "numMols": numMol,
                                }
                                _ref_dics.append(_ref_dic)
                    else:
                        print("Ignore the structure due to high energy", e2)

            # QZ: Output FF performances MSE, R2 for the selected structures
            if len(_ref_dics) == 0:
                print("There is a serious problem in depositing high energy")
                raise ValueError("The program needs to stop here")

            if self.ref_criteria is not None:
                _ref_dics = self.parameters.clean_ref_dics(
                    _ref_dics, self.ref_criteria)

            # print("Added {:d} new reference structures into training".format(len(_ref_dics)))
            print("FF performances")
            ff_engs = np.array(ff_engs)
            rf_engs = np.array(rf_engs)
            ff_fors = np.array(ff_fors)
            rf_fors = np.array(rf_fors)
            ff_strs = np.array(ff_strs)
            rf_strs = np.array(rf_strs)
            r2_engs = compute_r2(ff_engs, rf_engs)
            r2_fors = compute_r2(ff_fors, rf_fors)
            r2_strs = compute_r2(ff_strs, rf_strs)
            mse_engs = np.sqrt(np.mean((ff_engs - rf_engs) ** 2))
            mse_fors = np.sqrt(np.mean((ff_fors - rf_fors) ** 2))
            mse_strs = np.sqrt(np.mean((ff_strs - rf_strs) ** 2))

            print(f"R2   {r2_engs:8.4f} {r2_fors:8.4f} {r2_strs:8.4f}")
            print(f"RMSE {mse_engs:8.4f} {mse_fors:8.4f} {mse_strs:8.4f}")
            # self.parameters.generate_report(_ref_dics, params_opt)
            # import sys; sys.exit()
        else:
            # reduce the number of structures to save some time
            N_selected = min([N_min, self.ncpu])
            print("Create the reference data by augmentation", N_selected)
            if len(xtals) >= N_selected:
                ids = self.random_state.choice(
                    list(range(len(xtals))), N_selected)
                xtals = [xtals[id] for id in ids]
                numMols = [numMols[id] for id in ids]

            _ref_dics = self.parameters.add_multi_references(
                xtals,
                numMols,
                augment=True,
                steps=20,  # 50,
                N_vibs=1,
                logfile="ase.log",
            )
            if len(ref_dics) == 0:
                _, params_opt = self.parameters.optimize_offset(
                    _ref_dics, params_opt)
                self.parameters.generate_report(ref_dics, params_opt)
                # import sys; sys.exit()

        ref_dics.extend(_ref_dics)
        print(
            f"Add {len(_ref_dics):d} references in {(time() - t0) / 60:.2f} min")
        self.parameters.export_references(ref_dics, self.reference_file)

        # Optimize ff parameters if we get enough number of configurations
        N_added += len(_ref_dics)
        if N_added < N_min:
            print("Do not update ff, the current number of configurations is", N_added)
        else:
            t0 = time()
            _, params_opt = self.parameters.optimize_offset(
                ref_dics, params_opt)

            for data in [
                (["bond", "angle", "proper"], 50),
                (["proper", "vdW", "charge"], 50),
                (["bond", "angle", "proper", "vdW", "charge"], 50),
            ]:
                (terms, steps) = data

                # Actual optimization
                opt_dict = self.parameters.get_opt_dict(
                    terms, None, params_opt)
                x, fun, values, it = self.parameters.optimize_global(
                    ref_dics, opt_dict, params_opt, obj="R2", t0=0.1, steps=25
                )

                params_opt = self.parameters.set_sub_parameters(
                    values, terms, params_opt)

                opt_dict = self.parameters.get_opt_dict(
                    terms, None, params_opt)

                x, fun, values, it = self.parameters.optimize_local(
                    ref_dics, opt_dict, params_opt, obj="R2", steps=steps)

                params_opt = self.parameters.set_sub_parameters(
                    values, terms, params_opt)
                _, params_opt = self.parameters.optimize_offset(
                    ref_dics, params_opt)

                # To add Early termination

            t = (time() - t0) / 60
            print(f"FF optimization {t:.2f} min ", fun)
            # Reset N_added to 0
            N_added = 0

        # Export FF performances
        if gen < 10:
            gen_prefix = "gen_00" + str(gen)
        elif gen < 100:
            gen_prefix = "gen_0" + str(gen)
        else:
            gen_prefix = "gen_" + str(gen)

        performance_fig = f"{self.workdir:s}/FF_performance_{gen_prefix:s}.png"
        errs = self.parameters.plot_ff_results(performance_fig, ref_dics, [
                                               params_opt], labels=gen_prefix)

        param_fig = f"{self.workdir:s}/parameters_{gen_prefix:s}.png"
        self.parameters.plot_ff_parameters(param_fig, [params_opt])

        # Save parameters
        self.parameters.export_parameters(
            self.ff_parameters, params_opt, errs[0])
        self._prepare_chm_info(params_opt)
        # self.parameters.generate_report(ref_dics, params_opt)

        return N_added

    def _prepare_chm_info(self, params0, params1=None, folder="calc", suffix="pyxtal0"):
        """
        Prepar_chm_info with from the given params.

        Args:
            params0 (array or list): FF parameters array
            params1 (array or list): FF parameters array
            folder (str): folder path
            suffix (str): suffix of the temporary file

        Returns:
            atom_info
        """
        pwd = os.getcwd()
        os.chdir(self.workdir)
        if not os.path.exists(folder):
            os.mkdir(folder)
        suffix = folder + '/' + suffix

        # To remove the old pyxtal1 files
        if os.path.exists(suffix + ".rtf"):
            os.remove(suffix + ".rtf")
        if os.path.exists(suffix + ".prm"):
            os.remove(suffix + ".prm")

        ase_with_ff = self.parameters.get_ase_charmm(params0)
        ase_with_ff.write_charmmfiles(base=suffix)
        if params1 is not None:
            ase_with_ff = self.parameters.get_ase_charmm(params1)
            ase_with_ff.write_charmmfiles(base=suffix)
        os.chdir(pwd)

        # Info
        return ase_with_ff.get_atom_info()

    def get_label(self, i):
        if i < 10:
            folder = f"cpu00{i}"
        elif i < 100:
            folder = f"cpu0{i}"
        else:
            folder = f"cpu0{i}"
        return folder

    def print_matches(self, header=None):
        """
        Formatted output for the matched structures with xtal rep and eng rank
        """
        if self.rank == 0:
            all_engs = np.sort(np.array(self.engs))
            ranks = []
            xtals = []
            if self.ref_pxrd is not None:
                matches = sorted(
                    self.matches, key=lambda x: -x[4])  # similarity
            else:
                print(self.matches)
                matches = sorted(self.matches, key=lambda x: x[3]) # eng

            for match_data in matches:
                d1, match = None, None
                if self.ref_pxrd is not None:
                    (_, id, xtal, e, match, tag) = match_data
                    add = self.new_struc(xtal, xtals)
                    if add:
                        xtals.append(xtal)
                else:
                    (_, id, xtal, e, d1, d2, tag) = match_data
                    add = True

                if add:
                    rep0 = xtal.get_1D_representation()
                    if header is not None:
                        strs = header
                    else:
                        strs = ""
                    strs += rep0.to_string(eng=xtal.energy / sum(xtal.numMols))
                    if d1 is not None:
                        strs += f"{d1:6.3f}{d2:6.3f} Match "
                    if match is not None:
                        strs += f" {match:4.2f} "

                    if e is not None:
                        rank = len(all_engs[all_engs < (e - 1e-3)]) + 1
                        strs += f" {rank:d}/{self.N_struc:d} {tag:s}"
                        ranks.append(rank)

                    print(strs)
            if len(ranks) == 0:
                ranks = [0]
            return min(ranks)

    def _print_match(self, xtal, ref_pmg):
        """
        Print the matched structure

        Args:
            rep: 1d rep
            eng: energy
            ref_pmg: reference pmg structure
        """

        rep0 = xtal.get_1D_representation()
        pmg_s1 = xtal.to_pymatgen()
        pmg_s1.remove_species("H")
        strs = rep0.to_string(eng=xtal.energy / sum(xtal.numMols))
        rmsd = self.matcher.get_rms_dist(ref_pmg, pmg_s1)
        if rmsd is not None:
            strs += f"{rmsd[0]:6.3f}{rmsd[1]:6.3f} Match Ref"
            print(strs)
            return rmsd[0], rmsd[1]
        else:
            return None, None

    def _apply_gaussian(self, reps, engs, h1=0.1, h2=0.1, w1=0.2, w2=3):
        """
        Apply Gaussian to discourage the sampling of already visited configs.
        Consider both lattice abc and torsion
        """
        from copy import deepcopy

        # check torsion
        N_id = 8
        engs_gau = deepcopy(engs)
        for i, rep in enumerate(reps):
            gau = 0
            if rep is not None and engs[i] < 9999:
                sg1, abc1 = rep[0][0], np.array(rep[0][1:])
                tor1 = np.zeros(self.N_torsion)
                count = 0
                for j in range(1, len(rep)):
                    if len(rep[j]) > N_id:  # for Cl-
                        tor1[count: count +
                             len(rep[j]) - N_id - 1] = rep[j][N_id:-1]
                        count += len(rep[j]) - N_id

                for ref in self.best_reps:
                    sg2, abc2 = ref[0][0], np.array(ref[0][1:])
                    # Cell
                    g1 = 0
                    if sg1 == sg2:
                        diff1 = np.sum((abc1 - abc2) ** 2) / w1**2
                        g1 = h1 * np.exp(-0.5 * diff1)  # cell
                    # Torsion
                    g2 = 0
                    if len(tor1) > 0:
                        tor2 = np.zeros(self.N_torsion)
                        count = 0
                        for j in range(1, len(rep)):
                            if len(rep[j]) > N_id:  # for Cl-
                                tor2[count: count +
                                     len(ref[j]) - N_id - 1] = ref[j][N_id:-1]
                                count += len(ref[j]) - N_id

                        diff2 = np.sum((tor1 - tor2) ** 2) / w2**2
                        g2 = h2 * np.exp(-0.5 * diff2)  # torsion
                    gau += g1 + g2
                # if gau > 1e-2: print(sg1, diag1, abc1, tor1)
            # print("Gaussian", i, "eng", engs[i], "gau", gau)
            # import sys; sys.exit()
            engs_gau[i] += gau
        return np.array(engs_gau)

    def check_ref(self, reps=None, reference=None, filename="pyxtal.cif"):
        """
        Check if ground state structure is found.

        Args:
            reps: list of representations
            refernce: [pmg, eng]
            filename: filename
        """
        if os.path.exists(filename):
            os.remove(filename)

        if reference is not None:
            [pmg0, eng] = reference
            pmg0.remove_species("H")
            print("check if ground state structure is found")

            if reps is None:
                reps = np.array(self.reps)

            if eng is None:
                eng = np.min(reps[:, -1]) + 0.25

            reps = reps[reps[:, -1] < (eng + 0.1)]
            ids = np.argsort(reps[:, -1])
            reps = reps[ids]
            new_reps = []
            for rep in reps:
                eng1 = rep[-1]
                rep0 = representation(rep[:-1], self.smiles)
                xtal = rep0.to_pyxtal()
                pmg_s1 = xtal.to_pymatgen()
                pmg_s1.remove_species("H")
                new = True
                for ref in new_reps:
                    eng2 = ref[-1]
                    pmg_s2 = representation(
                        rep[:-1], self.smiles).to_pyxtal().to_pymatgen()
                    pmg_s2.remove_species("H")
                    if abs(eng1 - eng2) < 1e-2 and self.matcher().fit(pmg_s1, pmg_s2):
                        new = False
                        break
                if new:
                    new_reps.append(rep)
                    header = f"{len(new_reps):d}: {eng1:12.4f}"
                    xtal.to_file(filename, header=header, permission="a+")
                    strs = rep0.to_string(eng=eng1)
                    rmsd = self.matcher.get_rms_dist(pmg0, pmg_s1)
                    if rmsd is not None:
                        strs += f"{rmsd[0]:6.3f}{rmsd[1]:6.3f} True"
                        print(strs)
                        return True
                    else:
                        print(strs)
        return False

    def _get_local_optimization_args(self):
        args = [
            randomizer,
            optimizer,
            self.smiles,
            self.block,
            self.num_block,
            self.atom_info,
            self.workdir + "/" + "calc",
            self.sg,
            self.composition,
            self.lattice,
            self.torsions,
            self.molecules,
            self.sites,
            self.ref_pmg,
            self.matcher,
            self.ref_pxrd,
            self.use_hall,
            self.skip_ani,
            self.check_stable,
            self.pre_opt,
        ]
        return args

    def local_optimization(self, xtals, qrs=False, pool=None):
        """
        Perform MPI optimization for each structure in each generation.

        Args:
            xtals : list of (xtal, tag) tuples
            qrs (bool): Force mutation or not (related to QRS)
        """
        if self.use_mpi:
            return self.local_optimization_mpi(xtals, qrs=qrs, pool=pool)
        elif self.ncpu == 1:
            return self.local_optimization_serial(xtals, qrs)
        else:
            print(f"Local optimization by multi-threads {self.ncpu}")
            return self.local_optimization_mproc(xtals, self.ncpu, qrs=qrs, pool=pool)

    def local_optimization_serial(self, xtals, qrs=False):
        """
        Perform optimization for each structure in each generation.

        Args:
            xtals : list of (xtal, tag) tuples
            qrs (bool): Force mutation or not (related to QRS)
        """
        args = self._get_local_optimization_args()
        gen = self.generation
        gen_results = [(None, None, None)] * len(xtals)
        for pop in range(len(xtals)):
            xtal = xtals[pop][0]
            job_tag = self.tag + "-g" + str(gen) + "-p" + str(pop)
            mutated = False if qrs else xtal is not None
            my_args = [xtal, pop, mutated, job_tag, *args]
            xtal, match = optimizer_single(*tuple(my_args))
            gen_results[pop] = (pop, xtal, match)
        return gen_results

    def local_optimization_mpi(self, xtals, qrs, pool):
        """
        Perform MPI optimization for each structure in each generation.

        Args:
            xtals : list of (xtal, tag) tuples
            qrs (bool): Force mutation or not (related to QRS)
        """
        #t0 = time()
        gen = self.generation
        self.print("Local optimization enabled by MPI", self.size, self.ncpu)

        # Distribute args_lists across available ranks (processes)
        local_xtals = xtals[self.rank::self.size]

        local_ids = list(range(self.N_pop))[self.rank::self.size]

        # Call local_optimization_mproc
        self.logging.info(f"Rank {self.rank} gets {len(local_xtals)} strucs")
        results = self.local_optimization_mproc(local_xtals,
                                                self.ncpu,
                                                local_ids,
                                                qrs,
                                                pool)
        # Synchronize before gathering
        self.logging.info(f"Rank {self.rank} finish local_optimization_mproc")
        self.comm.Barrier()

        # Gather all results at the root process
        self.logging.info(f"Rank {self.rank} in MPI_Gather at gen {gen}")
        all_results = self.comm.gather(results, root=0)
        self.logging.info(f"Rank {self.rank} done MPI_Gather at gen {gen}")

        # If root process, process the results
        gen_results = None
        if self.rank == 0:
            gen_results = [(None, None, None)] * len(xtals)
            for result_set in all_results:
                for res in result_set:
                    (id, xtal, match) = res
                    gen_results[id] = (id, xtal, match)

        # Broadcast
        self.logging.info(f"Rank {self.rank} MPI_bcast at gen {gen}")
        gen_results = self.comm.bcast(gen_results, root=0)

        return gen_results

    def local_optimization_mproc(self, xtals, ncpu, ids=None, qrs=False, pool=None):
        """
        Perform optimization for each structure in multiprocess mode.

        Args:
            xtals : list of (xtal, tag) tuples
            ncpu (int): number of parallel python processes
            ids (list): list of ids of the associated xtals
            qrs (bool): Force mutation or not (related to QRS)
        """
        gen = self.generation
        t0 = time()
        args = self._get_local_optimization_args()
        if ids is None:
            ids = range(len(xtals))

        N_cycle = int(np.ceil(len(xtals) / ncpu))
        # Generator to create arg_lists for multiprocessing tasks
        def generate_args_lists():
            for i in range(ncpu):
                id1 = i * N_cycle
                id2 = min([id1 + N_cycle, len(xtals)])
                _ids = ids[id1: id2]
                job_tags = [self.tag + "-g" + str(gen)
                            + "-p" + str(id) for id in _ids]
                _xtals = [xtals[id][0] for id in range(id1, id2)]
                mutates = [False if qrs else xtal is not None for xtal in _xtals]
                my_args = [_xtals, _ids, mutates, job_tags, *args, self.rank, self.timeout]
                yield tuple(my_args)  # Yield args instead of appending to a list

        gen_results = []
        for result in pool.imap_unordered(process_task, generate_args_lists()):
            if result is not None:
                for _res in result:
                    gen_results.append(_res)

        return gen_results

    def gen_summary(self, t0, gen_results, xtals):
        """
        Write the generic summary for each generation.

        Args:
            t0 (float): time stamp
            gen_results: list of results (id, xtal, match)
            xtals: list of (xtal, tag) tuples
        """
        matches = [False] if self.ref_pxrd is None else [0.0]
        matches *= self.N_pop

        eng0s = [self.E_max] * self.N_pop
        reps = [None] * self.N_pop
        new_xtals = [(None, None)] * len(xtals)
        gen = self.generation

        for res in gen_results:
            (id, xtal, match) = res

            if xtal is not None:
                new_xtals[id] = (xtal, xtals[id][1])
                eng0s[id] = xtal.energy / sum(xtal.numMols)
                reps[id] = xtal.get_1D_representation()
                matches[id] = match

                # Don't write bad structure
                if self.cif is not None and xtal.energy < 9999:
                    if self.verbose:
                        print("Add qualified structure", id, xtal.energy)
                    with open(self.cif, "a+") as f:
                        label = self.tag + "-g" + str(gen) + "-p" + str(id)
                        f.writelines(xtal.to_file(header=label))
                self.engs.append(xtal.energy / sum(xtal.numMols))
                self.stats[gen][id][0] = xtal.energy / sum(xtal.numMols)
                self.stats[gen][id][1] = match

        self.min_energy = np.min(np.array(self.engs))
        self.N_struc = len(self.engs)
        strs = f"Generation {gen:d} finishes: {len(self.engs):d} strucs"
        print(strs)
        self.logging.info(strs)

        t1 = time()

        # Apply Gaussian
        reps_x = [rep.x if rep is not None else None for rep in reps]
        if self.ref_pxrd is None:
            engs = self._apply_gaussian(reps_x, eng0s)
        else:
            engs = self._apply_gaussian(reps_x, -1 * np.array(matches))

        # Store the best structures
        count = 0
        ref_xtals = []
        ids = np.argsort(engs)
        for id in ids:
            (xtal, tag) = new_xtals[id]
            rep, eng = reps[id], eng0s[id]
            if self.new_struc(xtal, ref_xtals):
                ref_xtals.append(xtal)
                self.best_reps.append(rep.x)
                # d_rep = representation(rep, self.smiles)
                tag = f"{tag:8s}"
                try:
                    strs = rep.to_string(None, eng, tag)
                    out = f"{gen:3d} {strs:s} Top"
                    if self.ref_pxrd is not None:
                        out += f" {matches[id]:6.3f}"
                    print(out)
                except:
                    print('Error', xtal)
                count += 1
            if count == 3:
                break

        t2 = time()
        gen_out = f"Gen{gen:3d} time usage: "
        gen_out += f"{t1 - t0:5.1f}[Calc] {t2 - t1:5.1f}[Proc]"
        print(gen_out)

        return new_xtals, matches, engs

    def plot_results(self, save=True, figsize=(8.0, 5.0), figname=None, ylim=None):
        """
        Plot the results

        Args:
            save (bool): whether or not save the data
            figsize: e.g. (8.5, 5.0)
            figname (str):
            ylim: e.g. (0, 1.0)
        """
        if self.rank == 0:
            import matplotlib.pyplot as plt
            import seaborn as sns
            sns.set_theme()
            sns.set_context("talk", font_scale=0.9)

            if figname is None:
                figname = self.suffix + "-results.pdf"

            data1 = []
            data2 = []
            # Extract (pop_id, eng, gen_id) when pxrd is False
            # Extract (pop_id, eng, sim) when pxrd is True
            for i in range(self.N_gen):
                for j in range(self.N_pop):
                    if self.ref_pxrd is not None:
                        data1.append(
                            [i, j, self.stats[i, j, 0], self.stats[i, j, 1]])
                    else:
                        data1.append([i, j, self.stats[i, j, 0]])

            for match in self.matches:
                if self.ref_pxrd is not None:
                    data2.append([match[0], match[1], match[3], match[4]])
                else:
                    data2.append([match[0], match[1], match[3]])

            fig = plt.figure(figsize=figsize)
            plt.ylabel("Lattice Energy (kcal)")  # , weight='bold')
            data1 = np.array(data1)
            if self.ref_pxrd is not None:
                # (similarity, eng, gen_id)
                x1, y1, z1 = data1[:, 3], data1[:, 2], data1[:, 0]
                plt.xlabel("XRD Similarity")  # , weight='bold')
            else:
                x1, y1, z1 = data1[:, 1], data1[:, 2], data1[:, 0]
                plt.xlabel("Population ID")  # , weight='bold')
            # Plot of all samples (PopID, Engs/Similarity)
            scatter = plt.scatter(x1, y1, s=10, c=z1,
                                  cmap='winter', alpha=0.5, label='Samples')
            cbar = plt.colorbar(scatter)
            cbar.set_label('Generation ID')  # , weight='bold')
            if ylim is None:
                y1 = np.array(y1)
                ymin = y1.min() - 0.25
                ymax = min([ymin + 10.0, y1.max()])
                ylim = (ymin, ymax)

            if len(data2) > 0:
                data2 = np.array(data2)
                if len(data2.shape) == 1:
                    data2 = data2.reshape(-1, 1)
                if self.ref_pxrd is not None:
                    x2, y2, z2 = data2[:, 3], data2[:, 2], data2[:, 0]
                else:
                    x2, y2, z2 = data2[:, 1], data2[:, 2], data2[:, 0]
                plt.scatter(x2, y2, s=10, c='red', marker='x', label='Matches')

            plt.legend(loc=1)  # , prop={'weight': 'bold'})
            plt.ylim(ylim)
            plt.title(f"{self.name:s}-{self.ff_style:s}")  # , weight='bold')
            plt.tight_layout()
            plt.savefig(figname)

            if save:
                if self.ref_pxrd is not None:
                    header = "#Generation, Population, Energy, Similarity"
                else:
                    header = "#Generation, Population, Energy"
                data_txt = self.suffix + "-data.txt"
                np.savetxt(data_txt, data1, header=header)

                if len(data2) > 0:
                    match_txt = self.suffix + "-match.txt"
                    np.savetxt(match_txt, data2, header=header)


if __name__ == "__main__":
    print("test")
