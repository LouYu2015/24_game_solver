import itertools
import time

# Operators
OP_CONST = 0
OP_ADD = 1
OP_SUB = 2
OP_MUL = 3
OP_DIV = 4
OP_POW = 5

operators = [OP_ADD,
             OP_SUB,
             OP_MUL,
             OP_DIV]

symbol_of_operator = {OP_ADD: "+",
                      OP_SUB: "-",
                      OP_MUL: "*",
                      OP_DIV: "/",
                      OP_POW: "^"}

priority_of_operator = {OP_ADD: 0,
                        OP_SUB: 0,
                        OP_MUL: 1,
                        OP_DIV: 1,
                        OP_POW: 2,
                        OP_CONST: 3}

is_operator_commutative = {OP_ADD: True,
                           OP_SUB: False,
                           OP_MUL: True,
                           OP_DIV: False,
                           OP_POW: False}


def evaluate_operation(op, a, b):
    if op == OP_ADD: return a + b
    if op == OP_SUB: return a - b
    if op == OP_MUL: return a * b

    try:
        if op == OP_POW: return a ** b
        if op == OP_DIV: return a / b
    except ZeroDivisionError:
        return float("NaN")


class Node:
    def __init__(self, value=None, left=None, right=None, op=OP_CONST):
        if op != OP_CONST and is_operator_commutative[op] \
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
            self._value = evaluate_operation(self.op, self.left.value, self.right.value)
        return self._value

    def __str__(self):
        if self.op == OP_CONST:
            return str(self._value)
        else:
            str_left = str(self.left)
            str_right = str(self.right)

            if priority_of_operator[self.left.op] < priority_of_operator[self.op]:
                str_left = "(" + str_left + ")"
            # str_left = "(" + str_left + ")"

            if priority_of_operator[self.right.op] < priority_of_operator[self.op] \
                or (priority_of_operator[self.right.op] == priority_of_operator[self.op]
                    and not is_operator_commutative[self.op]):
                str_right = "(" + str_right + ")"
            # str_right = "(" + str_right + ")"

            return str_left + symbol_of_operator[self.op] + str_right

    def str2(self):
        if self.op == OP_CONST:
            return str(self._value)
        else:
            str_left = self.left.str2()
            str_right = self.right.str2()

            str_left = "(" + str_left + ")"
            str_right = "(" + str_right + ")"

            return str_left + symbol_of_operator[self.op] + str_right


def enumerate_nodes(node_list, callback):
    if len(node_list) == 1:
        callback(node_list[0])

    for left, right in itertools.permutations(node_list, 2):
        new_node_list = node_list.copy()
        new_node_list.remove(left)
        new_node_list.remove(right)

        for op in operators:
            enumerate_nodes(new_node_list + [Node(left=left, right=right, op=op)], callback)

            if not is_operator_commutative[op] and str(left) != str(right):
                enumerate_nodes(new_node_list + [Node(left=right, right=left, op=op)], callback)


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
    if select_yes_no("Allow power operator?"):
        operators.append(OP_POW)
        print("Power operator enabled")
    else:
        print("Power operator disabled")

    print()

    enumerate_all = select_yes_no("Enumerate all target?")
    if enumerate_all:
        callback = CallbackAllTarget()
        print("Enumerate all targets")
    else:
        print("Just solve one target")

    print()

    target = 24

    while True:
        print("--------------------")
        if not enumerate_all:
            target = select_int("Enter a target:", default=target)
            callback = CallbackFindTarget(target=target)

            print("Target is %d" % target)
            print()

        inputs = [int(i) for i in input("Enter some numbers:").split(" ")]
        node_list = [Node(value=i) for i in inputs]

        print()
        start_time = time.time()
        enumerate_nodes(node_list, callback)
        end_time = time.time()

        callback.show(execution_time=end_time - start_time)

main()
