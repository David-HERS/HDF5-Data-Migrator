"""Criteria definitons for create hdf5 files and filter data"""
import numpy as np
import h5py

def is_dataset(h5_object):
    return isinstance(h5_object, h5py.Dataset)


def is_group(h5_object):
    return isinstance(h5_object, h5py.Group)

def criteria_name(
        path, in_path=[] , not_in_path=[],
        starts = [], ends = [], not_starts = [], not_ends = [],
        operator = 'and'):
    """
    """
    if operator == 'and':
        operator= np.prod
    elif operator == 'or':
        operator= np.sum
    else:
        operator= np.sum

    if in_path:
        __in_path = bool(operator(np.array(
            [(include in path) for include in in_path])))
    else: __in_path = True
    if starts:
        __starts = bool(operator(np.array(
            [path.startswith(criteria) for criteria in starts])))
    else: __starts = True
    if ends:
        __ends =  bool(operator(np.array(
            [path.endswith(criteria) for criteria in ends])))
    else: __ends = True
    if not_in_path:
        __not_in_path = bool(operator(np.array(
            [not(not_inc in path) for not_inc in not_in_path])))
    else: __not_in_path = True
    if not_starts:
        __not_starts = bool(operator(np.array(
            [not(path.startswith(criteria)) for criteria in not_starts])))
    else: __not_starts = True 
    if not_ends:
        __not_ends =  bool(operator(np.array(
            [not(path.endswith(criteria)) for criteria in not_ends])) )
    else: __not_ends = True 
    
    satisfy = (__in_path and __not_in_path and  __starts and  __not_starts
            and __ends and __not_ends)
    return satisfy

