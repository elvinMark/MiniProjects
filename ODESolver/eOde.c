#include "eOde.h"

int steps = 50;
double prec = 0.0001;
double h = 0.01;
int max_it = 20;

double** ode_solver(char* streq, char* initial, char* tdom){
	int i;

	char** tmp = split_string(streq,'=');
	char *left_side, *right_side;
	int left_degree, right_degree, degree;
	enode *left_eq,*right_eq, *eq,*aux,*aux1;

	char **initial_str, **tdom_str;
	double* initial_cond, *t_domain;
	double **out;
	
	left_side = remove_spaces(tmp[0]);
	right_side = remove_spaces(tmp[1]);
	
	init_parsing(left_side);
	left_eq = parse_expression();
	left_degree =get_eq_degree();
	
	init_parsing(right_side);
	right_eq = parse_expression();
	right_degree = get_eq_degree();
	
	eq = create_enode("expression");
	aux = create_enode("operation");
	aux1 = create_enode("-");
	add_child(aux1,left_eq);
	add_child(aux1,right_eq);
	add_child(aux,aux1);
	add_child(eq,aux);

	degree = left_degree>right_degree?left_degree:right_degree;

	initial_str = split_string(initial,',');
	tdom_str = split_string(tdom,',');

	initial_cond = create_vector(degree);
	t_domain = create_vector(2);

	for(i=0;i<degree;i++)
		initial_cond[i] = atof(initial_str[i]);
	
	t_domain[0] = atof(tdom_str[0]);
	t_domain[1] = atof(tdom_str[1]);
	
	double* funf(double *u, double t, int dim){
		int i;
		double *out = create_vector(dim);
		double tmp;
		set_variable(0,u[0]);
		set_variable(1,t);
		for(i=1;i<dim;i++){
			out[i-1] = u[i];
			set_derivative(i,u[i]);
		}
		double fun_f(double y){
			set_derivative(dim,y);
			return eval_enode(eq);
		}
		double dfun_f(double y){
			return (fun_f(y+h) - fun_f(y))/h;
		}
		tmp = newton_method(fun_f,dfun_f,u[0],max_it,prec);
		out[dim-1] = tmp;
		return out;
	}

	out = runge_kutta(funf,initial_cond,t_domain,steps,degree);
	print_matrix(out,steps,degree+1);
	return out;
}