import os
import random
import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict


class ParserState(Enum):
    START = 0
    WAITING_FOR_STRUCTS = 1
    PARSING_STRUCTS = 2
    PARSING_STRUCT = 3
    PARSING_GLOBAL_VARIABLES = 4
    WAITING_FOR_MAIN = 5
    INSERT_CODE = 6
    DONE = 7


@dataclass
class StructField:
    name: str
    type: str
    is_const: bool
    is_volatile: bool
    bits: int


@dataclass
class GlobalVariable:
    name: str
    type: str
    is_struct: bool
    is_volatile: bool
    dimensions: List[int]


def indented_line(line: str, level: int = 0) -> str:
    return f"{' '*4*(level + 1)}{line}\n"


def generate_indices(dimensions: List[int], prefix: str = "") -> List[str]:
    head = dimensions[0]
    tail = dimensions[1:]
    outlist = []

    for i in range(head):
        this_prefix = prefix + f"[{i}]"
        if len(tail) == 0:
            outlist.append(this_prefix)
        else:
            outlist.extend(generate_indices(tail, this_prefix))

    return outlist


def source_to_source_translation():
    random.seed()
    base_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(base_path, "tokenized")
    base_entry: os.DirEntry

    begin_struct_string = "/* --- Struct/Union Declarations --- */"
    begin_global_var_string = "/* --- GLOBAL VARIABLES --- */"
    end_global_var_string = "/* --- FORWARD DECLARATIONS --- */"

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for base_entry in os.scandir(os.path.join(base_path, "programs")):
        if base_entry.is_file():
            state = ParserState.START
            new_source_code = ""
            current_struct_name = ""
            structs: Dict[str, List[StructField]] = dict()
            variables: List[GlobalVariable] = []

            with open(base_entry, "r") as f:
                for line in f:
                    new_source_code += line

                    if state == ParserState.START:
                        if line.startswith("#include \"csmith.h\""):
                            new_source_code += "#include <stdlib.h>\n"
                            state = ParserState.WAITING_FOR_STRUCTS
                    elif state == ParserState.WAITING_FOR_STRUCTS:
                        if line.startswith(begin_struct_string):
                            state = ParserState.PARSING_STRUCTS
                        elif line.startswith(begin_global_var_string):
                            state = ParserState.PARSING_GLOBAL_VARIABLES
                        elif line.startswith(end_global_var_string):
                            state = ParserState.WAITING_FOR_MAIN
                    elif state == ParserState.PARSING_STRUCTS:
                        if line.startswith(begin_global_var_string):
                            state = ParserState.PARSING_GLOBAL_VARIABLES
                        elif line.startswith(end_global_var_string):
                            state = ParserState.WAITING_FOR_MAIN
                        elif m := re.match(r"^struct\s+(?P<struct_name>S[0-9]+)\s+{$", line):
                            state = ParserState.PARSING_STRUCT
                            current_struct_name = m.group("struct_name")
                            structs[current_struct_name] = []
                    elif state == ParserState.PARSING_STRUCT:
                        if line.startswith("};"):
                            state = ParserState.PARSING_STRUCTS
                        elif m := re.match(r"^\s+(?P<is_const>const)?\s*(?P<is_volatile>volatile)?\s*(?P<type>[a-z0-9_]+)\s+(?P<name>f[0-9]+)( : (?P<bits>[0-9]+))?;$", line):
                            structs[current_struct_name].append(StructField(
                                name=m.group("name"),
                                type=m.group("type"),
                                is_const=m.group("is_const") is not None,
                                is_volatile=m.group("is_volatile") is not None,
                                bits=-1 if m.group("bits") is None else m.group("bits")
                            ))
                    elif state == ParserState.PARSING_GLOBAL_VARIABLES:
                        if line.startswith(end_global_var_string):
                            state = ParserState.WAITING_FOR_MAIN
                        elif m := re.match(r"^static\s+(?P<is_volatile>volatile)?\s*(?P<type>[a-z0-9_]+)\s+(?P<name>[a-z0-9_]+)(?P<dimensions>(\[[0-9]+\])+)?\s+=", line):
                            dimensions = m.group("dimensions")

                            if dimensions is None:
                                dimensions = []
                            else:
                                dimensions = list(map(int, dimensions[1:-1].split("][")))

                            variables.append(GlobalVariable(
                                name=m.group("name"),
                                type=m.group("type"),
                                is_struct=False,
                                is_volatile=m.group("is_volatile") is not None,
                                dimensions=dimensions
                            ))
                        elif m := re.match(r"^static\s+(?P<is_volatile>volatile)?\s*struct\s+(?P<type>S[0-9]+)\s+(?P<name>[a-z0-9_]+)(?P<dimensions>(\[[0-9+]\])+)?\s+=", line):
                            dimensions = m.group("dimensions")

                            if dimensions is None:
                                dimensions = []
                            else:
                                dimensions = list(map(int, dimensions[1:-1].split("][")))

                            variables.append(GlobalVariable(
                                name=m.group("name"),
                                type=m.group("type"),
                                is_struct=True,
                                is_volatile=m.group("is_volatile") is not None,
                                dimensions=dimensions
                            ))
                    elif state == ParserState.WAITING_FOR_MAIN:
                        if line.startswith("int main (int argc, char* argv[])"):
                            state = ParserState.INSERT_CODE
                    elif state == ParserState.INSERT_CODE:
                        buff_size = 100
                        assignment_code = ""
                        assignment_idx = 0

                        for var in variables:
                            if len(var.dimensions) == 0:
                                indices = [""]
                            else:
                                indices = generate_indices(var.dimensions)

                            for idx in indices:
                                if var.is_struct:
                                    for field in structs[var.type]:
                                        if not field.is_const:
                                            assignment_code += indented_line(f"{var.name}{idx}.{field.name} = s2s_input[{assignment_idx}];")
                                            assignment_idx += 1
                                else:
                                    assignment_code += indented_line(f"{var.name}{idx} = s2s_input[{assignment_idx}];")
                                    assignment_idx += 1

                        new_source_code += indented_line(f"/* START AUTOGENERATED CODE BY S2S TRANSLATION */")
                        new_source_code += indented_line(f"int s2s_nr_inputs = {assignment_idx};")
                        new_source_code += indented_line(f"int *s2s_input = (int *) calloc(s2s_nr_inputs, sizeof(int));")
                        new_source_code += indented_line(f"FILE *s2s_file = fopen(argv[1], \"r\");")
                        new_source_code += indented_line(f"char s2s_buffer[{buff_size}];")
                        new_source_code += indented_line(f"int s2s_i = 0;")
                        new_source_code += indented_line(f"while((fgets(s2s_buffer, {buff_size} - 1, s2s_file) != NULL) && s2s_i < s2s_nr_inputs) {{")
                        new_source_code += indented_line(f"s2s_input[s2s_i] = atoi(s2s_buffer);", 1)
                        new_source_code += indented_line(f"s2s_i++;", 1)
                        new_source_code += indented_line(f"}}")
                        new_source_code += indented_line(f"fclose(s2s_file);")
                        new_source_code += assignment_code
                        new_source_code += indented_line(f"free(s2s_input);")
                        new_source_code += indented_line(f"/* END AUTOGENERATED CODE BY S2S TRANSLATION */")
                        new_source_code += indented_line("", -1)

                        state = ParserState.DONE

            if assignment_idx == 0:
                print(f"The program \"{base_entry.name}\" has no non-constant global variables! Skipping...")
                continue

            program_path = os.path.join(output_path, base_entry.name[:-2])

            if not os.path.exists(program_path):
                os.mkdir(program_path)

            program_file = os.path.join(program_path, base_entry.name)
            with open(program_file, "w+") as f:
                f.write(new_source_code)

            input_file = os.path.join(program_path, "initial_input.txt")
            with open(input_file, "w+") as f:
                for i in range(assignment_idx):
                    suffix = "" if i == assignment_idx - 1 else "\n"
                    f.write(f"{random.randrange(256)}{suffix}")


if __name__ == '__main__':
    source_to_source_translation()
