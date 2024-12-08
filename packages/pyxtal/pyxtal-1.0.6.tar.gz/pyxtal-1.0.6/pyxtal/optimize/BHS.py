import numpy as np
from random import choice
from ase.units import kB
from copy import deepcopy
import pymatgen.analysis.structure_matcher as sm
from pyxtal import pyxtal
from pyxtal.representation import representation
from pyxtal.molecule import find_id_from_smile
from htocsp.util import unique_rows

class BasinHopping():
    """
    Basin hopping algorithm.
    Wales and Doye, J. Phys. Chem. A, vol 101 (1997) 5111-5116
    """

    def __init__(self, x, sg, smile, atom_info, workdir, tag,
                 optimizer, kT=0.1*kB, dr=0.1,
                 composition=None, lattice=None, torsions=None,
                ):
        """
        Args:
            x: 1D list [a, b, c, ....]
            sg: space group number
            smile:
            atom_info: a dictinonary for atom properties (e.g., label, charge)
            workdir:
            sg:
            optimizer:
            kT: boltzmann factor (default: `0.1kB`)
            dr: magnitude of mutation (default: `0.2`)
        """
        # BH parameters
        self.kT = kT
        self.dr = dr

        # setup for local optimization
        self.lattice = lattice
        if lattice is None:
            self.opt_lat = True
        else:
            self.opt_lat = False
        self.optimizer = optimizer
        self.smile = smile
        self.atom_info = atom_info
        self.workdir = workdir
        self.tag = tag
        self.sg = sg
        self.torsions = torsions
        self.smiles = self.smile.split('.') #list
        if composition is None:
            self.composition = [1] * len(self.smiles)
        else:
            self.composition = composition
        self.N_torsion = 0
        for smi, comp in zip(self.smiles, self.composition):
            self.N_torsion += len(find_id_from_smile(smi))*comp
        print(self)

        # initial guess
        self.x = x

        # all structures
        self.reps = []

    def __str__(self):
        s = "\n------Basin Hopping Algorithm------"
        s += "\nkT      : {:6.2f}".format(self.kT)
        s += "\ndr      : {:6.2f}".format(self.dr)
        s += "\nsmile   : {:s}".format(self.smile)
        s += "\ndiretory: {:s}".format(self.workdir)
        s += "\nZprime    : {:s}".format(str(self.composition))
        s += "\nN_torsion : {:d}".format(self.N_torsion)
        s += "\nsg        : {:s}".format(str(self.sg))
        s += "\nopt_lat   : {:s}\n".format(str(self.opt_lat))
        return s

    def __repr__(self):
        return str(self)

    def run(self, steps=100, show=False):
        """
        Hop the basins for defined number of steps.
        """
        # Initial solution
        self.x, Eo, strs = self.get_energy(self.x)
        strs = "{:3d}".format(0) + strs
        print(strs)

        #print("FIRST", self.x[:5])
        for step in range(steps):
            En = None
            while En is None:
                rn = self.move()
                rn, En, strs = self.get_energy(rn)
            #print(Eo, En, np.exp((Eo-En)/self.kT))

            accept = False
            diff = Eo-En
            if diff>0:
                if abs(diff) > 5e-3: #identical
                    accept = True
            else:
                if np.exp(diff/self.kT)>np.random.uniform():
                    accept = True
            if accept:
                self.x = deepcopy(rn)
                self.reps.append(rn)
                Eo = En
                strs += "+++"
            strs = "{:3d}".format(step+1) + strs
            if show and accept: print(strs)

        print("Calculation is complete")

    def move(self):
        # displace coordinates
        x = self.x
        dr = self.dr
        # perturb cell
        x_new = deepcopy(x)
        if self.opt_lat:
            sg = x[0][0]
            disp_cell = np.random.uniform(-1., 1., len(x[0])-2)
            x_new[0][2:] *= (1+dr*disp_cell)

            #flip the inclination angle
            if 3 <= sg <= 15 and np.random.random() > 0.7:
                if abs(90-x_new[0][-1])<15:
                    x_new[0][-1] = 180-x_new[0][-1]

        # perturb molecules
        for i in range(1, len(x)):
            disp_mol = np.random.uniform(-1., 1., len(x_new[i])-1)
            x_new[i][:-1] *= (1+dr*disp_mol)
            # change the orientation and torsions
            for j in range(3, len(x_new[i])-1):
                rad_num = np.random.random()
                if rad_num < 0.25:
                    x_new[i][j] += choice([45.0, 90.0])
                elif rad_num < 0.5:
                    x_new[i][j] *= -1
        return x_new

    def get_energy(self, x):
        """
        Return the energy of the nearest local minimum.
        """
        res = self.optimizer(x, self.smiles, self.composition, self.atom_info,\
                             self.workdir, self.tag, opt_lat=self.opt_lat)
        #print(res); import sys; sys.exit()
        if res is not None:
            rep, eng = res['rep'], res['energy']
            myrep = representation(rep, self.smiles)
            strs = myrep.to_string(None, eng)
            return rep, eng, strs
        return None, None, None


    def check_ref(self, xtal):
        """
        check if ground state structure is found

        Args:
            - xtal: pyxtal object
        """

        print("check if ground state structure is found")
        rep = representation.from_pyxtal(xtal)
        print("\n" + rep.to_string() + ' reference')
        pmg0 = xtal.to_pymatgen()
        pmg0.remove_species('H')

        for d in self.reps:
            rep0 = representation(d, self.smiles)
            s = rep0.to_pyxtal(composition=self.composition)
            pmg_struc = s.to_pymatgen()
            pmg_struc.remove_species('H')
            found = sm.StructureMatcher().fit(pmg_struc, pmg0)
            if found:
                strs += " " + str(found)
                print(strs)
                break

def basin_hopping_runner(smile, atom_info, workdir, tag, sg, comp, optimize, \
                         kT, rep=None, steps=100, xtal_ref=None,
                         show=False, seed=None):
    smiles = smile.split('.')
    if rep is None:
        g = Group(sg)[0]
        mult = len(g)
        letter = g.letter
        numIons = [c*mult for c in comp]
        sites = []
        for c in comp:
            sites.append([str(mult)+letter]*c)

        while True:
            if seed is None:
                np.random.seed()
            diag = choice([True, False])
            xtal = pyxtal(molecular=True)
            xtal.from_random(3, sg, smiles, numIons, force_pass=True, diag=diag)
            rep = representation.from_pyxtal(xtal)
            print(rep.x, smiles, composition, workdir, tag)
            print(atom_info)
            res = optimize(rep.x, smiles, comp, atom_info, workdir, tag)
            if res is not None:
                break
    elif isinstance(rep, str):
        rep = representation.from_string(rep, smiles, comp)

    go = BasinHopping(rep.x, sg, smile, atom_info, workdir, tag, optimize, kT, composition=comp)
    print('  0' + rep.to_string())
    go.run(steps, show)

    if xtal_ref is not None:
        go.check_ref(xtal_ref)


if __name__ == "__main__":
    from pyxtal import pyxtal
    from htocsp.localopt import optimize
    from htocsp.util import parse_mol
    from htocsp.interfaces.charmm import RTF, PRM
    from optparse import OptionParser
    import random

    parser = OptionParser()
    parser.add_option("-t", "--tag", dest="tag", default='job_bh',
                      help="job tag, optional")
    parser.add_option("-k", "--kT", dest="kT", type=float, default=0.5,
                      help="kT factor, optional")
    parser.add_option("-s", "--step", dest="step", type=int, default=10,
                      help="number of steps, optional")
    parser.add_option("-n", "--npar", dest="npar", type=int, default=1,
                      help="number of parallel computation, optional")
    parser.add_option("-r", "--repeats", dest="repeats", type=int, default=1,
                      help="repeat")


    (options, args) = parser.parse_args()
    random.seed(10)
    seed = 4 #needed for pyxtal orientation
    np.random.seed(seed)
    smile, workdir, name, sg, f, composition = 'CC(=O)OC1=CC=CC=C1C(=O)O', 'BH', 'ACSALA', 14, 'benchmarks/aspirin.cif', [1]
    xtal_ref = pyxtal(molecular=True)
    xtal_ref.from_seed(f, molecules=[smile+'.smi'])

    #print(xtal_ref)
    p_mol, rtf, prm = parse_mol(name=name, smi=smile)
    charmm_info = {}
    charmm_info['label']   = [p_mol.site_properties['charmm_label']]
    charmm_info['resName'] = [p_mol.site_properties['resName'][0]]
    prm = PRM(prm.split('\n')); rtf = RTF(rtf.split('\n'))
    charmm_info['prm'] = prm.to_string(); charmm_info['rtf'] = rtf.to_string()
    prm = open(workdir+'/pyxtal.prm', 'w'); prm.write(charmm_info['prm']); prm.close()
    rtf = open(workdir+'/pyxtal.rtf', 'w'); rtf.write(charmm_info['rtf']); rtf.close()

    rep = "14 0 11.43  6.49 11.19 83.31 1  0.77  0.57  0.53 48.55 24.31 145.9 -77.85 -4.40 170.9 0" #None
    tag = options.tag
    kT = options.kT
    steps = options.step
    npar = options.npar
    repeats = options.repeats

    basin_hopping_runner(smile, charmm_info, workdir, tag, sg, composition,\
                         optimize, kT, rep, steps, xtal_ref,
                         show=True, seed=seed)
