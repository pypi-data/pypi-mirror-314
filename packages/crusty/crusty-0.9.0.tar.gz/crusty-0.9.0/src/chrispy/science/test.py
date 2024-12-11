


import numpy as np

return_shape = (3, 1544 , 1592)

out_shape  = [46]

array_out = np.zeros((*out_shape, *return_shape[-2:]))

print(array_out.shape)