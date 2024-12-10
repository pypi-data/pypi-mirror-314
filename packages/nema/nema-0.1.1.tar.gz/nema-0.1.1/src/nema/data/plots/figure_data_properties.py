from dataclasses import dataclass
from typing import Optional

from nema.data.data_properties import DataProperties, FileDataProperties


@dataclass
class FigureDataProperties(DataProperties):
    pass


@dataclass
class Image(FigureDataProperties, FileDataProperties):

    extension: Optional[str] = None

    def get_default_file_extension(self):
        return self.extension if self.extension else "png"

    @property
    def data_type(self):
        return "IMAGE.V0"
