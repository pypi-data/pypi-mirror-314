"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import aidge_core
from functools import reduce

import numpy as np


class test_tensor(unittest.TestCase):
    """Test tensor binding
    """
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_getcoord_getidx(self):
        dims = [2,2,2]
        size = reduce((lambda x, y: x*y), dims)

        np_array = np.arange(size).reshape(dims)

        t = aidge_core.Tensor(np_array)
        for i in range(size):
            coord = t.get_coord(i)
            idx = t.get_idx(coord)
            self.assertEqual(idx, i)

    def test_getavailable_backends(self):
        self.assertTrue("cpu" in aidge_core.Tensor.get_available_backends())

    def test_numpy_int_to_tensor(self):
        np_array = np.arange(9).reshape(1,1,3,3).astype(np.int32)
        # Numpy -> Tensor
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int32)
        for i_t, i_n in zip(t, np_array.flatten()):
            self.assertTrue(i_t == i_n)
        for i,j in zip(t.dims(), np_array.shape):
            self.assertEqual(i,j)
    def test_tensor_int_to_numpy(self):
        np_array = np.arange(9).reshape(1,1,3,3)
        # Numpy -> Tensor
        t = aidge_core.Tensor(np_array)
        # Tensor -> Numpy
        nnarray = np.array(t)
        for i_nn, i_n in zip(nnarray.flatten(), np_array.flatten()):
            self.assertTrue(i_nn == i_n)
        for i,j in zip(t.dims(), nnarray.shape):
            self.assertEqual(i,j)

    def test_numpy_int64_to_tensor(self):
        np_array = np.arange(9).reshape(1,1,3,3).astype(np.int64)
        # Numpy -> Tensor
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int64)
        for i_t, i_n in zip(t, np_array.flatten()):
            self.assertTrue(i_t == i_n)
        for i,j in zip(t.dims(), np_array.shape):
            self.assertEqual(i,j)

    def test_numpy_float_to_tensor(self):
        t = aidge_core.Tensor()
        np_array = np.random.rand(1, 1, 3, 3).astype(np.float32)
        # Numpy -> Tensor
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.float32)
        for i_t, i_n in zip(t, np_array.flatten()):
            self.assertTrue(i_t == i_n) # TODO : May need to change this to a difference
        for i,j in zip(t.dims(), np_array.shape):
            self.assertEqual(i,j)

    def test_get_set(self):
        dims = [2,2,2]

        np_array = np.arange(8).reshape(dims).astype(np.int32)
        # Numpy -> Tensor
        t = aidge_core.Tensor(np_array)
        for i in range(8):
            self.assertEqual(t[i], i)
            t[i] = 5
            self.assertEqual(t[i], 5)

if __name__ == '__main__':
    unittest.main()
