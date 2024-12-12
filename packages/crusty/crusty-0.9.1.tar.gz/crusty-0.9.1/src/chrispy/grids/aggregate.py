
def apply(array, axes, method: str):

    """
    Aggregate with the method along the axis
    with the method (e.g. mean, max, mean, variance).
    The method has to be a numpy attribute.
    The given axis dimension(s) will be shrunk.
    """

    import numpy as np

    # find the method in numpy attributes
    method_np           = getattr(np, method)

    # apply the method along given axis
    array_agg           = method_np(array, axis = axes)

    return array_agg


def select_o_apply_d(array, array_sel_4d = None, method_sel = 'argmax', 
                     axis_sel: int = 0, axis_sel_shrink: int = 0, 
                     method_agg_4d: str = 'mean', method_agg_time: str ='mean'):
    
    from my_gridded.aggregate import apply
    from my_gridded.dimensions import select_by_other, select_apply_4d

    var_array_3d                = select_apply_4d(array, sel_func = select_by_other,
                                                    sel_func_args = {'array_sel': array_sel_4d,
                                                        'method': method_sel, 'axis_select': axis_sel,
                                                        'axis_shrink': axis_sel_shrink},
                                                    apply_args = {'axes': axis_sel_shrink,
                                                        'method': method_agg_4d})
    
    var_array_2d                = apply(var_array_3d, axes = 0, method = method_agg_time)

    return var_array_2d
    

