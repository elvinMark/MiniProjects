#include <Autograd/Node.hpp>
#include <Autograd/Session.hpp>
#include <Autograd/Variable.hpp>
#include <iostream>
#include <string>

using namespace std;

int main() {
  Session *sess = new Session();
  Variable *a = new Variable(3.4);
  Variable *b = new Variable(5.6);
  Variable *c = new Variable(7.8);
  Variable *d = sess->__mul__(a, b);
  Variable *e = sess->__div__(c, b);
  Variable *f = sess->__add__(d, e);
  Variable *g = sess->__add__(a, c);
  Variable *h = sess->__div__(f, g);

  h->node->print();
  cout << h->eval() << endl;
  h->backward(1);
  cout << a->grad << endl;
  cout << b->grad << endl;
  cout << c->grad << endl;
  return 0;
}
