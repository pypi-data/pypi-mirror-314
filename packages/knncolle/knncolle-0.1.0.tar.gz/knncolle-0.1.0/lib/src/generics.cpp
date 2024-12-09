#include "def.h"
#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"
#include "pybind11/stl.h"

#include <algorithm>
#include <cstdint>
#include <optional>

typedef pybind11::array_t<double, pybind11::array::f_style | pybind11::array::forcecast> DataMatrix;

PrebuiltPointer generic_build(const BuilderPointer& builder, const DataMatrix& data) {
    auto buffer = data.request();
    uint32_t NR = buffer.shape[0], NC = buffer.shape[1];
    return PrebuiltPointer(builder->build_raw(SimpleMatrix(NR, NC, static_cast<const double*>(buffer.ptr))));
}

uint32_t generic_num_obs(const PrebuiltPointer& prebuilt) {
    return prebuilt->num_observations();
}

uint32_t generic_num_dims(const PrebuiltPointer& prebuilt) {
    return prebuilt->num_dimensions();
}

/*********************************
 ********* KNN functions *********
 *********************************/

template<typename Value_>
using OutputMatrix = pybind11::array_t<Value_, pybind11::array::c_style>;

template<typename Value_>
Value_* prepare_output(OutputMatrix<Value_>& mat, bool report, uint32_t k, uint32_t nobs) {
    if (report) {
        mat = OutputMatrix<Value_>({ nobs, k });
        return static_cast<Value_*>(mat.request().ptr);
    } else {
        return NULL;
    }
}

template<typename Value_>
pybind11::list format_range_output(const std::vector<std::vector<Value_> >& results) {
    pybind11::list output(results.size());
    for (size_t r = 0, end = results.size(); r < end; ++r) {
        output[r] = pybind11::array_t<Value_>(results[r].size(), results[r].data());
    }
    return output;
}

typedef pybind11::array_t<uint32_t, pybind11::array::f_style | pybind11::array::forcecast> NeighborVector;

typedef pybind11::array_t<uint32_t, pybind11::array::f_style | pybind11::array::forcecast> ChosenVector;

pybind11::object generic_find_knn(
    const PrebuiltPointer& prebuilt,
    const NeighborVector& num_neighbors,
    bool force_variable_neighbors,
    std::optional<ChosenVector> chosen,
    int num_threads,
    bool last_distance_only,
    bool report_index,
    bool report_distance)
{
    uint32_t nobs = prebuilt->num_observations();

    // Checking if we have to handle subsets.
    uint32_t num_output = nobs;
    const uint32_t* subset_ptr = NULL;
    if (chosen.has_value()) {
        const auto& subset = *chosen;
        num_output = subset.size();
        for (uint32_t i = 0; i < num_output; ++i) {
            auto s = subset.at(i);
            if (s < 0 || s >= nobs) {
                throw std::runtime_error("'subset' contains out-of-range indices");
            } 
        }
        subset_ptr = static_cast<const uint32_t*>(subset.request().ptr);
    }

    // Checking that the 'k' is valid.
    auto sanitize_k = [&](int k) -> int {
        if (k < nobs) {
            return k;
        }
        //Rcpp::warning("'k' capped at the number of observations minus 1");
        if (nobs >= 1) {
            return nobs - 1;
        } else {
            return 0;
        }
    };

    bool is_k_variable = false;
    uint32_t const_k = 0;
    std::vector<uint32_t> variable_k;
    if (num_neighbors.size() != 1 || force_variable_neighbors) {
        is_k_variable = true;
        if (static_cast<uint32_t>(num_neighbors.size()) != num_output) {
            throw std::runtime_error("length of 'k' must be equal to the number of points in the index or 'subset'");
        }
        variable_k.resize(num_output);
        for (uint32_t o = 0; o < num_output; ++o) {
            variable_k[o] = sanitize_k(num_neighbors.at(o));
        }
    } else {
        const_k = sanitize_k(num_neighbors.at(0));
    }

    // Formatting all the possible output containers.
    OutputMatrix<uint32_t> const_i;
    OutputMatrix<double> const_d;
    pybind11::array_t<double> last_d;
    uint32_t* out_i_ptr = NULL; 
    double* out_d_ptr = NULL; 
    std::vector<std::vector<uint32_t> > var_i;
    std::vector<std::vector<double> > var_d;

    if (last_distance_only) {
        last_d = pybind11::array_t<double>(num_output);
        out_d_ptr = static_cast<double*>(last_d.request().ptr);
        report_index = false;
        report_distance = true;

    } else if (is_k_variable) {
        if (report_index) {
            var_i.resize(num_output);
        }
        if (report_distance) {
            var_d.resize(num_output);
        }

    } else {
        out_i_ptr = prepare_output(const_i, report_index, const_k, num_output);
        out_d_ptr = prepare_output(const_d, report_distance, const_k, num_output);
    }

    knncolle::parallelize(num_threads, num_output, [&](int tid, uint32_t start, uint32_t length) {
        auto searcher = prebuilt->initialize();
        std::vector<uint32_t> tmp_i;
        std::vector<double> tmp_d;

        for (uint32_t o = start, end = start + length; o < end; ++o) {
            searcher->search(
                (subset_ptr != NULL ? subset_ptr[o] : o),
                (is_k_variable ? variable_k[o] : const_k),
                (report_index ? &tmp_i : NULL),
                (report_distance ? &tmp_d : NULL)
            );

            if (report_index) {
                if (is_k_variable) {
                    var_i[o].swap(tmp_i);
                } else {
                    size_t out_offset = static_cast<size_t>(o) * static_cast<size_t>(const_k); // using size_t to avoid overflow.
                    std::copy_n(tmp_i.begin(), const_k, out_i_ptr + out_offset); 
                }
            }

            if (report_distance) {
                if (last_distance_only) {
                    out_d_ptr[o] = (tmp_d.empty() ? 0 : tmp_d.back());
                } else if (is_k_variable) {
                    var_d[o].swap(tmp_d);
                } else {
                    size_t out_offset = static_cast<size_t>(o) * static_cast<size_t>(const_k); // using size_t to avoid overflow.
                    std::copy_n(tmp_d.begin(), const_k, out_d_ptr + out_offset); 
                }
            }
        }
    });

    if (last_distance_only) {
        return last_d;

    } else if (is_k_variable) {
        pybind11::tuple output(2);
        if (report_index) {
            output[0] = format_range_output(var_i);
        } else {
            output[0] = pybind11::none();
        }
        if (report_distance) {
            output[1] = format_range_output(var_d);
        } else {
            output[1] = pybind11::none();
        }
        return output;

    } else {
        pybind11::tuple output(2);
        if (report_index) {
            output[0] = const_i;
        } else {
            output[0] = pybind11::none();
        }
        if (report_distance) {
            output[1] = const_d;
        } else {
            output[1] = pybind11::none();
        }
        return output;
    }
} 

pybind11::object generic_query_knn(
    const PrebuiltPointer& prebuilt,
    const DataMatrix& query,
    const NeighborVector& num_neighbors,
    bool force_variable_neighbors,
    int num_threads,
    bool last_distance_only,
    bool report_index,
    bool report_distance)
{
    int nobs = prebuilt->num_observations();
    size_t ndim = prebuilt->num_dimensions();

    auto buf_info = query.request();
    uint32_t nquery = buf_info.shape[1];
    const double* query_ptr = static_cast<const double*>(buf_info.ptr);
    if (static_cast<size_t>(buf_info.shape[0]) != ndim) {
        throw std::runtime_error("mismatch in dimensionality between index and 'query'");
    }

    // Checking that 'k' is valid.
    auto sanitize_k = [&](int k) -> int {
        if (k <= nobs) {
            return k;
        }
        //Rcpp::warning("'k' capped at the number of observations");
        return nobs;
    };

    bool is_k_variable = false;
    uint32_t const_k = 0;
    std::vector<uint32_t> variable_k;
    if (num_neighbors.size() != 1 || force_variable_neighbors) {
        is_k_variable = true;
        if (static_cast<uint32_t>(num_neighbors.size()) != nquery) {
            throw std::runtime_error("length of 'k' must be equal to the number of points in the index or 'subset'");
        }
        variable_k.resize(nquery);
        for (uint32_t o = 0; o < nquery; ++o) {
            variable_k[o] = sanitize_k(num_neighbors.at(o));
        }
    } else {
        const_k = sanitize_k(num_neighbors.at(0));
    }

    // Formatting all the possible output containers.
    OutputMatrix<uint32_t> const_i;
    OutputMatrix<double> const_d;
    pybind11::array_t<double> last_d;
    uint32_t* out_i_ptr = NULL; 
    double* out_d_ptr = NULL; 
    std::vector<std::vector<uint32_t> > var_i;
    std::vector<std::vector<double> > var_d;

    if (last_distance_only) {
        last_d = pybind11::array_t<double>(nquery);
        out_d_ptr = static_cast<double*>(last_d.request().ptr);
        report_index = false;
        report_distance = true;

    } else if (is_k_variable) {
        if (report_index) {
            var_i.resize(nquery);
        }
        if (report_distance) {
            var_d.resize(nquery);
        }

    } else {
        out_i_ptr = prepare_output(const_i, report_index, const_k, nquery);
        out_d_ptr = prepare_output(const_d, report_distance, const_k, nquery);
    }

    knncolle::parallelize(num_threads, nquery, [&](int tid, uint32_t start, uint32_t length) {
        auto searcher = prebuilt->initialize();
        std::vector<uint32_t> tmp_i;
        std::vector<double> tmp_d;

        size_t query_offset = static_cast<size_t>(start) * ndim; // using size_t to avoid overflow.
        for (uint32_t o = start, end = start + length; o < end; ++o, query_offset += ndim) {
            searcher->search(
                query_ptr + query_offset,
                (is_k_variable ? variable_k[o] : const_k),
                (report_index ? &tmp_i : NULL),
                (report_distance ? &tmp_d : NULL)
            );

            if (report_index) {
                if (is_k_variable) {
                    var_i[o].swap(tmp_i);
                } else {
                    size_t out_offset = static_cast<size_t>(o) * static_cast<size_t>(const_k); // using size_t to avoid overflow.
                    std::copy_n(tmp_i.begin(), const_k, out_i_ptr + out_offset); 
                }
            }

            if (report_distance) {
                if (last_distance_only) {
                    out_d_ptr[o] = (tmp_d.empty() ? 0 : tmp_d.back());
                } else if (is_k_variable) {
                    var_d[o].swap(tmp_d);
                } else {
                    size_t out_offset = static_cast<size_t>(o) * static_cast<size_t>(const_k); // using size_t to avoid overflow.
                    std::copy_n(tmp_d.begin(), const_k, out_d_ptr + out_offset); 
                }
            }
        }
    });

    if (last_distance_only) {
        return last_d;

    } else if (is_k_variable) {
        pybind11::tuple output(2);
        if (report_index) {
            output[0] = format_range_output(var_i);
        } else {
            output[0] = pybind11::none();
        }
        if (report_distance) {
            output[1] = format_range_output(var_d);
        } else {
            output[1] = pybind11::none();
        }
        return output;

    } else {
        pybind11::tuple output(2);
        if (report_index) {
            output[0] = const_i;
        } else {
            output[0] = pybind11::none();
        }
        if (report_distance) {
            output[1] = const_d;
        } else {
            output[1] = pybind11::none();
        }
        return output;
    }
}

/***********************************
 ********* Range functions *********
 ***********************************/

typedef pybind11::array_t<double, pybind11::array::f_style | pybind11::array::forcecast> ThresholdVector;

pybind11::object generic_find_all(
    const PrebuiltPointer& prebuilt, 
    std::optional<ChosenVector> chosen,
    const ThresholdVector& thresholds,
    int num_threads,
    bool report_index,
    bool report_distance) 
{
    uint32_t nobs = prebuilt->num_observations();

    uint32_t num_output = nobs;
    const uint32_t* subset_ptr = NULL;
    if (chosen.has_value()) {
        const auto& subset = *chosen;
        num_output = subset.size();
        for (uint32_t i = 0; i < num_output; ++i) {
            auto s = subset.at(i);
            if (s < 0 || s >= nobs) {
                throw std::runtime_error("'subset' contains out-of-range indices");
            } 
        }
        subset_ptr = static_cast<const uint32_t*>(subset.request().ptr);
    }

    std::vector<std::vector<double> > out_d(report_distance ? num_output : 0);
    std::vector<std::vector<uint32_t> > out_i(report_index ? num_output : 0);

    bool store_count = !report_distance && !report_index;
    pybind11::array_t<uint32_t> counts(store_count ? num_output : 0);
    uint32_t * counts_ptr = static_cast<uint32_t*>(counts.request().ptr);

    uint32_t nthresholds = thresholds.size();
    bool multiple_thresholds = (nthresholds != 1);
    if (multiple_thresholds && nthresholds != num_output) {
        throw std::runtime_error("'threshold' should have length equal to the number of observations or 'subset'");
    }
    const double* threshold_ptr = static_cast<const double*>(thresholds.request().ptr);

    bool no_support = false;
    knncolle::parallelize(num_threads, num_output, [&](int tid, uint32_t start, uint32_t length) {
        auto searcher = prebuilt->initialize();

        if (!searcher->can_search_all()) {
            if (tid == 0) {
                no_support = true;
            }
            return;
        }

        for (int o = start, end = start + length; o < end; ++o) {
            auto count = searcher->search_all(
                (subset_ptr != NULL ? subset_ptr[o] : o),
                threshold_ptr[multiple_thresholds ? o : 0],
                (report_index ? &out_i[o] : NULL),
                (report_distance ? &out_d[o] : NULL)
            ); 
            if (store_count) {
                counts_ptr[o] = count;
            }
        }
    });

    if (no_support) {
        throw std::runtime_error("algorithm does not support search by distance");
    }

    if (store_count) {
        return counts;
    } else {
        pybind11::tuple output(2);
        if (report_index) {
            output[0] = format_range_output(out_i);
        } else {
            output[0] = pybind11::none();
        }
        if (report_distance) {
            output[1] = format_range_output(out_d);
        } else {
            output[1] = pybind11::none();
        }
        return output;
    }
} 

pybind11::object generic_query_all(
    const PrebuiltPointer& prebuilt, 
    const DataMatrix& query,
    const ThresholdVector& thresholds,
    int num_threads,
    bool report_index,
    bool report_distance) 
{
    size_t ndim = prebuilt->num_dimensions();

    auto buf_info = query.request();
    uint32_t nquery = buf_info.shape[1];
    const double* query_ptr = static_cast<const double*>(buf_info.ptr);
    if (static_cast<size_t>(buf_info.shape[0]) != ndim) {
        throw std::runtime_error("mismatch in dimensionality between index and 'query'");
    }

    std::vector<std::vector<double> > out_d(report_distance ? nquery : 0);
    std::vector<std::vector<uint32_t> > out_i(report_index ? nquery : 0);

    bool store_count = !report_distance && !report_index;
    pybind11::array_t<uint32_t> counts(store_count ? nquery : 0);
    uint32_t* counts_ptr = static_cast<uint32_t*>(counts.request().ptr);

    uint32_t nthresholds = thresholds.size();
    bool multiple_thresholds = (nthresholds != 1);
    if (multiple_thresholds && nthresholds != nquery) {
        throw std::runtime_error("'threshold' should have length equal to 'subset'");
    }
    const double* threshold_ptr = static_cast<const double*>(thresholds.request().ptr);

    bool no_support = false;
    knncolle::parallelize(num_threads, nquery, [&](int tid, uint32_t start, uint32_t length) {
        auto searcher = prebuilt->initialize();

        if (!searcher->can_search_all()) {
            if (tid == 0) {
                no_support = true;
            }
            return;
        }

        size_t query_offset = static_cast<size_t>(start) * ndim; // using size_t to avoid overflow.
        for (int o = start, end = start + length; o < end; ++o, query_offset += ndim) {
            auto current_ptr = query_ptr + query_offset;
            auto count = searcher->search_all(
                current_ptr,
                threshold_ptr[multiple_thresholds ? o : 0],
                (report_index ? &out_i[o] : NULL),
                (report_distance ? &out_d[o] : NULL)
            ); 

            if (store_count) {
                counts_ptr[o] = count;
            }
        }
    });

    if (no_support) {
        throw std::runtime_error("algorithm does not support search by distance");
    }

    if (store_count) {
        return counts;
    } else {
        pybind11::tuple output(2);
        if (report_index) {
            output[0] = format_range_output(out_i);
        } else {
            output[0] = pybind11::none();
        }
        if (report_distance) {
            output[1] = format_range_output(out_d);
        } else {
            output[1] = pybind11::none();
        }
        return output;
    }
} 

/*********************************
 ********* Init function *********
 *********************************/

void init_generics(pybind11::module& m) {
    m.def("generic_build", &generic_build);
    m.def("generic_num_obs", &generic_num_obs);
    m.def("generic_num_dims", &generic_num_dims);
    m.def("generic_find_knn", &generic_find_knn);
    m.def("generic_query_knn", &generic_query_knn);
    m.def("generic_find_all", &generic_find_all);
    m.def("generic_query_all", &generic_query_all);
}
