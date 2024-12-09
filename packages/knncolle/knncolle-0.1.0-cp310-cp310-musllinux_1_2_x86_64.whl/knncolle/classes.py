from abc import ABC
from . import lib_knncolle as lib


class Parameters(ABC):
    """
    Abstract base class for the parameters of a nearest neighbor search. Each
    search algorithm should implement a subclass that contains the relevant
    parameters for controlling index construction or search.
    """
    pass


class Index(ABC):
    """
    Abstract base class for a prebuilt nearest neighbor-search index. Each
    search algorithm should implement their own subclasses, but are free
    to use any data structure to represent their search indices.
    """
    pass


class GenericIndex(Index):
    """
    Abstract base class for a prebuilt nearest neighbor-search index that is
    represented as a ``std::shared_ptr<knncolle::Prebuilt<uint32_t, uint32_t,
    double> >``. Compatible algorithms should implement their own subclasses.
    """

    def num_observations(self) -> int:
        """
        Returns:
            Number of observations in this index.
        """
        return lib.generic_num_obs(self.ptr)

    def num_dimensions(self) -> int:
        """
        Returns:
            Number of dimensions in this index.
        """
        return lib.generic_num_dims(self.ptr)
