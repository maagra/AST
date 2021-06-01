#include <stdio.h>
#include <stdlib.h>

#define BUFSIZE 20

int main(int argc, char *argv[]){
	int *input = (int *) malloc(6*sizeof(int));

	//printf("file name: %s\n", argv[1]);
	FILE *f = fopen(argv[1], "r");
		
	char buff[20]; /* a buffer to hold what you read in */

	int i = 0;
	while(fgets(buff, BUFSIZE - 1, f) != NULL) {
		//printf ("%s\n", buff); 
		input[i] = atoi(buff);
		//printf("input[%d]: %d\n", i, input[i]);
		i++;
	}
	fclose(f); /* close the file */ 

	int a = input[0];
	printf("a: %d\n", a);
	int b = input[1];
	printf("b: %d\n", b);
	int c = input[2];
	printf("c: %d\n", c);
	if (a+b < input[3]){
		c = input[4]*b;
	} else if (a == input[5]){
		c = a;
	}
	printf("This is our c: %d\n", c);

}


