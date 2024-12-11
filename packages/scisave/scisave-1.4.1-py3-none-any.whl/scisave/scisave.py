"""
Module for serialization and deserialization.
    - load JSON/YAML configuration files
    - load and write JSON/Pickle data files
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "BSD License"

import ast
import os.path
import json
import pickle
import gzip
import yaml
import numpy as np


class _YamlLoader(yaml.Loader):
    """
    This Python class offers extension to the YAML format.
        - parse relative paths (with respect to the YAML file)
        - include other YAML files (recursion possible)
        - evaluate a Python literal (using literal_eval)
        - substitute YAML strings with values from environment variables
        - substitute YAML strings with values from a provided dictionary
        - merge list of dicts
        - merge list of lists
    """

    def __init__(self, stream, substitute):
        """
        Constructor.
        Custom YAML loader subclassing the default loader.
        """

        # get the path of the YAML file for relative paths
        self.path_root = os.path.abspath(stream.name)
        self.path_root = os.path.dirname(self.path_root)
        self.substitute = substitute

        # flag indicating if any merge commands are used
        self.has_merge = False

        # call the constructor of the parent
        super().__init__(stream)

        # handling of YAML files inclusion
        def fct_handle_include(self, node):
            res = _YamlLoader._yaml_handling(self, node, self._extract_yaml)
            return res

        # handling of relative paths
        def fct_handle_path(self, node):
            res = _YamlLoader._yaml_handling(self, node, self._extract_path)
            return res

        # handling of string substitution from environment variables
        def fct_handle_env(self, node):
            res = _YamlLoader._yaml_handling(self, node, self._extract_env)
            return res

        # handling of string substitution from dictionary values
        def fct_handle_sub(self, node):
            res = _YamlLoader._yaml_handling(self, node, self._extract_sub)
            return res

        # handling of literal evaluation
        def fct_handle_eval(self, node):
            res = _YamlLoader._yaml_handling(self, node, self._extract_eval)
            return res

        # handling merge of a list of dicts
        def fct_handle_merge_dict(self, node):
            self.has_merge = True
            res = _MergeObj(self.construct_sequence(node), "dict")
            return res

        # handling merge of a list of lists
        def fct_handle_merge_list(self, node):
            self.has_merge = True
            res = _MergeObj(self.construct_sequence(node), "list")
            return res

        # add the extension to the YAML format
        _YamlLoader.add_constructor("!include", fct_handle_include)
        _YamlLoader.add_constructor("!path", fct_handle_path)
        _YamlLoader.add_constructor("!eval", fct_handle_eval)
        _YamlLoader.add_constructor("!env", fct_handle_env)
        _YamlLoader.add_constructor("!sub", fct_handle_sub)
        _YamlLoader.add_constructor("!merge_dict", fct_handle_merge_dict)
        _YamlLoader.add_constructor("!merge_list", fct_handle_merge_list)

    def _yaml_handling(self, node, fct):
        """
        Apply a function to a YAML node for list, dict, scalar.
        """

        if isinstance(node, yaml.ScalarNode):
            return fct(self.construct_scalar(node))
        elif isinstance(node, yaml.SequenceNode):
            result = []
            for arg in self.construct_sequence(node):
                result.append(fct(arg))
            return result
        elif isinstance(node, yaml.MappingNode):
            result = {}
            for tag, arg in self.construct_mapping(node).items():
                result[tag] = fct(arg)
            return result
        else:
            raise yaml.YAMLError("invalid YAML node type")

    def _extract_path(self, filename):
        """
        Find the path with respect to the YAML file path.
        """

        # check type
        if type(filename) is not str:
            raise yaml.YAMLError("path command arguments should be strings")

        # construct relative path
        filepath = os.path.join(self.path_root, filename)

        return filepath

    def _extract_yaml(self, filename):
        """
        Load an included YAML file.
        """

        # check type
        if type(filename) is not str:
            raise yaml.YAMLError("include command arguments should be strings")

        # construct relative path
        filepath = os.path.join(self.path_root, filename)

        # load YAML file
        data = _load_yaml(filepath, extension=True, substitute=self.substitute)

        return data

    def _extract_env(self, name):
        """
        Replace a string with a YAML data contained in an environment variable.
        """

        # check type
        if type(name) is not str:
            raise yaml.YAMLError("env command arguments should be strings")

        # get and check the variable
        value = os.getenv(name)
        if value is None:
            raise yaml.YAMLError("env variable is not existing: %s" % name)

        # load YAML string
        data = yaml.safe_load(value)

        return data

    def _extract_sub(self, name):
        """
        Replace a string with a Python data contained in a provided dictionary.
        """

        # check type
        if type(name) is not str:
            raise yaml.YAMLError("sub command arguments should be strings")

        # get and check the variable
        if self.substitute is None:
            raise yaml.YAMLError("sub dictionary is cannot be empty")

        # get and check the variable
        if name not in self.substitute:
            raise yaml.YAMLError("sub variable is not existing: %s" % name)

        # load YAML string
        data = self.substitute[name]

        return data

    def _extract_eval(self, var):
        """
        Evaluate a Python literal with the AST.
        """

        # check type
        if type(var) is not str:
            raise yaml.YAMLError("eval command arguments should be strings")

        # get and check the variable
        data = ast.literal_eval(var)

        return data


class _JsonNumPyEncoder(json.JSONEncoder):
    """
    This Python class offers extension to the JSON format (encoder).
        - encode NumPy scalar types
        - encode NumPy array types
    """

    def __init__(self, **kwargs):
        """
        Constructor
        """

        super().__init__(**kwargs)

    def default(self, obj):
        """
        Function encoding NumPy types as dictionaries.
        """

        # encode numpy scalars and arrays
        if np.isscalar(obj) and np.iscomplexobj(obj):
            return {
                "__complex__": None,
                "real": obj.real,
                "imag": obj.imag,
            }
        elif np.isscalar(obj) and np.issubdtype(obj.dtype, np.integer):
            return int(obj)
        elif np.isscalar(obj) and np.issubdtype(obj.dtype, np.floating):
            return float(obj)
        elif np.isscalar(obj) and np.issubdtype(obj.dtype, bool):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            # handle numpy array
            if np.iscomplexobj(obj):
                return {
                    "__numpy__": None,
                    "dtype": "complex",
                    "shape": obj.shape,
                    "data": {
                        "real": obj.real.flatten().tolist(),
                        "imag": obj.imag.flatten().tolist(),
                    },
                }
            elif np.issubdtype(obj.dtype, np.floating):
                return {
                    "__numpy__": None,
                    "dtype": "float",
                    "shape": obj.shape,
                    "data": obj.flatten().tolist(),
                }
            elif np.issubdtype(obj.dtype, np.integer):
                return {
                    "__numpy__": None,
                    "dtype": "int",
                    "shape": obj.shape,
                    "data": obj.flatten().tolist(),
                }
            elif np.issubdtype(obj.dtype, bool):
                return {
                    "__numpy__": None,
                    "dtype": "bool",
                    "shape": obj.shape,
                    "data": obj.flatten().tolist(),
                }
            else:
                TypeError("invalid numpy array for serialization")
        else:
            # if not numpy, default to the base encoder
            return json.JSONEncoder.default(self, obj)


class _JsonNumPyDecoder(json.JSONDecoder):
    """
    This Python class offers extension to the JSON format (decoder).
        - decode NumPy scalar types
        - decode NumPy array types
    """

    def __init__(self, **kwargs):
        """
        Constructor
        """

        kwargs.setdefault("object_hook", self.parse)
        super().__init__(**kwargs)

    def parse(self, obj):
        """
        Function decoding NumPy types from dictionaries.
        """

        # if not dict, do nothing
        if not isinstance(obj, dict):
            return obj

        # parse the extensions
        if "__complex__" in obj:
            # handling complex scalar
            real = obj["real"]
            imag = obj["imag"]
            return complex(real, imag)
        elif "__numpy__" in obj:
            # handle numpy array
            dtype = obj["dtype"]
            shape = obj["shape"]
            data = obj["data"]

            # parse the type
            if dtype == "complex":
                real = np.array(data["real"], dtype=complex).reshape(shape)
                imag = np.array(data["imag"], dtype=complex).reshape(shape)
                return real+1j*imag
            elif dtype == "float":
                return np.array(data, dtype=float).reshape(shape)
            elif dtype == "int":
                return np.array(data, dtype=int).reshape(shape)
            elif dtype == "bool":
                return np.array(data, dtype=bool).reshape(shape)
        else:
            return obj


class _MergeObj:
    """
    This Python class is used to merge YAML data.
        - a custom merge command is used with a list of arguments
        - the arguments (lists or dicts) are merged together
        - the merge is performed recursively

    The merge objects are created during the YAML parsing.
    The merge objects are replaced by the merged data after the parsing.
    """

    def __init__(self, data_list, data_type):
        """
        Constructor.
        Assign the list of data to be merged and the data type.
        """

        if type(data_list) is not list:
            raise yaml.YAMLError("arguments of the merge_dict / merge_list should be a list")

        self.data_list = data_list
        self.data_type = data_type

    def extract(self):
        """
        Merge a list of dicts or a list of lists.
        The merge is performed recursively.
        """

        if self.data_type == "dict":
            res = {}
            for data in self.data_list:
                data = _merge_data(data)
                if type(data) is not dict:
                    raise yaml.YAMLError("merge_dict cannot only merge dictionaries")
                res.update(data)
        elif self.data_type == "list":
            res = []
            for data in self.data_list:
                data = _merge_data(data)
                if type(data) is not list:
                    raise yaml.YAMLError("merge_list cannot only merge lists")
                res += data
        else:
            raise yaml.YAMLError("invalid merge type")

        return res


def _merge_data(data):
    """
    Walk through the data recursively and merge it.
    Find the merge objects and replace them with merged data.
    This function is used for the YAML merge extensions.
    """

    if type(data) is dict:
        for tag, val in data.items():
            data[tag] = _merge_data(val)
    elif type(data) is list:
        for idx, val in enumerate(data):
            data[idx] = _merge_data(val)
    elif type(data) is _MergeObj:
        data = data.extract()
    else:
        pass

    return data


def _load_yaml(filename, extension=True, substitute=None):
    """
    Load a YAML stream (with custom extensions).
    If required, merge the data (custom merge commands).
    """

    with open(filename, "r") as fid:
        # create YAML loader (without or without extensions)
        if extension:
            loader = _YamlLoader(fid, substitute)
        else:
            loader = yaml.Loader(fid)

        # parse, merge, and clean
        try:
            data = loader.get_single_data()
            if loader.has_merge:
                data = _merge_data(data)
        finally:
            loader.dispose()

    return data


def _load_json(filename, extension=True, compress=False):
    """
    Load a JSON file (with extensions).
    The JSON file can be a text file or a gzip file.
    """

    # create JSON decoder (without or without extensions)
    if extension:
        cls = _JsonNumPyDecoder
    else:
        cls = json.JSONDecoder

    # load the JSON data
    if compress:
        with gzip.open(filename, "rt", encoding="utf-8") as fid:
            data = json.load(fid, cls=cls)
    else:
        with open(filename, "r") as fid:
            data = json.load(fid, cls=cls)

    return data


def _write_json(filename, data, extension=True, compress=False):
    """
    Write a JSON file (with extensions).
    The JSON file can be a text file or a gzip file.
    """

    # create JSON encoder (without or without extensions)
    if extension:
        cls = _JsonNumPyEncoder
    else:
        cls = json.JSONEncoder

    # write the JSON data
    if compress:
        with gzip.open(filename, "wt", encoding="utf-8") as fid:
            json.dump(data, fid, cls=cls, indent=None)
    else:
        with open(filename, "w") as fid:
            json.dump(data, fid, cls=cls, indent=4)

    return data


def _load_pickle(filename):
    """
    Load a pickle file.
    """

    # load the Pickle file
    with open(filename, "rb") as fid:
        data = pickle.load(fid)

    return data


def _write_pickle(filename, data):
    """
    Write a pickle file.
    """

    # save the Pickle file
    with open(filename, "wb") as fid:
        pickle.dump(data, fid)


def load_config(filename, extension=True, substitute=None):
    """
    Load a configuration file (JSON or YAML).

    Parameters
    ----------
    filename : string
        Name and path of the file to be loaded.
        The file type is determined by the extension.
        For YAML files, the extension should be "yaml" or "yml".
        For JSON files, the extension should be "json" or "js".
        For GZIP/JSON files, the extension should be "gzip" or "gz".
    extension : bool
        Activate (or not) the YAML extensions.
        Activate (or not) the JSON extensions.
    substitute : dict
        Dictionary with the substitution.
        The key names are replaces by the values.
        Substitutions are only used for YAML files.

    Returns
    -------
    data : data
        Python data contained in the file content
    """

    (name, ext) = os.path.splitext(filename)
    if ext in [".json", ".js"]:
        data = _load_json(filename, extension=extension, compress=False)
    elif ext in [".gz", ".gzip"]:
        data = _load_json(filename, extension=extension, compress=True)
    elif ext in [".yaml", ".yml"]:
        data = _load_yaml(filename, extension=extension, substitute=substitute)
    else:
        raise ValueError("invalid file extension: %s" % filename)

    return data


def load_data(filename):
    """
    Load a data file (JSON or Pickle).

    Parameters
    ----------
    filename : string
        Name and path of the file to be loaded.
        The file type is determined by the extension.
        For JSON files, the extension should be "json" or "js".
        For GZIP/JSON files, the extension should be "gzip" or "gz".
        For Pickle files, the extension should be "pck".

    Returns
    -------
    data : data
        Python data contained in the file content
    """

    (name, ext) = os.path.splitext(filename)
    if ext in [".json", ".js"]:
        data = _load_json(filename, extension=True, compress=False)
    elif ext in [".gz", ".gzip"]:
        data = _load_json(filename, extension=True, compress=True)
    elif ext in [".pck", ".pkl", ".pickle"]:
        data = _load_pickle(filename)
    else:
        raise ValueError("invalid file extension: %s" % filename)

    return data


def write_data(filename, data):
    """
    Write a data file (JSON or Pickle).

    Parameters
    ----------
    filename : string
        Name and path of the file to be created.
        The file type is determined by the extension.
        For JSON files, the extension should be "json" or "js".
        For GZIP/JSON files, the extension should be "gzip" or "gz".
        For Pickle files, the extension should be "pck".
    data : data
        Python data to be saved.
    """

    (name, ext) = os.path.splitext(filename)
    if ext in [".json", ".js"]:
        _write_json(filename, data, extension=True, compress=False)
    elif ext in [".gz", ".gzip"]:
        _write_json(filename, data, extension=True, compress=True)
    elif ext in [".pck", ".pkl", ".pickle"]:
        _write_pickle(filename, data)
    else:
        raise ValueError("invalid file extension: %s" % filename)
