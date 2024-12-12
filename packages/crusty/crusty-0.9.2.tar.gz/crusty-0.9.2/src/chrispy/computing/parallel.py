
from mpi4py import MPI
from typing import Callable, Any
import numpy as np
import os

from my_.data.templates import gridded_data
from my_.files.netcdf import nc_open, variables_to_dict
from my_.files.handy import check_file_exists

def pixel_wise(func: Callable,
               variables: list[str],
               variables_out: list[str],
               data: dict | None = None,
               files: None | str = None,
               file_out: None | str = None,
               dtype: str = 'float32',
               year_start: int | None = None,
               year_end: int | None = None,
               return_shape: int | list[int] = 1,
               return_dims: str | list[str] = 'time',
               *args, **kwargs) -> Any:
    
    if check_file_exists(file_out): return

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    print(f'Rank {rank} out of {size} active.')

    comm.Barrier()

    if rank == 0:

        print(f'Rank {rank} is loading the data...')
        
        if (data is None) and (files is None):
            NotImplementedError('No dataset supplied...')
        
        if data is not None:

            data_ = gridded_data(**data)

            arrays = data_.get_values(variables_ = variables,
                                      y0 = year_start,
                                      y1 = year_end,
                                      dtype = dtype)
            
        if files is not None:

            data_ = nc_open(files)

            arrays = variables_to_dict(data = data_,
                                       variables = variables,
                                       dtype = dtype)

        shapes = {v: arrays[v].shape for v in variables}

        if isinstance(return_shape, int): return_shape = [return_shape]

        arrays_out = {v: np.empty([*return_shape, *shapes[variables[0]][-2:]],
                                   dtype = dtype) 
                                   for v in variables_out}
        
        for v in variables_out: arrays_out[v][:] = np.nan     

    elif rank != 0:

        print(f'Rank {rank} creating empty objects...')

        shapes = None

    shapes = comm.bcast(shapes, root = 0)
                                   

    if rank != 0:

        print(f'I am rank {rank} and I know the shapes: {shapes}.')
        print('Creating empty arrays...')

        arrays_recv = {v: np.empty(shapes[v][:-2], 
                                   dtype = dtype) 
                                   for v in variables}

                                   
    comm.Barrier()


    print(f'I am rank {rank}. Ready for sending / receiving and calculations.')

    range_y = np.arange(shapes[variables[0]][-2])
    range_x = np.arange(shapes[variables[0]][-1])
    grid = np.array(np.meshgrid(range_y, range_x))
    cells = grid.T.reshape(-1, 2)
    length = len(cells)
    perrank = length // (size - 1)
    resid = length - perrank * (size - 1)

    for yx in range(perrank):
    
        if rank == 0:

            for r in range(1, size):

                r_n = (size - 1) * yx + (r - 1)
                y = cells[r_n][0]
                x = cells[r_n][1]

                arrays_yx = {v: arrays[v][..., y, x] for v in variables}

                print(f'Rank {rank} sending cell {r_n} corresponding to')
                print(f'grid indices {x}, {y} to rank {r}.')

                for v, array in arrays_yx.items(): 

                    comm.Send(np.ascontiguousarray(array), 
                              dest = r, 
                              tag = yx)

                print(f'Rank {rank} succesfully sent data to rank {r}.')
            
            for r in range(1, size):

                r_n = (size - 1) * yx + (r - 1)
                y = cells[r_n][0]
                x = cells[r_n][1]

                print(f'Rank {rank} receiving func {func.__name__} output')
                print(f'from grid indices {x}, {y} to rank {r}.')

                return_object = comm.recv(source = r, tag = yx)

                print(f'Rank {rank} received function output from rank {r},')
                print(f'from grid indices {x}, {y} to rank {r}.')

                for v in variables_out:

                    arrays_out[v][..., y, x] = return_object[v]

                    
        if rank != 0:

            r_m = (size - 1) * yx + (rank - 1)
            y = cells[r_m][0]
            x = cells[r_m][1]

            print(f'Rank {rank} receiving cell {r_m} corresponding to')
            print(f'grid indices {x}, {y} from rank 0.')

            for v in variables: comm.Recv(arrays_recv[v], source = 0, tag = yx)

            print(f'Rank {rank} received cell {r_m}.')
            print(f'Now executing function {func.__name__}...')

            out_func = func(arrays_recv, *args, **kwargs)

            print(f'Rank {rank} executed function for grid indices {x}, {y}.')
            print(f'Sending back the output to rank 0...')

            comm.send(out_func, dest = 0, tag = yx)
            
            print(f'Rank {rank} succesfully sent function output')
            print(f'for grid indices {x}, {y} to rank 0.')
    

    comm.Barrier()


    if (resid != 0) and (rank <= resid):

        print(f'Rank {rank} starting residual loop.')

        if rank == 0:
        
            for r in range(1, resid + 1):

                y = cells[-r][0]
                x = cells[-r][1]

                arrays_yx = {v: arrays[v][..., y, x] for v in variables}

                print(f'Rank {rank} sending cell {-r} corresponding to')
                print(f'grid indices {x}, {y} to rank {r}.')

                for v, array in arrays_yx.items(): 

                    comm.Send(np.ascontiguousarray(array),
                              dest = r, 
                              tag = yx)

                print(f'Rank {rank} succesfully sent data to rank {r}.')

            for r in range(1, resid + 1):

                y = cells[-r][0]
                x = cells[-r][1]

                print(f'Rank {rank} receiving func {func.__name__} output')
                print(f'from grid indices {x}, {y} to rank {r}.')

                return_object = comm.recv(source = r, tag = yx)

                print(f'Rank {rank} received function output from rank {r},')
                print(f'from grid indices {x}, {y} to rank {r}.')

                for v in variables_out:

                    arrays_out[v][..., y, x] = return_object[v]


        if rank != 0:

            y = cells[-rank][0]
            x = cells[-rank][1]

            print(f'Rank {rank} receiving cell {-rank} corresponding to')
            print(f'grid indices {x}, {y} from rank 0.')
            
            for v in variables: comm.Recv(arrays_recv[v], source = 0, tag = yx)

            print(f'Rank {rank} received cell {-rank}.')
            print(f'Now executing function {func.__name__}...')

            out_func = func(arrays_recv, *args, **kwargs)

            print(f'Rank {rank} executed function for grid indices {x}, {y}.')
            print(f'Sending back the output to rank 0...')

            comm.send(out_func, dest = 0, tag = yx)
            
            print(f'Rank {rank} succesfully sent function output')
            print(f'for grid indices {x}, {y} to rank 0.')


    comm.Barrier()


    if rank == 0:


        if file_out is not None:

            import xarray as xr

            if isinstance(return_dims, str): return_dims = [return_dims]

            out_vars = {v: ([*return_dims, 'lat', 'lon'], arrays_out[v]) for v in variables_out}

            DS_out = xr.Dataset(data_vars = out_vars)

            print('Now wrinting DS to netcdf...')

            DS_out.to_netcdf(path = file_out, mode='w')

            print('Script was successful! Bye bye!')
    
        else:
    
            print('Script was successful! Bye bye!')
    
            return arrays_out


def along_dim(func: Callable,
              dim: int,
              variables: list[str],
              variables_out: list[str],
              data: dict | None = None,
              files: str | None = None,
              file_out: None | str = None,
              dtype: str = 'float32',
              year_start: int | None = None,
              year_end: int | None = None,
              return_dims: str | list[str] = 'time',
              *args, **kwargs) -> Any:

    if check_file_exists(file_out): return

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    print(f'Rank {rank} out of {size} active.')

    comm.Barrier()

    if rank == 0:

        print(f'Rank {rank} is loading the data...')
        
        if (data is None) and (files is None):
            NotImplementedError('No dataset supplied...')
        
        if data is not None:

            data_ = gridded_data(**data)

            arrays = data_.get_values(variables_ = variables,
                                      y0 = year_start,
                                      y1 = year_end,
                                      dtype = dtype)
            
        if files is not None:

            data_ = nc_open(files)

            arrays = variables_to_dict(data = data_,
                                       variables = variables,
                                       dtype = dtype)

        shapes = {v: arrays[v].shape for v in variables}

        arrays_out = {v: np.empty([*shapes[v]],
                                   dtype = dtype) 
                                   for v in variables_out}
        
        for v in variables_out: arrays_out[v][:] = np.nan     

    elif rank != 0:

        print(f'Rank {rank} creating empty objects...')

        shapes = None

    shapes = comm.bcast(shapes, root = 0)
                                   

    if rank != 0:

        print(f'I am rank {rank} and I know the shapes: {shapes}.')
        print('Creating empty arrays...')

        arrays_recv = {v: np.empty(shapes[v][:dim] +  
                                   shapes[v][dim + 1:],
                                   dtype = dtype) 
                                   for v in variables}

                                   
    comm.Barrier()


    print(f'I am rank {rank}. Ready for sending / receiving and calculations.')

    length = shapes[variables[0]][dim]
    ndims = len(shapes[variables[0]])
    
    perrank = length // (size - 1)
    resid = length - perrank * (size - 1)

    for idx in range(perrank):
    
        if rank == 0:

            for r in range(1, size):

                r_n = (size - 1) * idx + (r - 1)
                
                slx = [slice(0, None)] * ndims
                slx[dim] = r_n
                slx = tuple(slx)

                arrays_yx = {v: arrays[v][slx] for v in variables}

                print(f'Rank {rank} sending cell {r_n} corresponding to')
                print(f'dimension {dim}, index {r_n} to rank {r}.')

                for v, array in arrays_yx.items(): 

                    comm.Send(np.ascontiguousarray(array), 
                              dest = r, 
                              tag = idx)

                print(f'Rank {rank} succesfully sent data to rank {r}.')
            
            for r in range(1, size):

                r_n = (size - 1) * idx + (r - 1)

                slx = [slice(0, None)] * ndims
                slx[dim] = r_n
                slx = tuple(slx)

                print(f'Rank {rank} receiving func {func.__name__} output')
                print(f'dimension {dim}, index {r_n} from rank {r}.')

                return_object = comm.recv(source = r, tag = idx)

                print(f'Rank {rank} received function output from rank {r},')
                print(f'dimension {dim}, index {r_n} from rank {r}.')

                for v in variables_out:

                    arrays_out[v][slx] = return_object[v]

                    
        if rank != 0:

            r_m = (size - 1) * idx + (rank - 1)

            print(f'Rank {rank} receiving cell {r_m} corresponding to')
            print(f'dimension {dim}, index {r_m} from rank 0.')

            for v in variables: comm.Recv(arrays_recv[v], source = 0, tag = idx)

            print(f'Rank {rank} received cell {r_m}.')
            print(f'Now executing function {func.__name__}...')

            out_func = func(arrays_recv, *args, **kwargs)

            print(f'Rank {rank} executed function for dimension {dim}, index {r_m}.')
            print(f'Sending back the output to rank 0...')

            comm.send(out_func, dest = 0, tag = idx)
            
            print(f'Rank {rank} succesfully sent function output')
            print(f'dimension {dim}, index {r_m} to rank 0.')
    

    comm.Barrier()

    if (resid != 0) and (rank <= resid):

        print(f'Rank {rank} starting residual loop.')

        if rank == 0:
        
            for r in range(1, resid + 1):
                
                slx = [slice(0, None)] * ndims
                slx[dim] = -r
                slx = tuple(slx)

                arrays_yx = {v: arrays[v][slx] for v in variables}

                print(f'Rank {rank} sending cell {-r} corresponding to')
                print(f'dimension {dim}, index {-r} to rank {r}.')

                for v, array in arrays_yx.items(): 

                    comm.Send(np.ascontiguousarray(array),
                              dest = r, 
                              tag = r)

                print(f'Rank {rank} succesfully sent data to rank {r}.')

            for r in range(1, resid + 1):

                slx = [slice(0, None)] * ndims
                slx[dim] = -r
                slx = tuple(slx)

                print(f'Rank {rank} receiving func {func.__name__} output')
                print(f'dimension {dim}, index {-r} from rank {r}.')

                return_object = comm.recv(source = r, tag = r)

                print(f'Rank {rank} received function output from rank {r},')
                print(f'dimension {dim}, index {-r} from rank {r}.')

                for v in variables_out:

                    arrays_out[v][slx] = return_object[v]


        if rank != 0:

            print(f'Rank {rank} receiving cell {-rank} corresponding to')
            print(f'dimension {dim}, index {-rank} from rank 0.')
            
            for v in variables: comm.Recv(arrays_recv[v], source = 0, tag = rank)

            print(f'Rank {rank} received cell {-rank}.')
            print(f'Now executing function {func.__name__}...')

            out_func = func(arrays_recv, *args, **kwargs)

            print(f'Rank {rank} executed function for dimension {dim}, index {-rank}.')
            print(f'Sending back the output to rank 0...')

            comm.send(out_func, dest = 0, tag = rank)
            
            print(f'Rank {rank} succesfully sent function output')
            print(f'for dimension {dim}, index {-rank} to rank 0.')


    comm.Barrier()


    if rank == 0:


        if file_out is not None:

            import xarray as xr

            if isinstance(return_dims, str): return_dims = [return_dims]

            out_vars = {v: ([*return_dims, 'lat', 'lon'], arrays_out[v]) for v in variables_out}

            DS_out = xr.Dataset(data_vars = out_vars)

            print('Now wrinting DS to netcdf...')

            DS_out.to_netcdf(path = file_out, mode = 'w', format = 'NETCDF4_CLASSIC')

            print('Script was successful! Bye bye!')
    
        else:
    
            print('Script was successful! Bye bye!')
    
            return arrays_out




if __name__ == '__main__':

    from my_.science.anomalies import standard_index

    pixel_wise(func = standard_index,
               variables = ['QFLX_EVAP_GRND'],
               variables_out = ['SXI_ET_GRND'],
               files =  '/p/scratch/cjibg31/jibg3105/data/CLM5EU3/006/join_8d/*.nc',
               file_out = 'SXI_ET_GRND.nc',
               return_shape = 46*24,
               return_dims = 'time',
               year_start = 1995,
               year_end = 1997)