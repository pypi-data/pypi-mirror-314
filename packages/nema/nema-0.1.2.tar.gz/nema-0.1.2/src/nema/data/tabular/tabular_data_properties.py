import pandas as pd
from dataclasses import dataclass
from typing import Optional
import os

from nema.utils.file_name import generate_random_file_name
from nema.data.data_properties import BlobDataProperties


@dataclass
class TableDataProperties(BlobDataProperties):
    pass


@dataclass
class CSVData(TableDataProperties):
    df: Optional[pd.DataFrame] = None

    def __nema_marshall__(self):
        return {}

    @classmethod
    def __nema_unmarshall__(cls, data: dict):
        return cls()

    def get_value(self):
        return self.df

    def write_data_to_file_and_return_file_name(self, destination_folder: str):
        # move to destination folder
        output_file_name = generate_random_file_name("csv")
        destination_file_path = os.path.join(destination_folder, output_file_name)

        self.df.to_csv(destination_file_path, index=False)

        return output_file_name

    def get_contents(self) -> pd.DataFrame:
        return self.df

    def extract_contents(self, file_path: str):
        self.df = pd.read_csv(file_path)

        return self.df

    @property
    def data_type(self):
        return "CSV.V0"
