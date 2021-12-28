#include <Autograd/Session.hpp>

using namespace std;

Session::Session() {}

Variable *Session::__add__(Variable *x, Variable *y) {
  Node *node_ = new Node(OP_ADD, x->node, y->node);
  return (Variable *)node_->var;
}

Variable *Session::__sub__(Variable *x, Variable *y) {
  Node *node_ = new Node(OP_SUB, x->node, y->node);
  return (Variable *)node_->var;
}

Variable *Session::__mul__(Variable *x, Variable *y) {
  Node *node_ = new Node(OP_MUL, x->node, y->node);
  return (Variable *)node_->var;
}

Variable *Session::__div__(Variable *x, Variable *y) {
  Node *node_ = new Node(OP_DIV, x->node, y->node);
  return (Variable *)node_->var;
}
