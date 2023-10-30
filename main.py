def find_pivot_column(obj: list) -> int:
    small = []
    for i in range(len(obj)):
        if obj[i] < 0:
            small.append(obj[i])
    if not small:
        return -1
    return obj.index(min(small))


def find_pivot_row(eq: list[[]], con: list, p_c: int) -> int:
    theta = []
    for x in range(0, len(eq)):
        if eq[x][p_c] > 0:
            theta.append([con[x] / eq[x][p_c], x])
    if not theta:
        return -1
    theta.sort()
    return theta[0][1]


def row_combination(eq_p: list, lst_z: list, p_c: int, pivot_val: int) -> list:
    row_operated = []
    for i in range(len(eq_p)):
        row_operated.append(lst_z[i] - ((lst_z[p_c]/pivot_val) * eq_p[i]))
    return row_operated


def row_scale_to_one(eq_p: list, p_c: int) -> list:
    scalar = 1/(eq_p[p_c])
    for i in range(len(eq_p)):
        eq_p[i] = scalar * eq_p[i]
    return eq_p


def pivot_step(eq: list[[]], con: list, obj: list, p_c: int, p_r: int, cost: int) -> (list[[]], list, list, int):
    if eq[p_r][p_c] != 1:
        con[p_r] = (1/eq[p_r][p_c]) * con[p_r]
        eq[p_r] = row_scale_to_one(eq[p_r], p_c)

    pivot_val = eq[p_r][p_c]
    for r in range(len(eq)):
        if r != p_r:
            con[r] = con[r] - ((eq[r][p_c]/pivot_val) * con[p_r])
            eq[r] = row_combination(eq[p_r], eq[r], p_c, pivot_val)

    if obj[p_c] != 0:
        cost = cost - ((obj[p_c]/pivot_val) * con[p_r])
        obj = row_combination(eq[p_r], obj, p_c, pivot_val)

    return eq, con, obj, cost


def optimality_criterion(obj: list) -> bool:
    return min(obj) >= 0


def get_solution_bfs(eq: list[[]], con: list, basic_var: list) -> list:
    solution = []
    basic_var = basic_var[len(basic_var) - len(con)::]
    while len(solution) < len(eq[0]):
        for var in basic_var:
            if len(solution) == var[1]:
                solution.append(con[var[1]])
            else:
                solution.append(0)
    return solution


def simplex_method(eq: list[[]], con: list, obj: list, basic_var: list, cost: int) -> None:
    while not optimality_criterion(obj):
        p_c = find_pivot_column(obj)
        if p_c == -1:
            print("broke lol")
            break
        p_r = find_pivot_row(eq, con, p_c)
        if p_r == -1:
            print("No optimal solution")
            break;
        basic_var.append((p_r, p_c))
        eq, con, obj, cost = pivot_step(eq, con, obj, p_c, p_r, cost)

    print(get_solution_bfs(eq, con, basic_var))
    print(cost)


if __name__ == '__main__' :
    A = [[2, 2, 1, 0],
          [5, 3, 0, 1]]
    b = [8, 15]
    objective_func = [-120, -100, 0, 0]
    init_cost = 0
    basic_vars = [(0, 2), (1, 3)]
    simplex_method(A, b, objective_func, basic_vars, init_cost)

"""for x in range(len(eq[0])):
        for var in basic_var:
            if x == var[1]:
                if not solution:
                    solution.append(con[var[0]])
                else:
                    solution[x] = con[var[0]]
            elif len(solution) < len(eq[0]):
                solution.append(0)"""
