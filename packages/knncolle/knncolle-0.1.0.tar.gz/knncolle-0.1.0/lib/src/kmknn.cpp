#include "def.h"
#include "pybind11/pybind11.h"

BuilderPointer create_kmknn_builder(std::string distance) {
    if (distance == "Manhattan") {
        return BuilderPointer(new knncolle::KmknnBuilder<knncolle::ManhattanDistance, SimpleMatrix, double>);

    } else if (distance == "Euclidean") {
        return BuilderPointer(new knncolle::KmknnBuilder<knncolle::EuclideanDistance, SimpleMatrix, double>);

    } else if (distance == "Cosine") {
        return BuilderPointer(
            new knncolle::L2NormalizedBuilder<SimpleMatrix, double>(
                new knncolle::KmknnBuilder<
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

void init_kmknn(pybind11::module& m) {
    m.def("create_kmknn_builder", &create_kmknn_builder);
}
