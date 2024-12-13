import re
import os
import numpy as np

import aidge_core

from aidge_core.export_utils.code_generation import *
from aidge_core.mem_info import compute_default_mem_info

from aidge_export_cpp.utils import ROOT
from aidge_export_cpp.utils.converter import numpy_dtype2ctype
from aidge_export_cpp import ExportLibCpp
from aidge_export_cpp.utils.generation import *
# from aidge_export_cpp.memory import *


def generate_input_file(export_folder:str,
                        array_name:str,
                        array: np.ndarray):

    # If directory doesn't exist, create it
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    generate_file(
        file_path=f"{export_folder}/{array_name}.h",
        template_path=str(ROOT / "templates" / "data" / "inputs.jinja"),
        dims = array.shape,
        data_t = numpy_dtype2ctype(array.dtype),
        name = array_name,
        values = array.tolist()
    )


def export(export_folder_name, graphview, scheduler, mem_wrapping=False):
    aidge_core.export_utils.scheduler_export(
        scheduler,
        export_folder_name,
        ExportLibCpp,
        memory_manager=compute_default_mem_info
    )

    # export_folder = Path().absolute() / export_folder_name

    # os.makedirs(str(export_folder), exist_ok=True)

    # dnn_folder = export_folder / "dnn"
    # os.makedirs(str(dnn_folder), exist_ok=True)

    # list_actions = []
    # list_configs = []
    # peak_mem, mem_info = compute_default_mem_info(scheduler)
    # list_forward_nodes = scheduler.get_static_scheduling()

    # for node in list_forward_nodes:
    #     if ExportLibCpp.exportable(node):
    #         op = ExportLibCpp.get_export_node(node)(node, mem_info[node])
    #         # For configuration files
    #         list_configs = op.export(dnn_folder, list_configs)

    #         # For forward file
    #         list_actions = op.forward(list_actions)
    #     else:
    #         raise RuntimeError(f"Operator not supported: {node.type()} !")

    # # Memory management
    # # stats_folder = export_folder / "statistics"
    # # os.makedirs(str(stats_folder), exist_ok=True)
    # # mem_size, mem_info = generate_optimized_memory_info(stats_folder, scheduler, mem_wrapping)
    # # peak_mem, mem_info = compute_default_mem_info(scheduler)

    # # Generate the memory file
    # # generate_file(
    # #     str(dnn_folder / "memory" / "mem_info.h"),
    # #     str(ROOT / "templates" / "memory" / "mem_info.jinja"),
    # #     mem_size = mem_size,
    # #     mem_info_legends = MEMORY_INFO_TEMPLATE,
    # #     mem_info = mem_info
    # # )
    # # list_configs.append("memory/mem_info.h")

    # # Get entry nodes
    # # Store the datatype & name
    # list_inputs_name = []
    # for node in graphview.get_input_nodes():
    #     for idx, node_input_tuple in enumerate(node.inputs()):
    #         node_input, _ = node_input_tuple
    #         if node_input is None:
    #             export_type = aidge2c(node.get_operator().get_output(0).dtype())
    #             list_inputs_name.append((export_type, f"{node.name()}_input_{idx}"))
    #         elif node_input not in graphview.get_nodes():
    #             export_type = aidge2c(node_input.get_operator().get_output(0).dtype())
    #             list_inputs_name.append((export_type, node_input.name()))


    # # Get output nodes
    # # Store the datatype & name, like entry nodes
    # list_outputs_name = []
    # for node in graphview.get_nodes():
    #     if len(node.get_children()) == 0:
    #         export_type = aidge2c(node.get_operator().get_output(0).dtype())
    #         list_outputs_name.append((export_type, f"{node.name()}_output_0"))

    # # Generate forward file
    # # TODO: for now the mem type is bound for all intermediate results, should change.
    # # Note that we may have all inputs constants, hence select output type
    # assert len(list_outputs_name) >= 1, f"TODO: requires some output to determine mem type"
    # mem_ctype = list_outputs_name[0][0]
    # generate_file(
    #     str(dnn_folder / "src" / "forward.cpp"),
    #     str(ROOT / "templates" / "network" / "network_forward.jinja"),
    #     headers=set(list_configs),
    #     actions=list_actions,
    #     inputs= list_inputs_name,
    #     outputs=list_outputs_name,
    #     mem_ctype=mem_ctype,
    #     peak_mem=peak_mem
    # )

    # # Generate dnn API
    # generate_file(
    #     str(dnn_folder / "include" / "dnn.hpp"),
    #     str(ROOT / "templates" / "network" / "dnn_header.jinja"),
    #     libraries=[],
    #     functions=get_functions_from_c_file(str(dnn_folder / "src" / "forward.cpp")),
    # )

    # # Copy all static files in the export
    # shutil.copy(str(ROOT / "static" / "main.cpp"), str(export_folder))
    # shutil.copy(str(ROOT / "static" / "Makefile"), str(export_folder))
    # shutil.copytree(str(ROOT / "static" / "include"), str(dnn_folder / "include"), dirs_exist_ok=True)
