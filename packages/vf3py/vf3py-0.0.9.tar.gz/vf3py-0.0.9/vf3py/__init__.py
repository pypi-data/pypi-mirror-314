__version__ = '0.0.9'
import platform
import string
import multiprocessing
from typing import (
    Union,
    Callable,
    Tuple,
    List,
    Dict,
    Optional,
    Literal,
    Iterable,
    Set,
    Mapping,
)
import networkx as nx

assert platform.system() != "Windows", "Only Linux platform is supported in newer releases"
# if platform.system() == "Windows":
#     mypath = os.path.dirname(os.path.realpath(__file__))
#     if mypath not in sys.path:
#         sys.path.insert(0, mypath)
#     os.add_dll_directory(mypath)

from .cpppart import cpppart

VF3_VARIANTS = ('B', 'P', 'L')
VF3_VARIANTS_TYPE = Literal[VF3_VARIANTS]
MAX_THREADS = multiprocessing.cpu_count()

DOC_STRINGS = {
    'FIRST_GRAPH': "main_graph (nx.Graph | nx.DiGraph): First graph.",
    'SECOND_GRAPH': "ref_graph (nx.Graph | nx.DiGraph): Second graph.",
    'ANY_GRAPH': "graph (nx.Graph | nx.DiGraph): The graph of interest.",
    'LARGE_GRAPH': "graph (nx.Graph | nx.DiGraph): Searching for maps *into* this graph.",
    'SUBGRAPH': "subgraph (nx.Graph | nx.DiGraph): Searching for maps *of* this graph.",
    'NODE_MATCH': "node_match (Callable[[dict, dict], bool], optional): Nodes are allowed to be matched only if this function returns ``True`` for the nodes' attributes. Order of arguments: (1) dict of the source graph/subgraph, (2) target graph. Defaults to ``None``.",
    'EDGE_MATCH': "edge_match (Callable[[dict, dict], bool], optional): Edges are allowed to be matched only if this function returns ``True`` for the edges' attributes. Order of arguments: (1) dict of the source graph/subgraph, (2) target graph. Defaults to ``None``.",
    'ALL_SOLUTIONS': "all_solutions (bool, optional): Whether to generate all possible subgraph->graph matches (``True``) or only one (``False``). Defaults to ``True``.",
    'RETURN_INTEGERS': "return_integers (bool, optional): Whether to represent isomorphisms using integers (``True``) or the original labels of NetworkX graphs (``False``). Defaults to ``False``.",
    'VARIANT': f"variant (str, optional): The VF3 variant to be used. One of ``{VF3_VARIANTS}``. Defaults to ``'B'``.",
    'NUM_THREADS': "num_threads (int, optional): Number of threads to be used in parallel variant. Defaults to ``1``.",
    'VERBOSE': "verbose (bool, optional): Whether to print info on some intermediate steps. Defaults to ``False``.",
    'INDUCED': "induced (bool, optional): Whether to search for monomorphisms (``False``) or isomorphisms (``True``). Iso does not allow the target graph to have additional edges that are not present in the source graph. Defaults to ``True``.",
    'BIJECTIVE_FOR_NODES': "bijective_for_nodes (bool, optional): Whether to search for mono/isomorphisms between entire graphs (``True``) or allow to match with a subgraph of the target graph (``False``). Defaults to ``False``.",
}

GRAPH_TYPE = Union[nx.Graph, nx.DiGraph]

class NetworkxView(Set, Mapping):
    pass

def _keys_as_list(mask: str) -> list:
    return [
        t[1]
        for t in string.Formatter().parse(mask)
        if t[1] is not None
    ]


def _format_docstring(func: Callable) -> Callable:
    # Get the original docstring
    original_docstring = func.__doc__ if func.__doc__ else ""

    # Substitute placeholders with actual values
    formatted_docstring = original_docstring.format(**{
        key: DOC_STRINGS[key]
        for key in _keys_as_list(original_docstring)
    })

    # Set the new formatted docstring to the function
    func.__doc__ = formatted_docstring

    return func


VF3_CALLS = {
    # (variant, use_node_attrs, use_edge_attrs) => Appropriate function of the base pybind11 module
    ('B', False, False) : cpppart.calc_noattrs,
    ('B', True, False)  : cpppart.calc_nodeattr,
    ('B', False, True)  : cpppart.calc_edgeattr,
    ('B', True, True)   : cpppart.calc_bothattrs,
    ('L', False, False) : cpppart.calc_l_noattrs,
    ('L', True, False)  : cpppart.calc_l_nodeattr,
    ('L', False, True)  : cpppart.calc_l_edgeattr,
    ('L', True, True)   : cpppart.calc_l_bothattrs,
    ('P', False, False) : cpppart.calc_p_noattrs,
    ('P', True, False)  : cpppart.calc_p_nodeattr,
    ('P', False, True)  : cpppart.calc_p_edgeattr,
    ('P', True, True)   : cpppart.calc_p_bothattrs,
}


class ApplicabilityScopeError(Exception):
    """VF3Py has two limitations:

    * ``nx.MultiGraph`` and ``nx.MultiDiGraph`` are not supported.

    * Complex rules for matching nodes and edges. In particular, can not allow the same node (or edge) to be matched with multiple 'colors'.
    
    This exception can be thrown by any of these functions: ``are_isomorphic``, ``get_automorphisms``, ``get_exact_isomorphisms``, ``get_subgraph_isomorphisms``, ``has_subgraph``, ``main_vf3_caller``.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def _ensure_graph_correctness(graph: GRAPH_TYPE) -> None:
    if isinstance(graph, nx.MultiGraph) or isinstance(graph, nx.MultiDiGraph):
        raise ApplicabilityScopeError("Cannot accept Multigraph type for isomorphism calculations")

    assert isinstance(graph, nx.Graph) or isinstance(graph, nx.DiGraph), \
        f"Cannot accept graph of type '{type(graph)}' (nx.Graph or nx.DiGraph is expected)"

    assert graph.number_of_nodes() > 0, \
        "Graph must contain non-zero number of nodes"

    if graph.number_of_edges() == 0:
        raise ApplicabilityScopeError("Cannot accept Graph with no edges")


def _process_graph(graph: GRAPH_TYPE) -> Tuple[Dict, Dict, bool]:
    assert isinstance(graph, nx.Graph) or isinstance(graph, nx.DiGraph), \
        f"Provided '{repr(graph)}' is not a NetworkX graph"

    directed = isinstance(graph, nx.DiGraph)

    int_relabel = [
        node
        for node in graph.nodes
    ]

    relabeling = {
        'to_int': {
            node: i
            for i, node in enumerate(int_relabel)
        },
        'from_int': int_relabel
    }

    return {
        'nodes': [i for i in range(graph.number_of_nodes())],
        'edges': [
            [relabeling['to_int'][vA], relabeling['to_int'][vB]]
            for vA, vB in graph.edges
        ],

        # Attr lists will be filled later
        'node_attrs': [],
        'edge_attrs': [],
    }, relabeling, directed


def _group_attrs(
        itemviewA: NetworkxView, # Nodes/edges of the two graphs
        itemviewB: NetworkxView,
        match_function,
        item_type: Literal['node', 'edge'],
        bijective=False,
    ) -> Tuple[Union[Dict, None], Union[Dict, None]]:

    assert match_function is not None

    dep_graph = nx.Graph()
    a_nodes = []
    i = 0
    for item_name in itemviewA:
        dep_graph.add_node(i, base='A', name=item_name)
        a_nodes.append(i)
        i += 1

    b_nodes = []
    for item_name in itemviewB:
        dep_graph.add_node(i, base='B', name=item_name)
        b_nodes.append(i)
        i += 1

    for a_node in a_nodes:
        for b_node in b_nodes:
            if match_function(itemviewA[dep_graph.nodes[a_node]['name']], itemviewB[dep_graph.nodes[b_node]['name']]):
                dep_graph.add_edge(a_node, b_node)

    a_attrs = {}
    b_attrs = {}
    a_failed = False
    b_failed = False
    for attr_index, component in enumerate(nx.connected_components(dep_graph)):
        comp_subgraph = dep_graph.subgraph(component)
        a_number = sum(
            1
            for node, keys in comp_subgraph.nodes(data=True)
            if keys['base'] == 'A'
        )
        b_number = sum(
            1
            for node, keys in comp_subgraph.nodes(data=True)
            if keys['base'] == 'B'
        )

        if a_number == 0 and bijective:
            # Some attrs of target graph may be missing in source if bijection is not required
            a_failed = True
        if b_number == 0:
            # This condition means that there are no appropriate nodes/edges in B for node/edge of A to be mapped to
            b_failed = True

        num_edges = comp_subgraph.number_of_edges()
        if num_edges != a_number * b_number:
            raise ApplicabilityScopeError(f"Unable to create valid {item_type} attributes for {repr(match_function)}")

        for node, keys in comp_subgraph.nodes(data=True):
            if keys['base'] == 'A':
                a_attrs[keys['name']] = attr_index
            else:
                b_attrs[keys['name']] = attr_index

    if a_failed:
        a_attrs = None
    if b_failed:
        b_attrs = None
    return a_attrs, b_attrs


def _get_log_function(verbose: bool) -> Callable[[str], None]:
    if verbose:
        return lambda message: print(f"[VF3Py] {message}")
    else:
        return lambda message: None


@_format_docstring
def main_vf3_caller(
        subgraph: GRAPH_TYPE,
        graph:    GRAPH_TYPE,
        node_match: Optional[Callable[[dict, dict], bool]] = None,
        edge_match: Optional[Callable[[dict, dict], bool]] = None,
        all_solutions: bool=True,
        return_integers: bool=False,
        verbose: bool=False,
        variant: VF3_VARIANTS_TYPE = 'B',
        num_threads: int=1,
        induced: bool=True,
        bijective_for_nodes: bool=False,
    ) -> List[Dict]:
    """The core routine of the VF3Py library. It solves the subgraph iso/monomorphism problem, i.e. finds ways to match nodes of ``subgraph`` with some/all nodes of ``graph``. Only NetworkX graphs are accepted (either nx.Graph or nx.DiGraph). **NOTE**: It is not practical to call this function directly -- use one of the front-end functions instead: ``are_isomorphic``, ``get_exact_isomorphisms``, ``get_automorphisms``, ``has_subgraph``, ``get_subgraph_isomorphisms``.

    Args:
        {SUBGRAPH}
        {LARGE_GRAPH}
        {NODE_MATCH}
        {EDGE_MATCH}
        {ALL_SOLUTIONS}
        {RETURN_INTEGERS}
        {VARIANT}
        {NUM_THREADS}
        {VERBOSE}
        {INDUCED}
        {BIJECTIVE_FOR_NODES}

    Returns:
        List[Dict]: List of subgraph->graph isomorphisms. Each isomorphism is represented by a dict that maps: 'subgraph' labels -> 'graph' labels.
    """
    
    log = _get_log_function(verbose)

    if bijective_for_nodes and (subgraph.number_of_nodes() != graph.number_of_nodes()):
        log("Initial check indicates the absence of solutions")
        return []
    
    assert num_threads == 1 or variant == 'P', "Only VF3P variant supports multithreading"
    assert num_threads >= 1 and num_threads <= MAX_THREADS, f"Number of threads must be between 1 and {MAX_THREADS}"
    assert variant in VF3_VARIANTS, f"VF3 variant must be one of {VF3_VARIANTS}"
    if variant == 'P':
        assert num_threads > 1, "Parallel version should use more than one thread. Set num_threads accordingly"

    _ensure_graph_correctness(graph)
    _ensure_graph_correctness(subgraph)
    log("Graph correctness checks were passed")

    target_dict, target_labels, target_directed = _process_graph(graph)
    pattern_dict, pattern_labels, pattern_directed = _process_graph(subgraph)
    assert not (target_directed ^ pattern_directed), \
        f"Both graphs must be either directed or undirected"
    directed = target_directed
    log("Graphs were loaded successfully")

    if node_match is not None:
        log("Generating node attributes")
        subgraph_node_attrs, graph_node_attrs = _group_attrs(subgraph.nodes, graph.nodes, node_match, 'node',
                                                             bijective=bijective_for_nodes)
        if graph_node_attrs is None or subgraph_node_attrs is None:
            log("Initial check indicates the absence of solutions")
            return []
        
        use_node_attrs = (len(set(graph_node_attrs.values())) > 1) and (len(set(subgraph_node_attrs.values())) > 1)
        if use_node_attrs:
            target_dict['node_attrs'] = [
                graph_node_attrs[original_label]
                for original_label in target_labels['from_int']
            ]
            pattern_dict['node_attrs'] = [
                subgraph_node_attrs[original_label]
                for original_label in pattern_labels['from_int']
            ]
            log("Node attributes were generated successfully")
        else:
            log("Use of node attributes is redundant")
    else:
        log("Skipping node attributes generation")
        use_node_attrs = False

    if edge_match is not None:
        log("Generating edge attributes")
        subgraph_edge_attrs, graph_edge_attrs = _group_attrs(subgraph.edges, graph.edges, edge_match, 'edge',
                                                             bijective=(bijective_for_nodes and induced))
        if graph_edge_attrs is None or subgraph_edge_attrs is None:
            log("Initial check indicates the absence of solutions")
            return []
        
        use_edge_attrs = (len(set(graph_edge_attrs.values())) > 1) and (len(set(subgraph_edge_attrs.values())) > 1)
        log(f"graph_edge_attrs = {repr(graph_edge_attrs)}")
        log(f"subgraph_edge_attrs = {repr(subgraph_edge_attrs)}")
        if use_edge_attrs:
            target_dict['edge_attrs'] = [
                graph_edge_attrs[target_labels['from_int'][vA], target_labels['from_int'][vB]]
                for vA, vB in target_dict['edges']
            ]
            pattern_dict['edge_attrs'] = [
                subgraph_edge_attrs[pattern_labels['from_int'][vA], pattern_labels['from_int'][vB]]
                for vA, vB in pattern_dict['edges']
            ]
            log("Edge attributes were generated successfully")
        else:
            log("Use of edge attributes is redundant")
    else:
        log("Skipping edge attributes generation")
        use_edge_attrs = False

    log("Loading finished. Entering C++ part...")
    result = VF3_CALLS[variant, use_node_attrs, use_edge_attrs](
        target=target_dict, pattern=pattern_dict,
        directed=directed, all_solutions=all_solutions, verbose=verbose, induced=induced,
        num_threads=num_threads,
    )
    log(f"Returned to Python. Found {len(result)} solutions")
    if not return_integers:
        result = [
            {
                pattern_labels['from_int'][source]: target_labels['from_int'][target]
                for source, target in match_data
            }
            for match_data in result
        ]
        log("Successfully translated solutions to the original node labels")
    return result


# FRONT-END FUNCTIONS
# Exact matches

@_format_docstring
def are_isomorphic(source_graph: GRAPH_TYPE,
                   target_graph: GRAPH_TYPE,
                   get_mapping: bool = False,
                   **kwargs) -> Union[bool, Tuple[bool, Union[Dict, None]]]:
    """Check if two graphs are isomorphic. This includes checks for number of nodes - ``are_isomorphic`` always returns False if two graphs have different number of nodes, as opposed to graph-subgraph isomorphisms.

    Args:
        {FIRST_GRAPH}
        {SECOND_GRAPH} Swap between source_graph <-> target_graph changes nothing.
        {NODE_MATCH}
        {EDGE_MATCH}
        {VARIANT}
        {NUM_THREADS}
        {VERBOSE}

    Returns:
        bool: True if graphs are isomorphic, False - otherwise.
        Also, optionally returns Dict | None. The Dict represents the mapping 'target_graph' labels -> 'source_graph' labels. Returned only if get_mapping set to True.
    """

    isom_list = main_vf3_caller(source_graph,
                                target_graph,
                                bijective_for_nodes=True,
                                all_solutions=False,
                                **kwargs)
    if get_mapping:
        return len(isom_list) > 0, isom_list[0] if len(isom_list) > 0 else None
    else:
        return len(isom_list) > 0


@_format_docstring
def get_exact_isomorphisms(source_graph: GRAPH_TYPE, target_graph: GRAPH_TYPE, **kwargs) -> List[Dict]:
    """Get a list of all isomorphisms between two NetworkX graphs. This includes checks for number of nodes - ``get_exact_isomorphisms`` always returns ``[]`` if two graphs have different number of nodes, as opposed to graph-subgraph isomorphisms.

    Args:
        {FIRST_GRAPH}
        {SECOND_GRAPH} Swap between source_graph <-> target_graph swaps keys with values in the resulting isomorphisms dicts.
        {NODE_MATCH}
        {EDGE_MATCH}
        {RETURN_INTEGERS}
        {VARIANT}
        {NUM_THREADS}
        {VERBOSE}

    Returns:
        List[Dict]: List of source_graph<->target_graph isomorphisms. Each isomorphism is represented by a dict that maps: 'target_graph' labels -> 'source_graph' labels.
    """
    return main_vf3_caller(source_graph, target_graph,
                           bijective_for_nodes=True,
                           all_solutions=True,
                           **kwargs)


@_format_docstring
def get_automorphisms(graph: GRAPH_TYPE, **kwargs) -> List[Dict]:
    """Get isomorphic mappings of NetworkX graph onto itself (automorphism).

    Args:
        {ANY_GRAPH}
        {NODE_MATCH}
        {EDGE_MATCH}
        {RETURN_INTEGERS}
        {VARIANT}
        {NUM_THREADS}
        {VERBOSE}

    Returns:
        List[Dict]: List of graph<->graph isomorphisms (represented as dicts).
    """
    return main_vf3_caller(graph, graph,
                           bijective_for_nodes=True,
                           all_solutions=True,
                           **kwargs)


# FRONT-END FUNCTIONS
# Subgraph matches

@_format_docstring
def has_subgraph(
        subgraph: GRAPH_TYPE, graph: GRAPH_TYPE, get_mapping: bool = False, **kwargs
    ) -> Union[bool, Tuple[bool, Union[Dict, None]]]:
    """Check if `subgraph` is a subgraph of `graph` using VF3 algorithm.

    Args:
        {SUBGRAPH}
        {LARGE_GRAPH}
        {NODE_MATCH}
        {EDGE_MATCH}
        {RETURN_INTEGERS}
        {VARIANT}
        {NUM_THREADS}
        {VERBOSE}

    Returns:
        bool: True if `subgraph` is, indeed, a subgraph of `graph`, False - otherwise.
        Also, optionally returns Dict | None: subgraph->graph isomorphism represented by a dict that maps: 'subgraph' labels -> 'graph' labels. Returned only if get_mapping set to True.
    """
    isom_list = main_vf3_caller(subgraph, graph, all_solutions=False, **kwargs)
    if get_mapping:
        return len(isom_list) > 0, isom_list[0] if len(isom_list) > 0 else None
    else:
        return len(isom_list) > 0


@_format_docstring
def get_subgraph_isomorphisms(subgraph: GRAPH_TYPE, graph: GRAPH_TYPE, **kwargs) -> List[Dict]:
    """Solve subgraph isomorphism problem, i.e. find ways to match nodes of `subgraph` with some/all nodes of `graph`.

    Args:
        {SUBGRAPH}
        {LARGE_GRAPH}
        {NODE_MATCH}
        {EDGE_MATCH}
        {RETURN_INTEGERS}
        {VARIANT}
        {NUM_THREADS}
        {VERBOSE}

    Returns:
        List[Dict]: List of subgraph->graph isomorphisms. Each isomorphism is represented by a dict that maps: 'subgraph' labels -> 'graph' labels.
    """
    return main_vf3_caller(subgraph, graph, all_solutions=True, **kwargs)

@_format_docstring
def has_monomorphic_subgraph(
        subgraph: GRAPH_TYPE, graph: GRAPH_TYPE, get_mapping: bool = False, **kwargs
    ) -> Union[bool, Tuple[bool, Union[Dict, None]]]:
    """Check if `subgraph` is a subgraph of `graph` using VF3 algorithm.

    Args:
        {SUBGRAPH}
        {LARGE_GRAPH}
        {NODE_MATCH}
        {EDGE_MATCH}
        {RETURN_INTEGERS}
        {VARIANT}
        {NUM_THREADS}
        {VERBOSE}

    Returns:
        bool: True if `subgraph` is, indeed, a subgraph of `graph`, False - otherwise.
        Also, optionally returns Dict | None: subgraph->graph isomorphism represented by a dict that maps: 'subgraph' labels -> 'graph' labels. Returned only if get_mapping set to True.
    """

    isom_list = main_vf3_caller(subgraph, graph, induced=False, all_solutions=False, **kwargs)
    if get_mapping:
        return len(isom_list) > 0, isom_list[0] if len(isom_list) > 0 else None
    else:
        return len(isom_list) > 0

@_format_docstring
def get_subgraph_monomorphisms(subgraph: GRAPH_TYPE, graph: GRAPH_TYPE, **kwargs) -> List[Dict]:
    """Solve subgraph monomorphism problem, i.e. find ways to match nodes of `subgraph` with some/all nodes of `graph`.

    Args:
        {SUBGRAPH}
        {LARGE_GRAPH}
        {NODE_MATCH}
        {EDGE_MATCH}
        {RETURN_INTEGERS}
        {VARIANT}
        {NUM_THREADS}
        {VERBOSE}

    Returns:
        List[Dict]: List of subgraph->graph isomorphisms. Each isomorphism is represented by a dict that maps: 'subgraph' labels -> 'graph' labels.
    """
    return main_vf3_caller(subgraph, graph, induced=False, all_solutions=True, **kwargs)
