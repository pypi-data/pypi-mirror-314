#include "def.h"
#include "pybind11/pybind11.h"

// Turn off manual vectorization always, to avoid small inconsistencies in
// distance calculations across otherwise-compliant machines. 
#define NO_MANUAL_VECTORIZATION

#include "knncolle_hnsw/knncolle_hnsw.hpp"

BuilderPointer create_hnsw_builder(int nlinks, int ef_construct, int ef_search, std::string distance) {
    knncolle_hnsw::HnswOptions<uint32_t, float> opt;
    opt.num_links = nlinks;
    opt.ef_construction = ef_construct;
    opt.ef_search = ef_search;

    if (distance == "Manhattan") {
        opt.distance_options.create = [&](int dim) -> hnswlib::SpaceInterface<float>* {
            return new knncolle_hnsw::ManhattanDistance<float>(dim);
        };
        return BuilderPointer(new knncolle_hnsw::HnswBuilder<SimpleMatrix, double>(opt));

    } else if (distance == "Euclidean") {
        return BuilderPointer(new knncolle_hnsw::HnswBuilder<SimpleMatrix, double>(opt));

    } else if (distance == "Cosine") {
        return BuilderPointer(
            new knncolle::L2NormalizedBuilder<SimpleMatrix, double>(
                new knncolle_hnsw::HnswBuilder<
                    knncolle::L2NormalizedMatrix<SimpleMatrix>,
                    double
                >(opt)
            )
        );

    } else {
        throw std::runtime_error("unknown distance type '" + distance + "'");
        return BuilderPointer();
    }
}

void init_hnsw(pybind11::module& m) {
    m.def("create_hnsw_builder", &create_hnsw_builder);
}
