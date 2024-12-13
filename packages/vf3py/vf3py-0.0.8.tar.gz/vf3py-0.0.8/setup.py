PACKAGE_DATA = {'package': 'vf3py', 'module': 'vf3py', 'version': '0.0.8', 'author': 'Nikolai Krivoshchapov', 'platforms': ['Linux'], 'python_versions': '>=3.8.0', 'install_requires': ['numpy', 'networkx'], 'project_summary': 'Interfacing Python and NetworkX with VF3 – the fastest algorithm for graph/subgraph isomorphism calculation', 'project_urls': 'Project-URL: Gitlab home page, https://gitlab.com/knvvv/vf3py\nProject-URL: Docs, https://knvvv.gitlab.io/vf3py', 'readme_content': 'Description-Content-Type: text/markdown\n\n# VF3Py\n\nInterfacing Python and NetworkX with VF3 – the fastest algorithm for graph/subgraph isomorphism calculation.\n\n## Setup\n\nMake sure that your OS is either Linux or Windows. For Linux, you need to have Python >= 3.7. For Windows, you need to have Python >= 3.8.\n\nVF3Py can be installed using this command:\n\n```\npip install vf3py\n```\nTest your installation:\n\n```\n$ python\n>>> import vf3py.test\n>>> vf3py.test.run_tests()\n(...lots of output...)\nOK\n>>> \n```\n\n## Documentation\n\n[![pipeline status](https://gitlab.com/knvvv/vf3py/badges/master/pipeline.svg)](https://gitlab.com/knvvv/vf3py/-/commits/master)\n\nAvailable [here](https://knvvv.gitlab.io/vf3py)\n\n\n## Other projects that use VF3Py\n\nFor now, all projects are mine:\n\n* [algebra_repr](https://gitlab.com/knvvv/algebra_repr) (TODO: come up with a better name) -- uses SageMath to construct finite algebraic structures (groups, rings, fields), then represents them as graphs. Graph isomorphism allows to check if any two algebraic structures are isomorphic or not.\n\n* [PyXYZ](https://gitlab.com/knvvv/pyxyz) -- A Python Library for Molecular Geometry Manipulation. TODO: Use VF3Py to generate automorphisms groups for molecular graphs.\n\n\n## Links\n\n[Gitlab home page](https://gitlab.com/knvvv/vf3py)\n\n[VF3Py PyPi page](https://pypi.org/project/vf3py)\n\n[Original VF3 implementation](https://github.com/MiviaLab/vf3lib)\n\n\n## References\n\n1. Challenging the time complexity of exact subgraph isomorphism for huge and dense graphs with VF3 - Carletti V., Foggia P., Saggese A., Vento M. - IEEE transactions on pattern analysis and machine intelligence - 2018\n2. Introducing VF3: A new algorithm for subgraph isomorphism - Carletti V., Foggia P., Saggese A., Vento M. - International Workshop on Graph-Based Representations in Pattern Recognition - 2017\n3. Comparing performance of graph matching algorithms on huge graphs - Carletti V., Foggia P., Saggese A., Vento M. - Pattern Recognition Letters - 2018\n4. A Parallel Algorithm for Subgraph Isomorphism - V. Carletti, P. Foggia, P. Ritrovato, M. Vento, V. Vigilante - International Workshop on Graph-Based Representations in Pattern Recognition - 2019\n', 'files': '', 'install_requires_lines': 'numpy\nnetworkx', 'platforms_lines': 'Platform: Linux'}
import platform
import glob
import ntpath
import os
import json
import shutil
from setuptools import setup

# OS specifics
CUR_OS = platform.system()
SHAREDOBJ_TEMPLATE = {
    'Windows': ["vf3py_base.cp{py_ver}-win_amd64.pyd", "vf3py_vf3l.cp{py_ver}-win_amd64.pyd", "vf3py_vf3p.cp{py_ver}-win_amd64.pyd"],
    'Linux': ["vf3py_base.cpython-{py_ver}*-x86_64-linux-gnu.so", "vf3py_vf3l.cpython-{py_ver}*-x86_64-linux-gnu.so", "vf3py_vf3p.cpython-{py_ver}*-x86_64-linux-gnu.so"],
}

assert CUR_OS in ['Linux', 'Windows'], "Only Linux and Windows platforms are supported"

if CUR_OS == 'Windows':
    DLLDEPS_JSON = 'win_dlldeps.json'
    DLL_STORAGE_DIR = 'win_dlls'
    assert os.path.isfile(DLLDEPS_JSON), f'Required file "{DLLDEPS_JSON}" not found'

# Python version specifics
python_version_tuple = platform.python_version_tuple()
py_ver = int(f"{python_version_tuple[0]}{python_version_tuple[1]}")

object_names = []
for somask in SHAREDOBJ_TEMPLATE[CUR_OS]:
    so_list = glob.glob(os.path.join('./vf3py', somask.format(py_ver=py_ver)))
    assert len(so_list) == 1
    object_names.append(ntpath.basename(so_list[0]))

for file in glob.glob('./vf3py/*.pyd') + glob.glob('./vf3py/*.so'):
    if ntpath.basename(file) not in object_names:
        os.remove(file)

if CUR_OS == 'Windows':
    assert os.path.isfile(DLLDEPS_JSON), f'Required file "{DLLDEPS_JSON}" not found'

    with open(DLLDEPS_JSON, 'r') as f:
        dlldeps_data = json.load(f)
    
    for object_name in object_names:
        assert object_name in dlldeps_data, f"'{object_name}' is not accounted in {DLLDEPS_JSON}"
        for file in dlldeps_data[object_name]:
            shutil.copy2(os.path.join(DLL_STORAGE_DIR, file), './vf3py')
    
    ADDITIONAL_FILES = ['*.dll']

elif CUR_OS == 'Linux':
    ADDITIONAL_FILES = []

setup(
    name=PACKAGE_DATA['package'],
    version=PACKAGE_DATA['version'],
    author=PACKAGE_DATA['author'],
    python_requires=f'=={python_version_tuple[0]}.{python_version_tuple[1]}.*',
    install_requires=PACKAGE_DATA['install_requires'],
    platforms=PACKAGE_DATA['platforms'],
    packages=[PACKAGE_DATA['package']],
    package_data={'vf3py': ['__init__.py', *object_names, 'cpppart/*.py*', 'test/*.py', 'test/mols/*.sdf', *ADDITIONAL_FILES]}
)
