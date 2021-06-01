# Finding inputs with AFL++

The Python script `afl_find_inputs.py` can be used to find inputs for programs that reach new branches.

To add a new program, follow these steps:

1. Create a new directory inside the `programs` directory with the same name as
   the C source file (without trailing `.c`). For example, when adding the source
   file `my_new_test.c`, name the directory `my_new_test`.
2. Put the C source file into the newly created directory.
3. Put the initial input also into the newly created subdirectory and name it `initial_input.txt`

Now, the script should automatically pick up the new program and find inputs that reach new branches by using AFL++. The fuzzing duration can be set by editing the `AFL_FUZZING_TIMEOUT` variable in the script.

The newly found inputs will be put into new subdirectories called `unique` inside each program directory. There are also directories called `bin`, `inputs`, and `outputs`. These directories are used by the script and by AFL++.
