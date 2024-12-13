import os
import numpy as np
from pathlib import Path
import aidge_core
from aidge_core.export_utils import ExportNode, ExportNodeCpp, generate_file
from aidge_export_cpp.utils import ROOT
from aidge_export_cpp.utils.converter import numpy_dtype2ctype
from aidge_export_cpp import ExportLibCpp

##############################################
############## Export functions ##############
##############################################

def export_params(name: str,
                  array: np.ndarray,
                  filepath: str):

    # Get directory name of the file
    dirname = os.path.dirname(filepath)

    # If directory doesn't exist, create it
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    generate_file(
        filepath,
        str(ROOT / "templates" / "data" / "parameters.jinja"),
        name=name,
        data_t=numpy_dtype2ctype(array.dtype),
        values=array.tolist()
    )


##############################################
############## Operators helper ##############
##############################################

@ExportLibCpp.register("Producer", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class ProducerCPP(ExportNode):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.values = np.array(self.operator.get_output(0))

        if len(self.values.shape) == 4:  # Note: export in HWC
            self.values = np.transpose(self.values, (0, 2, 3, 1))

    def export(self, export_folder: Path):
        header_path = f"include/parameters/{self.attributes['name']}.h"
        export_params(
            self.attributes['out_name'][0],
            self.values.reshape(-1),
            str(export_folder / header_path))
        return [header_path]

    def forward(self):
        # A Producer does nothing during forward
        return []

# TODO : find a way to remove this dummy exportnode
@ExportLibCpp.register("Pad2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class Pad_ARMCortexM(ExportNodeCpp):
    def __init__(self, node, mem_info):
        raise NotImplementedError("Pad2D nodes is not implemented")


@ExportLibCpp.register("ReLU", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class ReLUCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["activation"] = "Rectifier"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "activation_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "activation_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]

@ExportLibCpp.register("Conv2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class ConvCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        # No padding with Conv
        # Use PaddedConv to add padding attribute
        self.attributes["padding"] = [0, 0]
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "convolution_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "convolution_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "convolution.hpp"),
            str(ROOT / "kernels" / "macs.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]

@ExportLibCpp.register_metaop("PaddedConv2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class PaddedConvCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        # TODO find a way to retrive attr for meta op
        for n in self.operator.get_micro_graph().get_nodes():
            if n.type() == "Pad2D":
                self.attributes["padding"] = n.get_operator(
                ).attr.begin_end_borders
            if n.type() == "Conv2D":
                self.attributes["kernel_dims"] = n.get_operator(
                ).attr.kernel_dims
                self.attributes["stride_dims"] = n.get_operator(
                ).attr.stride_dims
                self.attributes["dilation_dims"] = n.get_operator(
                ).attr.dilation_dims
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "convolution_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "convolution_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "convolution.hpp"),
            str(ROOT / "kernels" / "macs.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]

@ExportLibCpp.register("Add", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class AddCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["elemwise_op"] = "Add"
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "elemwise_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "elemwise_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "elemwise.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]

@ExportLibCpp.register("Sub", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class SubCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["elemwise_op"] = "Sub"
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "elemwise_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "elemwise_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "elemwise.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]


@ExportLibCpp.register("Mul", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class MulCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["elemwise_op"] = "Mul"
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "elemwise_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "elemwise_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "elemwise.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]

@ExportLibCpp.register("MaxPooling2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class MaxPoolCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # No padding with MaxPooling
        # Use PaddedMaxPooling to add padding attribute
        self.attributes["padding"] = [0, 0]
        self.attributes["pool_type"] = "Max"
        self.attributes["activation"] = "Linear"

        self.config_template = str(
            ROOT / "templates" / "configuration" / "pooling_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "pooling_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "pooling.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]


@ExportLibCpp.register_metaop("PaddedMaxPooling2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class PaddedMaxPoolCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        for n in self.operator.get_micro_graph().get_nodes():
            if n.type() == "Pad2D":
                self.attributes["padding"] = n.get_operator(
                ).attr.begin_end_borders
            if n.type() == "MaxPooling2D":
                self.attributes["kernel_dims"] = n.get_operator(
                ).attr.kernel_dims
                self.attributes["stride_dims"] = n.get_operator(
                ).attr.stride_dims
        self.attributes["pool_type"] = "Max"
        self.attributes["activation"] = "Linear"

        self.config_template = str(
            ROOT / "templates" / "configuration" / "pooling_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "pooling_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "pooling.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]


@ExportLibCpp.register("GlobalAveragePooling", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class GlobalAveragePoolCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        self.attributes["stride_dims"] = [1, 1]
        # No padding with MaxPooling
        # Use PaddedMaxPooling to add padding attribute
        self.attributes["padding"] = [0, 0]
        self.attributes["kernel_dims"] = [
            self.attributes["in_height"][0],
            self.attributes["in_width"][0],
        ]
        self.attributes["pool_type"] = "Average"
        self.attributes["activation"] = "Linear"

        self.config_template = str(
            ROOT / "templates" / "configuration" / "pooling_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "pooling_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "pooling.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]

@ExportLibCpp.register("FC", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class FcCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "fullyconnected_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "fullyconnected_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "fullyconnected.hpp"),
            str(ROOT / "kernels" / "macs.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]
