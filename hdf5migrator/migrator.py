"""HDF5-Data-Migrator"""

from pathlib import Path

import h5py
import numpy as np
from PIL import Image


class Builder(object):
    """Directory tree Structure
    """
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last,
            h5_file = None, h5_objects = None):
        self.path = Path(str(path))
        self.parent = parent_path
        self.children = ''
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0
        
        #For make_hdf5 method 
        self.h5_file = None #For file (root node)
        self.h5_objects = None #For groups and datasets  (intermediate nodes)
        self.data_criteria = self.__default_criteria
        self.object_criteria = self.__default_criteria

            
    #Build a list for folders and data that will migrated to HDF5
    @classmethod
    def make_tree(cls, root, parent = None, is_last=False, 
                  criteria=None, depth = 2):
        """
        make_tree(root, criteria=user_criteria, depth=user_depth)
        Create a tree directories with criteria implemetend
        
        Parameters
        ---------------------------------------------------------------------- 
        root: str
              Root folder.
        parent: None
                Parent Folder.
        is_last: False
                 flag to recursive method.
        criteria: Function
                  or method like user_criteria(path) with return bool value.
        depth: int
               Depth limit counted root as depth=0
                
        Returns
        ---------------------------------------------------------------------- 
        class object: HDF5Builder object
        
                      For print tree use the object method 'displayable'
                      path in paths:
                      for path in paths:
                          print(path.displayable())


        References
        ----------------------------------------------------------------------  
        abstrus's-https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
        """
        root = Path(str(root))
        criteria = criteria or cls.__default_criteria

        displayable_root = cls(root, parent, is_last)
        displayable_root.children = sorted(list(path for path in root.iterdir()
                            if criteria(path)), key=lambda s: str(s).lower())
        
        yield displayable_root

        count = 1
        if displayable_root.depth < depth: 
            for path in displayable_root.children:
                is_last = count == len(displayable_root.children)
                if path.is_dir():
                    yield from cls.make_tree(path, parent=displayable_root,
                                             is_last=is_last, criteria=criteria,
                                             depth= depth)
                else:
                    yield cls(path, displayable_root, is_last)
                count += 1
        else:
            None
 
    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name
    
    @property
    def name(self):
        if self.path.is_dir():
            return self.path.name
        return self.path.name


    def displayable(self):
        if self.parent is None:
            return '['+str(self.depth)+ ']:' + self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(
            '['+str(self.depth)+ ']:'
            +_filename_prefix,
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent
        
        return ''.join(reversed(parts))
    
    @classmethod
    def __default_criteria(cls, path):
        return True
    
    #Create a hdf5 file with extension *.h5
    @classmethod
    def make_hdf5(cls, root, depth = 5, parent=None, is_last=False,
                  criteria=None, group = None, name = '', close = True):
        """
        make_hdf5(root, criteria=user_criteria, depth=user_depth,
                name=user_name, close=True)
        Create a tree directories with criteria implemetend
        
        Parameters
        ----------------------------------------------------------------------  
        root: str
              Root folder.
        parent: None
                Parent Folder.
        is_last: False
                 flag to recursive method.
        criteria: Function
                  or method like user_criteria(path) with return bool value.
        depth: int
               Depth limit counted root as depth=0
        name: str
              hdf5 name, if you use the string './dir1/dir2/.../file'
              imports file.h5 in the respective path.
        close: bool
               For close the h5 file.

                
        Returns
        ---------------------------------------------------------------------- 
        class object: HDF5Builder object

                      If you use close = False, you can use the attribute h5_file.
                      if close = True you must use h5py library to read h5 file created
        file: H5 File 
        """
       
        root = Path(str(root))
        criteria = criteria or cls.__default_criteria
        hdf5_file = cls(str(root), parent, is_last)
        
        if hdf5_file.parent is None:
            hdf5_file.h5_file = h5py.File("{!s}.h5".format(name or 
                                                             root.name), "w")
            group = hdf5_file.h5_file
        
        hdf5_file.children = sorted(list(path for path in root.iterdir() 
                            if criteria(path)),key=lambda s: str(s).lower())
        
        hdf5_file.h5_objects = [None]*len(hdf5_file.children)
        
        count = 1
        if hdf5_file.depth < depth: 
            for path in hdf5_file.children:
                is_last = count == len(hdf5_file.children)
                if path.is_dir():
                    hdf5_file.h5_objects[count-1] = group.create_group(path.name)

                    #Children works as container of  hdf5.h5_objects
                    hdf5_file.children[count-1] =  hdf5_file.make_hdf5(path,
                             parent= hdf5_file, is_last=is_last, criteria=criteria,
                            group = hdf5_file.h5_objects[count-1], depth = depth)

                elif path.is_file():
                    if path.name.endswith('.dat'):
                        comments = ('0001:AREA1:1-Channel(X)',
                                '#',
                                )
                        dat=np.loadtxt(path, comments = comments)
                        # hdf5_file.dsets[count-1] = group.create_dataset(path.name[:-4], data = dat)
                        #adding .dat to name is more easier to indentify datasets
                        hdf5_file.h5_objects[count-1] = group.create_dataset(path.name[:], data = dat)
                    elif    (
                            path.name.endswith('.png')
                            or path.name.endswith('.jpg')
                            or path.name.endswith('.jpeg')
                            ):
                        img = Image.open(path)
                        img_data = np.array(img)
                        hdf5_file.h5_objects[count-1] = group.create_dataset(path.name[:], data = img_data)
                    else:
                        print("Oops! {!s} isn't file for import in hdf5. ()".format(path.name))
                        hdf5_file.h5_objects[count-1] = None

                count += 0

        if hdf5_file.parent is None and close:
            hdf5_file.h5_file.close()
        return hdf5_file
    
    @property
    def data_criteria(self):
        return self._data_criteria

    @data_criteria.setter
    def data_criteria(self, criteria):
        self._data_criteria= criteria
        
    @property
    def object_criteria(self):
        return self._object_criteria

    @object_criteria.setter
    def object_criteria(self, criteria):
        self._object_criteria = criteria
        
    def h5_keys(self, data_criteria = None, object_criteria = None, deep = 10):
        """Return names of the h5_obj with criteria name and object"""
        
        def __all_keys(h5_obj, deep = deep):
            "Recursively find all keys in an h5py.Group."
            keys = (h5_obj.name,)
            deep  = abs(deep) #for bool(0jj)
            if isinstance(h5_obj, h5py.Group) and bool(deep):
                deep -= 1
                for key, value in h5_obj.items():
                    if isinstance(value, h5py.Group):
                        keys = keys + __all_keys(value, deep)
                        #deep-=1
                    elif isinstance(value, h5py.Dataset):
                        #deep-=1
                        keys = keys + (value.name,)
            else:
                #print("Incorrect HDF5 object or deep limit achieved")
                None
            return keys

        def __default_criteria(path):
            return True

        if isinstance(self, h5py.File):
            h5_obj = self.get('/')
            object_criteria = object_criteria or __default_criteria
            data_criteria = data_criteria or __default_criteria
        elif isinstance(self, h5py.Group):
            h5_obj = self
            object_criteria = object_criteria or __default_criteria
            data_criteria = data_criteria or __default_criteria
        else:
            h5_obj = self.h5_file.get('/') #the root group of the file
            object_criteria = object_criteria or self.object_criteria
            data_criteria = data_criteria or self.data_criteria
            
        names = __all_keys(h5_obj, deep = deep)
        names_criteria = [name for name in names 
                if object_criteria(h5_obj.get(name)) and data_criteria(name)]
        return names_criteria
   
