import warnings
import random
from pathlib import Path
import pandas as pd

from pymatgen.core import Structure
from pymatgen.core.lattice import Lattice

from torch.utils.data import Dataset
from torch_geometric.data import Data

from chemeleon.datasets.dataset_utils import atoms_to_pyg_data


warnings.filterwarnings("ignore", message="Issues encountered while parsing CIF:")


class MPGNoMEDataset(Dataset):
    def __init__(
        self,
        data_dir: str,
        split: str,
        text_guide: bool = False,
        composition_guide: bool = False,
        property_guide: bool = False,
    ):
        super().__init__()
        self.data_dir = Path(data_dir)
        self.split = split
        self.text_guide = text_guide
        self.composition_guide = composition_guide
        self.property_guide = property_guide

        path_data = Path(self.data_dir, f"{self.split}.h5")
        if not path_data.exists():
            raise FileNotFoundError(f"{path_data} does not exist.")
        self.data = pd.read_hdf(path_data, key="df")
        self.data = self.data[["id", "cif"]]
        if text_guide:
            if composition_guide:
                pass
            elif property_guide:
                path_property = Path(self.data_dir, "crystal_text.csv")
                df_property = pd.read_csv(path_property)
                self.data = self.data.merge(df_property, on="id")
            else:
                path_prompt = Path(self.data_dir, "prompt.h5")
                if not path_prompt.exists():
                    raise FileNotFoundError(f"{path_prompt} does not exist.")
                df_prompt = pd.read_hdf(path_prompt, key="df")
                self.data = self.data.merge(df_prompt, on="id")

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Data:
        data = self.data.iloc[idx]
        str_cif = data.cif
        # read cif
        st = Structure.from_str(str_cif, fmt="cif")
        # niggli reduction
        reduced_st = st.get_reduced_structure()
        canonical_st = Structure(
            lattice=Lattice.from_parameters(*reduced_st.lattice.parameters),
            species=reduced_st.species,
            coords=reduced_st.frac_coords,
            coords_are_cartesian=False,
        )
        # convert to ase atoms
        atoms = canonical_st.to_ase_atoms()
        if self.text_guide:
            if self.composition_guide:
                text = st.composition.alphabetical_formula
            elif self.property_guide:
                properties = [
                    f"composition: {st.composition.alphabetical_formula}",
                    f"crystal system: {data['crystal_system']}",
                    f"space group symbol: {data['space_group_symbol']}",
                    f"dimensionality: {data['dimensionality']} D",
                ]
                random.shuffle(properties)
                text = ", ".join(properties)
            else:
                rand_int = random.randint(0, 4)
                text = data[f"prompt_{rand_int}"]
                # all_texts = [data[f"prompt_{i}"] for i in range(5)] # TODO
            return atoms_to_pyg_data(atoms, text=text)
        else:
            return atoms_to_pyg_data(atoms)
