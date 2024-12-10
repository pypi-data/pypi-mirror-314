from dataclasses import dataclass, field
import ast
from enum import StrEnum
from typing import List, Optional, Set, Any

from nema.data.data_type import DataType

### THIS IS PRETTY MUCH ALL COPIED FROM PROD CODE ###


@dataclass
class DataCoreSubTypeForAppArgument:
    type: Optional[DataType] = None
    union: Optional[Set[DataType]] = None
    any: Optional[List[Any]] = None

    def marshall(self):
        return {
            "type": self.type.value if self.type else None,
            "union": [t.value for t in self.union] if self.union else None,
            "any": self.any,
        }


@dataclass
class DataSubTypeForAppArgument(DataCoreSubTypeForAppArgument):
    list: Optional[DataCoreSubTypeForAppArgument] = None
    dictionary: Optional[DataCoreSubTypeForAppArgument] = None

    def marshall(self):
        core = super().marshall()
        return {
            **core,
            "list": self.list.marshall() if self.list else None,
            "dictionary": self.dictionary.marshall() if self.dictionary else None,
        }


@dataclass
class AppDataArgument:
    id_in_app: str
    description: str
    artifact_type: DataSubTypeForAppArgument

    def marshall(self):

        return {
            "id_in_app": self.id_in_app,
            "description": self.description,
            "artifact_type": self.artifact_type.marshall(),
        }


@dataclass
class AppIO:
    """
    Class used to keep the extracted input and output arguments from an app.
    """

    input_data: list[AppDataArgument] = field(default_factory=list)
    output_data: list[AppDataArgument] = field(default_factory=list)


NEMA_PY_TYPE_MAPPING = {
    "StringValue": DataType.STRING,
    "IntegerValue": DataType.INT,
    "FloatValue": DataType.FLOAT,
    "CurrencyValue": DataType.CURRENCY,
    "FloatValueWithArbitraryUnit": DataType.FLOAT_WITH_ARBITRARY_UNIT_V0,
    "IntValueWithArbitraryUnit": DataType.INT_WITH_ARBITRARY_UNIT_V0,
    "FloatValueWithPhysicalUnit": DataType.FLOAT_WITH_PHYSICAL_UNIT_V0,
    "IntValueWithPhysicalUnit": DataType.INT_WITH_PHYSICAL_UNIT_V0,
    "ArbitraryFile": DataType.ARBITRARY_FILE_V0,
    "ArbitraryFileCollection": DataType.ARBITRARY_FILE_COLLECTION_V0,
    "Dictionary": DataType.DICTIONARY_V0,
    "CSVData": DataType.CSV_V0,
    "Image": DataType.IMAGE_V0,
    "FloatVector": DataType.FLOAT_VECTOR_V0,
    "FloatVectorWithPhysicalUnits": DataType.FLOAT_VECTOR_WITH_PHYSICAL_UNITS_V0,
    "FloatMatrix": DataType.FLOAT_MATRIX_V0,
    "NormalDistribution": DataType.NORMAL_DISTRIBUTION_V0,
    "UniformDistribution": DataType.UNIFORM_DISTRIBUTION_V0,
    "ExponentialDistribution": DataType.EXPONENTIAL_DISTRIBUTION_V0,
    "TriangularDistribution": DataType.TRIANGULAR_DISTRIBUTION_V0,
}


def extract_input_and_output_from_python_contents(code: str) -> AppIO:

    tree = ast.parse(code)
    data_inputs = []
    data_outputs = []

    # Walk through the AST to find the run function
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "run":
            # Extract the argument type annotation of the `run` function
            for arg in node.args.args:
                if arg.annotation and isinstance(arg.annotation, ast.Name):
                    inputs_class_name = arg.annotation.id
                    data_inputs = extract_field_from_ast_tree(tree, inputs_class_name)

            # Extract the return type annotation of the `run` function
            if node.returns and isinstance(node.returns, ast.Name):
                outputs_class_name = node.returns.id
                data_outputs = extract_field_from_ast_tree(tree, outputs_class_name)

    return AppIO(
        input_data=data_inputs,
        output_data=data_outputs,
    )


def extract_field_from_ast_tree(
    tree: ast.Module, class_name: str
) -> list[AppDataArgument]:
    fields = []

    # Look for the class definition of the given class_name
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            # Extract fields from the dataclass
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign):
                    key = stmt.target.id

                    if isinstance(stmt.annotation, ast.Subscript) and isinstance(
                        stmt.annotation.value, ast.Name
                    ):
                        if stmt.annotation.value.id == "list":
                            # Extract the type(s) of the list
                            element_types = extract_types(stmt.annotation.slice)

                            artifact_type = DataSubTypeForAppArgument(
                                list=element_types,
                            )

                        elif stmt.annotation.value.id == "dict":

                            key_value_types = stmt.annotation.slice
                            if (
                                isinstance(key_value_types, ast.Tuple)
                                and len(key_value_types.elts) == 2
                            ):
                                # Extract key and value types, handling Union in value
                                key_type = extract_types(key_value_types.elts[0])[
                                    0
                                ]  # Keys are usually single types

                                if key_type != "str":
                                    raise ValueError(
                                        f"Invalid key type for dict: {key_type}. Only string is supported."
                                    )

                                value_types = extract_types(key_value_types.elts[1])
                                artifact_type = DataSubTypeForAppArgument(
                                    dictionary=value_types,
                                )
                            else:
                                raise ValueError(
                                    f"Invalid dict type annotation: {stmt.annotation}"
                                )

                        elif stmt.annotation.value.id == "Union":
                            # Extract all types within Union
                            if isinstance(stmt.annotation.slice, ast.Tuple):
                                artifact_type = DataSubTypeForAppArgument(
                                    union=[
                                        NEMA_PY_TYPE_MAPPING[elt.id]
                                        for elt in stmt.annotation.slice.elts
                                        if isinstance(elt, ast.Name)
                                    ]
                                )
                            elif isinstance(stmt.annotation.slice, ast.Name):
                                artifact_type = DataSubTypeForAppArgument(
                                    type=NEMA_PY_TYPE_MAPPING[stmt.annotation.slice.id]
                                )

                        else:
                            artifact_type = DataSubTypeForAppArgument(any=[])

                    elif isinstance(stmt.annotation, ast.Name):

                        if stmt.annotation.id.lower() == "any":
                            artifact_type = DataSubTypeForAppArgument(any=[])
                        else:
                            artifact_type = DataSubTypeForAppArgument(
                                type=NEMA_PY_TYPE_MAPPING[stmt.annotation.id]
                            )

                    else:
                        artifact_type = DataSubTypeForAppArgument(any=[])

                    fields.append(
                        AppDataArgument(
                            id_in_app=key,
                            description="",
                            artifact_type=artifact_type,
                        )
                    )

    return fields


def extract_types(annotation):
    """Recursively extract types from annotations."""
    if isinstance(annotation, ast.Name):
        # Single type like `int`, `str`, etc.
        return DataCoreSubTypeForAppArgument(type=NEMA_PY_TYPE_MAPPING[annotation.id])
    elif isinstance(annotation, ast.Subscript):
        # Handle subscripted types (e.g., Union, List, Dict)
        if isinstance(annotation.value, ast.Name) and annotation.value.id == "Union":
            # Extract all types within Union
            if isinstance(annotation.slice, ast.Tuple):
                return DataCoreSubTypeForAppArgument(
                    union=[
                        NEMA_PY_TYPE_MAPPING[elt.id]
                        for elt in annotation.slice.elts
                        if isinstance(elt, ast.Name)
                    ]
                )
            elif isinstance(annotation.slice, ast.Name):
                return DataCoreSubTypeForAppArgument(
                    type=NEMA_PY_TYPE_MAPPING[annotation.slice.id]
                )
        elif isinstance(annotation.slice, ast.Name):
            if annotation.slice.id.lower() == "any":
                return DataCoreSubTypeForAppArgument(any=[])

            return DataCoreSubTypeForAppArgument(
                type=NEMA_PY_TYPE_MAPPING[annotation.slice.id]
            )
        elif isinstance(annotation.slice, ast.Tuple):
            return DataCoreSubTypeForAppArgument(
                union=[
                    NEMA_PY_TYPE_MAPPING[elt.id]
                    for elt in annotation.slice.elts
                    if isinstance(elt, ast.Name)
                ]
            )
    elif isinstance(annotation, ast.Tuple):
        # Handle tuple types directly
        return DataCoreSubTypeForAppArgument(
            union=[
                NEMA_PY_TYPE_MAPPING[elt.id]
                for elt in annotation.elts
                if isinstance(elt, ast.Name)
            ]
        )

    return DataCoreSubTypeForAppArgument(any=[])


######


def find_matches_in_workflow_arguments(
    arguments: List[dict],
    id_in_app: str,
):

    return [x for x in arguments if x["id_in_app"] == id_in_app]


def map_workflow_arguments_to_app_arguments(
    workflow_arguments: List[dict],
    app_arguments: List[AppDataArgument],
):

    app_inputs = {}
    for input_data_type in app_arguments:
        id_in_app = input_data_type.id_in_app

        argument_matches = find_matches_in_workflow_arguments(
            workflow_arguments, id_in_app
        )

        if (
            input_data_type.artifact_type.type is not None
            or input_data_type.artifact_type.any is not None
        ):
            assert len(argument_matches) == 1

            global_id_of_match = argument_matches[0]["artifact"]

            app_inputs[id_in_app] = global_id_of_match

        elif input_data_type.artifact_type.dictionary is not None:
            this_dict = {}
            for argument_match in argument_matches:
                global_id_of_match = argument_match["artifact"]
                this_dict[argument_match.member_type.key_in_dictionary] = (
                    global_id_of_match
                )
            app_inputs[id_in_app] = this_dict

        elif input_data_type.artifact_type.list is not None:
            this_list = [None for _ in argument_matches]
            for argument_match in argument_matches:
                global_id_of_match = argument_match["artifact"]
                idx = argument_match["member_type"]["index_in_list"]
                this_list[idx] = global_id_of_match
            app_inputs[id_in_app] = this_list

    return app_inputs
