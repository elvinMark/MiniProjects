#include <iostream>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <stdarg.h>
#include <string>

#ifndef E_ARRAY
#define E_ARRAY

using namespace std;

class eArray{
private:
  double* data;
  int size;
  int dim;
  int* shape;
  int* stride;
  int offset;
  int* acc_shape;
  
public:
  eArray(int x, ...);
  eArray(double* data, int size, int dim, int* shape,int* stride, int offset, int* acc_shape);
  void zeros();
  void ones();
  void random();

  int get_index(int idx);
  void get_index(int *idx, int* pos);
  void get_index(int* new_size, int* new_dim, int **new_shape, int ** new_stride, int* new_offset, int** new_acc_shape, int *pos);
  
  void at(double *val, int x, ...);
  void at(eArray** t, int x, ...);
  void set(double* val, int x, ...);
  void set(eArray* t, int x, ...);
  
  string to_string();  
};

#endif
