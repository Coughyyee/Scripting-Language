from runtime.values import RuntimeVal


"""IDK if i should keep it as ValueError(..) or not."""


class Environment:
    def __init__(self, parent_env=None):
        self._parent = parent_env
        self._variables = {}

    def declare_var(self, varname: str, value: RuntimeVal) -> RuntimeVal:
        if varname in self._variables:
            raise ValueError(
                f"Cannot declare variable {varname} as it is already defined."
            )

        self._variables[varname] = value
        return value

    def assign_var(self, varname: str, value: RuntimeVal) -> RuntimeVal:
        env = self.resolve(varname)
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