#include <Autograd/Variable.hpp>

using namespace std;

Variable::Variable(double data) {
  this->data = data;
  this->grad = 0;
  this->node = new Node(this);
}

Variable::Variable(Node *node) {
  this->data = 0;
  this->grad = 0;
  this->node = node;
}

void Variable::set_data(double data) {
  this->data = data;
  this->grad = 0;
}

void Variable::set_grad(double grad) { this->grad = grad; }

void Variable::acc_grad(double grad) { this->grad += grad; }

void Variable::zero_grad() { this->grad = 0; }

double Variable::eval() {
  if (this->node->is_leaf())
    return this->data;

  double left, right, result;
  left = ((Variable *)this->node->left->var)->eval();
  right = ((Variable *)this->node->right->var)->eval();

  switch (this->node->op_type) {
  case OP_ADD:
    result = left + right;
    break;
  case OP_SUB:
    result = left - right;
    break;
  case OP_MUL:
    result = left * right;
    break;
  case OP_DIV:
    result = left / right;
    break;
  default:
    return 0.0;
  }
  this->set_data(result);
  return result;
}

void Variable::backward(double e) {
  if (this->node->is_leaf()) {
    this->acc_grad(e);
    return;
  }
  Variable *left = (Variable *)this->node->left->var;
  Variable *right = (Variable *)this->node->right->var;

  switch (this->node->op_type) {
  case OP_ADD:
    left->backward(e);
    right->backward(e);
    break;
  case OP_SUB:
    left->backward(e);
    right->backward(-e);
    break;
  case OP_MUL:
    left->backward(e * right->data);
    right->backward(e * left->data);
    break;
  case OP_DIV:
    left->backward(e / right->data);
    right->backward(-e * left->data / (right->data * right->data));
    break;
  default:
    break;
  }
}
