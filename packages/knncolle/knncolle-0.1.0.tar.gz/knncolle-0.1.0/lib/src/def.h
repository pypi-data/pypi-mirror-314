#ifndef DEF_H
#define DEF_H

#include <cstdint>
#include <memory>

#include "knncolle/knncolle.hpp"

typedef knncolle::SimpleMatrix<uint32_t, uint32_t, double> SimpleMatrix;

typedef knncolle::Builder<SimpleMatrix, double> Builder;

typedef std::shared_ptr<Builder> BuilderPointer;

typedef knncolle::Prebuilt<uint32_t, uint32_t, double> Prebuilt;

typedef std::shared_ptr<Prebuilt> PrebuiltPointer;

#endif
