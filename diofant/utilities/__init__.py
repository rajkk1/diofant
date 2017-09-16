"""This module contains some general purpose utilities."""

from .iterables import (flatten, group, take, subsets,  # noqa: F401
                        variations, numbered_symbols, capture, dict_merge,
                        postorder_traversal, prefixes, postfixes, sift,
                        topological_sort, unflatten, has_dups, has_variety,
                        reshape, default_sort_key, ordered)

from .misc import filldedent  # noqa: F401

from .lambdify import lambdify  # noqa: F401

from .decorator import public  # noqa: F401
