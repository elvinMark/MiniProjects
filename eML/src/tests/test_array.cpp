#include <eML.hpp>

int main(){
  eArray *t = new eArray(3,3,STOP);
  double v = 5;
  t->random();
  t->at(&v,2,2,STOP);
  printf("%f\n",v);
  
  return 0;
}
