from setuptools import setup

from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir


__version__ = "1.3.2"

ext_modules = [
    Pybind11Extension("PyORCHESTRA",
        ["main.cpp",
        "source/Calculator.cpp",
        "source/Expander.cpp",
        "source/ExpressionGraph.cpp",
        "source/ExpressionString.cpp",
        "source/FileBasket.cpp",
        "source/IO.cpp",
        "source/MemoryNode.cpp",
        "source/Node.cpp",
        "source/NodeIOObject.cpp",
        "source/NodeIOPair.cpp",
        "source/NodeIOVar.cpp",
        "source/NodeProcessor.cpp",
        "source/NodeType.cpp",
        "source/OObject.cpp",
        "source/OObjectBasket.cpp",
        "source/OObjectPieceOfText.cpp",
        "source/OrchestraReader.cpp",
        "source/ParameterList.cpp",
        "source/Parser.cpp",
        "source/ParserStringTokenizer.cpp",
        "source/StopFlag.cpp",
        "source/StringTokenizer.cpp",
        "source/UnEq.cpp",
        "source/UnEqGroup.cpp",
        "source/Var.cpp",
        "source/VarGroup.cpp",
        ],
    cxx_std = 17,
        define_macros = [('VERSION_INFO', __version__)],
        ),
]

setup(
    name = "PyORCHESTRA",
    version = __version__,
    description= "use ORCHESTRA in Python",
    long_description="version allows user to differentiate between functions",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
