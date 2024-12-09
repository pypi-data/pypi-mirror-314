#include "def.h"
#include "pybind11/pybind11.h"

BuilderPointer create_exhaustive_builder(std::string distance) {
    if (distance == "Manhattan") {
        return BuilderPointer(new knncolle::BruteforceBuilder<knncolle::ManhattanDistance, SimpleMatrix, double>);

    } else if (distance == "Euclidean") {
        return BuilderPointer(new knncolle::BruteforceBuilder<knncolle::EuclideanDistance, SimpleMatrix, double>);

    } else if (distance == "Cosine") {
        return BuilderPointer(
            new knncolle::L2NormalizedBuilder(
                new knncolle::BruteforceBuilder<
                    knncolle::EuclideanDistance,
                    knncolle::L2NormalizedMatrix<SimpleMatrix>,
                    double
                >
            )
        );

    } else {
        throw std::runtime_error("unknown distance type '" + distance + "'");
        return BuilderPointer();
    }
}

void init_exhaustive(pybind11::module& m) {
    m.def("create_exhaustive_builder", &create_exhaustive_builder);
}
