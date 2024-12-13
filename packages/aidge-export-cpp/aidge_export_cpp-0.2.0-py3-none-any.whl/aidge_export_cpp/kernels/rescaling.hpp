#ifndef __AIDGE_EXPORT_CPP_NETWORK_RESCALING__
#define __AIDGE_EXPORT_CPP_NETWORK_RESCALING__


struct NoScaling {

    template<typename Sum_T>
    Sum_T operator()(Sum_T weightedSum, unsigned int /*output*/) const 
    {
        return weightedSum;
    }

};


#endif  // __AIDGE_EXPORT_CPP_NETWORK_RESCALING__
