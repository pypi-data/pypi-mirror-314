#ifndef __AIDGE_EXPORT_CPP_KERNELS_BATCHNORM__
#define __AIDGE_EXPORT_CPP_KERNELS_BATCHNORM__

#include "network/typedefs.hpp"
#include "kernels/rescaling.hpp"
#include <math.h>

// WARNING: this kernel only works for 32-bits floating point values

template<int NB_OUTPUTS,
         int OUTPUTS_HEIGHT, int OUTPUTS_WIDTH,
         ActivationFunction_T ACTIVATION,
         typename Input_T, typename Output_T,
         typename Param_T>
__attribute__((always_inline)) inline
void batchnorm_forward (
    const Input_T* __restrict inputs,
    Output_T* __restrict outputs,
    const Param_T* __restrict biases,
    const Param_T* __restrict variances,
    const Param_T* __restrict means,
    const Param_T* __restrict scales,
    const double epsilon)
{
    for (unsigned int output = 0; output < NB_OUTPUTS; ++output) {
        const Output_T var = sqrt(variances[output] + epsilon);

        for (int oy = 0; oy < OUTPUTS_HEIGHT; ++oy) {
            for (int ox = 0; ox < OUTPUTS_WIDTH; ++ox) {
                const int outputOffset = OUTPUTS_HEIGHT * oy + ox;

                const Output_T normalized = (inputs[outputOffset + output] - means[output]) / var;
                const Output_T sAs = scales[output] * normalized + biases[output];
                outputs[outputOffset + output] = sat<Output_T>(sAs, output, ACTIVATION, NoScaling);
            }
        }
    }
}


#endif  // __AIDGE_EXPORT_CPP_KERNELS_BATCHNORM__
