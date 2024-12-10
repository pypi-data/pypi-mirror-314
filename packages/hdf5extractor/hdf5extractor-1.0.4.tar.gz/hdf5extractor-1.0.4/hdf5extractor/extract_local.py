#
# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
#
import argparse
import os
import re
import zipfile
from io import BytesIO

from hdf5extractor.h5handler import (
    write_h5,
    find_data_ref_in_xml,
    write_h5_memory_in_local,
    find_data_ref_in_energyml_files,
)
from hdf5extractor.common import FILE_NAME_REGEX


def process_files_old(
    file_path: str, input_h5: str, output_folder: str, overwrite=False
):
    print(FILE_NAME_REGEX)
    to_process_files = []
    if file_path.endswith(".xml"):
        file_name = file_path
        if "/" in file_name:
            file_name = file_name[file_name.rindex("/") + 1 :]
        if "\\" in file_name:
            file_name = file_name[file_name.rindex("\\") + 1 :]

        xml_content = open(file_path, "rb").read()
        to_process_files.append((xml_content, file_name))
    elif file_path.endswith(".epc"):
        with zipfile.ZipFile(file_path) as epc_as_zip:
            for f_name in epc_as_zip.namelist():
                if not f_name.startswith("_rels/") and re.match(
                    FILE_NAME_REGEX, f_name
                ):
                    with epc_as_zip.open(f_name) as myfile:
                        to_process_files.append((myfile.read(), f_name))

    for f_content, f_name in to_process_files:
        write_h5(
            input_h5,
            output_folder + "/" + f_name[: f_name.rindex(".")] + ".h5",
            find_data_ref_in_xml(f_content),
            overwrite,
        )


def process_files_memory(file_path: str, input_h5: str, single_file: bool):
    to_process_files = []
    if file_path.endswith(".xml"):
        file_name = file_path
        if "/" in file_name:
            file_name = file_name[file_name.rindex("/") + 1 :]
        if "\\" in file_name:
            file_name = file_name[file_name.rindex("\\") + 1 :]

        xml_content = open(file_path, "rb").read()
        to_process_files.append((xml_content, file_name))
    elif file_path.endswith(".epc"):
        with zipfile.ZipFile(file_path) as epc_as_zip:
            for f_name in epc_as_zip.namelist():
                if not f_name.startswith("_rels/") and re.match(
                    FILE_NAME_REGEX, f_name
                ):
                    with epc_as_zip.open(f_name) as myfile:
                        to_process_files.append((myfile.read(), f_name))

    mapper = {}
    if single_file:
        lll = []
        for f_content, f_name in to_process_files:
            data_refs = find_data_ref_in_xml(f_content)
            if data_refs is not None:
                print("-", data_refs.values())
                lll = lll + list(data_refs.values())[0]
        try:
            print(lll)
            mapper[f_name] = write_h5_memory_in_local(
                input_h5,
                lll,
            )
        except Exception:
            print(f"Error with file : {f_name}")
    else:
        for f_content, f_name in to_process_files:
            try:
                data_refs = find_data_ref_in_xml(f_content)
                if data_refs is not None:
                    mapper[f_name] = write_h5_memory_in_local(
                        input_h5,
                        list(data_refs.values())[0],
                    )
            except Exception:
                print(f"Error with file : {f_name}")
    # filter None
    mapper = {k: v for k, v in mapper.items() if v is not None}

    # print(mapper)
    return mapper


def process_files(
    file_path: str, input_h5: str, output_folder: str, single_file: bool, overwrite=False
):
    h5_name = os.path.basename(file_path)[:-4] + ".h5"
    mini_h5_map = process_files_memory(file_path, input_h5, single_file)
    print(mini_h5_map)

    if single_file:
        with open(output_folder + "/" + h5_name, "wb") as file:
            for f_name in mini_h5_map:
                print(f"{f_name} : {mini_h5_map[f_name]}")
                file.write(mini_h5_map[f_name].getbuffer())
    else:
        for f_name in mini_h5_map:
            print(f"{f_name} : {mini_h5_map[f_name]}")
            with open(
                    output_folder + "/" + f_name[: f_name.rindex(".")] + ".h5", "wb"
            ) as file:
                file.write(mini_h5_map[f_name].getbuffer())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=str,
        help="[Required] Input file (xml of epc) from which the\
        referenced data path are taken",
    )
    parser.add_argument(
        "--h5",
        required=True,
        type=str,
        help="[Required] Input h5 file or folder that contains h5 files",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="extracted",
        type=str,
        help="H5 output folder",
    )
    # parser.add_argument(
    #     "--force",
    #     "-f",
    #     action="store_true",
    #     help="Force the overwrite the output files if allready exists",
    # )
    parser.add_argument(
        "--group",
        "-g",
        action="store_true",
        help="Group all individual h5 files",
    )
    args = parser.parse_args()

    try:
        os.makedirs(args.output)
    except OSError:
        pass

    print("reading", args.input)
    process_files(
        file_path=args.input,
        input_h5=args.h5,
        output_folder=args.output,
        # overwrite=args.force,
        single_file=args.group,
    )
