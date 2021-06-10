#include <stdio.h>



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
	

