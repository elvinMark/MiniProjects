#include <Autograd/Node.hpp>
#include <Autograd/Variable.hpp>

using namespace std;

Node::Node(void *var) {
  this->op_type = NONE;
  this->var = var;
  this->left = NULL;
  this->right = NULL;
}

Node::Node(int op_type, Node *left, Node *right) {
  this->op_type = op_type;
  this->var = new Variable(this);
  this->left = left;
  this->right = right;
}

int Node::is_leaf() { return this->left == NULL && this->right == NULL; }

void Node::print_(int depth) {
  if (this->left)
    this->left->print_(depth + SPACING);
  cout << string(depth, ' ');
  if (this->is_leaf())
    cout << ((Variable *)this->var)->data;
  else
    cout << "op," << this->op_type;
  cout << endl;
  if (this->right)
    this->right->print_(depth + SPACING);
}

void Node::print() { this->print_(0); }
