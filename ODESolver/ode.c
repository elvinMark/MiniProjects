#include "eOde.h"

int main(int argc, char **args){
	double** out = ode_solver(args[1],args[2],args[3]);
	return 0;
}