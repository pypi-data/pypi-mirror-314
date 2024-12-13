#ifndef __AIDGE_EXPORT_CPP_KERNELS_FULLYCONNECTED__
#define __AIDGE_EXPORT_CPP_KERNELS_FULLYCONNECTED__

#include "network/typedefs.hpp"
#include "kernels/rescaling.hpp"
#include "network/utils.hpp"
#include "kernels/macs.hpp"
#include "kernels/activation.hpp"

template<int NB_CHANNELS,
         int CHANNELS_HEIGHT, int CHANNELS_WIDTH,
         int NB_OUTPUTS,
         int OUTPUTS_HEIGHT, int OUTPUTS_WIDTH,
         ActivationFunction_T ACTIVATION,
         typename Input_T, typename Output_T,
         typename Weight_T, typename Bias_T,
         typename Rescaling_T>
__attribute__((always_inline)) inline
void fullyconnected_forward (
    const Input_T* __restrict inputs,
    Output_T* __restrict outputs,
    const Weight_T* __restrict weights,
    const Bias_T* __restrict biases,
    const Rescaling_T& __restrict rescaling)
{
    // Warning, there is a trick here !
    // To use this kernel, the inputs have to be in NHWC and the weights are in NCHW
    // It is only an issue if the FC was after a flatten layer.
    // Otherwise it is not an issue for the other FC because CHANNELS_WIDTH = CHANNELS_HEIGHT = 1
    // Solution: Add a system to check dataformat
    for (int och = 0; och < NB_OUTPUTS; och++) {

        Bias_T weightedSum = biases[och];

        for (int iy = 0; iy < CHANNELS_HEIGHT; ++iy) {
            for (int ix = 0; ix < CHANNELS_WIDTH; ++ix) {
                for (int ch = 0; ch < NB_CHANNELS; ++ch) {
                    weightedSum += inputs[CHANNELS_WIDTH*NB_CHANNELS*iy + NB_CHANNELS*ix + ch]
                                * weights[CHANNELS_HEIGHT*CHANNELS_WIDTH*NB_CHANNELS*och + CHANNELS_HEIGHT*CHANNELS_WIDTH*ch + CHANNELS_HEIGHT*iy + ix];
                }
            }
        }

        outputs[och] = activation_forward_value<Output_T>(weightedSum, och, ACTIVATION, rescaling);
    }
/*
Here the kernel to use with inputs in NHWC and weights in NHWC
#pragma omp parallel for
    for (int och = 0; och < NB_OUTPUTS; och++) {

        Bias_T weightedSum = biases[och];

        for (int iy = 0; iy < CHANNELS_HEIGHT; ++iy) {
            const int iPos = (CHANNELS_WIDTH * iy);
            int iOffset = NB_CHANNELS * iPos;

            const int wOffset = NB_CHANNELS * CHANNELS_WIDTH
                                    * (iy + CHANNELS_HEIGHT * och);

            macsOnRange<NB_CHANNELS * CHANNELS_WIDTH>(
                inputs + iOffset,
                weights + wOffset,
                weightedSum);
        }

        outputs[och] = activation_forward_value<Output_T>(weightedSum, och, ACTIVATION, rescaling);
    }
*/
}


#endif  // __AIDGE_EXPORT_CPP_KERNELS_FULLYCONNECTED__
