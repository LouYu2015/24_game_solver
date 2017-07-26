import itertools
import time
import math

# Operators
OP_CONST = 0
OP_ADD = 1
OP_SUB = 2
OP_MUL = 3
OP_DIV = 4
OP_POW = 5

OP_SQRT = 6
OP_FACT = 7
OP_LOG = 8
OP_C = 9
OP_P = 10


operators = [OP_ADD,
             OP_SUB,
             OP_MUL,
             OP_DIV]

advanced_operators = [OP_POW,
                      OP_LOG,
                      OP_C,
                      OP_P]

_unary_operators = [OP_SQRT,
                    OP_FACT]

unary_operators = []

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

priority_of_operator = {OP_ADD: 0,
                        OP_SUB: 0,
                        OP_MUL: 1,
                        OP_DIV: 1,
                        OP_POW: 2,
                        OP_FACT: 3,
                        OP_SQRT: 4,
                        OP_LOG: 4,
                        OP_C: 4,
                        OP_P: 4,
                        OP_CONST: 5}

is_operator_commutative = {OP_ADD: True,
                           OP_SUB: False,
                           OP_MUL: True,
                           OP_DIV: False,
                           OP_POW: False,
                           OP_LOG: False,
                           OP_C: False,
                           OP_P: False}


def evaluate_operation(op, a, b=None):
    if op == OP_ADD: return a + b
    if op == OP_SUB: return a - b
    if op == OP_MUL: return a * b

    try:
        if op == OP_POW and abs(a) < 20 and abs(b) < 20:
            return a ** b

        if op == OP_FACT and a < 10:
            return math.factorial(a)

        if op == OP_C and a >= b and a < 10:
            return len(set(itertools.combinations(range(a), b)))

        if op == OP_P and a >= b and a < 10:
            return len(set(itertools.permutations(range(a), b)))

        if op == OP_SQRT and a < 1000:
            return math.sqrt(a)

        if op == OP_DIV: return a / b
        if op == OP_LOG: return math.log(b, a)
    except (ZeroDivisionError, ValueError, TypeError):
        pass
    except OverflowError:
        print(a, b)

    return float("NaN")


def fit_to_int(x, eps=1e-9):
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
        if self.op == OP_CONST:
            return str(self._value)
        elif self.op in unary_operators:
            str_left = str(self.left)

            if priority_of_operator[self.left.op] < priority_of_operator[self.op]:
                str_left = "(" + str_left + ")"

            return symbol_of_operator[self.op] % str_left
        else:
            str_left = str(self.left)
            str_right = str(self.right)

            if priority_of_operator[self.left.op] < priority_of_operator[self.op]:
                str_left = "(" + str_left + ")"

            if priority_of_operator[self.right.op] < priority_of_operator[self.op] \
                or (priority_of_operator[self.right.op] == priority_of_operator[self.op]
                    and not is_operator_commutative[self.op]):
                str_right = "(" + str_right + ")"

            return symbol_of_operator[self.op] % (str_left, str_right)


def enumerate_nodes(node_list, callback, max_depth):
    if len(node_list) == 1:
        callback(node_list[0])

    if max_depth == 0:
        return

    for left, right in itertools.permutations(node_list, 2):
        new_node_list = node_list.copy()
        new_node_list.remove(left)
        new_node_list.remove(right)

        for op in operators:
            enumerate_nodes(new_node_list + [Node(left=left, right=right, op=op)], callback, max_depth-1)

            if not is_operator_commutative[op] and str(left) != str(right):
                enumerate_nodes(new_node_list + [Node(left=right, right=left, op=op)], callback, max_depth-1)

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
    answer = input(prompt).lower()
    if answer == "y":
        return True
    if answer == "n":
        return False
    return default


def select_int(prompt, default):
    try:
        return int(input(prompt))
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
    else:
        print("Unary operator disabled")

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

        inputs = [int(i) for i in input("Enter some numbers:").split(" ")]
        node_list = [Node(value=i) for i in inputs]

        print()
        start_time = time.time()
        enumerate_nodes(node_list, callback, max_depth=len(node_list))
        end_time = time.time()

        callback.show(execution_time=end_time - start_time)

main()
