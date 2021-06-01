# Differential Testing

The Python script `diff_testing.py` can be used for differential testing of programs with different inputs.

To add a new program, follow these steps:

1. Create a new directory inside the `programs` directory with the same name as
   the C source file (without trailing `.c`). For example, when adding the source
   file `my_new_test.c`, name the directory `my_new_test`.
2. Put the C source file into the newly created directory.
3. Create a new directory called `inputs` inside the newly created directory.
4. Put all input files into the `inputs` directory.

Now, the script should automatically pick up the new program and test it with differential testing.

## Supported Compilers

Currently, the following compilers and optimization levels are supported:

- gcc with -O0, -O1, -O2, -O3, -Os, -Ofast, and -Og
- clang with -O0, -O1, -O2, -O3, -Os, -Ofast, and -Oz
