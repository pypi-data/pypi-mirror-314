from dataclasses import dataclass, KW_ONLY
from helpers.maths.types import Matrix, Vector

import sympy as sp

from sympy import latex
from IPython.display import Math, display


@dataclass(frozen=True)
class FormattingContext:
    _: KW_ONLY
    m: int
    n: int
    start_limit: int
    end_limit: int
    precision: int
    hide_small_values: bool
    v_dots: sp.Symbol
    c_dots: sp.Symbol
    d_dots: sp.Symbol

    @property
    def limit(self) -> int:
        return self.start_limit + self.end_limit

    @staticmethod
    def create_for(
        matrix: Matrix,
        *,
        start_limit: int,
        end_limit: int,
        precision: int,
        hide_small_values: bool,
    ) -> "FormattingContext":
        return FormattingContext(
            m=matrix.shape[0],
            n=matrix.shape[1],
            start_limit=start_limit,
            end_limit=end_limit,
            precision=precision,
            hide_small_values=hide_small_values,
            v_dots=sp.symbols(r"\vdots"),
            c_dots=sp.symbols(r"\cdots"),
            d_dots=sp.symbols(r"\ddots"),
        )


def truncate(matrix: Matrix, *, context: FormattingContext) -> sp.Matrix:
    m, n = matrix.shape
    start_limit = context.start_limit
    end_limit = context.end_limit

    if m <= context.limit and n <= context.limit:
        return sp.Matrix(matrix)

    rows = list(matrix[:start_limit])
    if m > context.limit:
        rows.extend(matrix[-end_limit:])

    result = sp.Matrix(rows)

    if n > context.limit:
        result = result.extract(
            [i for i in range(result.rows)],
            list(range(start_limit)) + list(range(n - end_limit, n)),
        )

    return result


def extend_horizontally(matrix: sp.Matrix, *, context: FormattingContext) -> sp.Matrix:
    m = context.m
    start_limit, limit = context.start_limit, context.limit
    v_dots = context.v_dots

    if m > limit:
        columns = matrix.shape[1]
        matrix = matrix.row_insert(
            start_limit, sp.Matrix([[v_dots for _ in range(columns)]])
        )

    return matrix


def extend_vertically(matrix: sp.Matrix, *, context: FormattingContext) -> sp.Matrix:
    n = context.n
    start_limit, limit = context.start_limit, context.limit
    c_dots = context.c_dots

    if n > limit:
        rows = matrix.shape[0]
        matrix = matrix.col_insert(
            start_limit, sp.Matrix([c_dots for _ in range(rows)])
        )

    return matrix


def extend_diagonally(matrix: sp.Matrix, *, context: FormattingContext) -> sp.Matrix:
    m, n = context.m, context.n
    start_limit, limit = context.start_limit, context.limit
    d_dots = context.d_dots

    if m > limit and n > limit:
        matrix[start_limit, start_limit] = d_dots

    return matrix


def format_numbers(matrix: sp.Matrix, *, context: FormattingContext) -> sp.Matrix:
    precision = context.precision

    def format_entry(entry: sp.Expr) -> sp.Symbol | float | str:
        if isinstance(entry, sp.Symbol):
            return entry

        number = float(entry)
        if abs(number) < 1e-3 and number != 0:
            return 0 if context.hide_small_values else f"{number:.{precision}e}"
        else:
            return f"{number:.{precision}f}"

    return sp.Matrix(
        [[format_entry(value) for value in row] for row in matrix.tolist()]
    )


def pretty_latex(
    value: Vector | Matrix,
    start_limit: int = 5,
    end_limit: int = 5,
    precision: int = 3,
    hide_small_values: bool = True,
) -> str:
    """Generates a pretty LaTeX representation of the given vector or matrix.

    This is what [`pretty`](#helpers.maths.pretty) uses to generate the LaTeX representation.
    """
    if value.ndim == 1:
        value = value.reshape(-1, 1)

    context = FormattingContext.create_for(
        value,
        start_limit=start_limit,
        end_limit=end_limit,
        precision=precision,
        hide_small_values=hide_small_values,
    )

    symbolic = truncate(value, context=context)
    symbolic = extend_horizontally(symbolic, context=context)
    symbolic = extend_vertically(symbolic, context=context)
    symbolic = extend_diagonally(symbolic, context=context)
    symbolic = format_numbers(symbolic, context=context)

    return latex(symbolic)


def pretty(
    value: Vector | Matrix,
    *,
    start_limit: int = 5,
    end_limit: int = 5,
    precision: int = 3,
    hide_small_values: bool = True,
) -> None:
    """Pretty prints the given vector or matrix using LaTeX.

    Args:
        value: The vector or matrix to print.
        start_limit: The number of rows and columns to show at the beginning of the matrix.
        end_limit: The number of rows and columns to show at the end of the matrix.
        precision: The number of decimal places to show for each number.
        hide_small_values: Whether to hide small values in scientific notation, i.e. replace them with 0.

    Example:
        ```python
        import numpy as np
        from helpers.maths import pretty

        matrix = np.random.rand(100, 100)
        pretty(matrix)
        # This will display the first and last 5 rows and columns of the matrix.
        ```
    """
    display(
        Math(
            pretty_latex(
                value,
                start_limit=start_limit,
                end_limit=end_limit,
                precision=precision,
                hide_small_values=hide_small_values,
            )
        )
    )
