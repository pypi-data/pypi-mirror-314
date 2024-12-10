import aidge_core
import os
import shutil
from pathlib import Path
from aidge_core.export_utils import ExportLib, generate_file, copy_file
from typing import List, Tuple


def scheduler_export(scheduler, export_folder_path: str, export_lib: ExportLib = None, memory_manager=None, memory_manager_args=None, test_mode=False) -> None:
    """Exports an aidge_core.Scheduler to C++ code.

    This function generates files for a given computation graph, including forward-pass functions,
    configuration headers, and the main API entry point for the exported model. It requires a
    memory manager to allocate resources, and optionally an `ExportLib` instance to handle backend
    configurations for node operators.


    1. **Export Preparation**:
        - Initializes export and DNN folders, checking that required memory management functions are defined.
        - Retrieves peak memory usage and memory details for each node using the `memory_manager`.

    2. **Configuration Generation**:
        - Iterates over nodes scheduled by `scheduler`, configuring backends if `export_lib` is specified.
        - Exports configuration headers and forward-pass actions for each node by invoking `op.export()`
            and `op.forward()`, appending these to `list_configs` and `list_actions`, respectively.
        - Collects information on input and output nodes, including their names, data types, and sizes.

    3. **Code Generation**:
        - Defines the forward-pass function, `model_forward`, with inputs and outputs based on node attributes.
        - Generates the following files:

            - **forward.cpp**: Implements the model forward pass using templates, applying configurations
            and actions for each node.

            - **forward.hpp**: Exports the forward API, defining inputs and outputs.

            - **main.cpp**: Main entry file, serving as the model's forward-pass interface.

    4. **Static File Export (Optional)**:
        - If `export_lib` is specified, static files are copied to the export folder based on `export_lib`
        specifications.


    :param scheduler: Scheduler instance managing the computation graph.
                    Uses `graph_view` and `get_static_scheduling` methods
                    to retrieve the computation graph layout and ordered nodes.
    :type scheduler: aidge_core.Scheduler
    :param export_folder_path: Path to the folder where the generated export files will be saved.
                            Creates this folder, along with subdirectories for model and source files.
    :type export_folder_path: str
    :param export_lib: Library providing the backend implementation for node operators.
                    Defaults to None. If provided, each node's backend is set to the library's name.
    :type export_lib: ExportLib, optional
    :param memory_manager: Required function for managing memory allocation. It should take
                        `scheduler` and optional `memory_manager_args` as parameters, returning
                        `peak_mem` (peak memory usage) and `mem_info` (memory details for each node).
    :type memory_manager: callable
    :param memory_manager_args: Additional arguments passed to `memory_manager`. Defaults to an empty dictionary.
    :type memory_manager_args: dict, optional
    :param test_mode: Additional argument which may be used during forward generation.
    :type test_mode: bool, optional
    """
    graphview = scheduler.graph_view()
    export_folder = Path().absolute() / export_folder_path

    os.makedirs(str(export_folder), exist_ok=True)

    dnn_folder = export_folder / "dnn"
    os.makedirs(str(dnn_folder), exist_ok=True)

    if memory_manager_args is None:
        memory_manager_args = {}

    if memory_manager is None:
        raise ValueError("A memory manager is required (no default value yet).")
    peak_mem, mem_info = memory_manager(
        scheduler, **memory_manager_args)

    # List of function call for forward.cpp
    list_actions: List[str] = []
    # List of headers for forward.cpp
    list_configs: List[str] = []

    inputs_name: List[str] = []
    inputs_dtype: List[str] = []
    outputs_name: List[str] = []
    outputs_dtype: List[str] = []
    outputs_size: List[int] = []

    # List of aidge_core.Node ordered by scheduler
    list_forward_nodes: List[aidge_core.Node] = scheduler.get_static_scheduling()

    # If exportLib define use it
    # else parse component in platform
    # if export_lib is None:
    #     raise ValueError("Export need an ExportLib.")
    for node in list_forward_nodes:
        if export_lib is not None:
            aidge_core.Log.debug(f"Setting backend {export_lib._name} to {node.name()}[{node.type()}].")
            node.get_operator().set_backend(export_lib._name)

        op_impl = node.get_operator().get_impl()
        if op_impl is None:
            raise RuntimeError(f"Operator {node.name()}[{node.type()}] doesn't have an implementation.")
        if not isinstance(op_impl, ExportLib):
            raise RuntimeError(f"Operator {node.name()}[{node.type()}] doesn't have an exportable backend ({op_impl}).")

        is_input:bool  = node in graphview.get_input_nodes()
        is_output:bool = node in graphview.get_output_nodes()

        if is_input:
            # GraphView.get_inputs_nodes() returns the nodes that have an Input set to None or not in the graph
            # However, some inputs are Optional and thus the node may not be an input of the graph!
            # So we need to check that all the inputs of the nodes or in the graph or not optional
            # This is what the following code block is checking.
            for idx, node_in in enumerate(node.inputs()):
                optional:bool = node.get_operator().input_category(idx) == aidge_core.InputCategory.OptionalData
                # Note: node_in is a Tuple(Node, out_idx)
                in_graph:bool = node_in[0] in graphview.get_nodes()
                is_input &= (in_graph or not optional)

        # Get operator current specs
        required_specs = op_impl.get_required_spec()
        # Get specs of the implementation that match current specs
        specs = op_impl.get_best_match(required_specs)
        # Retrieve said implementation
        export_node = op_impl.get_export_node(specs)

        if export_node is None:
            raise RuntimeError(f"Could not find export node for {node.name()}[{node.type()}].")
        # Instanciate ExportNode
        op = export_node(node, mem_info[node])

        # For configuration files
        list_configs += op.export(dnn_folder)
        # For forward file
        list_actions += op.forward()
        if is_input:
            for idx, node_in in enumerate(node.inputs()):
                if node_in[0] not in graphview.get_nodes():
                    inputs_name.append(op.attributes["in_name"][idx])
                    inputs_dtype.append(
                        op.attributes["in_cdtype"][idx]
                    )
        if is_output:
            for idx in range(len(node.outputs())):
                outputs_name.append(op.attributes["out_name"][idx])
                outputs_dtype.append(
                    op.attributes["out_cdtype"][idx]
                )
                outputs_size.append(op.attributes["out_size"][idx])

    func_name = "model_forward"
    ROOT = Path(__file__).resolve().parents[0]

    forward_template = str(ROOT / "templates" / "forward.jinja")
    if export_lib.forward_template != None:
        forward_template = export_lib.forward_template

    list_node_names = []
    for node in list_forward_nodes:
        if node.type() != "Producer":
            list_node_names.append(node.name())

    generate_file(
        str(dnn_folder / "src" / "forward.cpp"),
        forward_template,
        func_name=func_name,
        headers=set(list_configs),
        actions=list_actions,
        # Note: Graph may not have inputs, so we need to check with output
        # In the future, we should remove this as it is not compatible
        # with a mix precision approach.
        mem_ctype=outputs_dtype[0],  # Legacy behavior ...
        mem_section=export_lib.mem_section,
        peak_mem=peak_mem,
        inputs_name=inputs_name,
        inputs_dtype=inputs_dtype,
        outputs_name=outputs_name,
        outputs_dtype=outputs_dtype,
        test_mode=test_mode,
        list_node_names=list_node_names
    )

    forward_header_template = str(ROOT / "templates" / "forward_header.jinja")
    if export_lib.forward_header_template != None:
        forward_header_template = export_lib.forward_header_template

    # Generate dnn API
    generate_file(
        str(dnn_folder / "include" / "forward.hpp"),
        forward_header_template,
        libraries=[],
        func_name=func_name,
        inputs_name=inputs_name,
        inputs_dtype=inputs_dtype,
        outputs_name=outputs_name,
        outputs_dtype=outputs_dtype,
        test_mode=test_mode
    )

    if len(outputs_name) != len(outputs_dtype) or len(outputs_name) != len(outputs_size):
        raise RuntimeError("FATAL: Output args list does not have the same length this is an internal bug.")

    if export_lib is not None:
        # Copy all static files in the export
        for source, destination in export_lib.static_files.items():
            copy_file(source, str(export_folder / destination))
