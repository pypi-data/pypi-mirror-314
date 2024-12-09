from .classes import Parameters, GenericIndex
from typing import Literal, Tuple

from . import lib_knncolle as lib
from .classes import Parameters, GenericIndex
from .define_builder import define_builder


class ExhaustiveParameters(Parameters):
    """Parameters for an exhaustive search. """

    def __init__(
        self,
        distance: Literal["Euclidean", "Manhattan", "Cosine"] = "Euclidean",
    ):
        """
        Args:
            distance:
                Distance metric for index construction and search. This should
                be one of ``Euclidean``, ``Manhattan`` or ``Cosine``.
        """
        self.distance = distance

    @property
    def distance(self) -> str:
        """Distance metric, see :meth:`~__init__()`."""
        return self._distance

    @distance.setter
    def distance(self, distance: str):
        """
        Args:
            distance:
                Distance metric, see :meth:`~__init__()`.
        """
        if distance not in ["Euclidean", "Manhattan", "Cosine"]:
            raise ValueError("unsupported 'distance'")
        self._distance = distance


class ExhaustiveIndex(GenericIndex):
    """A prebuilt index for an exhaustive search, created by
    :py:func:`~knncolle.define_builder.define_builder` with a
    :py:class:`~knncolle.exhaustive.ExhaustiveParameters` instance.
    """

    def __init__(self, ptr):
        """
        Args:
            ptr:
                Shared pointer to a ``knncolle::Prebuilt<uint32_t, uint32_t,
                double>``, created and wrapped by pybind11.
        """
        self._ptr = ptr

    @property
    def ptr(self):
        """Pointer to the prebuilt index, see :py:meth:`~__init__`."""
        return self._ptr


@define_builder.register
def _define_builder_exhaustive(x: ExhaustiveParameters) -> Tuple:
    return (lib.create_exhaustive_builder(x.distance), ExhaustiveIndex)
