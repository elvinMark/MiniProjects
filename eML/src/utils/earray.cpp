#include <eML.hpp>

eArray::eArray(int x, ...){
  va_list l;

  va_start(l, x);

  this->shape = args2arr(x, l, & this->dim);
  va_end(l);
  
  this->size = 1;
  this->stride = (int *) create_empty_arr(this->dim * sizeof(int));
  
  for(int i = this->dim - 1; i >= 0 ;i--){
    this->stride[i] = this->size;
    this->size *= this->shape[i];
  }

  this->acc_shape = this->stride;
  
  this->data = (double*) create_empty_arr(this->size * sizeof(double));

  this->offset = 0;
}

eArray::eArray(double* data, int size, int dim, int* shape,int* stride, int offset, int *acc_shape){
  this->data = data;
  this->size = size;
  this->dim = dim;
  this->shape = shape;
  this->stride = stride;
  this->offset = offset;
  this->acc_shape = acc_shape;
}

void eArray::zeros(){
  int idx;
  for(int i = 0;i<this->size;i++){
    idx = this->get_index(i);
    this->data[idx] = 0;
  }
}

void eArray::ones(){
  int idx;
  for(int i = 0;i<this->size;i++){
    idx = this->get_index(i);
    this->data[idx] = 1;
  }
}


void eArray::random(){
  int idx;
  for(int i = 0;i<this->size;i++){
    idx = this->get_index(i);
    this->data[idx] = random_number();
  }
}

int eArray::get_index(int idx){
  int tmp = this->offset;
  for(int i = 0;i < this->dim;i++){
    tmp += (this->stride[i] * (idx / this->acc_shape[i]));
    idx = idx % this->acc_shape[i];
  }

  return tmp;
}

void eArray::get_index(int *idx, int *pos){
  *idx = offset;

  for(int i = 0; i< dim; i++)
    *idx += stride[i] * pos[i];
}

void eArray::get_index(int* new_size, int* new_dim, int **new_shape, int ** new_stride, int* new_offset, int ** new_acc_shape, int *pos){
  *new_size = 1;
  *new_dim = 0;
  *new_shape = (int *) malloc(sizeof(int));
  *new_stride = (int *) malloc(sizeof(int));
  *new_offset = this->offset;
  
  for(int i = 0;i < this->dim; i++){
    if(pos[i] == ALL){
      *new_stride[*new_dim] = this->stride[i];
      *new_shape[*new_dim] = this->shape[i];
      *new_dim += 1;
      *new_stride = (int*) realloc(*new_stride,sizeof(int)*(*new_dim + 1));
      *new_shape = (int*) realloc(*new_shape,sizeof(int)*(*new_dim + 1));
    }
    else
       *new_offset += this->stride[i] * pos[i];
    *new_size *= this->shape[i];
  }
  
  *new_acc_shape = (int *)create_empty_arr(sizeof(int) * (*new_dim));
  int tmp = 1;
  for(int i = *new_dim - 1; i>=0 ; i--){
    *new_acc_shape[i] = tmp;
    tmp *= *new_shape[i];
  }
}

void eArray::at(double *val, int x, ...){
  va_list l;

  va_start(l , x);

  int d;
  int* pos = args2arr(x, l, &d);
  va_end(l);
  
  int idx;
  this->get_index(&idx, pos);
  *val = this->data[idx];
}

void eArray::at(eArray** t, int x, ...){
  va_list l;

  va_start(l , x);

  int d;
  int *pos = args2arr(x, l, &d);
  va_end(l);

  int new_size, new_dim, new_offset;
  int *new_shape, *new_stride, *new_acc_shape;
  
  this->get_index(&new_size,&new_dim,&new_shape,&new_stride,&new_offset, &new_acc_shape, pos);

  *t = new eArray(this->data, new_size, new_dim, new_shape, new_stride, new_offset, new_acc_shape);
}

void eArray::set(double *val, int x, ...){
  va_list l;

  va_start(l , x);

  int d;
  int *pos = args2arr(x, l, &d);
  va_end(l);

  int idx;
  this->get_index(&idx, pos);
  this->data[idx] = *val;
}

void eArray::set(eArray* t, int x, ...){
  va_list l;

  va_start(l , x);

  int d;
  int *pos = args2arr(x, l, &d);
  va_end(l);
}


string eArray::to_string(){
  string out = "";
  return out;
}
