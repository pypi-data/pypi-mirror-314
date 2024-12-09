#include "def.h"
#include "pybind11/pybind11.h"

// Turn off manual vectorization always, to avoid small inconsistencies in
// distance calculations across otherwise-compliant machines. 
#define NO_MANUAL_VECTORIZATION 1

#include "knncolle_annoy/knncolle_annoy.hpp"

BuilderPointer create_annoy_builder(int num_trees, double search_mult, std::string distance) {
    knncolle_annoy::AnnoyOptions opt;
    opt.num_trees = num_trees;
    opt.search_mult = search_mult;

    if (distance == "Manhattan") {
        return BuilderPointer(new knncolle_annoy::AnnoyBuilder<Annoy::Manhattan, SimpleMatrix, double>(opt));

    } else if (distance == "Euclidean") {
        return BuilderPointer(new knncolle_annoy::AnnoyBuilder<Annoy::Euclidean, SimpleMatrix, double>(opt));

    } else if (distance == "Cosine") {
        return BuilderPointer(
            new knncolle::L2NormalizedBuilder<SimpleMatrix, double>(
                new knncolle_annoy::AnnoyBuilder<
                    Annoy::Euclidean,
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

void init_annoy(pybind11::module& m) {
    m.def("create_annoy_builder", &create_annoy_builder);
}
