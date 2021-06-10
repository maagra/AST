# AFL-driven value mutation testing for compilers
This is a project for the "Automated Software Testing" SS21 course at ETH Zurich by Sven Grübel and Rahel Maag.

By executing `python3 test_script.py` the following steps will be done automatically:

 - Generating random programs with Csmith
 - Refactoring Csmith random programs to make them input dependent (an example of a simplified Csmith program can be found under `project_related/s2s_example_presentation`)
 - Using AFL++ to generate new inputs for all newly accessible paths
 - Differential Testing with multiple compilers/compiler options

If you want to try out our script then you need to have the following programs already installed:

 - [AFL++](https://github.com/AFLplusplus/AFLplusplus)
 - [Csmith](https://github.com/csmith-project/csmith)

 Furthermore, `CSMITH_INCLUDE_DIRECTORY` variable needs to be changed in `test_script.py` to where your Csmith header file is located. In this file `RANDOM_PROGRAM_COUNT` and `AFL_FUZZING_DURATION` can also be adjusted. Our default values are 5 and 900 (time in seconds) respectively. Depending on the random program 900 seconds might not be enough to find all paths.

For differential testing we are using the following compilers with the following flags:

 - gcc with -O0, -O1, -O2, -O3, -Os, -Ofast, -Og
 - clang with -O0, -O1, -O2, -O3, -Os, -Ofast, -Oz

To add more compilers/flags a new dictionary entry must be added to `compiler_options` in `differential_testing/diff_testing.py`.
