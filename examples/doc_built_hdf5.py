import os 
from pathlib import Path

from HDF5Migrator import  HDF5Builder
from criterias import criteria_name


CurrentPath = os.path.abspath(__file__)
ExamplePath = Path(CurrentPath).parent /'data' / '2022-04-08'
h5Name = Path(CurrentPath).parent /'hdf5_files' / '2022-04-08'

user_criteria = lambda path: criteria_name(path.name,
        not_in_path=['exp'],
        not_starts=['laser-spectrum', 'potencias-probe'],
        not_ends=['.pdf'], operator='and')

paths = HDF5Builder.make_hdf5(ExamplePath,
                       criteria=user_criteria, depth= 4, name = h5Name, close = False)

#print(paths.h5_keys(), sep = '\n')
paths.h5_file.close()
