import os
from pathlib import Path

from hdf5migrator import  Builder as HDF5Builder

def user_criteria(path):
    return  not (path.name.endswith(".pdf") or 
                path.name.endswith('.jpg') or
                path.name.startswith('laser-spectrum') or 
                path.name.startswith('potencias-probe') or
                'exp' in path.name
                 )

CurrentPath = os.path.abspath(__file__)
ExamplePath = Path(CurrentPath).parent /'data' / '2022-04-08'
paths = HDF5Builder.make_tree(ExamplePath,
                       criteria=user_criteria, depth=3)
for path in paths:
    print(path.displayable())
