def run_tests():
    from .basic_graphs import main as f_basic_graphs
    from .edge_test import main as f_edge_attrs
    from .mol_isoms import main as f_molecular
    from .mono import main as f_mono
    from .mono_random import main as f_mono_random

    TEST_FUNCTIONS = {
        'basic_graphs': f_basic_graphs,
        'edge_attrs': f_edge_attrs,
        'molecular': f_molecular,
        'monomorphism': f_mono,
        # 'random monomorphism': f_mono_random,
    }

    for function_name, function in TEST_FUNCTIONS.items():
        print(f"=== Running test '{function_name}' ===")
        function()
    
    print("OK")


if __name__ == "__main__":
    run_tests()
