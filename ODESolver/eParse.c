#include "eParse.h"

char *eq_buffer;
int len_buffer;
int curr_index;
int eq_degree;

char* CONS[LEN_CONS] = {"e\0","pi\0"};
char* VAR[LEN_VAR] = {"u0\0","t\0"};
char* DERIV[LEN_DERIV] = {"u0\0","u1\0","u2\0","u3\0","u4\0","u5\0"};
char* OP[LEN_OP] = {"+\0","-\0","*\0","/\0","^\0"};

double cons_def[2] = {M_E,M_PI};
double var_def[2] = {0.0,0.0};
double deriv_def[6] = {0.0,0.0,0.0,0.0,0.0,0.0};

void print_spaces(int depth){
	int i;
	for(i = 0 ;i < depth;i++)
		printf(" ");
}

char* extract_string(char* str,int init,int final){
	char* tmp;
	int idx;
	tmp = (char*)malloc(sizeof(char)*MAX_STR_LENGTH);
	for(idx=0;idx<(final - init);idx++)
		tmp[idx] = str[init + idx];
	tmp[idx] = '\0';
	return tmp;
}

char* remove_spaces(char* s){
	char* tmp = (char*) malloc(sizeof(char)*MAX_EQ_LENGTH);
	int idx = 0;
	while(*s != '\0' && *s!='\n'){
		if(*s != ' '){
			tmp[idx] = *s;
			idx++;
		}
		s++;
	}
	tmp[idx] = '\0';
	return tmp;
}

char* replace_char(char* s, char c1, char c2){
	char* tmp = (char*) malloc(sizeof(char)*MAX_EQ_LENGTH);
	int idx=0;
	while(*s != '\0' && *s!='\n'){
		if(*s == c1)
			tmp[idx] = c2;
		else
			tmp[idx] = *s;
		s++;\
		idx++;
	}
	tmp[idx] = '\0';
	return tmp;
}

int is_number(char c){
	return c >= '0' && c <= '9' || c=='.';
}

int is_letter(char c){
	return c >= 'a' && c <= 'z';
}

int len_str(char* s){
	int i=0;
	while(s[i]!='\0' && s[i]!='\n')
		i++;
	return i;
}

int cmp_str(char* str1, char* str2){
	while(*str1 != '\0' && *str2 != '\0'){
		if(*str1 != *str2)
			return 0;
		str1++;
		str2++;
	}
	if(*str1 == '\0' && *str2 == '\0')
		return 1;
	return 0;
}

int is_constant(char* s){
	int i;
	for(i=0;i<LEN_CONS;i++){
		if(cmp_str(s,CONS[i]))
			return 1;
	}
	return 0;
}

int is_variable(char c){
	if(c =='x')
		return 1;
	else if(c == 't')
		return 2;
	return 0;
}

int char2number(char c){
	return c - '0';
}

int is_operation(char c){
	switch(c){
		case '+':
			return 1;
		case '-':
			return 2;
		case '*':
			return 3;
		case '/':
			return 4;
		case '^':
			return 5;	
	}
	return 0;
}

int is_term(char c){
	return c=='d' || c=='f' || c=='c' || is_number(c) || c=='(' || is_variable(c);
}

char** split_string(char* s, char delim){
	int i=0, n=0, prev=0;
	char** out = (char**) malloc(sizeof(char*));
	while(s[i]!='\0' && s[i]!='\n'){
		if(s[i] == delim){
			out[n] = extract_string(s,prev,i);
			n++;
			out = (char**) realloc(out,sizeof(char*)*n);
			prev = i+1;
		}
		i++;
	}
	out[n] = extract_string(s,prev,i);
	return out;
}

void set_variable(int idx, double value){
	var_def[idx] = value;
}

void set_derivative(int idx, double value){
	deriv_def[idx] = value;
}

double get_variable(int idx){
	return var_def[idx];
}

double get_derivative(int idx){
	return deriv_def[idx];
}

int get_eq_degree(){
	return eq_degree;
}

enode* create_enode(char* type){
	enode *tmp;
	tmp = (enode*) malloc(sizeof(enode));
	tmp->type = type;
	tmp->child = NULL;
	tmp->num_child = 0;
	return tmp;
}

void add_child(enode* root, enode* child){
	if(root->child == NULL)
		root->child = (enode**) malloc(sizeof(enode*));
	root->child = (enode**)realloc(root->child,sizeof(enode*)*(root->num_child+1));
	root->child[root->num_child] = child;
	root->num_child += 1;
}
enode* pop_child(enode* root){
	root->num_child--;
	return root->child[root->num_child];
}

void print_tree(enode* root, int depth){
	int i;
	print_spaces(depth);
	printf("%s\n",root->type);
	for(i=0;i<root->num_child;i++)
		print_tree(root->child[i],depth+1);
}	

void init_parsing(char* eq){
	int i;
	eq_buffer = remove_spaces(eq);
	curr_index = 0;
	len_buffer = len_str(eq_buffer);
	eq_degree = 0;
}

void print_error(char* s,int i){
	printf("Parsing Error when parsing %s\n at index %d\n",s,i);
	exit(0);
}

enode* parse_constant(){ // const_(name)
	char *tmp;
	int idx;
	enode* out = create_enode("constant");
	enode* aux;
	curr_index += 6;
	idx = curr_index;
	while(is_letter(eq_buffer[curr_index])){
		curr_index++;
		if(curr_index==len_buffer)
			break;
	}
	tmp = extract_string(eq_buffer,idx,curr_index);
	if(is_constant(tmp)){
		aux = create_enode(tmp);
		add_child(out,aux);
	}
	else
		print_error("constant",curr_index);
	return out;
}

enode* parse_variable(){ // x or t
	int tmp = is_variable(eq_buffer[curr_index]);
	enode* out = create_enode("variable");
	enode* aux;
	curr_index++;
	if(tmp){
		aux = create_enode(VAR[tmp-1]);
		add_child(out,aux);
	}
	else
		print_error("variable",curr_index);
	return out;
}

enode* parse_number(){
	enode* out = create_enode("number");
	enode* aux;
	char* tmp;
	int idx;
	idx = curr_index;
	while(is_number(eq_buffer[curr_index])){
		curr_index++;
		if(curr_index == len_buffer)
			break;
	}
	tmp = extract_string(eq_buffer,idx,curr_index);
	aux = create_enode(tmp);
	add_child(out,aux);
	return out;
}

enode* parse_function(){ // func_(name)
	enode* out = create_enode("function");
	enode* aux;
	enode* aux1;
	char* tmp;
	int idx;
	curr_index += 5;
	idx = curr_index;
	while(is_letter(eq_buffer[curr_index])){
		curr_index++;
		if(curr_index == len_buffer)
			break;
	}
	tmp = extract_string(eq_buffer,idx,curr_index);
	aux = create_enode(tmp);
	if(eq_buffer[curr_index]!='(')
		print_error("function",curr_index);
	curr_index++;
	aux1 = parse_expression();
	if(eq_buffer[curr_index]!=')')
		print_error("function",curr_index);
	curr_index++;
	add_child(aux,aux1);
	add_child(out,aux);
	return out;
}

enode* parse_derivative(){ // dkx/dtk | dx/dt
	enode* out = create_enode("derivative");
	enode* aux;
	int degree;
	curr_index++;
	if(is_number(eq_buffer[curr_index])){
		degree = char2number(eq_buffer[curr_index]);
		curr_index += 6;
	}
	else{
		degree = 1;
		curr_index += 4;
	}
	if(degree>eq_degree)
		eq_degree = degree;
	aux = create_enode(DERIV[degree]);
	add_child(out,aux);
	return out;
}

enode* parse_term(){
	enode* out = create_enode("term");
	enode* aux;
	enode* tmp;
	enode* aux1;
	while(eq_buffer[curr_index] != '+' && eq_buffer[curr_index] != '-' && eq_buffer[curr_index] != ')'){
		if(is_number(eq_buffer[curr_index])){
			aux = parse_number();
			add_child(out,aux);
		}
		else if(eq_buffer[curr_index] == 'c'){
			aux = parse_constant();
			add_child(out,aux);
		}
		else if(is_variable(eq_buffer[curr_index])){
			aux = parse_variable();
			add_child(out,aux);
		}
		else if(eq_buffer[curr_index] == 'f'){
			aux = parse_function();
			add_child(out,aux);
		}
		else if(eq_buffer[curr_index] == 'd'){
			aux = parse_derivative();
			add_child(out,aux);
		}
		else if(eq_buffer[curr_index] == '('){
			curr_index++;
			aux = parse_expression();
			add_child(out,aux);
			if(eq_buffer[curr_index] != ')')
				print_error("term",curr_index);
			curr_index++;
		}
		else if(is_operation(eq_buffer[curr_index]) > 2){
			int opt = is_operation(eq_buffer[curr_index]);
			aux = create_enode("operation");
			tmp = create_enode(OP[opt-1]);
			if(out->num_child > 0)
				add_child(tmp,pop_child(out));
			else
				print_error("operation",curr_index);
			curr_index++;
			aux1 = parse_term();
			add_child(tmp,aux1);
			add_child(aux,tmp);
			add_child(out,aux);
		}
		if(curr_index == len_buffer)
			break;
	}
	return out;
}

enode* parse_expression(){
	enode* out = create_enode("expression");
	enode* tmp;
	enode* aux;
	enode* aux1;
	enode* aux2;
	while(curr_index < len_buffer){
		if(is_operation(eq_buffer[curr_index])){
			tmp = create_enode("operation");
			aux = create_enode(OP[is_operation(eq_buffer[curr_index]) - 1]);
			if(out->num_child == 0){
				if(eq_buffer[curr_index] == '-'){
					aux2 = create_enode("term");
					aux1 = create_enode("number");
					add_child(aux1,create_enode("0"));
					add_child(aux2,aux1);
					add_child(out,aux2);
				}
				else
					print_error("expression",curr_index);
			}
			curr_index++;
			add_child(aux,pop_child(out));
			aux1 = parse_term();
			add_child(aux,aux1);
			add_child(tmp,aux);
			add_child(out,tmp);
		}
		else if(is_term(eq_buffer[curr_index])){
			tmp = parse_term();
			add_child(out,tmp);
		}
		else
			break;
	}
	return out;
}

void print_eval_error(char* s){
	printf("Error evaluating %s\n",s);
	exit(0);
}

double eval_constant(enode* node){
	if(cmp_str(node->type,"e\0"))
		return cons_def[0];
	else if(cmp_str(node->type,"pi\0"))
		return cons_def[1];
	else
		print_eval_error("constant");
	return 0;
}

double eval_variable(enode* node){
	if(cmp_str(node->type,"u0\0"))
		return var_def[0];
	else if(cmp_str(node->type,"t\0"))
		return var_def[1];
	else
		print_eval_error("variable");
	return 0;
}

double eval_number(enode* node){
	return atof(node->type);
}

double eval_function(enode* node){
	char* fun = node->type;
	enode* tmp = node->child[0];
	double s = eval_enode(tmp);
	if(cmp_str(fun,"sin"))
		return sin(s);
	else if(cmp_str(fun,"cos"))
		return cos(s);
	else if(cmp_str(fun,"tan"))
		return tan(s);
	else if(cmp_str(fun,"csc"))
		return 1/sin(s);
	else if(cmp_str(fun,"sec"))
		return 1/cos(s);
	else if(cmp_str(fun,"cot"))
		return 1/tan(s);
	else if(cmp_str(fun,"asin"))
		return asin(s);
	else if(cmp_str(fun,"acos"))
		return acos(s);
	else if(cmp_str(fun,"atan"))
		return atan(s);
	else if(cmp_str(fun,"log"))
		return log(s);
	else if(cmp_str(fun,"exp"))
		return exp(s);
	else
		print_eval_error("function");
	return 0;
}

double eval_derivative(enode* node){
	int k = char2number(node->type[1]);
	return deriv_def[k];
}

double eval_term(enode* node){
	return eval_enode(node);
}

double eval_operation(enode* node){
	char* tmp = node->type;
	double s1,s2;
	s1 = eval_enode(node->child[0]);
	s2 = eval_enode(node->child[1]);
	if(cmp_str(tmp,"+\0"))
		return s1+s2;
	else if(cmp_str(tmp,"-\0"))
		return s1-s2;
	else if(cmp_str(tmp,"*\0"))
		return s1*s2;
	else if(cmp_str(tmp,"/\0"))
		return s1/s2;
	else if(cmp_str(tmp,"^\0"))
		return pow(s1,s2);
	return 0;
}

double eval_expression(enode* node){
	return eval_enode(node);
}	

double eval_enode(enode* node){
	if(cmp_str(node->type,"variable"))
		return eval_variable(node->child[0]);
	else if(cmp_str(node->type,"constant"))
		return eval_constant(node->child[0]);
	else if(cmp_str(node->type,"number"))
		return eval_number(node->child[0]);
	else if(cmp_str(node->type,"derivative"))
		return eval_derivative(node->child[0]);
	else if(cmp_str(node->type,"function"))
		return eval_function(node->child[0]);
	else if(cmp_str(node->type,"operation"))
		return eval_operation(node->child[0]);
	else if(cmp_str(node->type,"expression"))
		return eval_expression(node->child[0]);
	else if(cmp_str(node->type,"term"))
		return eval_term(node->child[0]);
}