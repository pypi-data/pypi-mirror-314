from tqdm import tqdm
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib import distances


class HydrationAnalysis:
    def __init__(self, trj, top):
        """Initialize with trajectory and topology files."""
        self.universe = mda.Universe(top, trj)
        self.drug_atoms_groups = None
        self.micelle_atoms = None
        self.interface_atoms = None
        self.water_atoms = None

    def select_drug_atoms(self, resname, num_oxygens):
        """Select drug oxygen atoms based on resname and number of oxygens."""
        self.drug_atoms_groups = [
            self.universe.select_atoms(f'resname {resname} and name O{i}')
            for i in range(1, num_oxygens + 1)
        ]

    def select_micelle_atoms(self, selection='resname TRITO and (name C19 C20 C21 C22 C23 C24)'):
        """Select micelle atoms."""
        self.micelle_atoms = self.universe.select_atoms(selection)

    def calculate_interface(self):
        """Calculate the interface atoms of the micelle using the selected micelle atoms."""
        micelle_com = self.micelle_atoms.center_of_mass()
        distances_to_com = np.linalg.norm(self.micelle_atoms.positions - micelle_com, axis=1)

        # Define interface threshold as the top 10% farthest atoms
        threshold_distance = np.percentile(distances_to_com, 90)
        self.interface_atoms = self.micelle_atoms[distances_to_com >= threshold_distance]
        print(f"Interface calculated: {len(self.interface_atoms)} atoms selected as interface.")

    def select_water_atoms(self, selection='resname SOL and name OW'):
        """Select water molecules."""
        self.water_atoms = self.universe.select_atoms(selection)

    def calculate_hydration(self, cutoffs, skip=10):
        """
        Calculate hydration analysis.
        Calculates Δr and hydration data for solubilized and non-solubilized drugs.
        """
        count2 = [np.zeros(100) for _ in range(len(cutoffs))]  # Initialize arrays for counts
        num = [np.zeros(100) for _ in range(len(cutoffs))]     # Initialize arrays for occurrences
        frames = list(self.universe.trajectory[::skip])
        hydration_data = {f'O{i}': {"delta_r": [], "water_counts": []} for i in range(1, len(cutoffs) + 1)}

        with tqdm(total=len(frames), desc="Processing hydration frames") as pbar:
            for ts in frames:
                micelle_com = self.micelle_atoms.center_of_mass()

                for i, drug_atoms in enumerate(self.drug_atoms_groups):
                    for drug_atom in drug_atoms:
                        # Calculate rd: Distance of drug oxygen atom to micelle center of mass
                        rd = np.linalg.norm(drug_atom.position - micelle_com)

                        # Calculate Δr
                        delta_r = rd - micelle_com[2]  # Use z-component of micelle COM for interface alignment
                        bin_index = int(abs(delta_r))  # Convert Δr to an index

                        # Count water molecules around drug oxygen within cutoff
                        water_distances = distances.distance_array(drug_atom.position.reshape(1, -1), self.water_atoms.positions)
                        count = np.sum(water_distances < cutoffs[i])

                        # Update count2 and num arrays
                        if bin_index < len(count2[i]):
                            count2[i][bin_index] += count
                            num[i][bin_index] += 1

                        # Append to hydration data for plotting
                        hydration_data[f'O{i + 1}']["delta_r"].append(delta_r)
                        hydration_data[f'O{i + 1}']["water_counts"].append(count)

                pbar.update(1)

        # Calculate average counts
        average_counts = [count / (num[i] + 1e-6) for i, count in enumerate(count2)]
        return hydration_data, average_counts
