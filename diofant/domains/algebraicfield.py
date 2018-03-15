"""Implementation of :class:`AlgebraicField` class. """

from ..core import Integer, sympify
from ..polys.polyclasses import ANP
from ..polys.polyerrors import (CoercionFailed, DomainError, IsomorphismFailed,
                                NotAlgebraic)
from .characteristiczero import CharacteristicZero
from .field import Field
from .simpledomain import SimpleDomain


__all__ = ('AlgebraicField',)


class AlgebraicField(Field, CharacteristicZero, SimpleDomain):
    """A class for representing algebraic number fields. """

    dtype = ANP

    is_AlgebraicField = is_Algebraic = True
    is_Numerical = True

    has_assoc_Ring = False
    has_assoc_Field = True

    def __init__(self, dom, *ext):
        if not dom.is_QQ:
            raise DomainError("ground domain must be a rational field")

        ext = [sympify(_).as_expr() for _ in ext]

        from ..polys.numberfields import primitive_element
        from ..polys.rootoftools import RootOf

        minpoly, coeffs, H = primitive_element(ext)

        # canonicalization

        ext = sum(c*e for c, e in zip(coeffs, ext))

        for n in range(minpoly.degree()):
            r = RootOf(minpoly, n)
            if (r - ext).evalf(2, chop=True).is_zero:
                ext = r
                break

        self.ext = ext
        self.minpoly = minpoly
        self.mod = minpoly.rep
        self.domain = dom

        self.ngens = 1
        self.symbols = self.gens = (self.ext.as_expr(),)

        self.root = sum(self(h) for h in H)
        self.unit = self([dom(1), dom(0)])

        self.zero = self.dtype.zero(self.mod.rep, dom)
        self.one = self.dtype.one(self.mod.rep, dom)

        self.rep = str(self.domain) + '<' + str(self.ext) + '>'

    def new(self, element):
        if isinstance(element, list):
            return self.dtype([self.domain.convert(_) for _ in element],
                              self.mod.rep, self.domain)
        else:
            return self.convert(element)

    def __hash__(self):
        return hash((self.__class__.__name__, self.dtype, self.domain, self.ext))

    def __eq__(self, other):
        """Returns ``True`` if two domains are equivalent. """
        return isinstance(other, AlgebraicField) and \
            self.dtype == other.dtype and self.ext == other.ext

    def algebraic_field(self, *extension):
        r"""Returns an algebraic field, i.e. `\mathbb{Q}(\alpha, \ldots)`. """
        return AlgebraicField(self.domain, *((self.ext.as_expr(),) + extension))

    def to_diofant(self, a):
        """Convert ``a`` to a Diofant object. """
        return sum((c*self.ext**n for n, c in enumerate(reversed(a.rep))), Integer(0))

    def from_diofant(self, a):
        """Convert Diofant's expression to ``dtype``. """
        from ..polys.numberfields import to_number_field
        try:
            return to_number_field(a, self)
        except (NotAlgebraic, IsomorphismFailed):
            raise CoercionFailed("%s is not a valid algebraic number in %s" % (a, self))

    def from_ZZ_python(self, a, K0):
        """Convert a Python ``int`` object to ``dtype``. """
        return self([self.domain.convert(a, K0)])

    def from_QQ_python(self, a, K0):
        """Convert a Python ``Fraction`` object to ``dtype``. """
        return self([self.domain.convert(a, K0)])

    def from_ZZ_gmpy(self, a, K0):
        """Convert a GMPY ``mpz`` object to ``dtype``. """
        return self([self.domain.convert(a, K0)])

    def from_QQ_gmpy(self, a, K0):
        """Convert a GMPY ``mpq`` object to ``dtype``. """
        return self([self.domain.convert(a, K0)])

    def from_RealField(self, a, K0):
        """Convert a mpmath ``mpf`` object to ``dtype``. """
        return self([self.domain.convert(a, K0)])

    def from_AlgebraicField(self, a, K0):
        return self.from_diofant(K0.to_diofant(a))

    @property
    def ring(self):
        """Returns a ring associated with ``self``. """
        raise AttributeError('there is no ring associated with %s' % self)

    def is_positive(self, a):
        """Returns True if ``a`` is positive. """
        return self.domain.is_positive(a.LC())

    def is_negative(self, a):
        """Returns True if ``a`` is negative. """
        return self.domain.is_negative(a.LC())

    def is_nonpositive(self, a):
        """Returns True if ``a`` is non-positive. """
        return self.domain.is_nonpositive(a.LC())

    def is_nonnegative(self, a):
        """Returns True if ``a`` is non-negative. """
        return self.domain.is_nonnegative(a.LC())
