"""
Generic 3-dimensional kd-tree to perform spatial searches.

```../examples/mathutils.kdtree.py```

"""

import typing
import collections.abc
import typing_extensions
import mathutils

class KDTree:
    """KdTree(size) -> new kd-tree initialized to hold size items."""

    def balance(self):
        """Balance the tree."""

    def find(
        self, co, filter: collections.abc.Callable | None = None
    ) -> tuple[mathutils.Vector, int, float]:
        """Find nearest point to co.

        :param co: 3D coordinates.
        :param filter: function which takes an index and returns True for indices to include in the search.
        :type filter: collections.abc.Callable | None
        :return: Returns (position, index, distance).
        :rtype: tuple[mathutils.Vector, int, float]
        """

    def find_n(self, co, n: int) -> list[tuple[mathutils.Vector, int, float]]:
        """Find nearest n points to co.

        :param co: 3D coordinates.
        :param n: Number of points to find.
        :type n: int
        :return: Returns a list of tuples (position, index, distance).
        :rtype: list[tuple[mathutils.Vector, int, float]]
        """

    def find_range(
        self, co, radius: float
    ) -> list[tuple[mathutils.Vector, int, float]]:
        """Find all points within radius of co.

        :param co: 3D coordinates.
        :param radius: Distance to search for points.
        :type radius: float
        :return: Returns a list of tuples (position, index, distance).
        :rtype: list[tuple[mathutils.Vector, int, float]]
        """

    def insert(self, co, index: int):
        """Insert a point into the KDTree.

        :param co: Point 3d position.
        :param index: The index of the point.
        :type index: int
        """

    def __init__(self, size):
        """

        :param size:
        """
