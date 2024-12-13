#ifndef __AIDGE_EXPORT_CPP_MACS_HPP__
#define __AIDGE_EXPORT_CPP_MACS_HPP__

template<int NB_ITERATIONS,
             int INPUTS_INC = 1,
             int WEIGHTS_INC = 1,
             class Input_T,
             class Weight_T,
             class Sum_T>
static void macsOnRange(const Input_T* __restrict inputs, 
                        const Weight_T* __restrict weights, 
                        Sum_T& __restrict weightedSum) 
{
    for (int iter = 0; iter < NB_ITERATIONS; ++iter) {
        weightedSum += inputs[iter*INPUTS_INC] * weights[iter*WEIGHTS_INC];
    }
}

#endif
