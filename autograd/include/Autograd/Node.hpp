#ifndef NODE
#define NODE

#include <iostream>
#include <string>
#define SPACING 5

enum { NONE, OP_ADD, OP_SUB, OP_MUL, OP_DIV };

class Node {
public:
  Node *left;
  Node *right;
  void *var;
  int op_type;

public:
  Node(void *var);
  Node(int op_type, Node *left, Node *right);
  int is_leaf();
  void print_(int depth);
  void print();
};

#endif
