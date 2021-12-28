#ifndef SESSION
#define SESSION

#include <Autograd/Node.hpp>
#include <Autograd/Variable.hpp>
#include <iostream>

class Session {
public:
  Node *root;
  Node *cursor;

public:
  Session();
  Variable *__add__(Variable *x, Variable *y);
  Variable *__sub__(Variable *x, Variable *y);
  Variable *__mul__(Variable *x, Variable *y);
  Variable *__div__(Variable *x, Variable *y);
};

#endif
