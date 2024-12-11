import MDAnalysis as mda
import numpy as np
from tqdm import tqdm

class FlipFlopAnalysis:
    def __init__(self, tpr_file, trj_file):
        """
        Initialize the FlipFlopAnalysis class with the necessary files.

        :param tpr_file: Path to the topology file (.tpr)
        :param trj_file: Path to the trajectory file (.xtc, .trr, etc.)
        """
        self.tpr_file = tpr_file
        self.trj_file = trj_file
        self.u = mda.Universe(tpr_file, trj_file)
        self.drug_selection = None
        self.membrane_selection = None
        self.num_molecules = 20  # Default number of molecules

    def select_drugs(self, lig_resname):
        """
        Select the drug residues.

        :param lig_resname: Residue name of the ligand (e.g., 'ETOH')
        """
        self.drug_selection = self.u.select_atoms(f'resname {lig_resname} and name C2')

    def select_membrane(self, membrane_name):
        """
        Select the membrane atoms.

        :param membrane_name: Atom name of the membrane (e.g., 'P')
        """
        self.membrane_selection = self.u.select_atoms(f'name {membrane_name}')

    def set_num_molecules(self, num_molecules):
        """
        Set the number of drug molecules in the model system.

        :param num_molecules: Number of drug molecules in the system
        """
        self.num_molecules = num_molecules

    def _get_leaflet_region(self, z, zmid):
        """
        Determine the leaflet region based on z-coordinate and midplane.

        :param z: z-coordinate of the atom
        :param zmid: Middle z-coordinate (membrane midplane)
        :return: 'U' (upper leaflet), 'L' (lower leaflet), or 'M' (middle region)
        """
        zmid_lower = zmid - 2.5
        zmid_upper = zmid + 2.5
        if z > zmid_upper:
            return 'U'
        elif z < zmid_lower:
            return 'L'
        else:
            return 'M'

    def analyze(self, max_time_ns=None):
        """
        Perform the flip-flop analysis.

        :param max_time_ns: Maximum time (in nanoseconds) to analyze (default: None for full trajectory)
        :return: A dictionary with flip-flop counts, z-coordinates, and times
        """
        if self.drug_selection is None or self.membrane_selection is None:
            raise ValueError("Drug and membrane selections must be set before analysis.")

        times, z_lig, z_p = [], [], []

        frames = list(self.u.trajectory)
        if max_time_ns:
            frames = [ts for ts in frames if ts.time / 1000 <= max_time_ns]

        z_p2 = []

        with tqdm(total=len(frames), desc="Processing trajectory frames") as pbar:
            for ts in frames:
                time_ns = ts.time / 1000  # Convert time to nanoseconds
                times.append(time_ns)
                z_lig.append(self.drug_selection.positions[:, 2])
                z_p_frame = self.membrane_selection.positions[:, 2]
                z_p.append(z_p_frame)
                z_p2.extend(z_p_frame)
                pbar.update(1)

        zmin, zmax = np.amin(z_p2), np.amax(z_p2)
        zmid = (zmax + zmin) / 2

        flipflop_count = [0] * self.num_molecules
        prev_regions = [None] * self.num_molecules
        midpoint_crossed = [False] * self.num_molecules
        region_counts = [0] * self.num_molecules

        # Analyze flip-flops
        for j in range(self.num_molecules):
            z_lig_foreach = [z[j] for z in z_lig]

            for i, z in enumerate(z_lig_foreach):
                current_region = self._get_leaflet_region(z, zmid)

                if prev_regions[j] is not None and current_region != prev_regions[j]:
                    if current_region == 'M':
                        midpoint_crossed[j] = True
                    elif midpoint_crossed[j]:
                        if (current_region == 'U' and prev_regions[j] == 'L') or (current_region == 'L' and prev_regions[j] == 'U'):
                            flipflop_count[j] += 1
                            midpoint_crossed[j] = False
                        if current_region != 'M':
                            region_counts[j] += 1

                prev_regions[j] = current_region

        total_flipflop_count = sum(flipflop_count)
        avg_flipflop_count = total_flipflop_count / self.num_molecules

        return {
            'times': times,
            'z_lig': z_lig,
            'z_p': z_p,
            'zmin': zmin,
            'zmax': zmax,
            'zmid': zmid,
            'flipflop_count': flipflop_count,
            'total_flipflop_count': total_flipflop_count,
            'avg_flipflop_count': avg_flipflop_count
        }
