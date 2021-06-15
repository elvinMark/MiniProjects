#ifndef UTILS
#define UTILS

#include <stdarg.h>
#include <stdlib.h>
#include <time.h>

double* create_arr(double value, int size);
double random_number();
void* create_empty_arr(int tot_size);
int* args2arr(int start, va_list l,int* dim);

void print_list(int size, int* l);

#endif
