from aidge_core.export_utils import ExportLib
from aidge_export_cpp.utils import ROOT

class ExportLibCpp(ExportLib):
    _name="export_cpp"
    static_files={
        str(ROOT / "static" / "Makefile"): "",
        str(ROOT / "static" / "include" / "network" / "typedefs.hpp"): "dnn/include/network",
        str(ROOT / "static" / "include" / "network" / "utils.hpp"): "dnn/include/network",
    }
