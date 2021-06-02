#include <stdio.h>

// the number after : specifies bitlength of field; bitlength cannot exceed length of type e.g. int = 32 bits max
struct S0 {
	unsigned f0: 1;
	int f1: 32;
};

struct S1 {
	int f0: 8;
	int f1: 24;
	unsigned const f2: 22;
};

struct S2 {
	int f0: 32;
	struct S0 f1;
};

// GLOBAL VARIABLES
int g0 = 345; // normal int should be replaced
const int g1 = 89; // const int should stay the same
int g2[3] = {0, 1, 2}; //int array
struct S0 g3 = {1, 2}; // struct
struct S1 g4[2][2] = {{{1,2,3},{1,2,3}}, {{1,2,3},{1,2,3}}};	     // struct array
struct S2 g5 = {3, {0, 2}}; 
struct S1 g6 = {4,5,6};



int main(int argc, char *argv){
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
