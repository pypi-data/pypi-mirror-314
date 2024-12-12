
def keys_same_value(idict: dict):

    from itertools import groupby

    grouped                 = groupby(sorted(idict, key = idict.get), key = idict.get)

    dict_grouped            = {v: list(ks) for v, ks in grouped}

    return dict_grouped


def translate_dict_values(idict: dict, idict_translate: dict):

    idict_translated        = {}

    for k, v in idict.items():
        
        if isinstance(v, list):
            
            idict_translated.update({k: [idict_translate[vv] for vv in v]})

        else:

            idict_translated.update({k: idict_translate[v]})

    return idict_translated


def filter_dict_values(idict, ilist):

    idict_filtered          = {}

    for k, v in idict.items():
        
        if isinstance(v, list):
            
            idict_filtered.update({k: [vv for vv in v if vv in ilist]})

        else:

            if v in ilist:

                idict_filtered.update({k: v})

    return idict_filtered


def filter_dict_keys(idict, ilist):

    idict_filtered          = {k: v for k, v in idict.items() if k in ilist}

    return idict_filtered


def list_to_array(ilist):

    import numpy as np

    array_T                 = np.array(ilist)

    array                   = array_T.T

    return array