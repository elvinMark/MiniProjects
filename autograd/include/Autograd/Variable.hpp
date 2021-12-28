#ifndef VARIABLE
#define VARIABLE

#include <Autograd/Node.hpp>

class Variable {
public:
  double data;
  double grad;
  Node *node;

public:
  Variable(Node *node);
  Variable(double data);
  void set_data(double data);
  void set_grad(double grad);
  void acc_grad(double grad);
  void zero_grad();
  double eval();
  void backward(double e);
};

#endif
