from collections import defaultdict


def _normalize(dist):
    s = sum(dist.values())
    if s <= 0:
        return dist
    return {k: v / s for k, v in dist.items()}


def sum_product_tree(fg, root_var):
    """
    Sum-product for tree-structured factor graphs.
    Returns approximate marginals for each variable (exact on trees).
    """
    # Messages:
    # var->factor: m_vf[(v,f)] = dict[value] -> weight
    # factor->var: m_fv[(f,v)] = dict[value] -> weight
    m_vf = {}
    m_fv = {}

    # Build adjacency for traversal
    var_neighbors = {v: fg.neighbors_of_var(v) for v in fg.variables}
    factor_neighbors = {f: [v.name for v in fg.factors[f].vars] for f in fg.factors}

    # Simple synchronous updates until convergence (safe for small trees)
    for _ in range(30):
        # var -> factor
        for v_name, neigh_factors in var_neighbors.items():
            var = fg.variables[v_name]
            for f_name in neigh_factors:
                dist = {val: 1.0 for val in var.domain}
                for other_f in neigh_factors:
                    if other_f == f_name:
                        continue
                    msg = m_fv.get((other_f, v_name))
                    if msg:
                        for val in var.domain:
                            dist[val] *= msg.get(val, 0.0)
                m_vf[(v_name, f_name)] = dist

        # factor -> var
        for f_name, v_names in factor_neighbors.items():
            factor = fg.factors[f_name]
            for target_v in v_names:
                target_var = fg.variables[target_v]
                out = {val: 0.0 for val in target_var.domain}

                # iterate assignments in factor table
                for assignment, weight in factor.table.items():
                    # assignment aligns with factor.vars order
                    assign_map = {factor.vars[i].name: assignment[i] for i in range(len(factor.vars))}
                    tv = assign_map[target_v]
                    prod = weight
                    for other_v in v_names:
                        if other_v == target_v:
                            continue
                        msg = m_vf.get((other_v, f_name))
                        if msg:
                            prod *= msg.get(assign_map[other_v], 0.0)
                    out[tv] += prod
                m_fv[(f_name, target_v)] = out

    # Compute marginals
    marginals = {}
    for v_name, neigh_factors in var_neighbors.items():
        var = fg.variables[v_name]
        dist = {val: 1.0 for val in var.domain}
        for f_name in neigh_factors:
            msg = m_fv.get((f_name, v_name))
            if msg:
                for val in var.domain:
                    dist[val] *= msg.get(val, 0.0)
        marginals[v_name] = _normalize(dist)
    return marginals


