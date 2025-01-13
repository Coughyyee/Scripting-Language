from frontend.syntax_tree import AssignmentExpr, BinaryExpr, Identifier, ObjectLiteral
from runtime.environment import Environment
from runtime.values import MK_NULL, MK_NUMBER, NumberVal, ObjectVal, RuntimeVal


def eval_numeric_binary_expr(
    leftHandSide: NumberVal, rightHandSide: NumberVal, operator: str
) -> NumberVal:
    result: float = 0
    if operator == "+":
        result = leftHandSide.value + rightHandSide.value
    elif operator == "-":
        result = leftHandSide.value - rightHandSide.value
    elif operator == "*":
        result = leftHandSide.value * rightHandSide.value
    elif operator == "/":
        # TODO: Division by zero checks
        result = leftHandSide.value / rightHandSide.value
    elif operator == "%":
        result = leftHandSide.value % rightHandSide.value

    return MK_NUMBER(result)


def eval_binary_expr(binop: BinaryExpr, env: Environment) -> RuntimeVal:
    from runtime.interpreter import evaluate

    leftHandSide = evaluate(binop.left, env)
    rightHandSide = evaluate(binop.right, env)

    if leftHandSide.type == "number" and rightHandSide.type == "number":
        return eval_numeric_binary_expr(leftHandSide, rightHandSide, binop.operator)

    # One or both are NULL
    return MK_NULL()


def eval_identifier(ident: Identifier, env: Environment) -> RuntimeVal:
    val = env.lookup_var(ident.symbol)
    return val


def eval_assignment(node: AssignmentExpr, env: Environment) -> RuntimeVal:
    from runtime.interpreter import evaluate

    if node.assigne.kind != "Identifier":
        raise ValueError(f"Invalid LHS inaide assignment expr {node.assigne}")

    if isinstance(node.assigne, Identifier):
        varname = node.assigne.symbol
    return env.assign_var(varname, evaluate(node.value, env))


def eval_object_expr(obj_lit: ObjectLiteral, env: Environment) -> RuntimeVal:
    from runtime.interpreter import evaluate

    obj = ObjectVal({})
    for prop in obj_lit.properties:
        key = prop.key
        value = prop.value
        # { foo } == { foo: foo }
        runtime_val = env.lookup_var(key) if value is None else evaluate(value, env)

        obj.properties[key] = runtime_val

    return obj
