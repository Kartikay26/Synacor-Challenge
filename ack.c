/* ACK!! */

#include <stdio.h>
#include <stdlib.h>

#define M 32768

int ack41(int z);

int main(){
	printf("true ack(4,1) = %d\n",ack41(1));
	for(int z=0; z<M; z++){
		printf("for z=%d, ack(4,1) = %d\n",z,ack41(z));
	}
}

int ack41(int z){
	int* Amn  = malloc(M*sizeof(int));
	int* Amn1 = malloc(M*sizeof(int));
	for(int n=0; n<M; n++){
		Amn[n] = (n+1)%M;
	}
	for(int m=0; m<4; m++){
		int* oldlist = Amn;
		int* newlist = Amn1;
		newlist[0] = oldlist[z];
		// generate m'th line of ack table
		for(int n=1; n<M; n++){
			newlist[n] = oldlist[newlist[n-1]];
		}
		// next rows
		free(Amn);
		Amn = Amn1;
		Amn1 = malloc(M*sizeof(int));
	}
	int r = Amn[1];
	free(Amn1);
	free(Amn);
	return r;
}
