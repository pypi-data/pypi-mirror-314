#ifndef __AIDGE_EXPORT_CPP_KERNELS_LEAKYRELU__
#define __AIDGE_EXPORT_CPP_KERNELS_LEAKYRELU__

#include "network/typedefs.hpp"

template<int NB_DATA,
         typename Input_T, typename Output_T>
__attribute__((always_inline)) inline 
void leakyrelu_forward (
    const Input_T* __restrict inputs,
    Output_T* __restrict outputs,
    const float negative_slope)
{
#pragma omp parallel for
    for (int i = 0; i < NB_DATA; ++i) {
        if (inputs[i] >= 0) {
            outputs[i] = inputs[i];
        } else {
            outputs[i] = negative_slope * inputs[i];
        }
    }
}


#endif  // __AIDGE_EXPORT_CPP_KERNELS_LEAKYRELU__