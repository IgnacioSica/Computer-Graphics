#include "array.h"
#include <stdlib.h>

Array array_new(int capacity, long int data_size);
{
    Array result;
    result.count = 0;
    result.cap = capacity;
    result.inc = capacity;
    result.data_size = data_size;
    result.data = malloc(data_size*capacity);
}
void array_append(Array pArray, float new_data);
void array_free(Array pArray);
