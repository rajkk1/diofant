# -*- coding: utf-8 -*-

try:
    import diofant
except ImportError:
    import sympy as diofant


class _Polynomial:

    expr = None
    x = diofant.Symbol('x', real=True)
    x0 = diofant.symbols('x0', real=True)
    x1 = diofant.symbols('x1', real=True)

    def __init__(self, c=None):
        self.c = c

    def diff(self, deg):
        return self.expr.diff(self.x, deg)

    # Below are properties to be subclassed
    @property
    def expr(self):
        return sum(c*self.x**o for o, c in enumerate(self.c))

    def eval(self, x_val, deriv=0):
        return self.expr.diff(self.x, deriv).subs({self.x: x_val})


def _make_poly(order, Poly=None):
    if Poly is None:
        Poly = _Polynomial
    c = [diofant.Symbol('c_' + str(o), real=True) for o in range(order+1)]
    return Poly(c)


def _mk_eqs(wy=3, **kwargs):
    # Equations for fitting a wy*2 - 1 degree polynomial between two points,
    # at end points derivatives are known up to order: wy - 1
    p = _make_poly(2*wy-1, **kwargs)
    y0 = [diofant.Symbol('y0_' + str(i), real=True) for i in range(wy)]
    y1 = [diofant.Symbol('y1_' + str(i), real=True) for i in range(wy)]
    eqs = []
    for i in range(wy):
        eqs.append(p.diff(i).subs({p.x: p.x0}) - y0[i])
        eqs.append(p.diff(i).subs({p.x: p.x1}) - y1[i])
    return eqs, p, (y0, y1)


class TimeSolve01:

    def setup(self):
        self.eqs, self.p, self.y = _mk_eqs(2)  # running with wy=3 is too slow (~5s)

    def time_solve(self):
        diofant.solve(self.eqs, *self.p.c)

    def time_solve_nocheck(self):
        diofant.solve(self.eqs, *self.p.c, check=False)


def _matrix_solve_setup():

        n = 3

        A = diofant.Matrix(n, n, lambda i, j: diofant.Symbol('a{}{}'.format(i, j)))
        b = diofant.Matrix(n, 1, lambda i, j: diofant.Symbol('b{}{}'.format(i, j)))
        A_sym = diofant.Matrix(n, n, lambda i, j:
                               diofant.Symbol('a{}{}'.format(*sorted((i, j)))))

        return A, b, A_sym


class TimeMatrixSolve:

    params = ['GE', 'LU', 'ADJ']

    def setup(self, name):

        self.A, self.b, _ = _matrix_solve_setup()

    def time_solve(self, name):

        self.A.solve(self.b, method=name)


class TimeMatrixSolve2:

    def setup(self):

        self.A, self.b, self.A_sym = _matrix_solve_setup()

    def time_lusolve(self):

        self.A.LUsolve(self.b)

    def time_cholesky_solve(self):

        self.A_sym.cholesky_solve(self.b)


class TimeMatrixOperations:
    # first param is the size of the matrix, second is the number of symbols in it
    params = ((3, 4), (0, 2, 5))

    def setup(self, n, num_symbols):
        # every test will be based of a submatrix of this matrix
        big_mat = diofant.Matrix([[3, 8, 10, 5, 10, 7, 10, 10, 8, 6],
                                  [10, 9, 3, 7, 10, 1, 4, 2, 8, 1],
                                  [5, 9, 9, 0, 2, 10, 5, 9, 3, 9],
                                  [1, 8, 0, 7, 8, 8, 0, 4, 1, 10],
                                  [6, 5, 3, 0, 3, 4, 6, 1, 10, 5],
                                  [7, 10, 8, 9, 10, 7, 2, 8, 3, 2],
                                  [10, 8, 5, 10, 3, 5, 10, 4, 2, 3],
                                  [8, 4, 10, 9, 1, 9, 7, 4, 8, 6],
                                  [6, 2, 4, 1, 1, 0, 1, 3, 1, 9],
                                  [9, 2, 6, 10, 9, 4, 10, 2, 1, 8]])
        symbol_locations = [(2, 2), (1, 9), (0, 0), (0, 7), (9, 1),
                            (6, 9), (8, 9), (4, 0), (3, 8), (3, 2),
                            (2, 8), (1, 8), (5, 3), (5, 9), (6, 4),
                            (5, 5), (7, 9), (5, 1), (1, 0), (3, 3),
                            (7, 1), (2, 5), (1, 5), (4, 4), (4, 2),
                            (7, 3), (3, 4), (6, 6), (9, 5), (1, 6),
                            (9, 0), (3, 1), (0, 4), (8, 3), (2, 3),
                            (3, 9), (9, 6), (4, 8), (9, 3), (8, 0),
                            (6, 7), (5, 7), (8, 6), (3, 6), (4, 5),
                            (1, 2), (9, 8), (7, 4), (8, 8), (6, 1),
                            (0, 3), (4, 7), (7, 0), (9, 7), (5, 4),
                            (7, 6), (2, 6), (3, 7), (3, 5), (1, 4),
                            (5, 0), (4, 9), (7, 8), (6, 8), (2, 1),
                            (9, 2), (3, 0), (7, 7), (2, 7), (2, 0),
                            (8, 1), (7, 5), (4, 3), (1, 3), (9, 9),
                            (0, 6), (4, 1), (5, 8), (8, 4), (0, 8),
                            (2, 4), (9, 4), (7, 2), (1, 7), (6, 3),
                            (6, 5), (5, 2), (6, 0), (0, 1), (8, 2),
                            (2, 9), (8, 5), (0, 2), (0, 9), (8, 7),
                            (4, 6), (0, 5), (1, 1), (6, 2), (5, 6)]

        symbol_locations = [(i, j) for (i, j) in symbol_locations if i <= n and j <= n]
        symbol_locations = symbol_locations[:num_symbols]

        def entry(i, j):
            if (i, j) in symbol_locations:
                return diofant.Symbol('x')
            return big_mat[i, j]
        self.A = diofant.Matrix(n, n, entry)

    def time_rank(self, n, num_symbols):
        self.A.rank()

    def time_rref(self, n, num_symbols):
        self.A.rref()

    def time_det(self, n, num_symbols):
        self.A.det()

    def time_det_berkowitz(self, n, num_symbols):
        self.A.det(method='berkowitz')


class TimeMatrixArithmetic:
    # first param is the size of the matrix, second is the number of symbols in it
    params = ((3, 4, 6, 10), (0, 5))

    def setup(self, n, num_symbols):
        # every test will be based off a submatrix of this matrix
        big_mat = diofant.Matrix([[3, 8, 10, 5, 10, 7, 10, 10, 8, 6],
                                  [10, 9, 3, 7, 10, 1, 4, 2, 8, 1],
                                  [5, 9, 9, 0, 2, 10, 5, 9, 3, 9],
                                  [1, 8, 0, 7, 8, 8, 0, 4, 1, 10],
                                  [6, 5, 3, 0, 3, 4, 6, 1, 10, 5],
                                  [7, 10, 8, 9, 10, 7, 2, 8, 3, 2],
                                  [10, 8, 5, 10, 3, 5, 10, 4, 2, 3],
                                  [8, 4, 10, 9, 1, 9, 7, 4, 8, 6],
                                  [6, 2, 4, 1, 1, 0, 1, 3, 1, 9],
                                  [9, 2, 6, 10, 9, 4, 10, 2, 1, 8]])
        symbol_locations = [(2, 2), (1, 9), (0, 0), (0, 7), (9, 1),
                            (6, 9), (8, 9), (4, 0), (3, 8), (3, 2),
                            (2, 8), (1, 8), (5, 3), (5, 9), (6, 4),
                            (5, 5), (7, 9), (5, 1), (1, 0), (3, 3),
                            (7, 1), (2, 5), (1, 5), (4, 4), (4, 2),
                            (7, 3), (3, 4), (6, 6), (9, 5), (1, 6),
                            (9, 0), (3, 1), (0, 4), (8, 3), (2, 3),
                            (3, 9), (9, 6), (4, 8), (9, 3), (8, 0),
                            (6, 7), (5, 7), (8, 6), (3, 6), (4, 5),
                            (1, 2), (9, 8), (7, 4), (8, 8), (6, 1),
                            (0, 3), (4, 7), (7, 0), (9, 7), (5, 4),
                            (7, 6), (2, 6), (3, 7), (3, 5), (1, 4),
                            (5, 0), (4, 9), (7, 8), (6, 8), (2, 1),
                            (9, 2), (3, 0), (7, 7), (2, 7), (2, 0),
                            (8, 1), (7, 5), (4, 3), (1, 3), (9, 9),
                            (0, 6), (4, 1), (5, 8), (8, 4), (0, 8),
                            (2, 4), (9, 4), (7, 2), (1, 7), (6, 3),
                            (6, 5), (5, 2), (6, 0), (0, 1), (8, 2),
                            (2, 9), (8, 5), (0, 2), (0, 9), (8, 7),
                            (4, 6), (0, 5), (1, 1), (6, 2), (5, 6)]

        symbol_locations = [(i, j) for (i, j) in symbol_locations if i <= n and j <= n]
        symbol_locations = symbol_locations[:num_symbols]

        # create a matrix with the appropriate number of symbols based on
        # a pre-determined list of positions.
        def entry(i, j):
            if (i, j) in symbol_locations:
                return diofant.Symbol('x')
            return big_mat[i, j]
        self.A = diofant.Matrix(n, n, entry)

    def time_dense_multiply(self, n, num_symbols):
        self.A * self.A

    def time_dense_add(self, n, num_symbols):
        self.A + self.A
