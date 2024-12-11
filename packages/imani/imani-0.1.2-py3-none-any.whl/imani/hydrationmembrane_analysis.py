import numpy as np
import MDAnalysis as mda
from tqdm import tqdm
from MDAnalysis.lib import distances
import pandas as pd

class HydrationMembraneAnalysis:
    def __init__(self, trj, top):
        """
        Initialize with trajectory and topology files.

        :param trj: Path to the trajectory file (.xtc, .trr, etc.)
        :param top: Path to the topology file (.tpr, .gro, etc.)
        """
        self.universe = mda.Universe(top, trj)
        self.drug_atoms_groups = None
        self.membrane_atoms = None
        self.water_atoms = None
        self.cutoffs = None
        self.num_oxygens = 4  # Default to 4 oxygens, can be updated by the user

    def select_drug_atoms(self, resname, num_oxygens):
        """
        Select drug oxygen atoms based on resname and number of oxygens.

        :param resname: Residue name of the drug (e.g., 'ASP')
        :param num_oxygens: Number of oxygen atoms in the drug
        """
        self.num_oxygens = num_oxygens
        self.drug_atoms_groups = [
            self.universe.select_atoms(f'resname {resname} and name O{i}')
            for i in range(1, num_oxygens + 1)
        ]

    def select_membrane_atoms(self, selection):
        """
        Select membrane atoms.

        :param selection: Selection string for membrane atoms (e.g., 'resname DPPC and name P')
        """
        self.membrane_atoms = self.universe.select_atoms(selection)

    def select_water_atoms(self, selection):
        """
        Select water atoms.

        :param selection: Selection string for water atoms (e.g., 'resname TIP3 and name OH2')
        """
        self.water_atoms = self.universe.select_atoms(selection)

    def set_cutoffs(self, cutoffs):
        """
        Set cutoff distances for hydration analysis.

        :param cutoffs: List of cutoff distances for each oxygen atom
        """
        if len(cutoffs) != self.num_oxygens:
            raise ValueError("Number of cutoffs must match the number of oxygens in the drug.")
        self.cutoffs = cutoffs

    def calculate_hydration(self):
        """
        Perform hydration analysis.

        :return: A dictionary containing average hydration counts and dzmem value
        """
        if not (self.drug_atoms_groups and self.membrane_atoms and self.water_atoms and self.cutoffs):
            raise ValueError("Drug, membrane, water atoms, and cutoffs must be set before analysis.")

        count2 = [np.zeros(100) for _ in range(self.num_oxygens)]
        num = [np.zeros(100) for _ in range(self.num_oxygens)]
        dzmem = 0

        with tqdm(total=len(self.universe.trajectory), desc="Processing trajectory frames") as pbar:
            for ts in self.universe.trajectory:
                midpoint = np.mean(self.membrane_atoms.positions[:, 2])
                lower = np.min(self.membrane_atoms.positions[:, 2])
                upper = np.max(self.membrane_atoms.positions[:, 2])
                dzmem = ((upper - midpoint) + (midpoint - lower)) / 2.0

                for i in range(self.num_oxygens):
                    for asp_atoms in self.drug_atoms_groups[i]:
                        dz = abs(asp_atoms.positions[:, 2] - midpoint)
                        iz = int(dz)

                        asp_tip3_distances = distances.distance_array(asp_atoms.positions, self.water_atoms.positions)
                        count = np.sum(asp_tip3_distances < self.cutoffs[i])

                        if iz < len(count2[i]):
                            count2[i][iz] += count
                            num[i][iz] += 1
                pbar.update(1)

        average_counts = [count / (num[i] + 1e-6) for i, count in enumerate(count2)]
        return {
            'average_counts': average_counts,
            'dzmem': dzmem
        }
