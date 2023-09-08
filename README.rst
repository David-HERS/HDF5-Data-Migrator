HDF5 Data Migrator
===============================================================================

Overview
_______________________________________________________________________________
The program recursively searches through folders for .dat files and images,
converting them into datasets within an HDF5 file. It utilizes the NumPy
library for data handling and the h5py library for HDF5 file manipulation.

The process involves creating groups in the HDF5 file to mirror the folder
structure, and within these groups, datasets are created containing the
converted file's data. This program aids in organizing and consolidating
various data types into a single HDF5 file, facilitating easier management
and analysis.

Installation via pip
_______________________________________________________________________________
Recommended create a virtual environment, navigate to the root package folder
and run the following command to install:


.. code-block:: bash

    pip install .

Or in developed mode:

.. code-block:: bash

    pip install -e .

Example
_______________________________________________________________________________
You can filter the data using your own criteria and then verify if it is
the correct output:

.. code-block:: python

   import os
   from pathlib import Path
   
   from HDF5Migrator import  HDF5Builder
   
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

Which prints:

.. code:: text

  >>>python ./examples/doc_built_tree.py
  [0]:2022-04-08/
  [1]:├── powers/
  │   [2]:├── 00_5mW/
  │   │   [3]:└── M4_3522_T=21_0K__0_0V__0grados.dat
  │   [2]:├── 01_0mW/
  │   │   [3]:└── M4_3522_T=21_0K__0_0V__0grados.dat
  │   [2]:├── 01_5mW/
  │   │   [3]:└── M4_3522_T=21_0K__0_0V__0grados.dat
  │   [2]:└── Bitacora.txt
  [1]:├── spot/
  [1]:└── temperaturas/
      [2]:├── 100k/
      │   [3]:├── 00_5mW/
      │   [3]:├── 01_5mW/
      │   [3]:└── 09_0mW/
      [2]:├── 23k/
      │   [3]:├── 00_5mW/
      │   [3]:├── 01_5mW/
      │   [3]:└── 09_0mW/
      [2]:├── 50k/
      │   [3]:├── 00_5mW/
      │   [3]:├── 01_5mW/
      │   [3]:└── 09_0mW/
      [2]:└── Bitacora.txt

When you are certain, proceed to create the HDF5 file. You can also use 
the ``criteria_name`` function to filter the directories:

.. code-block:: python

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
   
   paths.h5_file.close()

Which prints:

.. code:: text

  >>>python ./examples/doc_built_hdf5.py
  Oops! Bitacora.txt isn't file for import in hdf5. ()
  Oops! Bitacora.txt isn't file for import in hdf5. ()

If you decide not to close the file, you can continue using it with the
``h5_file`` variable, or you can close the document and reopen 
it using the ``h5py`` library.

Try creating hdf5 files with the example 
`doc_built_hdf5 <./examples/doc_built_hdf5.py>`
