#include <eML/utils.hpp>
#include <eML/constants.hpp>

double* create_arr(double value, int size){
  double* out =  (double*) malloc(sizeof(double) * size);
  for(int i = 0; i < size; i++)
    out[i] = value;
  return out;
}

void* create_empty_arr(int tot_size){
  return (void*) malloc(tot_size);
}

int* args2arr(int start, va_list l, int *dim){
  int *out = (int *) malloc(sizeof(int));
  *dim = 0;
  for(int i = start; i >= ALL; i = va_arg(l, int)){
    out[*dim] = i;
    *dim += 1;
    out = (int *) realloc(out,sizeof(int)*(*dim + 1));
  }
  return out;
}

double random_number(){
  srand(time(NULL));
  return rand()%1000 / 1000.0; 
}

void print_list(int size, int* l){
  for(int i = 0;i < size; i++)
    printf("(")
    printf("%d, ",l[i]);
  printf(")\n");
}
