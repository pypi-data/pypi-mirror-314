#ifndef __AIDGE_EXPORT_CPP_KERNELS_MATMUL__
#define __AIDGE_EXPORT_CPP_KERNELS_MATMUL__

#include "network/typedefs.hpp"
#include "kernels/activation.hpp"

// Generic function for matmul and activation

template<int M,
         int K,
         int N,
         ActivationFunction_T ACTIVATION,
         typename Input_T, typename Output_T,
         typename Rescaling_T>
__attribute__((always_inline)) inline
void matmul_forward (
    const Input_T* __restrict inputs1,
    const Input_T* __restrict inputs2,
    Output_T* __restrict outputs,
    const Rescaling_T& __restrict rescaling)
{
    for (int m = 0; m < M; ++m) {
        for (int n = 0; n < N; ++n) {
            Output_T sum = Output_T(0);
            for (int k = 0; k < K; ++k) {
                sum += inputs1[K*m + k] * inputs2[N*k + n];
            }
            outputs[N*m + n] = activation_forward_value<Output_T>(sum, 0/*not applicable*/, ACTIVATION, rescaling);
        }
    }
}

#endif  // __AIDGE_EXPORT_CPP_KERNELS_MATMUL__
