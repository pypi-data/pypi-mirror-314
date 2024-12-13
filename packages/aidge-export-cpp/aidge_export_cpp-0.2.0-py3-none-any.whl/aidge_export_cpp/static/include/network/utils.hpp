#ifndef __AIDGE_EXPORT_CPP_NETWORK_UTILS__
#define __AIDGE_EXPORT_CPP_NETWORK_UTILS__

#ifdef SAVE_OUTPUTS
#include <sys/types.h>
#include <sys/stat.h>
#include <cstdio>      // fprintf
#include <type_traits> // std::is_floating_point
#endif

/**
 * @brief   Integer clamping
 * @param[in]  v   Value to be clamped
 * @param[in]  lo  Saturating lower bound
 * @param[in]  hi  Saturating higher bound
 * @returns         Value clamped between lo and hi
 *
 */
__attribute__((always_inline)) static inline
int clamp (int v, int lo, int hi)
{
    if(v < lo) {
        return lo;
    }
    else if(v > hi) {
        return hi;
    }
    else {
        return v;
    }
}

/**
 * @brief   Maximum of two integer values
 */
__attribute__((always_inline)) static inline
int max (int lhs, int rhs)
{
    return (lhs >= rhs) ? lhs : rhs;
}

/**
 * @brief   Minimum of two integer values
 */
__attribute__((always_inline)) static inline
int min (int lhs, int rhs)
{
    return (lhs <= rhs) ? lhs : rhs;
}


#ifdef SAVE_OUTPUTS
enum class Format {
    Default,
    NCHW,
    NHWC,
    CHWN,
    NCDHW,
    NDHWC,
    CDHWN
};


template<typename Output_T>
inline void saveOutputs(
    int NB_OUTPUTS,
    int OUTPUTS_HEIGHT, int OUTPUTS_WIDTH,
    int OUTPUT_MEM_CONT_OFFSET,
    int OUTPUT_MEM_CONT_SIZE,
    int OUTPUT_MEM_WRAP_OFFSET,
    int OUTPUT_MEM_WRAP_SIZE,
    int OUTPUT_MEM_STRIDE,
    const Output_T* __restrict outputs,
    FILE* pFile,
    Format format)
{
    // default is NHCW !
    if (format == Format::NHWC) {
        fprintf(pFile, "(");
        for(int oy = 0; oy < OUTPUTS_HEIGHT; oy++) {
            fprintf(pFile, "(");

            for(int ox = 0; ox < OUTPUTS_WIDTH; ox++) {
                fprintf(pFile, "(");

                const int oPos = (ox + OUTPUTS_WIDTH * oy);
                int oOffset = OUTPUT_MEM_STRIDE * oPos;

                if (OUTPUT_MEM_WRAP_SIZE > 0
                    && oOffset >= OUTPUT_MEM_CONT_SIZE)
                {
                    oOffset += OUTPUT_MEM_WRAP_OFFSET - OUTPUT_MEM_CONT_OFFSET
                                - OUTPUT_MEM_CONT_SIZE;
                }

                for (int output = 0; output < NB_OUTPUTS; output++) {
                    if (std::is_floating_point<Output_T>::value)
                        fprintf(pFile, "%f", static_cast<float>(outputs[oOffset + output]));
                    else
                        fprintf(pFile, "%d", static_cast<int>(outputs[oOffset + output]));

                    fprintf(pFile, ", ");
                }

                fprintf(pFile, "), \n");
            }

            fprintf(pFile, "), \n");
        }

        fprintf(pFile, ")\n");
    }
    else if (format == Format::NCHW || format == Format::Default) {
        for(int output = 0; output < NB_OUTPUTS; output++) {
            fprintf(pFile, "%d:\n", output);
            for(int oy = 0; oy < OUTPUTS_HEIGHT; oy++) {
                for(int ox = 0; ox < OUTPUTS_WIDTH; ox++) {
                    const int oPos = (ox + OUTPUTS_WIDTH * oy);
                    int oOffset = OUTPUT_MEM_STRIDE * oPos;
                    if (OUTPUT_MEM_WRAP_SIZE > 0
                        && oOffset >= OUTPUT_MEM_CONT_SIZE)
                    {
                        oOffset += OUTPUT_MEM_WRAP_OFFSET
                            - OUTPUT_MEM_CONT_OFFSET - OUTPUT_MEM_CONT_SIZE;
                    }

                    if (std::is_floating_point<Output_T>::value)
                        fprintf(pFile, "%f", static_cast<float>(outputs[oOffset + output]));
                    else
                        fprintf(pFile, "%d",  static_cast<int>(outputs[oOffset + output]));

                    fprintf(pFile, " ");
                }

                fprintf(pFile, "\n");
            }

            fprintf(pFile, "\n");
        }

        fprintf(pFile, "\n");
    }
    else {
        printf("Warning unsupported dataformat.\n");
    }
}
#endif // SAVE_OUTPUTS

#endif // __AIDGE_EXPORT_CPP_NETWORK_UTILS__
