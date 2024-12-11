"""
This module contains helping function for the derivation of the formulas for the cross section processors.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2024 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.

## Libs
import re

from IPython.core.display_functions import display
from sympy import Symbol, Matrix, linear_eq_to_matrix, latex, Function
from sympy.printing.pycode import pycode

from PreDoCS.util.Logging import get_module_logger
log = get_module_logger(__name__)


## Functions

def get_coefficients(expr, args):
    ## Gibt die Koeffizientenliste von expr für args zurück. Der Rest ist residual. args nach Exponent ansteigend geordnet.
    coeffs = []
    residual = expr.expand()
    for i in range(len(args)):
        arg = args[i]
        c = residual.coeff(arg)
        coeffs.append(c)
        residual = residual - arg*c
    return coeffs, residual.simplify()


def get_coefficients_square(expr, args):
    ## Gibt die Koeffizientenliste von expr für args zurück. Der Rest ist residual. args nach Exponent ansteigend geordnet.
    coeff_matrix = []
    residual = expr
    for i in range(len(args)):
        row = []
        for j in range(len(args)):
            arg = args[i] * args[j]
            c = residual.coeff(arg)
            row.append(c)
            residual = residual - arg*c
        coeff_matrix.append(row)
    return coeff_matrix, residual.simplify()


def get_coefficients_matrix(expressions, args):
    ## Gibt die Koeffizientenliste von expr für args zurück. Der Rest ist residual. args nach Exponent ansteigend geordnet.
    res = []
    for expr in expressions:
        coeffs, residual = get_coefficients(expr, args)
        assert residual == 0
        res.append(coeffs)
    return Matrix(res)


def get_symbols_matrix_symmetric(size, prefix):
    res = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(Symbol('{}_{}_{}'.format(prefix, i, j)))
        res.append(row)
    return Matrix(res)


def get_functions_matrix(shape, prefix, parameter):
    res = []
    for i in range(shape[0]):
        row = []
        for j in range(shape[1]):
            row.append(Function('{}_{}{}'.format(prefix, i+1, j+1))(parameter))
        res.append(row)
    return Matrix(res)


def linear_equation_to_coeff_matrix(equations, x, b):
    ## A x = b
    A, a = linear_eq_to_matrix([eq.expand() for eq in equations], b)
    D = Matrix(get_coefficients_matrix(a, x))
    return A * D


def get_matrix_coefficient_strings(coeffs, half=True, convert_method='latex', simplify=False, prefix_format_string='M_{{{}{}}} = '):
    res = []
    for r in range(coeffs.shape[0]):
        if half:
            cols = range(r, coeffs.shape[1])
        else:
            cols = range(coeffs.shape[1])
        for c in cols:
            coeff = coeffs[r, c].simplify() if simplify else coeffs[r, c]
            prefix = prefix_format_string.format(r+1, c+1)
            if convert_method == 'latex':
                res.append(prefix+latex(coeff))
            else:
                res.append(prefix+str(coeff))
    return res


def print_matrix_coefficients(coeffs, convert_method, half=True, prefix='', simplify=False, prefix_format_string=None):
    if prefix_format_string is None:
        prefix_format_string = prefix+'{{{}{}}} = '
    
    if convert_method == 'display':
        for r in range(coeffs.shape[0]):
            if half:
                cols = range(r, coeffs.shape[1])
            else:
                cols = range(coeffs.shape[1])
            for c in cols:
                coeff = coeffs[r, c].simplify() if simplify else coeffs[r, c]
                print(prefix_format_string.format(r+1, c+1))
                display(coeff)
    elif convert_method == 'latex':
        strings = get_matrix_coefficient_strings(coeffs, half=half, convert_method='latex', simplify=simplify, prefix_format_string=prefix_format_string)
        for string in strings:
            print(string+r' \\')
    else:
        strings = get_matrix_coefficient_strings(coeffs, half=half, convert_method='print', simplify=simplify, prefix_format_string=prefix_format_string)
        for string in strings:
            print(string)


################# 1D FEM #####################


def get_node_vectors(shape_functions, prefix, num_additional_dof=0):
    node_dof = []
    node_beam_dof = []
    node_dof_with_shape_function = []
    for i in range(len(shape_functions)):
        shape_function = shape_functions[i]
        beam_dof = []
        for j in range(len(shape_function)):
            new_symbol = Symbol('{}_{}_{}'.format(prefix, i, j))
            beam_dof.append(new_symbol)
            node_dof.append(new_symbol)
        node_beam_dof.append(beam_dof)
        node_dof_with_shape_function.append(Matrix(beam_dof).dot(Matrix(shape_function)))
    for i in range(num_additional_dof):
        new_symbol = Symbol('{}_add_{}'.format(prefix, i))
        node_dof.append(new_symbol)
    return node_dof, node_beam_dof, Matrix(node_dof_with_shape_function)


def get_coefficients_matrix_with_residual(expressions, args):
    ## Gibt die Koeffizientenliste von expr für args zurück. Der Rest ist residual. args nach Exponent ansteigend geordnet.
    res = []
    res_residual = []
    for expr in expressions:
        coeffs, residual = get_coefficients(expr, args)
        res_residual.append(residual)
        res.append(coeffs)
    return Matrix(res), Matrix(res_residual)


def get_symbols_matrix(size, prefix):
    res = []
    for i in range(size[0]):
        row = []
        for j in range(size[1]):
            row.append(Symbol('{}_{}{}'.format(prefix, i+1, j+1)))
        res.append(row)
    return Matrix(res)


def matrix_operation(matrix, operation):
    result_matrix = []
    for r in range(matrix.shape[0]):
        row = []
        for c in range(matrix.shape[1]):
            row.append(operation(matrix[r,c]))
        result_matrix.append(row)
    return Matrix(result_matrix)


def do_matrix_integration(matrix):
    return matrix_operation(matrix, lambda e: e.expand().doit(manual=True))


def matrix_simplify(matrix):
    return matrix_operation(matrix, lambda e: e.simplify())


def get_symbols_from_matrix(matrix, symbol_type=Symbol):
    sym = set()
    _ = matrix_operation(matrix, lambda e: sym.update(e.atoms(symbol_type)))
    return sym


def matrix_substitutions(matrix, prefix):
    res = {}
    for r in range(matrix.shape[0]):
        row = {}
        for c in range(matrix.shape[1]):
            element = matrix[r,c]
            if not element.equals(0):
                row[element] = Symbol('{}_{}{}'.format(prefix, r+1, c+1))
        res.update(row)
    return res


def repl(matchobj, prefix, with_idx, subs_matrices_as_dict=False):
    idx = int(matchobj.group(1)) - 11
    idx1 = idx // 10
    idx2 = idx - idx1*10
    if subs_matrices_as_dict:
        return '{}[{}{}]'.format(prefix, idx1+1, idx2+1)
    else:
        if with_idx:
            return '{}[idx({}{})]'.format(prefix, idx1+1, idx2+1)
        else:
            return '{}[{},{}]'.format(prefix, idx1, idx2)


def symbols_matrix_to_python_code(
        matrix,
        matrix_name,
        summarization,
        matrix_substitutions=None,
        intent=3,
        full_matrix=True,
        with_idx=False,
        subs_matrices_as_dict=False,
        simplify=False,
        write_zero_terms=False,
):
    if matrix_substitutions is None:
        matrix_substitutions = {}

    if summarization:
        equal_symbol = '+='
    else:
        equal_symbol = '='

    intent_string = ''
    for i in range(intent):
        intent_string += '    '

    res = ''
    for r in range(matrix.shape[0]):
        if full_matrix:
            cols = range(matrix.shape[1])
        else:
            cols = range(r, matrix.shape[1])
        for c in cols:
            term = matrix[r, c]
            if simplify:
                term = term.simplify()

            if term == 0:
                if write_zero_terms:
                    if with_idx:
                        res += intent_string + '#{}[idx({},{})] {} 0\n'.format(matrix_name, r + 1, c + 1, equal_symbol)
                    else:
                        res += intent_string + '#{}[{},{}] {} 0\n'.format(matrix_name, r, c, equal_symbol)
            else:
                s = pycode(term, strict=False)

                for k, v in matrix_substitutions.items():
                    p = re.compile(k + r'([1-9]{2})')
                    s = p.sub(lambda matchobj: repl(matchobj, v, with_idx, subs_matrices_as_dict=subs_matrices_as_dict), s)

                #s = s.replace('^', '**')

                if with_idx:
                    res += intent_string + '{}[idx({}{})] {} {}\n'.format(matrix_name, r + 1, c + 1, equal_symbol, s)
                else:
                    res += intent_string + '{}[{},{}] {} {}\n'.format(matrix_name, r, c, equal_symbol, s)

    return res
