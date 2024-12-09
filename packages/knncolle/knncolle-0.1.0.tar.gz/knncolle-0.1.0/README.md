<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/knncolle.svg?branch=main)](https://cirrus-ci.com/github/<USER>/knncolle)
[![ReadTheDocs](https://readthedocs.org/projects/knncolle/badge/?version=latest)](https://knncolle.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/knncolle/main.svg)](https://coveralls.io/r/<USER>/knncolle)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/knncolle.svg)](https://anaconda.org/conda-forge/knncolle)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/knncolle)
-->

[![PyPI-Server](https://img.shields.io/pypi/v/knncolle.svg)](https://pypi.org/project/knncolle/)
[![Monthly Downloads](https://static.pepy.tech/badge/knncolle/month)](https://pepy.tech/project/knncolle)
![Unit tests](https://github.com/knncolle/knncolle-py/actions/workflows/pypi-test.yml/badge.svg)

# Python bindings to knncolle

## Overview

The **knncolle** Python package implements Python bindings to the [C++ library of the same name](https://github.com/knncolle) for nearest neighbor (NN) searches.
Downstream packages can re-use the NN search algorithms in **knncolle**, either via Python or by directly calling C++ through shared pointers.
This is inspired by the [**BiocNeighbors** Bioconductor package](https://bioconductor/packages/BiocNeighbors), which does the same thing for R packages.

## Quick start

Install it:

```shell
pip install knncolle
```

And run the desired search:

```python
# Mocking up data with 20 dimensions, 1000 observations
import numpy
y = numpy.random.rand(20, 1000) 

# Building a search index with vantage point trees:
import knncolle
params = knncolle.VptreeParameters()
idx = knncolle.build_index(params, y)

# Performing the search:
res = knncolle.find_knn(idx, num_neighbors=10)
res.index
res.distance
```

Check out the [reference documentation](https://knncolle.github.io/knncolle-py) for details.

## Switching algorithms

We can easily switch to a different algorithm by just passing a different `params` object.
For example, we could use the [Approximate Nearest Neighbors Oh Yeah](https://github.com/spotify/annoy) (Annoy) algorithm:

```python
an_params = knncolle.AnnoyParameters()
an_idx = knncolle.build_index(an_params, y)
```

We can also tweak the search parameters in our `Parameters` object, during or after construction.
For example, with the [hierarchical navigable small worlds](https://github.com/nmslib/hnswlib) (HNSW) algorithm:

```python
h_params = knncolle.HnswParameters(num_links=20, distance="Manhattan")
h_params.ef_construction = 150
h_idx = knncolle.build_index(h_params, y)
```

Currently, we support Annoy, HNSW, vantage point trees, k-means k-nearest neighbors, and (for testing) an exhaustive brute-force search.
More algorithms can be added by extending **knncolle** as described [below](#extending-to-more-algorithms) without any change to end-user code.

## Other searches 

Given a query dataset, we can find the nearest neighbors in the prebuilt search index:

```python
q = numpy.random.rand(20, 50)
qres = knncolle.query_knn(idx, q, num_neighbors=10)
qres.index
qres.distance
```

We can ask `find_knn()` to report variable numbers of neighbors for each observation:

```python
variable_k = (numpy.random.rand(y.shape[1]) * 10).astype(numpy.uint32)
var_res = knncolle.find_knn(idx, num_neighbors=variable_k)
var_res.index
var_res.distance
```

We can find all observations within a distance threshold of each observation via `find_neighbors()`.
This also supports a variable threshold for each observation as well as querying of observations in a separate dataset.

```python
range_res = knncolle.find_neighbors(idx, threshold=10)
range_res.index
range_res.distance
```

## Use with C++

The raison d'être of the **knncolle** Python package is to enable re-use within ([**pybind11**](https://pybind11.readthedocs.io)-wrapped) C++ code in other Python packages.
The idea is that downstream packages will link against the **knncolle** C++ interface so that they can re-use the search indices created by the **knncolle** Python package.
This allows downstream packages to (i) save time by avoiding the need to re-compile all algorithms and (ii) support more algorithms in **knncolle** extensions.
To do so:

1. Add `assorthead.includes()` to the compiler's include path for your package.
This can be done through `include_dirs=` of the `Extension()` definition in `setup.py`
or by adding a `target_include_directories()` in CMake, depending on your build system.
2. Call `knncolle.build_index()` to construct a `GenericIndex` instance.
This exposes a shared pointer to the C++-allocated index via its `ptr` property.
3. Pass `ptr` to **pybind11**-wrapped C++ code as a [shared pointer to a `knncolle::Prebuilt`](lib/src/def.h),
which can be interrogated as described in the [**knncolle** documentation](https://github.com/knncolle/knncolle).

So, for example, the C++ code in our downstream package might look like this:

```cpp
int do_something(
    const std::shared_ptr<
        knncolle::Prebuilt<uint32_t, uint32_t, double> 
    >& index) 
{
    // Do something with the search index interface.
    return 1;
}

PYBIND11_MODULE(lib_downstream, m) {
    m.def("do_something", &do_something);
}
```

Which can then be called from Python:

```python
from . import lib_downstream as lib
from knncolle import GenericIndex

def do_something(idx: GenericIndex):
    return lib.do_something(idx.ptr)
```

In some scenarios, it may be more convenient to construct the search index inside C++,
e.g., if the dataset to be searched is not available before the call to the C++ function.
This can be accommodated by accepting a [shared pointer to a `knncolle::Builder`](lib/src/def.h) in the C++ code:

```cpp
int do_something_mk2(
    const std::shared_ptr<
        knncolle::Builder<
            knncolle::SimpleMatrix<uint32_t, uint32_t, double>,
            double
        >
    >& builder) 
{
    // The builder is a algorithm-specific factory that accepts a matrix and
    // returns a search index for that algorithm. Presumably we construct a
    // new search index inside this function and use it.
    return 1;
}

PYBIND11_MODULE(lib_downstream, m) {
    m.def("do_something_mk2", &do_something_mk2);
}
```

A pointer to the `knncolle::Builder` is then be created in Python by the `define_builder()` function, and then passed to C++:

```python
from . import lib_downstream as lib
from knncolle import define_builder, Parameters

def do_something(param: Parameters):
    builder, cls = define_builder(param)
    return lib.do_something_mk2(builder.ptr)
```

See also the definitions in [`lib/src/def.h`](lib/src/def.h) for the types of the pointers to be used in the C++ code.

## Extending to more algorithms

### Via `define_builder()`

The best way to extend **knncolle** is to do so in C++.
This involves writing subclasses of the `Builder`, `Prebuilt` and `Searcher` interfaces in the [**knncolle**](https://github.com/knncolle/knncolle) library.
Once this is done, it is a simple matter of writing the following Python bindings:

- Implement a `SomeNewParameters` class that inherits from `Parameters`.
- Implement a `SomeNewIndex` class that inherits from `GenericIndex`.
  This should accept a single `ptr` in its constructor and have a `ptr` property that returns the same value.
- Register a `define_builder()` method that dispatches on `SomeNewParameters`.
  This should call into C++ and return a tuple containing a **pybind11**-wrapped [`BuilderPointer`](lib/src/def.h) and the `SomeNewIndex` constructor.

No new methods are required for `find_knn()`, `build_index()`, etc. as the default method will work automatically if a `define_builder()` method is available.
This approach also allows the new method to be used in C++ code of downstream packages that accept a [`PrebuiltPointer`](lib/src/def.h) instance.

### Without `define_builder()`

If it is not possible to implement the search algorithm in C++, we can still extend **knncolle** in Python.
Each extension package should:

- Implement a `SomeNewParameters` class that inherits from `Parameters`.
- Implement a `SomeNewIndex` class that inherits from `Index`.
  This can have an arbitrary structure, i.e., it does not need to have a `ptr` property.
- Register a `build_index()` method that dispatches on `SomeNewParameters`.
  This should return an instance of `SomeNewIndex`.
- Register a method for any number of these generics: `find_knn()`, `find_distance()`, `find_neighbors()`, `query_knn()`, `query_distance()`, `query_neighbors()`.
  These methods should dispatch on `SomeNewParameters` and return the appropriate result object.

This approach will not support re-use by C++ code in other Python packages.
