"""
Simple script demonstrating the SciSave capabilities.
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "BSD License"

import os
import sys
import numpy as np
import scisave


if __name__ == "__main__":
    # set environment variables (used in the config file)
    os.environ['ENVDATA_A'] = 'data_env_a'
    os.environ['ENVDATA_B'] = 'data_env_b'

    # set substitution variables (used in the config file)
    substitute = {
        "sub_a": "data_sub_a",
        "sub_b": "data_sub_b",
    }

    # load the configuration file with custom YAML extensions
    tmp = scisave.load_config("config_main.yaml", extension=True, substitute=substitute)
    print("======================== CONFIG")
    print(tmp)

    # create a data with complex numbers and arrays
    data = {
        "complex_scalar": 3+4j,
        "int_array": np.array([1, 2, 3]),
        "float_array": np.array([1.0, 2.0, 3.0]),
        "complex_array": np.array([1+1j, 2+2j, 3+3j]),
        "bool_array": np.array([True, False, True]),
        "multi_array": np.array([[1, 2], [3, 4]]),
    }

    # dump and load the data as JSON/TXT
    scisave.write_data("dump.json", data)
    tmp = scisave.load_data("dump.json")
    print("======================== JSON/TXT")
    print(tmp)

    # dump and load the data as JSON/GZIP
    scisave.write_data("dump.gz", data)
    tmp = scisave.load_data("dump.gz")
    print("======================== JSON/GZIP")
    print(tmp)

    # dump and load the data as Pickle
    scisave.write_data("dump.pickle", data)
    tmp = scisave.load_data("dump.pickle")
    print("======================== PICKLE")
    print(tmp)

    sys.exit(0)
