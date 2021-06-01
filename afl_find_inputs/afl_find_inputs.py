import os
import shutil
import subprocess
import sys

AFL_FUZZING_TIMEOUT = 10


def afl_find_inputs():
    base_path = os.path.dirname(os.path.realpath(__file__))
    base_entry: os.DirEntry

    for base_entry in os.scandir(os.path.join(base_path, "programs")):
        if base_entry.is_dir():
            source_file = os.path.join(base_entry, f"{base_entry.name}.c")
            input_file_src = os.path.join(base_entry, "initial_input.txt")
            input_dir_path = os.path.join(base_entry, "inputs")
            input_file_dst = os.path.join(input_dir_path, "initial_input.txt")
            output_dir_path = os.path.join(base_entry, "outputs")
            queue_dir_path = os.path.join(output_dir_path, "default", "queue")
            unique_dir_path = os.path.join(base_entry, "unique")
            bin_dir_path = os.path.join(base_entry, "bin")
            bin_file = os.path.join(bin_dir_path, base_entry.name)

            if not os.path.exists(input_dir_path):
                os.mkdir(input_dir_path)

            if not os.path.exists(output_dir_path):
                os.mkdir(output_dir_path)

            if not os.path.exists(unique_dir_path):
                os.mkdir(unique_dir_path)

            if not os.path.exists(bin_dir_path):
                os.mkdir(bin_dir_path)

            # Process output
            print(f"Starting fuzzing process of program \"{base_entry.name}\"")

            # Compile the source file with AFL++
            compile_command = subprocess.run(["afl-gcc-fast", "-o", bin_file, source_file], capture_output=True)

            if compile_command.returncode != 0:
                print(f"Could not compile source code for AFL++!\n"
                      f"This is a major error, the script is terminated.\n"
                      f"Here is some info that might help with finding the problem:\n"
                      f"Source: {source_file}\n"
                      f"Binary: {bin_file}\n"
                      f"Subprocess error output:\n"
                      f"{compile_command.stderr}",
                      file=sys.stderr)
                exit(1)

            # Copy the initial test case to the inputs directory
            shutil.copyfile(input_file_src, input_file_dst)

            # Run AFL++ on the compiled executable
            afl_command = subprocess.run(["afl-fuzz", "-i", input_dir_path, "-o", output_dir_path, "-V", str(AFL_FUZZING_TIMEOUT), "--", bin_file, "@@"],
                                         capture_output=True)

            if afl_command.returncode != 0:
                print(f"Could not run AFL++ on the compiled program!\n"
                      f"This is a major error, the script is terminated.\n"
                      f"Here is some info that might help with finding the problem:\n"
                      f"Source: {source_file}\n"
                      f"Binary: {bin_file}\n"
                      f"Subprocess error output:\n"
                      f"{afl_command.stdout.decode('utf-8')}",
                      file=sys.stderr)
                exit(1)

            # Run afl-cmin to get minimal test inputs
            cmin_command = subprocess.run(["afl-cmin", "-i", queue_dir_path, "-o", unique_dir_path, "--", bin_file, "@@"],
                                          capture_output=True)

            if cmin_command.returncode != 0:
                print(f"Could not minimize the test inputs!\n"
                      f"This is a major error, the script is terminated.\n"
                      f"Here is some info that might help with finding the problem:\n"
                      f"Source: {source_file}\n"
                      f"Binary: {bin_file}\n"
                      f"Queue: {queue_dir_path}\n"
                      f"Unique: {unique_dir_path}\n"
                      f"Subprocess error output:\n"
                      f"{afl_command.stdout.decode('utf-8')}",
                      file=sys.stderr)
                exit(1)

    print("Finished AFL++ for all programs")


if __name__ == '__main__':
    afl_find_inputs()
