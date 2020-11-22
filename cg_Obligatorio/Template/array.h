#ifndef ARRAY_H
#define ARRAY_H

typedef struct
{
    void* data;
    int count;
    int cap;
    int inc;
    long int data_size;
} Array;

Array array_new(int capacity, long int data_size);
void array_append(Array pArray, float new_data);
void array_free(Array pArray);
#endif // ARRAY_H
