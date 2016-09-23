import unittest
from nineml.abstraction.expressions.base import (ExpressionWithLHS, ExpressionWithSimpleLHS, Expression)
from nineml.utils.testing.comprehensive import instances_of_all_types
from nineml.exceptions import (NineMLRuntimeError)


class TestExpressionWithLHSExceptions(unittest.TestCase):

    def test_lhs_name_transform_inplace_notimplementederror(self):
        """
        line #: 447
        message: 

        context:
        --------
    def lhs_name_transform_inplace(self, name_map):
        """

        expressionwithlhs = next(instances_of_all_types['ExpressionWithLHS'].itervalues())
        self.assertRaises(
            NotImplementedError,
            expressionwithlhs.lhs_name_transform_inplace,
            name_map=None)

    def test_lhs_atoms_notimplementederror(self):
        """
        line #: 451
        message: 

        context:
        --------
    def lhs_atoms(self):
        """

        expressionwithlhs = next(instances_of_all_types['ExpressionWithLHS'].itervalues())
        with self.assertRaises(NotImplementedError):
            print expressionwithlhs.lhs_atoms


class TestExpressionWithSimpleLHSExceptions(unittest.TestCase):

    def test___init___ninemlruntimeerror(self):
        """
        line #: 470
        message: err

        context:
        --------
    def __init__(self, lhs, rhs, assign_to_reserved=False):
        ExpressionWithLHS.__init__(self, rhs)
        if not is_single_symbol(lhs):
            err = 'Expecting a single symbol on the LHS; got: %s' % lhs
        """

        expressionwithsimplelhs = next(instances_of_all_types['ExpressionWithSimpleLHS'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            expressionwithsimplelhs.__init__,
            lhs=None,
            rhs=None,
            assign_to_reserved=False)

    def test___init___ninemlruntimeerror2(self):
        """
        line #: 473
        message: err

        context:
        --------
    def __init__(self, lhs, rhs, assign_to_reserved=False):
        ExpressionWithLHS.__init__(self, rhs)
        if not is_single_symbol(lhs):
            err = 'Expecting a single symbol on the LHS; got: %s' % lhs
            raise NineMLRuntimeError(err)
        if not assign_to_reserved and not is_valid_lhs_target(lhs):
            err = 'Invalid LHS target: %s' % lhs
        """

        expressionwithsimplelhs = next(instances_of_all_types['ExpressionWithSimpleLHS'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            expressionwithsimplelhs.__init__,
            lhs=None,
            rhs=None,
            assign_to_reserved=False)


class TestExpressionExceptions(unittest.TestCase):

    def test_nineml_expression_ninemlruntimeerror(self):
        """
        line #: 184
        message: Incorrect arguments provided to expression ('{}'): '{}'


        context:
        --------
    def rhs_as_python_func(self):
        \"\"\" Returns a python callable which evaluates the expression in
        namespace and returns the result \"\"\"
        def nineml_expression(**kwargs):
            if isinstance(self.rhs, (bool, int, float, BooleanTrue,
                                     BooleanFalse)):
                val = self.rhs
            else:
                if self.rhs.is_Boolean:
                    try:
                        val = self.rhs.subs(kwargs)
                    except Exception:
        """

        expression = next(instances_of_all_types['Expression'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print expression.rhs_as_python_func()

    def test_nineml_expression_ninemlruntimeerror2(self):
        """
        line #: 193
        message: Incorrect arguments provided to expression '{}': '{}' (expected '{}')


        context:
        --------
    def rhs_as_python_func(self):
        \"\"\" Returns a python callable which evaluates the expression in
        namespace and returns the result \"\"\"
        def nineml_expression(**kwargs):
            if isinstance(self.rhs, (bool, int, float, BooleanTrue,
                                     BooleanFalse)):
                val = self.rhs
            else:
                if self.rhs.is_Boolean:
                    try:
                        val = self.rhs.subs(kwargs)
                    except Exception:
                        raise NineMLRuntimeError(
                            "Incorrect arguments provided to expression ('{}')"
                            ": '{}'\n".format(
                                "', '".join(self.rhs_symbol_names),
                                "', '".join(kwargs.keys())))
                else:
                    try:
                        val = self.rhs.evalf(subs=kwargs)
                    except Exception:
        """

        expression = next(instances_of_all_types['Expression'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print expression.rhs_as_python_func()

    def test_nineml_expression_ninemlruntimeerror3(self):
        """
        line #: 207
        message: Could not evaluate expression: {}

        context:
        --------
    def rhs_as_python_func(self):
        \"\"\" Returns a python callable which evaluates the expression in
        namespace and returns the result \"\"\"
        def nineml_expression(**kwargs):
            if isinstance(self.rhs, (bool, int, float, BooleanTrue,
                                     BooleanFalse)):
                val = self.rhs
            else:
                if self.rhs.is_Boolean:
                    try:
                        val = self.rhs.subs(kwargs)
                    except Exception:
                        raise NineMLRuntimeError(
                            "Incorrect arguments provided to expression ('{}')"
                            ": '{}'\n".format(
                                "', '".join(self.rhs_symbol_names),
                                "', '".join(kwargs.keys())))
                else:
                    try:
                        val = self.rhs.evalf(subs=kwargs)
                    except Exception:
                        raise NineMLRuntimeError(
                            "Incorrect arguments provided to expression '{}'"
                            ": '{}' (expected '{}')\n".format(
                                self.rhs,
                                "', '".join(kwargs.keys()),
                                "', '".join(self.rhs_symbol_names)))
                    try:
                        val = float(val)
                    except TypeError:
                        try:
                            locals_dict = deepcopy(kwargs)
                            locals_dict.update(str_to_npfunc_map)
                            val = eval(str(val), {}, locals_dict)
                        except Exception:
        """

        expression = next(instances_of_all_types['Expression'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print expression.rhs_as_python_func()

