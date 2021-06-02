#include <stdio.h>
#include <stdlib.h>

#define BUFSIZE 20


// the number after : specifies bitlength of field; bitlength cannot exceed length of type e.g. int = 32 bits max
struct S0 {
	unsigned f0: 1;
	int f1: 32;
};

struct S1 {
	int f0: 8;
	volatile int f1: 24;
	unsigned const f2: 22;
};

struct S2 {
	int f0: 32;
	struct S0 f1;
};

// GLOBAL VARIABLES
// we initialize all the values to the values specified in the original random c program because we want to keep the constant values
// in the main function we then give all the non-constant values the input from a textfile
int g0 = 345; // normal int should be replaced
const int g1 = 89; // const int should stay the same
int g2[3] = {0, 1, 2}; //int array
struct S0 g3 = {1, 2}; // struct
struct S1 g4[2][2] = {{{1,2,3},{1,2,3}}, {{1,2,3},{1,2,3}}};	     // struct array
struct S2 g5 = {3, {0, 2}}; 
struct S1 g6 = {4,5,6};


int main(int argc, char *argv[]){
    	int nr_inputs = 19;
	int *input = (int *) calloc(nr_inputs, sizeof(int));

	//printf("file name: %s\n", argv[1]);
	FILE *f = fopen(argv[1], "r");

	char buff[200]; /* a buffer to hold what you read in */

	int i = 0;
	while((fgets(buff, BUFSIZE - 1, f) != NULL) && i < nr_inputs) {
		input[i] = atoi(buff);
		i++;
	}

	fclose(f); /* close the file */ 
	
	//adjust global variables 
	// g0
	g0 = input[0];
	
	// g1 is const and therefore not initialized
	
	// g2
	g2[0] = input[1];
	g2[1] = input[2];
	g2[2] = input[3];
	
	// g3
	g3.f0 = input[4];
	g3.f1 = input[5];
	
	// g4
	g4[0][0].f0 = input[6];
	g4[0][0].f1 = input[7];
	//g4[0][0].f2 = input[8]; //const; we shouldn't change it
	g4[0][1].f0 = input[8];
	g4[0][1].f1 = input[9];
	//g4[0][1].f2 = input[11];
	g4[1][0].f0 = input[10];
	g4[1][0].f1 = input[11];
	//g4[1][0].f2 = input[14];
	g4[1][1].f0 = input[12];
	g4[1][1].f1 = input[13];
	//g4[1][1].f2 = input[17];
	
	// g5
	g5.f0 = input[14];
	g5.f1.f0 = input[15];
	g5.f1.f1 = input[16];
	
	//g6
	g6.f0 = input[17];
	g6.f1 = input[18];
	//g6.f2 = input[23];
	
	free(input);

	if (g2[1] + g3.f0 < 45){
		printf("g2[1] + g3.f0 < 45)\n");
	} else if (g5.f1.f1 == g3.f1){
		printf("g5.f1.f1 == g3.f1\n");
	}
	
	if (g4[0][0].f1 == g6.f1){
		printf("g4[0][0].f1 == g6.f1\n");
	} else {
		if (g0 - 1 == 22){
			printf("(g4[0][0].f1 != g6.f1) && (g0 - 1 == 22)\n");
		} else {
			printf("(g4[0][0].f1 != g6.f1) && (g0 - 1 != 22)\n");
		}
	}
	
	return 0;
	
}
