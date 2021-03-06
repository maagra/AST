import os
import sys
import shutil

from generate_random_programs.generate_random_programs import generate_random_programs
from source_to_source_translation.source_to_source_translation import source_to_source_translation
from afl_find_inputs.afl_find_inputs import afl_find_inputs
from differential_testing.diff_testing import diff_testing

RANDOM_PROGRAM_COUNT = 5
AFL_FUZZING_DURATION = 900  # in seconds -> 15 minutes
CSMITH_INCLUDE_DIRECTORY = "/home/sgruebel/installations/csmith/include"


def setup_test(csmith_include: str):
    # Check if all required programs are found
    required_programs = [
        "csmith",
        "afl-gcc-fast",
        "afl-fuzz",
        "afl-cmin"
    ]
    found = list(map(lambda program: shutil.which(program) is not None, required_programs))

    if not all(found):
        print("Oops, seems like your setup is not quite ready for this...\n"
              "The following programs are required:", file=sys.stderr)
        for p, f in zip(required_programs, found):
            print(f"- \"{p}\" ({'found...' if f else 'not found!'})", file=sys.stderr)
        exit(1)

    # Check if the provided CSmith include directory contains csmith.h
    if not os.path.exists(csmith_include):
        print(f"Oops, seems like your setup is not quite ready for this...\n"
              f"The provided include directory for CSmith does not exist!\n"
              f"You provided: {csmith_include}", file=sys.stderr)
        exit(1)

    header_file_path = os.path.join(csmith_include, "csmith.h")

    if not os.path.exists(header_file_path) or not os.path.isfile(header_file_path):
        print(f"Oops, seems like your setup is not quite ready for this...\n"
              f"The provided include directory for CSmith does not contain a file named \"csmith.h\"!\n"
              f"You provided: {csmith_include}", file=sys.stderr)
        exit(1)


def transfer_random_to_s2s():
    # SRC: ./generate_random_programs/random_programs/{filename}
    # DST: ./source_to_source_translation/programs/{filename}
    base_path = os.path.dirname(os.path.realpath(__file__))
    src_path = os.path.join(base_path, "generate_random_programs", "random_programs")
    dst_path = os.path.join(base_path, "source_to_source_translation", "programs")
    program_entry: os.DirEntry

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    for program_entry in os.scandir(src_path):
        if program_entry.is_file():
            src_file = program_entry.path
            dst_file = os.path.join(dst_path, program_entry.name)
            shutil.copy(src_file, dst_file)


def transfer_s2s_to_afl():
    # SRC: ./source_to_source_translation/tokenized/{programname}/*
    # DST: ./afl_find_inputs/programs/{programname}/*
    base_path = os.path.dirname(os.path.realpath(__file__))
    src_path = os.path.join(base_path, "source_to_source_translation", "tokenized")
    dst_path = os.path.join(base_path, "afl_find_inputs", "programs")
    program_entry: os.DirEntry

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    for program_entry in os.scandir(src_path):
        if program_entry.is_dir():
            program_path = program_entry.path
            program_dst_path = os.path.join(dst_path, program_entry.name)

            if not os.path.exists(program_dst_path):
                os.mkdir(program_dst_path)

            program_src_file = os.path.join(program_path, f"{program_entry.name}.c")
            program_dst_file = os.path.join(program_dst_path, f"{program_entry.name}.c")
            shutil.copy(program_src_file, program_dst_file)

            input_src_file = os.path.join(program_path, "initial_input.txt")
            input_dst_file = os.path.join(program_dst_path, "initial_input.txt")
            shutil.copy(input_src_file, input_dst_file)


def transfer_afl_to_diff():
    # SRC 1: ./afl_find_inputs/programs/{programname}/{programname}.c
    # SRC 2: ./afl_find_inputs/programs/{programname}/unique/*
    # DST 1: ./differential_testing/programs/{programname}/{programname}.c
    # DST 2: ./differential_testing/programs/{programname}/inputs/*
    base_path = os.path.dirname(os.path.realpath(__file__))
    src_path = os.path.join(base_path, "afl_find_inputs", "programs")
    dst_path = os.path.join(base_path, "differential_testing", "programs")
    program_entry: os.DirEntry
    input_entry: os.DirEntry

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    for program_entry in os.scandir(src_path):
        if program_entry.is_dir():
            program_dst_path = os.path.join(dst_path, program_entry.name)

            program_src_file = os.path.join(program_entry.path, f"{program_entry.name}.c")
            program_dst_file = os.path.join(program_dst_path, f"{program_entry.name}.c")
            unique_dst_path = os.path.join(program_dst_path, "inputs")
            unique_src_path = os.path.join(program_entry.path, "unique")

            unique_dir_scanner = list(os.scandir(unique_src_path))
            if len(unique_dir_scanner) == 0:
                print(f"The \"unique\" directory of \"{program_entry.name}\" is empty. Not copying...")
                continue

            if not os.path.exists(program_dst_path):
                os.mkdir(program_dst_path)

            shutil.copy(program_src_file, program_dst_file)

            if not os.path.exists(unique_dst_path):
                os.mkdir(unique_dst_path)

            for i, input_entry in enumerate(unique_dir_scanner):
                if input_entry.is_file():
                    input_src_file = input_entry.path
                    input_dst_file = os.path.join(unique_dst_path, f"unique_input_{i}")
                    shutil.copy(input_src_file, input_dst_file)


def run_tests():
    # STEP 0: Setup checker
    setup_test(CSMITH_INCLUDE_DIRECTORY)

    # STEP 1: Generate random C programs
    generate_random_programs(RANDOM_PROGRAM_COUNT)

    # TRANSFER 1: csmith -> s2s
    transfer_random_to_s2s()

    # STEP 2: Source-to-source translation
    source_to_source_translation()

    # TRANSFER 2: s2s -> AFL
    transfer_s2s_to_afl()

    # STEP 3: AFL fuzzing
    afl_find_inputs(AFL_FUZZING_DURATION, CSMITH_INCLUDE_DIRECTORY)

    # TRANSFER 3: AFL -> Diff
    transfer_afl_to_diff()

    # STEP 4: Differential testing
    diff_testing(CSMITH_INCLUDE_DIRECTORY)


if __name__ == '__main__':
    run_tests()
