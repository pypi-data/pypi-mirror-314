import sys
from importlib.metadata import PackageNotFoundError, version

# Import compiler config from external package 'compiler-config' and
# use it to create a new module named 'qcaas_client.compiler_config'
# for backwards compatibility with public code samples, e.g.:
#
#   from qcaas_client.compiler_config import CompilerConfig, QuantumResultsFormat, Tket, TketOptimizations
#
from compiler_config import config as _externalized_compiler_config

sys.modules.setdefault("qcaas_client.compiler_config", _externalized_compiler_config)

try:
    __version__ = version("oqc-qcaas-client")
except PackageNotFoundError:
    __version__ = "unknown"
