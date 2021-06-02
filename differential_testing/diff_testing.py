import os
import subprocess
import sys
from typing import Optional


def diff_testing(include_directory: Optional[str] = None):
    base_path = os.path.dirname(os.path.realpath(__file__))
    base_entry: os.DirEntry  # Type hint for entry variable
    input_entry: os.DirEntry

    if include_directory is None:
        include_directory = "./"
    elif not include_directory.endswith("/"):
        include_directory += "/"

    compiler_options = {
        "gcc": [
            "O0",
            "O1",
            "O2",
            "O3",
            "Os",
            "Ofast",
            "Og"
        ],
        "clang": [
            "O0",
            "O1",
            "O2",
            "O3",
            "Os",
            "Ofast",
            "Oz"
        ]
    }

    matches = 0
    mismatches = 0

    for base_entry in os.scandir(os.path.join(base_path, "programs")):
        if base_entry.is_dir():
            source_file = os.path.join(base_entry, f"{base_entry.name}.c")
            input_path = os.path.join(base_entry, "inputs")
            output_path = os.path.join(base_entry, "outputs")
            bin_path = os.path.join(base_entry, "bin")

            if not os.path.exists(output_path):
                os.mkdir(output_path)

            if not os.path.exists(bin_path):
                os.mkdir(bin_path)

            # For each compiler and optimization level -> Compile source file
            for compiler, options in compiler_options.items():
                for option in options:
                    # Compile source with given compiler and options
                    program_name = os.path.join(bin_path, f"{compiler}_{option}")
                    compile_command = subprocess.run([compiler, f"-{option}", "-o", program_name, source_file, f"-I{include_directory}"],
                                                     capture_output=True)

                    if compile_command.returncode != 0:
                        print(f"Could not compile source code!\n"
                              f"This is major error, the script is terminated.\n"
                              f"Here is some info that might help with finding the problem:\n"
                              f"Compiler: {compiler}\n"
                              f"Option: -{option}\n"
                              f"Source: {source_file}\n"
                              f"Subprocess error output:\n"
                              f"{compile_command.stderr.decode('utf-8')}",
                              file=sys.stderr)
                        exit(1)

                    # For every input -> Run compiled program with
                    for input_entry in os.scandir(input_path):
                        input_file = input_entry.path
                        run_command = subprocess.run([program_name, input_file], capture_output=True)

                        if run_command.returncode != 0:
                            print(f"Could not run compiled program!\n"
                                  f"This is major error, the script is terminated.\n"
                                  f"Here is some info that might help with finding the problem:\n"
                                  f"Compiler: {compiler}\n"
                                  f"Option: -{option}\n"
                                  f"Source: {source_file}\n"
                                  f"Executable: {program_name}\n"
                                  f"Subprocoess error output:\n"
                                  f"{run_command.stderr.decode('utf-8')}",
                                  file=sys.stderr)
                            exit(1)

                        output_file = os.path.join(output_path, f"{compiler}_{option}_{input_entry.name}")

                        with open(output_file, "w+") as f:
                            f.write(run_command.stdout.decode("utf-8"))

            # Loop over all input files and check the corresponding output files for every compiler
            for input_entry in os.scandir(input_path):
                reference_output = None
                reference_compiler = None
                reference_option = None

                for compiler, options in compiler_options.items():
                    for option in options:
                        output_file = os.path.join(output_path, f"{compiler}_{option}_{input_entry.name}")

                        if not os.path.exists(output_file):
                            print(f"Could not open output file!\n"
                                  f"This is major error, the script is terminated.\n"
                                  f"Here is some info that might help with finding the problem:\n"
                                  f"Compiler: {compiler}\n"
                                  f"Option: -{option}\n"
                                  f"Output File: {output_file}",
                                  file=sys.stderr)
                            exit(1)

                        with open(output_file, "r") as f:
                            this_output = f.read()

                        if reference_output is None:
                            reference_output = this_output
                            reference_compiler = compiler
                            reference_option = option
                        elif this_output != reference_output:
                            print(f"Mismatch found in {output_file}!\n"
                                  f"\t Current: {compiler} with option -{option}\n"
                                  f"\t Reference: {reference_compiler} with option -{reference_option}")
                            mismatches += 1
                        else:
                            matches += 1

    print("\n" + ("*" * 50) + "\n")
    print("Test summary:")
    print(f"{mismatches} mismatches found")
    print(f"{matches} matches found")
    print("\n" + ("*" * 50) + "\n")
    print("Conclusion:")

    if mismatches == 0:
        print("All compilations agree")
    else:
        print("There seem to be mismatches! Check above for which output files do not match...")


if __name__ == '__main__':
    diff_testing()
