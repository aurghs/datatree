import numpy as np
import xarray as xr

from datatree import DataTree
from datatree.testing import assert_equal

from .test_datatree import create_test_datatree


class TestDSMethodInheritance:
    def test_dataset_method(self):
        ds = xr.Dataset({"a": ("x", [1, 2, 3])})
        dt = DataTree("root", data=ds)
        DataTree("results", parent=dt, data=ds)

        expected = DataTree("root", data=ds.isel(x=1))
        DataTree("results", parent=expected, data=ds.isel(x=1))

        result = dt.isel(x=1)
        assert_equal(result, expected)

    def test_reduce_method(self):
        ds = xr.Dataset({"a": ("x", [False, True, False])})
        dt = DataTree("root", data=ds)
        DataTree("results", parent=dt, data=ds)

        expected = DataTree("root", data=ds.any())
        DataTree("results", parent=expected, data=ds.any())

        result = dt.any()
        assert_equal(result, expected)

    def test_nan_reduce_method(self):
        ds = xr.Dataset({"a": ("x", [1, 2, 3])})
        dt = DataTree("root", data=ds)
        DataTree("results", parent=dt, data=ds)

        expected = DataTree("root", data=ds.mean())
        DataTree("results", parent=expected, data=ds.mean())

        result = dt.mean()
        assert_equal(result, expected)

    def test_cum_method(self):
        ds = xr.Dataset({"a": ("x", [1, 2, 3])})
        dt = DataTree("root", data=ds)
        DataTree("results", parent=dt, data=ds)

        expected = DataTree("root", data=ds.cumsum())
        DataTree("results", parent=expected, data=ds.cumsum())

        result = dt.cumsum()
        assert_equal(result, expected)


class TestOps:
    def test_binary_op_on_int(self):
        ds1 = xr.Dataset({"a": [5], "b": [3]})
        ds2 = xr.Dataset({"x": [0.1, 0.2], "y": [10, 20]})
        dt = DataTree("root", data=ds1)
        DataTree("subnode", data=ds2, parent=dt)

        expected = DataTree("root", data=ds1 * 5)
        DataTree("subnode", data=ds2 * 5, parent=expected)

        result = dt * 5
        assert_equal(result, expected)

    def test_binary_op_on_dataset(self):
        ds1 = xr.Dataset({"a": [5], "b": [3]})
        ds2 = xr.Dataset({"x": [0.1, 0.2], "y": [10, 20]})
        dt = DataTree("root", data=ds1)
        DataTree("subnode", data=ds2, parent=dt)
        other_ds = xr.Dataset({"z": ("z", [0.1, 0.2])})

        expected = DataTree("root", data=ds1 * other_ds)
        DataTree("subnode", data=ds2 * other_ds, parent=expected)

        result = dt * other_ds
        assert_equal(result, expected)

    def test_binary_op_on_datatree(self):
        ds1 = xr.Dataset({"a": [5], "b": [3]})
        ds2 = xr.Dataset({"x": [0.1, 0.2], "y": [10, 20]})
        dt = DataTree("root", data=ds1)
        DataTree("subnode", data=ds2, parent=dt)

        expected = DataTree("root", data=ds1 * ds1)
        DataTree("subnode", data=ds2 * ds2, parent=expected)

        result = dt * dt
        assert_equal(result, expected)


class TestUFuncs:
    def test_tree(self):
        dt = create_test_datatree()
        expected = create_test_datatree(modify=lambda ds: np.sin(ds))
        result_tree = np.sin(dt)
        assert_equal(result_tree, expected)
