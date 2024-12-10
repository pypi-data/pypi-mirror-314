from typing import List


from nema.data.data_properties import DataProperties
from nema.connectivity import CONNECTIVITY_CONFIG
from nema.data.data import Data, FileData


def get_data_properties_from_global_id(global_id: int, branch: str) -> DataProperties:
    data = Data.init_from_cloud_and_download(global_id, branch=branch)

    if data.data.is_blob_data:
        data = FileData(
            _global_id=global_id,
            _data=data.data,
            _input_folder=CONNECTIVITY_CONFIG.nema_data_folder,
        )

        # TODO: this is super messy!
        if hasattr(data.data, "get_contents"):

            data.contents  # this downloads the file and extracts the contents

        elif hasattr(data.data, "get_file_name"):

            data.get_file_path()  # this downloads the file

    return data.data  # return the data properties


def convert_app_input_to_dict(inputs: dict, branch: str = "main") -> dict:
    """The input is a dictionary of global IDs. This function will convert the global IDs to the actual data properties"""
    converted_input = {}
    for key, value in inputs.items():
        if isinstance(value, list):
            converted_input[key] = [
                get_data_properties_from_global_id(v, branch) for v in value
            ]
        elif isinstance(value, dict):
            converted_input[key] = convert_app_input_to_dict(value, branch)
        else:
            converted_input[key] = get_data_properties_from_global_id(value, branch)

    return converted_input


def convert_app_output_to_nema_data(output, output_dict: dict) -> List[Data]:
    """The output is a dictionary of data properties. This function will convert the properties to Nema Data objects, which can be uploaded to Nema"""
    converted_output = []
    for key, value in output_dict.items():
        this_output = getattr(output, key)
        if isinstance(value, list):
            for idx, lv in enumerate(value):
                converted_output.append(
                    Data.init_from_properties(
                        global_id=lv, data_properties=this_output[idx]
                    )
                )
        elif isinstance(value, dict):
            for lk, lv in zip(value, getattr(output, key)):
                converted_output.append(
                    Data.init_from_properties(
                        global_id=lv, data_properties=this_output[lk]
                    )
                )
        else:
            converted_output.append(
                Data.init_from_properties(value, this_output, id_in_app=key)
            )

    return converted_output
