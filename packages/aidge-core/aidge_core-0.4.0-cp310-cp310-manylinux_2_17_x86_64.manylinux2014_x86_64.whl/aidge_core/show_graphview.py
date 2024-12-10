import os
import json
import builtins
import aidge_core
import numpy as np
from pathlib import Path
from typing import Any, Dict, List, Optional

def _retrieve_operator_attrs(node : aidge_core.Node) -> Dict[str, Optional[Any]]:
    """
    Returns the dictionary containing the attributes of a given Node.

    :param graph: A Node in the list of ordered nodes.
    :type graph: aidge_core.Node

    :return: A dictionary with the Node's attributes.
    :rtype: Dict[str, Optional[Any]]
    """

    if node.get_operator().attr is not None:
        node_attr_dict =  node.get_operator().attr.dict()
        for key,value in node_attr_dict.items():
            if not type(value).__name__ in dir(builtins):
                node_attr_dict[key] = value.name

    else:
        node_attr_dict = {}

    return node_attr_dict

def _create_dict(ordered_nodes : List[aidge_core.Node], write_trainable_params_embed : bool, write_trainable_params_ext : bool, path_trainable_params : Path, params_file_format : str) -> Dict[str, Optional[Any]]:
    """
    Creates a dictionary to store the information of a given ordered GraphView.

    :param ordered_nodes: A list with the GraphView's ordered nodes.
    :type graph: list
    :param write_trainable_params_embed: Whether or not to write the eventual trainable parameters of the Nodes in the same file as the dict (embed).
    :type write_trainable_params_embed: bool
    :param write_trainable_params_ext: Whether or not to write the eventual trainable parameters of the Nodes in an external file.
    :type write_trainable_params_ext: bool
    :param path_trainable_params: Path of the external file used to store the Nodes' trainable parameters.
    :type path_trainable_params: Path
    :param params_file_format: Format of the external file used to store the Nodes' trainable parameters. Options: ``npz`` or ``json``. Default : ``json``. Requires ``write_trainable_params_ext``.
    :type params_file_format: str

    :return: A dictionary with the GraphView description.
    :rtype: Dict[str, Optional[Any]]
    """

    graphview_dict = {'graph': []}

    for node in ordered_nodes:

        if node is not None:
            node_dict = {'name' : node.name(),
                         'optype' : node.get_operator().type(),
                         'nb_inputs' : node.get_operator().nb_inputs(),
                         'nb_outputs' : node.get_operator().nb_outputs()}

            inputs = []
            for input_idx in range(node.get_operator().nb_inputs()):
                input_dict = {'dims' : node.get_operator().get_input(input_idx).dims(),
                              'data_type' : str(node.get_operator().get_input(input_idx).dtype()),
                              'data_format' : str(node.get_operator().get_input(input_idx).dformat())}
                inputs.append(input_dict)

            node_dict['inputs'] = inputs

            outputs = []
            for output_idx in range(node.get_operator().nb_outputs()):
                output_dict = {'dims' : node.get_operator().get_output(output_idx).dims(),
                               'data_type' : str(node.get_operator().get_output(output_idx).dtype()),
                              'data_format' : str(node.get_operator().get_output(output_idx).dformat())}
                outputs.append(output_dict)

            node_dict['outputs'] = outputs

            parents = node.get_parents()
            if None in parents:
                if parents[0] is None: parents.append(parents.pop(0))
            else:
                pass

            parents_inputs = []
            input_idx = 0
            for parent in node.get_parents():
                if parent is not None:
                    for children in parent.outputs():
                        for child in children:
                            if child[0] == node and child[1] == input_idx:
                                parents_inputs.append((parent.name(), input_idx))

                elif parent is None:
                    if input_idx not in [item[1] for item in parents_inputs]:
                        parents_inputs.append((None, input_idx))

                input_idx += 1
            node_dict['parents'] = parents_inputs

            children_outputs = []
            output_idx = 0
            for children in node.get_ordered_children():
                for child in children:
                    if child is not None:
                        for parent in child.inputs():
                            if parent[0] == node and parent[1] == output_idx:
                                children_outputs.append((child.name(), output_idx))
                output_idx += 1
            node_dict['children'] = children_outputs

            # Check if my node is a metaop
            attributes_dict = {}
            if isinstance(node.get_operator(), aidge_core.MetaOperatorOp):
                attributes_dict['micro_graph'] = []
                for micro_node in node.get_operator().get_micro_graph().get_nodes():
                    micro_node_dict = {'name' : micro_node.name(),
                                        'optype' : micro_node.type()}

                    micro_node_attr_dict =  _retrieve_operator_attrs(micro_node)
                    micro_node_dict['attributes'] = micro_node_attr_dict
                    attributes_dict['micro_graph'].append(micro_node_dict)

            else:
                node_attr_dict = _retrieve_operator_attrs(node)
                attributes_dict.update(node_attr_dict)

            node_dict['attributes'] = attributes_dict

            if node.type() == 'Producer':
                if write_trainable_params_ext:

                    params_file_format.casefold()

                    if params_file_format=='npz':
                        np.savez_compressed(Path(path_trainable_params, node.name()), **{node.name() : node.get_operator().get_output(0)})
                        node_dict['tensor_data'] = str(Path(path_trainable_params, node.name() + '.npz'))

                    elif params_file_format=='json':
                        tensor = np.array(node.get_operator().get_output(0))
                        tensor_dict = {
                            node.name() :
                            {
                                'dims' : tensor.shape,
                                'data_type' : str(tensor.dtype),
                                'tensor_data' : tensor.tolist()
                            }
                        }

                        with open(Path(path_trainable_params, node.name() + '.json'), 'w') as fp:
                            json.dump(tensor_dict, fp, indent=4)

                        node_dict['tensor_data'] = str(Path(path_trainable_params, node.name() + '.json'))

                    else:
                        raise Exception("File format to write trainable parameters not recognized.")


                if write_trainable_params_embed:
                    node_dict['tensor_data'] = np.array(node.get_operator().get_output(0)).tolist()

                else:
                    pass

            graphview_dict['graph'].append(node_dict)

        else: # node is None
            pass

    return graphview_dict

def _write_dict_json(graphview_dict : Dict[str, Optional[Any]], json_path : str) -> None:
    """
    Writes dictionary containing GraphView description to a JSON file.

    :param graphview_dict: A dictionary with the GraphView description.
    :type graphview_dict: dict[str, int, float, bool, None]
    :param json_path: Path to write JSON file.
    :type json_path: str
    """

    with open(json_path, 'w') as fp:
        json.dump(graphview_dict, fp, indent=4)

    return None

def gview_to_json(gview : aidge_core.GraphView, json_path : Path, write_trainable_params_embed : bool = False, write_trainable_params_ext : bool = False, params_file_format : str = 'json') -> None:
    """
    Generates the description for a GraphView in the JSON format.

    :param graph: A GraphView of Aidge.
    :type graph: aidge_core.GraphView
    :param json_path: Path to write JSON file.
    :type json_path: Path
    :param write_trainable_params_embed: Whether or not to write the eventual trainable parameters of the Nodes in the same file as the dict (embed).
    :type write_trainable_params_embed: bool, optional
    :param write_trainable_params_ext: Whether or not to write the eventual trainable parameters of the Nodes in an external file.
    :type write_trainable_params_ext: bool, optional
    :param params_file_format: Format of the external file used to store the Nodes' trainable parameters. Options: ``npz`` or ``json``. Default : ``json``. Requires ``write_trainable_params_ext``.
    :type params_file_format: str, optional
    """

    if not json_path.suffix:
        if not json_path.is_dir():
            json_path.mkdir(parents=True, exist_ok=True)
        json_path = json_path.joinpath('model.json')

    else:
        if json_path.suffix != '.json':
            raise Exception('If ``json_path`` contains a filename, it must be of JSON format.')
        if not json_path.parent.is_dir():
            json_path.parent.mkdir(parents=True, exist_ok=True)

    if write_trainable_params_ext:
        path_trainable_params = (json_path.parent).joinpath(json_path.stem +  '_trainable_params/')
        path_trainable_params.mkdir(parents=True, exist_ok=True)

    else:
        path_trainable_params = Path()

    if isinstance(gview, aidge_core.GraphView):
        # Sort GraphView in topological order
        ordered_nodes = gview.get_ordered_nodes()

        # Create dict from GraphView
        graphview_dict = _create_dict(ordered_nodes, write_trainable_params_embed, write_trainable_params_ext, path_trainable_params, params_file_format)

        # Write dict to JSON
        _write_dict_json(graphview_dict, json_path)

    else:
        raise Exception("Graph must be an instance of aidge_core.GraphView.")

    return None