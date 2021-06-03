#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double** create_matrix(int rows, int cols);
void print_matrix(double** M, int rows, int cols);
double* create_vector(int length);
void print_vector(double* v, int length);
void setElements(double* v, double *v1, int length);
void zero_vector(double* v1, int length);
void add_vector(double *v1, double *v2, int length);
void times_vector(double* v1, double num, int length);

double newton_method(double funf(double), double dfunf(double), double x0, int maxIt, double prec);
double** runge_kutta(double* funf(double*,double,int),double* initial, double* tdom, int N, int dim);

