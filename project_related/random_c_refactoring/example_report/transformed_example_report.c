#include <stdio.h>
#include <stdlib.h>

#define BUFSIZE 100


struct S0 {
	unsigned f0: 1;
	int f1: 32;
};

struct S1 {
	int f0: 8;
	volatile int f1: 24;
	unsigned const f2: 22;
};

union U0 {
	int f0;
	unsigned f1;
};

union U1 {
	unsigned f0;
	const int f1;
};

// GLOBAL VARIABLES
int g0 = 345; 
const int g1 = 89; 
int g2[3] = {0, 1, 2}; 
struct S0 g3 = {1, 2}; 
struct S1 g4[2][2] = {{{1,2,3},{1,2,3}}, {{1,2,3},{1,2,3}}};	    
union U0 g5 = {22}; 
struct S1 g6 = {4, 5, 46};
union U1 g7[3] = {22, 23, 24};


int main(int argc, char *argv[]){
	// loading values from input file
	int nr_inputs = 17;
	int *input = (int *) calloc(nr_inputs, sizeof(int));

	FILE *f = fopen(argv[1], "r");

	char buff[BUFSIZE]; 

	int i = 0;
	while((fgets(buff, BUFSIZE - 1, f) != NULL) && i < nr_inputs) {
		input[i] = atoi(buff);
		i++;
	}

	fclose(f); 
	
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
	// no new value for f2 field of struct (const)
	g4[0][0].f0 = input[6];
	g4[0][0].f1 = input[7];
	
	g4[0][1].f0 = input[8];
	g4[0][1].f1 = input[9];
	
	g4[1][0].f0 = input[10];
	g4[1][0].f1 = input[11];
	
	g4[1][1].f0 = input[12];
	g4[1][1].f1 = input[13];
	
	
	// g5
	g5.f0 = input[14]; //which field we assign to doesn't matter
	
	//g6
	// no new value for f2 field of struct (const)
	g6.f0 = input[15];
	g6.f1 = input[16];
	
	//g7 is union and has const value 
	
	free(input);


	if (g2[1] + g3.f0 < 45){
		printf("g2[1] + g3.f0 < 45)\n");
	} else if (g5.f1 == g3.f1){
		printf("g5.f1 == g3.f1\n");
	}
	
	if (g4[0][0].f1 == g6.f1){
		printf("g4[0][0].f1 == g6.f1\n");
	} else {
		if (g0 - 1 == 22){
			printf("(g4[0][0].f1 != g6.f1)"
			       "&& (g0 - 1 == 22)\n");
		} else {
			printf("(g4[0][0].f1 != g6.f1)"
			       "&& (g0 - 1 != 22)\n");
		}
	}
	
	if (g1 == g7[2].f0){
		printf("g1 == g7[2].f0\n");
	} else {
		printf("g1 != g7[2].f0\n");
	}
	
	return 0;
}
	

