from runtime.values import MK_BOOL, MK_NULL, RuntimeVal


class Environment:
    def __init__(self, parent_env=None):
        self._parent = parent_env
        self._variables: dict[str, RuntimeVal] = {}
        self._constants: set[str] = set()

    def declare_var(
        self, varname: str, value: RuntimeVal, constant: bool
    ) -> RuntimeVal:
        if varname in self._variables:
            raise ValueError(
                f"Cannot declare variable {varname} as it is already defined."
            )

        self._variables[varname] = value
        if constant:
            self._constants.add(varname)
        return value

    def assign_var(self, varname: str, value: RuntimeVal) -> RuntimeVal:
        env = self.resolve(varname)

        # Cannot assign to constatn
        if varname in env._constants:
            raise ValueError(
                f"Cannot reassign to variable {varname} as it was declared as constant."
            )

        env._variables[varname] = value
        return value

    def lookup_var(self, varname: str) -> RuntimeVal:
        env = self.resolve(varname)
        return env._variables[varname]

    def resolve(self, varname: str) -> "Environment":
        if varname in self._variables:
            return self

        if self._parent is None:
            raise ValueError(f"Cannot resolve <{varname}> as it does not exist.")

        return self._parent.resolve(varname)


def create_global_env() -> Environment:
    env = Environment()

    env.declare_var("true", MK_BOOL(True), True)
    env.declare_var("false", MK_BOOL(False), False)
    env.declare_var("null", MK_NULL(), True)

    return env
