#include <stdio.h>

typedef __uint16_t number;

int main(int argc, char const *argv[]) {
  if (argc != 3) {
    printf("convert -- convert binary file to stream of 16-bit numbers\n");
    printf("USAGE: convert <binaryfile> <outfile>\n");
    return 1;
  }
  FILE* in_file = fopen(argv[1],"rb");
  FILE* out_file = fopen(argv[2],"w");
  number t;
  int x,n=0;
  do{
    x = fread(&t,sizeof(t),1,in_file);
    if(x==1){
      fprintf(out_file, "%u\n", t);
      n++;
    }
    else{
      printf("Read %d 16-bit numbers.\n", n);
      break;
    }
  } while(1);
  return 0;
}
