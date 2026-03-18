from FACTOR_GRAPHS.factor_graph import Factor, FactorGraph, Variable
from FACTOR_GRAPHS.sum_product import sum_product_tree


def binary_prior_table(p1):
    # P(X=1)=p1, P(X=0)=1-p1
    return {(0,): 1.0 - p1, (1,): p1}


def equal_factor_table():
    # encourages X==Y
    return {
        (0, 0): 2.0,
        (0, 1): 0.5,
        (1, 0): 0.5,
        (1, 1): 2.0,
    }


def main():
    fg = FactorGraph()
    x = fg.add_variable(Variable("X", [0, 1]))
    y = fg.add_variable(Variable("Y", [0, 1]))

    fg.add_factor(Factor("px", [x], binary_prior_table(0.8)))
    fg.add_factor(Factor("eq", [x, y], equal_factor_table()))

    marginals = sum_product_tree(fg, root_var="X")
    print("marginals:", marginals)


if __name__ == "__main__":
    main()
