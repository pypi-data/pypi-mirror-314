#ifndef __AIDGE_EXPORT_CPP_NETWORK_TYPEDEFS__
#define __AIDGE_EXPORT_CPP_NETWORK_TYPEDEFS__

#include <stdint.h>

typedef enum {
    Tanh,
    Saturation,
    Rectifier,
    Linear,
    Softplus
} ActivationFunction_T;

typedef enum {
    Max,
    Average
} Pooling_T;

typedef enum {
    Add,
    Sub,
    Mul
} ElemWise_T;

typedef enum {
    PerLayer,
    PerInput,
    PerChannel
} CoeffMode_T;


#endif  // __AIDGE_EXPORT_CPP_NETWORK_TYPEDEFS__
