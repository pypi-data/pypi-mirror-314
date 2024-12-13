#ifndef __AIDGE_EXPORT_CPP_KERNELS_ELEMWISE__
#define __AIDGE_EXPORT_CPP_KERNELS_ELEMWISE__

#include "network/typedefs.hpp"
#include "kernels/activation.hpp"

// Generic function for two inputs

template<int NB_ELTS,
         ElemWise_T ELEM_OP,
         ActivationFunction_T ACTIVATION,
         typename Input_T, typename Output_T,
         typename Rescaling_T>
__attribute__((always_inline)) inline
void elemwise_forward (
    Output_T* __restrict outputs,
    const Rescaling_T& __restrict rescaling,
    const Input_T* __restrict inputs1,
    const Input_T* __restrict inputs2)
{
    if (std::is_floating_point<Input_T>::value)
    {
        Input_T val = 0;

        switch (ELEM_OP) {
            case Add: {
                for (int i = 0; i < NB_ELTS; ++i) {
                    val = inputs1[i] + inputs2[i];
                    outputs[i] = activation_forward_value<Output_T>(val, i, ACTIVATION, rescaling);
                }
                break;
            }
            case Sub: {
                for (int i = 0; i < NB_ELTS; ++i) {
                    val = inputs1[i] - inputs2[i];
                    outputs[i] = activation_forward_value<Output_T>(val, i, ACTIVATION, rescaling);

                }
                break;
            }
            case Mul: {
                for (int i = 0; i < NB_ELTS; ++i) {
                    val = inputs1[i] * inputs2[i];
                    outputs[i] = activation_forward_value<Output_T>(val, i, ACTIVATION, rescaling);
                }
                break;
            }
            default: {
                // Copy inputs1 in outputs for default case
                for (int i = 0; i < NB_ELTS; ++i) {
                    val = inputs1[i];
                    outputs[i] = activation_forward_value<Output_T>(val, i, ACTIVATION, rescaling);
                }
                break;
            }
        }
    }
    else
    {
        int32_t val = 0;

        switch (ELEM_OP) {
            case Add: {
                for (int i = 0; i < NB_ELTS; ++i) {
                    val = inputs1[i] + inputs2[i];
                    outputs[i] = activation_forward_value<Output_T>(val, i, ACTIVATION, rescaling);
                }
                break;
            }
            case Sub: {
                for (int i = 0; i < NB_ELTS; ++i) {
                    val = inputs1[i] - inputs2[i];
                    outputs[i] = activation_forward_value<Output_T>(val, i, ACTIVATION, rescaling);
                }
                break;
            }
            case Mul: {
                for (int i = 0; i < NB_ELTS; ++i) {
                    val = inputs1[i] * inputs2[i];
                    outputs[i] = activation_forward_value<Output_T>(val, i, ACTIVATION, rescaling);
                }
                break;
            }
            default: {
                // Copy inputs1 in outputs for default case
                for (int i = 0; i < NB_ELTS; ++i) {
                    val = inputs1[i];
                    outputs[i] = activation_forward_value<Output_T>(val, i, ACTIVATION, rescaling);
                }
                break;
            }
        }
    }
}


// Generic function for multiple inputs
// Not working

// template<ElemWise_T ELEM_OP, typename Output_T>
// __attribute__((always_inline)) inline
// Output_T elemWise (int /*pos*/, int /*ch*/)
// {
//     return 0;
// }

// template<ElemWise_T ELEM_OP,
//          int NB_CHANNELS,
//          // For next inputs
//          int... ARGS,
//          typename... INPUTS,
//          // Types
//          typename Input_T, typename Output_T>
// __attribute__((always_inline)) inline
// Output_T elemWise (int pos, int ch,
//                    const Input_T* __restrict firstInputs,
//                    INPUTS... inputs)
// {
//     int iOffset = NB_CHANNELS * pos;

//     return firstInputs[iOffset + ch]
//                 + elemWise<ELEM_OP, ARGS...>(pos, ch, inputs...);
// }

// template<// For all inputs
//          int NB_CHANNELS,
//          int CHANNELS_HEIGHT, int CHANNELS_WIDTH,
//          int NB_ELTS,
//          int OUTPUTS_HEIGHT, int OUTPUTS_WIDTH,
//          ElemWise_T ELEM_OP,
//          ActivationFunction_T ACTIVATION,
//          // For next inputs
//          int... ARGS,
//          typename... INPUTS,
//          // Types
//          typename Input_T, typename Output_T,
//          typename Rescaling_T>
// __attribute__((always_inline)) inline
// void elemWise_forward (
//     Output_T* __restrict outputs,
//     const Rescaling_T& __restrict rescaling,
//     const Input_T* __restrict firstInputs,
//     INPUTS... inputs)
// {
//     for (int oy = 0; oy < OUTPUTS_HEIGHT; oy++) {
//         for (int ox = 0; ox < OUTPUTS_WIDTH; ox++) {
//             const int pos = (ox + OUTPUTS_WIDTH * oy);
//             int oOffset = NB_ELTS * pos;

//             for (int ch = 0; ch < NB_ELTS; ++ch) {
//                 const Add_T val = elemWise<ELEM_OP,
//                                         INPUT_NB_CHANNELS,
//                                         INPUT_MEM_CONT_OFFSET,
//                                         INPUT_MEM_CONT_NB_ELTS,
//                                         INPUT_MEM_WRAP_OFFSET,
//                                         INPUT_MEM_WRAP_NB_ELTS,
//                                         INPUT_MEM_STRIDE,
//                                         ARGS...>(pos, ch, firstInputs, inputs...);

//                 outputs[oOffset + ch]
//                     = sat<Output_T>(val, ch, ACTIVATION, rescaling);
//             }
//         }
//     }
// }





#endif  // __AIDGE_EXPORT_CPP_KERNELS_ELEMWISE__
