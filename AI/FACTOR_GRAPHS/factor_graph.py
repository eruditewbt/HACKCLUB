from collections import defaultdict


class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = list(domain)

    def __repr__(self):
        return f"Variable(name={self.name!r}, domain={self.domain!r})"


class Factor:
    """
    Discrete factor over variables with a table:
    table: dict[tuple(values)] -> weight
    Order is the same as self.vars.
    """

    def __init__(self, name, vars, table):
        self.name = name
        self.vars = list(vars)
        self.table = dict(table)

    def __repr__(self):
        return f"Factor(name={self.name!r}, vars={[v.name for v in self.vars]!r})"


class FactorGraph:
    def __init__(self):
        self.variables = {}
        self.factors = {}
        self.var_to_factors = defaultdict(list)

    def add_variable(self, var):
        self.variables[var.name] = var
        return var

    def add_factor(self, factor):
        self.factors[factor.name] = factor
        for v in factor.vars:
            self.var_to_factors[v.name].append(factor.name)
        return factor

    def neighbors_of_var(self, var_name):
        return list(self.var_to_factors.get(var_name, []))


