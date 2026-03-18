from __future__ import annotations

from factor import Factor
from bp_tree import sum_product_tree


def main():
    # Classic tiny BN:
    # B (burglary), E (earthquake) -> A (alarm) -> J (john calls), M (mary calls)
    dom = {
        "B": ("T", "F"),
        "E": ("T", "F"),
        "A": ("T", "F"),
        "J": ("T", "F"),
        "M": ("T", "F"),
    }

    fB = Factor.from_fn(["B"], dom, lambda a: 0.001 if a["B"] == "T" else 0.999)
    fE = Factor.from_fn(["E"], dom, lambda a: 0.002 if a["E"] == "T" else 0.998)

    def pA(a):
        b, e, alarm = a["B"], a["E"], a["A"]
        if alarm == "T":
            if b == "T" and e == "T":
                return 0.95
            if b == "T" and e == "F":
                return 0.94
            if b == "F" and e == "T":
                return 0.29
            return 0.001
        # A = F
        if b == "T" and e == "T":
            return 0.05
        if b == "T" and e == "F":
            return 0.06
        if b == "F" and e == "T":
            return 0.71
        return 0.999

    fA = Factor.from_fn(["B", "E", "A"], dom, pA)
    fJ = Factor.from_fn(["A", "J"], dom, lambda a: 0.90 if (a["A"], a["J"]) == ("T", "T") else
                        0.10 if (a["A"], a["J"]) == ("T", "F") else
                        0.05 if (a["A"], a["J"]) == ("F", "T") else 0.95)
    fM = Factor.from_fn(["A", "M"], dom, lambda a: 0.70 if (a["A"], a["M"]) == ("T", "T") else
                        0.30 if (a["A"], a["M"]) == ("T", "F") else
                        0.01 if (a["A"], a["M"]) == ("F", "T") else 0.99)

    # Factor graph: variables and factors as nodes, edges var<->factor.
    var_nodes = ["B", "E", "A", "J", "M"]
    factor_nodes = ["fB", "fE", "fA", "fJ", "fM"]
    factors = {"fB": fB, "fE": fE, "fA": fA, "fJ": fJ, "fM": fM}
    edges = [
        ("B", "fB"),
        ("E", "fE"),
        ("B", "fA"),
        ("E", "fA"),
        ("A", "fA"),
        ("A", "fJ"),
        ("J", "fJ"),
        ("A", "fM"),
        ("M", "fM"),
    ]

    evidence = {"J": "T", "M": "T"}
    marg = sum_product_tree(var_nodes, factor_nodes, edges, factors, evidence=evidence, root="A")

    print("Evidence: J=T, M=T")
    for v in ["B", "E", "A"]:
        f = marg[v]
        p_true = f.value({v: "T"})
        print(f"P({v}=T | evidence) = {p_true:.6f}")


if __name__ == "__main__":
    main()

