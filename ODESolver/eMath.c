#include "eMath.h"

double** create_matrix(int rows, int cols){
	double **out;
	int i;
	out = (double **) malloc(sizeof(double*)*rows);
	for(i = 0;i<rows;i++)
		out[i] = (double*) malloc(sizeof(double)*cols);
	return out;
}

void print_matrix(double** M, int rows, int cols){
	int i,j;
	for(i=0;i<rows;i++){
		for(j=0;j<cols;j++)
			printf("%lf ",M[i][j]);
		printf("\n");
	}
}

double* create_vector(int length){
	double* out = (double*) malloc(sizeof(double)*length);
	return out;
}

void print_vector(double* v, int length){
	int i;
	for(i = 0;i<length;i++)
		printf("%lf ",v[i]);
	printf("\n");
}

void setElements(double* v, double *v1, int length){
	int i;
	for(i=0;i<length;i++)
		v[i] = v1[i];
}

void zero_vector(double* v1, int length){
	int i;
	for(i = 0;i<length;i++)
		v1[i] = 0;
}

void add_vector(double *v1, double *v2, int length){
	int i;
	for(i = 0;i<length;i++)
		v1[i] += v2[i];
}

void times_vector(double* v1, double num, int length){
	int i;
	for(i = 0;i<length;i++)
		v1[i] *= num;
}

double newton_method(double funf(double), double dfunf(double), double x0, int maxIt, double prec){
	int i;
	double x;
	for(i = 0;i<maxIt;i++){
		x = x0 - funf(x0)/dfunf(x0);
		if(x0!=0)
			if(fabs((x-x0)/x0)<prec)
				break;
		x0 = x;
	}
	return x;
}

double** runge_kutta(double* funf(double*,double,int),double* initial, double* tdom, int N, int dim){
	int i;
	double **out, th, *aux1, *k1, *k2 , *k3 ,*k4;
	out = create_matrix(N,dim+1);
	aux1 = create_vector(dim);
	th = (tdom[1] - tdom[0])/(N-1.0);
	out[0][0] = tdom[0];
	setElements(out[0]+1,initial,dim);

	for(i=1;i<N;i++){
		out[i][0] = out[i-1][0] + th;
		k1 = funf(out[i-1]+1,out[i-1][0],dim);
		zero_vector(aux1,dim);
		add_vector(aux1, k1,dim);
		times_vector(aux1,0.5*th,dim);
		add_vector(aux1,out[i-1]+1,dim);
		k2 = funf(aux1,out[i-1][0] + 0.5*th,dim);
		zero_vector(aux1,dim);
		add_vector(aux1, k2,dim);
		times_vector(aux1,0.5*th,dim);
		add_vector(aux1,out[i-1]+1,dim);
		k3 = funf(aux1,out[i-1][0] + 0.5*th,dim);
		zero_vector(aux1,dim);
		add_vector(aux1, k2,dim);
		times_vector(aux1,th,dim);
		add_vector(aux1,out[i-1]+1,dim);
		k4 = funf(aux1,out[i-1][0] + th,dim);
		times_vector(k1,th/6.0,dim);
		times_vector(k2,th/3.0,dim);
		times_vector(k3,th/3.0,dim);
		times_vector(k4,th/6.0,dim);
		add_vector(k1,k2,dim);
		add_vector(k1,k3,dim);
		add_vector(k1,k4,dim);
		add_vector(k1,out[i-1]+1,dim);
		setElements(out[i]+1,k1,dim);
	}
	return out;
}
