#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_EQ_LENGTH 100
#define MAX_STR_LENGTH 50
#define LEN_CONS 2
#define LEN_VAR 2
#define LEN_DERIV 6
#define LEN_OP 5

typedef struct enode{
	char* type;
	struct enode** child;
	int num_child;
}enode;

// Useful functions
void print_spaces(int depth);
char* extract_string(char* str,int init,int final);
char* remove_spaces(char* s);
char* replace_char(char* s, char c1, char c2);
int is_number(char c);
int is_letter(char c);
int len_str(char* s);
int cmp_str(char* str1, char* str2);
int is_constant(char* s);
int is_variable(char c);
int char2number(char c);
int is_operation(char c);
int is_term(char c);
char** split_string(char* s, char delim);
void set_variable(int idx, double value);
void set_derivative(int idx, double value);
double get_variable(int idx);
double get_derivative(int idx);
int get_eq_degree();

// Nodes functions
enode* create_enode(char* type);
void add_child(enode* root, enode* child);
enode* pop_child(enode* root);
void print_tree(enode* root, int depth);

void init_parsing(char* eq);
void print_error(char* s,int i);

// Parsing functions
enode* parse_constant();
enode* parse_variable();
enode* parse_number();
enode* parse_function();
enode* parse_derivative();
enode* parse_term();
enode* parse_expression(); 

void print_eval_error(char* s);

// Evaluate functions
double eval_constant(enode* node);
double eval_variable(enode* node);
double eval_number(enode* node);
double eval_function(enode* node);
double eval_derivative(enode* node);
double eval_term(enode* node);
double eval_operation(enode* node);
double eval_expression(enode* node);
double eval_enode(enode* node);