"""
If the arbitrary constant class from issue sympy/sympy#4435 is ever implemented, this
should serve as a set of test cases.
"""

import pytest

from diofant import (Eq, Function, I, Integer, Integral, Pow, Symbol, acos,
                     cos, cosh, dsolve, exp, log, sin, sinh, sqrt, symbols)
from diofant.abc import x, y, z
from diofant.solvers.ode import constant_renumber, constantsimp


__all__ = ()

C1, C2, C3 = symbols('C1:4')
f = Function('f')


def test_constant_mul():
    # We want C1 (Constant) below to absorb the y's, but not the x's
    assert constant_renumber(constantsimp(y*C1, [C1]), 'C', 1, 1) == C1*y
    assert constant_renumber(constantsimp(C1*y, [C1]), 'C', 1, 1) == C1*y
    assert constant_renumber(constantsimp(x*C1, [C1]), 'C', 1, 1) == x*C1
    assert constant_renumber(constantsimp(C1*x, [C1]), 'C', 1, 1) == x*C1
    assert constant_renumber(constantsimp(2*C1, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(C1*2, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(y*C1*x, [C1, y]), 'C', 1, 1) == C1*x
    assert constant_renumber(constantsimp(x*y*C1, [C1, y]), 'C', 1, 1) == x*C1
    assert constant_renumber(constantsimp(y*x*C1, [C1, y]), 'C', 1, 1) == x*C1
    assert constant_renumber(constantsimp(C1*x*y, [C1, y]), 'C', 1, 1) == C1*x
    assert constant_renumber(constantsimp(x*C1*y, [C1, y]), 'C', 1, 1) == x*C1
    assert constant_renumber(constantsimp(C1*y*(y + 1), [C1]), 'C', 1, 1) == C1*y*(y+1)
    assert constant_renumber(constantsimp(y*C1*(y + 1), [C1]), 'C', 1, 1) == C1*y*(y+1)
    assert constant_renumber(constantsimp(x*(y*C1), [C1]), 'C', 1, 1) == x*y*C1
    assert constant_renumber(constantsimp(x*(C1*y), [C1]), 'C', 1, 1) == x*y*C1
    assert constant_renumber(constantsimp(C1*(x*y), [C1, y]), 'C', 1, 1) == C1*x
    assert constant_renumber(constantsimp((x*y)*C1, [C1, y]), 'C', 1, 1) == x*C1
    assert constant_renumber(constantsimp((y*x)*C1, [C1, y]), 'C', 1, 1) == x*C1
    assert constant_renumber(constantsimp(y*(y + 1)*C1, [C1, y]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp((C1*x)*y, [C1, y]), 'C', 1, 1) == C1*x
    assert constant_renumber(constantsimp(y*(x*C1), [C1, y]), 'C', 1, 1) == x*C1
    assert constant_renumber(constantsimp((x*C1)*y, [C1, y]), 'C', 1, 1) == x*C1
    assert constant_renumber(
        constantsimp(C1*x*y*x*y*2, [C1, y]), 'C', 1, 1) == C1*x**2
    assert constant_renumber(constantsimp(C1*x*y*z, [C1, y, z]), 'C', 1, 1) == C1*x
    assert constant_renumber(
        constantsimp(C1*x*y**2*sin(z), [C1, y, z]), 'C', 1, 1) == C1*x
    assert constant_renumber(constantsimp(C1*C1, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(C1*C2, [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(C2*C2, [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(C1*C1*C2, [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(
        constantsimp(C1*x*2**x, [C1]), 'C', 1, 1) == C1*x*2**x


def test_constant_add():
    assert constant_renumber(constantsimp(C1 + C1, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(C1 + 2, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(2 + C1, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(C1 + y, [C1, y]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(C1 + x, [C1]), 'C', 1, 1) == C1 + x
    assert constant_renumber(constantsimp(C1 + C1, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(C1 + C2, [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(C2 + C1, [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(C1 + C2 + C1, [C1, C2]), 'C', 1, 2) == C1


def test_constant_power_as_base():
    assert constant_renumber(constantsimp(C1**C1, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(Pow(C1, C1), [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(C1**C1, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(C1**C2, [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(C2**C1, [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(C2**C2, [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(C1**y, [C1, y]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(C1**x, [C1]), 'C', 1, 1) == C1**x
    assert constant_renumber(constantsimp(C1**2, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(
        constantsimp(C1**(x*y), [C1]), 'C', 1, 1) == C1**(x*y)


def test_constant_power_as_exp():
    assert constant_renumber(constantsimp(x**C1, [C1]), 'C', 1, 1) == x**C1
    assert constant_renumber(constantsimp(y**C1, [C1, y]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(x**y**C1, [C1, y]), 'C', 1, 1) == x**C1
    assert constant_renumber(
        constantsimp((x**y)**C1, [C1]), 'C', 1, 1) == (x**y)**C1
    assert constant_renumber(
        constantsimp(x**(y**C1), [C1, y]), 'C', 1, 1) == x**C1
    assert constant_renumber(constantsimp(x**C1**y, [C1, y]), 'C', 1, 1) == x**C1
    assert constant_renumber(
        constantsimp(x**(C1**y), [C1, y]), 'C', 1, 1) == x**C1
    assert constant_renumber(
        constantsimp((x**C1)**y, [C1]), 'C', 1, 1) == (x**C1)**y
    assert constant_renumber(constantsimp(2**C1, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(Integer(2)**C1, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(exp(C1), [C1]), 'C', 1, 1) == C1
    assert constant_renumber(
        constantsimp(exp(C1 + x), [C1]), 'C', 1, 1) == C1*exp(x)
    assert constant_renumber(constantsimp(Pow(2, C1), [C1]), 'C', 1, 1) == C1


def test_constant_function():
    assert constant_renumber(constantsimp(sin(C1), [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(f(C1), [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(f(C1, C1), [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(f(C1, C2), [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(f(C2, C1), [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(f(C2, C2), [C1, C2]), 'C', 1, 2) == C1
    assert constant_renumber(
        constantsimp(f(C1, x), [C1]), 'C', 1, 2) == f(C1, x)
    assert constant_renumber(constantsimp(f(C1, y), [C1, y]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(f(y, C1), [C1, y]), 'C', 1, 2) == C1
    assert constant_renumber(constantsimp(f(C1, y, C2), [C1, C2, y]), 'C', 1, 2) == C1


def test_constant_function_multiple():
    # The rules to not renumber in this case would be too complicated, and
    # dsolve is not likely to ever encounter anything remotely like this.
    assert constant_renumber(
        constantsimp(f(C1, C1, x), [C1]), 'C', 1, 1) == f(C1, C1, x)


def test_constant_multiple():
    assert constant_renumber(constantsimp(C1*2 + 2, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(constantsimp(x*2/C1, [C1]), 'C', 1, 1) == C1*x
    assert constant_renumber(constantsimp(C1**2*2 + 2, [C1]), 'C', 1, 1) == C1
    assert constant_renumber(
        constantsimp(sin(2*C1) + x + sqrt(2), [C1]), 'C', 1, 1) == C1 + x
    assert constant_renumber(constantsimp(2*C1 + C2, [C1, C2]), 'C', 1, 2) == C1


def test_constant_repeated():
    assert C1 + C1*x == constant_renumber( C1 + C1*x, 'C', 1, 3)


def test_ode_solutions():
    # only a few examples here, the rest will be tested in the actual dsolve tests
    assert constant_renumber(constantsimp(C1*exp(2*x) + exp(x)*(C2 + C3), [C1, C2, C3]), 'C', 1, 3) == \
        constant_renumber((C1*exp(x) + C2*exp(2*x)), 'C', 1, 2)
    assert constant_renumber(
        constantsimp(Eq(f(x), I*C1*sinh(x/3) + C2*cosh(x/3)), [C1, C2]),
        'C', 1, 2) == constant_renumber(Eq(f(x), C1*sinh(x/3) + C2*cosh(x/3)), 'C', 1, 2)
    assert constant_renumber(constantsimp(Eq(f(x), acos((-C1)/cos(x))), [C1]), 'C', 1, 1) == \
        Eq(f(x), acos(C1/cos(x)))
    assert constant_renumber(
        constantsimp(Eq(log(f(x)/C1) + 2*exp(x/f(x)), 0), [C1]),
        'C', 1, 1) == Eq(log(C1*f(x)) + 2*exp(x/f(x)), 0)
    assert constant_renumber(constantsimp(Eq(log(x*sqrt(2)*sqrt(1/x)*sqrt(f(x))
                                                 / C1) + x**2/(2*f(x)**2), 0), [C1]), 'C', 1, 1) == \
        Eq(log(C1*sqrt(x)*sqrt(f(x))) + x**2/(2*f(x)**2), 0)
    assert constant_renumber(constantsimp(Eq(-exp(-f(x)/x)*sin(f(x)/x)/2 + log(x/C1) -
                                             cos(f(x)/x)*exp(-f(x)/x)/2, 0), [C1]), 'C', 1, 1) == \
        Eq(-exp(-f(x)/x)*sin(f(x)/x)/2 + log(C1*x) - cos(f(x)/x) *
           exp(-f(x)/x)/2, 0)
    u2 = Symbol('u2')
    _a = Symbol('_a')
    assert constant_renumber(constantsimp(Eq(-Integral(-1/(sqrt(1 - u2**2)*u2),
                                                       (u2, _a, x/f(x))) + log(f(x)/C1), 0), [C1]), 'C', 1, 1) == \
        Eq(-Integral(-1/(u2*sqrt(1 - u2**2)), (u2, _a, x/f(x))) +
           log(C1*f(x)), 0)
    assert [constantsimp(i, [C1]) for i in [Eq(f(x), sqrt(-C1*x + x**2)), Eq(f(x), -sqrt(-C1*x + x**2))]] == \
        [Eq(f(x), sqrt(x*(C1 + x))), Eq(f(x), -sqrt(x*(C1 + x)))]

    # issue sympy/sympy5770
    k = Symbol('k', extended_real=True)
    t = Symbol('t')
    w = Function('w')
    sol = dsolve(w(t).diff((t, 6)) - k**6*w(t), w(t))
    assert len([s for s in sol.free_symbols if s.name.startswith('C')]) == 6
    assert constantsimp((C1*cos(x) + C2*cos(x))*exp(x), {C1, C2}) == \
        C1*cos(x)*exp(x)
    assert constantsimp(C1*cos(x) + C2*cos(x) + C3*sin(x), {C1, C2, C3}) == \
        C1*cos(x) + C3*sin(x)
    assert constantsimp(exp(C1 + x), {C1}) == C1*exp(x)
    assert constantsimp(x + C1 + y, {C1, y}) == C1 + x
    assert constantsimp(x + C1 + Integral(x, (x, 1, 2)), {C1}) == C1 + x


@pytest.mark.xfail
def test_nonlocal_simplification():
    assert constantsimp(C1 + C2+x*C2, [C1, C2]) == C1 + C2*x


def test_constant_Eq():
    # C1 on the rhs is well-tested, but the lhs is only tested here
    assert constantsimp(Eq(C1, 3 + f(x)*x), [C1]) == Eq(x*f(x), C1)
    assert constantsimp(Eq(C1, 3 * f(x)*x), [C1]) == Eq(f(x)*x, C1)
