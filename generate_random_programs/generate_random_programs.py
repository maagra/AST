import os
import subprocess
import sys


def generate_random_programs(program_count: int = 5):
    base_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(base_path, "random_programs")

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for i in range(program_count):
        output_file = os.path.join(output_path, f"random_program_{i}.c")

        random_command = subprocess.run(["csmith", "-o", output_file], capture_output=True)

        if random_command.returncode != 0:
            print(f"Could not generate random C file!\n"
                  f"This is major error, the script is terminated.\n"
                  f"Here is some info that might help with finding the problem:\n"
                  f"Subprocess error output:\n"
                  f"{random_command.stderr.decode('utf-8')}",
                  file=sys.stderr)
            exit(1)

        print(f"Generating {i+1} / {program_count} random programs")

    print(f"All {program_count} random programs have been generated")


if __name__ == '__main__':
    generate_random_programs()
