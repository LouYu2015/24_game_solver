import itertools
import time
import math

# Operators
OP_CONST = 0  # Constant
OP_ADD = 1  # Addition
OP_SUB = 2  # Subtraction
OP_MUL = 3  # Multiplication
OP_DIV = 4  # Divition
OP_POW = 5  # Exponentiation

OP_SQRT = 6  # Squreroot
OP_FACT = 7  # Factorial
OP_LOG = 8  # Logarithm
OP_C = 9  # Combinations
OP_P = 10  # Permutations

# List of basic operators
operators = [OP_ADD,
             OP_SUB,
             OP_MUL,
             OP_DIV]

# List of advanced operators
advanced_operators = [OP_POW,
                      OP_LOG,
                      OP_C,
                      OP_P]

# List of unary operators
_unary_operators = [OP_SQRT,
                    OP_FACT]

# List of enabled unary operators
unary_operators = []

# Symbol of operators
symbol_of_operator = {OP_ADD: "%s+%s",
                      OP_SUB: "%s-%s",
                      OP_MUL: "%s*%s",
                      OP_DIV: "%s/%s",
                      OP_POW: "%s^%s",
                      OP_SQRT: "sqrt(%s)",
                      OP_FACT: "%s!",
                      OP_LOG: "log_%s(%s)",
                      OP_C: "C(%s, %s)",
                      OP_P: "P(%s, %s)"}

# Priority of operators
priority_of_operator = {OP_ADD: 0,
                        OP_SUB: 0,
                        OP_MUL: 1,
                        OP_DIV: 1,
                        OP_POW: 2,
                        OP_LOG: 3,
                        OP_C: 3,
                        OP_P: 3,
                        OP_SQRT: 3,
                        OP_FACT: 4,
                        OP_CONST: 5}

# Whether operator is commutative
is_operator_commutative = {OP_ADD: True,
                           OP_SUB: False,
                           OP_MUL: True,
                           OP_DIV: False,
                           OP_POW: False,
                           OP_LOG: False,
                           OP_C: False,
                           OP_P: False}

# Whether inside bracket is needed when rendering
need_brackets = {OP_ADD: True,
                 OP_SUB: True,
                 OP_MUL: True,
                 OP_DIV: True,
                 OP_POW: True,
                 OP_FACT: True,
                 OP_SQRT: False,
                 OP_LOG: False,
                 OP_C: False,
                 OP_P: False}


def permutation(n, k):
    return math.factorial(n)/math.factorial(k)


def combination(n, k):
    return permutation(n, k)/math.factorial(n-k)


def evaluate_operation(op, a, b=None):
	"""
	Evaluate an operation on a and b.
	"""
    if op == OP_ADD: return a + b
    if op == OP_SUB: return a - b
    if op == OP_MUL: return a * b

    try:
        if op == OP_POW and abs(a) < 20 and abs(b) < 20:
            return a ** b

        if op == OP_FACT and a < 10:
            return math.factorial(a)

        if op == OP_C and 0 < b <= a <= 13:
            return combination(a, b)

        if op == OP_P and 0 < b <= a <= 13:
            return permutation(a, b)

        if op == OP_SQRT and a < 1000000:
            return math.sqrt(a)

        if op == OP_DIV: return a / b
        if op == OP_LOG: return math.log(b, a)
    except (ZeroDivisionError, ValueError, TypeError):
        pass
    except OverflowError:
        print(a, b)

    return float("NaN")


def fit_to_int(x, eps=1e-9):
	"""
	Convert x to int if x is close to an integer.
	"""
    try:
        if abs(round(x) - x) <= eps:
            return round(x)
        else:
            return x
    except ValueError:
        return float("NaN")
    except TypeError:
        return float("NaN")


class Node:
    def __init__(self, value=None, left=None, right=None, op=OP_CONST):
        if op not in unary_operators \
                and op != OP_CONST and is_operator_commutative[op] \
                and str(left) > str(right):
            left, right = right, left

        self._value = value
        self._str_cache = None
        self.left = left
        self.right = right
        self.op = op

    @property
    def value(self):
        if self._value is None:
            assert self.op != OP_CONST

            if self.op in unary_operators:
                self._value = evaluate_operation(self.op, self.left.value)
            else:
                self._value = evaluate_operation(self.op, self.left.value, self.right.value)

            self._value = fit_to_int(self._value)
        return self._value

    def __str__(self):
    	if self._str_cache is None:
    		self._str_cache = self._str()
    	return self._str_cache

    def _str(self):
    	# Constant
        if self.op == OP_CONST:
            return str(self._value)

        # Unary operator
        elif self.op in unary_operators:
            str_left = str(self.left)

            if need_brackets[self.op] \
            		and priority_of_operator[self.left.op] < priority_of_operator[self.op]:
                str_left = "(" + str_left + ")"

            return symbol_of_operator[self.op] % str_left

        # Other operator
        else:
            str_left = str(self.left)
            str_right = str(self.right)

            # Add brackets inside
            if need_brackets[self.op] \
            		and priority_of_operator[self.left.op] < priority_of_operator[self.op]:
                str_left = "(" + str_left + ")"

            if need_brackets[self.op] \
            		and (priority_of_operator[self.right.op] < priority_of_operator[self.op] \
                	or (priority_of_operator[self.right.op] == priority_of_operator[self.op]
                    and not is_operator_commutative[self.op])):
                str_right = "(" + str_right + ")"

            # Render
            return symbol_of_operator[self.op] % (str_left, str_right)


def enumerate_nodes(node_list, callback, max_depth):
	# Found an expression
    if len(node_list) == 1:
        callback(node_list[0])

    # Constrain maximum depth
    if max_depth == 0:
        return

    # Non-unary operators
    for left, right in itertools.permutations(node_list, 2):
        new_node_list = node_list.copy()
        new_node_list.remove(left)
        new_node_list.remove(right)

        for op in operators:
            enumerate_nodes(new_node_list + [Node(left=left, right=right, op=op)], callback, max_depth-1)

            if not is_operator_commutative[op] and str(left) != str(right):
                enumerate_nodes(new_node_list + [Node(left=right, right=left, op=op)], callback, max_depth-1)

    # Unary operators
    for number in node_list:
        new_node_list = node_list.copy()
        new_node_list.remove(number)

        for op in unary_operators:
            new_node = Node(left=number, op=op)
            if new_node.value == number.value:
                continue

            enumerate_nodes(new_node_list + [new_node], callback, max_depth-1)

class CallbackFindTarget:
    def __init__(self, target):
        self.target = target
        self.results = []
        self.duplication_count = 0
        self.enumeration_count = 0

    def __call__(self, node):
        if node.value == self.target and str(node) not in self.results:
            print(self.target, "=", node)
            self.results.append(str(node))
        elif node.value == self.target:
            self.duplication_count += 1

        self.enumeration_count += 1

    def show(self, execution_time):
        print()
        print("%d solution(s) in %.3f seconds" % (len(self.results), execution_time))
        print("%d duplication(s)" % self.duplication_count)
        print("%d combination(s)" % self.enumeration_count)


class CallbackAllTarget:
    def __init__(self):
        self.results = {}
        self.enumeration_count = 0

    def __call__(self, node):
        try:
            int(node.value)
        except ValueError:
            return

        if node.value not in self.results \
                and int(node.value) == node.value:
            self.results[node.value] = node

        self.enumeration_count += 1

    def __str__(self):
        string = ""
        for value in sorted(self.results.keys()):
            string += "%d = %s" % (value, str(self.results[value]))
            string += "\n"
        return string

    def show(self, execution_time):
        print(self)
        print()
        print("%d targets(s) in %.3f seconds" % (len(self.results), execution_time))
        print("%d combination(s)" % self.enumeration_count)


def select_yes_no(prompt, default=False):
    answer = input(prompt).strip().lower()
    if answer == "y":
        return True
    if answer == "n":
        return False
    return default


def select_int(prompt, default):
    try:
        return int(input(prompt).strip())
    except ValueError:
        return default


def main():
    global operators
    global unary_operators

    if select_yes_no("Allow advanced operators?"):
        operators += advanced_operators
        print("Advanced operators enabled")
    else:
        print("Advanced operators disabled")

    print()

    if select_yes_no("Allow unary operator?"):
        unary_operators += _unary_operators
        print("Unary operator enabled")

        print()

        unary_operators_allowed = select_int("Number of unary operators allowed:", default=1)
        print("%d unary operators allowed" % unary_operators_allowed)
    else:
        print("Unary operator disabled")

        unary_operators_allowed = 0

    print()

    enumerate_all = select_yes_no("Enumerate all target?")
    if enumerate_all:
        print("Solve all targets")
    else:
        print("Just solve one target")

    print()

    if not enumerate_all:
        target = select_int("Enter a target:", default=24)
        callback = CallbackFindTarget(target=target)

        print("Target is %d" % target)
        print()

    while True:
        print("--------------------")

        if enumerate_all:
            callback = CallbackAllTarget()
        else:
            callback = CallbackFindTarget(target=target)

        inputs = [int(i) for i in input("Enter some numbers:").split(" ")
        		  if i != ""]
        node_list = [Node(value=i) for i in inputs]

        print()
        start_time = time.time()
        enumerate_nodes(node_list, callback, max_depth=len(node_list)-1+unary_operators_allowed)
        end_time = time.time()

        callback.show(execution_time=end_time - start_time)

main()
