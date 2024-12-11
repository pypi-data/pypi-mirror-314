import numpy as np
import MDAnalysis as mda
from tqdm import tqdm

class OrientationAnalysis:
    def __init__(self, trj, top):
        """
        Initialize with trajectory and topology files.

        :param trj: Path to the trajectory file (.xtc, .trr, etc.)
        :param top: Path to the topology file (.tpr, .gro, etc.)
        """
        self.universe = mda.Universe(top, trj)
        self.drug_selection = None
        self.membrane_selection = None
        self.tilt_atoms = None

    def select_drugs(self, resname, tilt_atoms):
        """
        Select the drug residue and tilt atoms.

        :param resname: Residue name of the drug (e.g., 'ASP')
        :param tilt_atoms: List of two atom names used for tilt vector calculation (e.g., ['C1', 'C3'])
        """
        self.drug_selection = self.universe.select_atoms(f'resname {resname}')
        self.tilt_atoms = tilt_atoms

    def select_membrane(self, selection):
        """
        Select membrane atoms.

        :param selection: Selection string for membrane atoms (e.g., 'name P')
        """
        self.membrane_selection = self.universe.select_atoms(selection)

    def analyze_orientation(self):
        """
        Perform orientation analysis.

        :return: A dictionary containing tilt angles, cos(theta), and z-coordinates
        """
        if self.drug_selection is None or self.membrane_selection is None or not self.tilt_atoms:
            raise ValueError("Drug, membrane, and tilt atoms must be set before analysis.")

        lig_resids = self.drug_selection.residues.resids
        ff_cos_theta, ff_tilt, ff_zatom = [], [], []

        with tqdm(total=len(self.universe.trajectory), desc="Processing trajectory frames") as pbar:
            for ts in self.universe.trajectory:
                for resid in lig_resids:
                    coord_atom1 = self.universe.select_atoms(
                        f'resname {self.drug_selection.resnames[0]} and name {self.tilt_atoms[0]} and resid {resid}',
                        updating=True
                    ).positions
                    coord_atom2 = self.universe.select_atoms(
                        f'resname {self.drug_selection.resnames[0]} and name {self.tilt_atoms[1]} and resid {resid}',
                        updating=True
                    ).positions

                    if coord_atom1.size > 0 and coord_atom2.size > 0:
                        vector_1_2 = coord_atom1 - coord_atom2
                        vector_1_2 = vector_1_2.flatten()

                        midpoint = np.mean(self.membrane_selection.positions[:, 2])
                        normal = np.array([0, 0, -1]) if coord_atom1[0, 2] > midpoint else np.array([0, 0, -1])

                        dot_product = np.dot(vector_1_2, normal)
                        length_1_2 = np.linalg.norm(vector_1_2)
                        cos_theta = dot_product / length_1_2
                        theta = np.degrees(np.arccos(cos_theta))

                        ff_cos_theta.append(cos_theta)
                        ff_tilt.append(theta)
                        ff_zatom.append(coord_atom1[0, 2])

                pbar.update(1)

        return {
            'cos_theta': ff_cos_theta,
            'tilt_angles': ff_tilt,
            'z_coordinates': ff_zatom
        }
