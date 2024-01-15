from prettytable import PrettyTable
# Print Footprint

def print_as_table(data):
    if not data:
        print("Empty dictionary.")
        return

    table = PrettyTable()
    table.field_names = [""] + list(data.keys())

    symbols = {0: '#', 1: '->', 2: '<-', 3: '||'}

    for key, inner_dict in data.items():
        row = [key]
        row.extend(symbols.get(value, value) for value in inner_dict.values())
        table.add_row(row)

    print(table)


def printPairs(pairs):
    formatted_pairs = "{" + ",".join(f"({x}, {y})" for x, y in pairs) + "}"

    print(formatted_pairs)


def print_as_sets(list_of_lists):
    result = []

    for sublist in list_of_lists:
        formatted_set = "({})".format(", ".join("{" + ", ".join(inner) + "}" for inner in sublist))
        result.append(formatted_set)

    print("{" + ", ".join(result) + "}")


def printPlaces(list_of_lists):
    result = []

    for sublist in list_of_lists:
        formatted_set = "P({})".format(", ".join("{" + ", ".join(inner) + "}" for inner in sublist))
        result.append(formatted_set)

    print("{ Iw, " + ", ".join(result) + " ,Ow }")

def printFollows(X):
    my_dict = {}
    j = 0
    for i in X:
        if i[0] not in my_dict.values():
            my_dict[j] = i[0]
            j += 1
        if i[1] not in my_dict.values():
            my_dict[j] = i[1]
            j += 1
    return my_dict

def get_int_keys_by_value(my_dict, target_value):
    keys = [key for key, value in my_dict.items() if value == target_value and isinstance(key, int)]
    return ", ".join(map(str, keys))


def printMap(Map, X):
    Pairs = []
    for i in X:
        first = get_int_keys_by_value(Map,i[0])
        second = get_int_keys_by_value(Map,i[1])
        Pairs.append((first, second))

    return Pairs
# get the input of the traces (Ti)
def getTI(Traces):
    res = []
    for inner_list in Traces:
        if inner_list[0] not in res:
            res.append(inner_list[0])
    res.sort()
    return res


# get the (To) in the traces
def getOI(Traces):
    res = []
    for inner_list in Traces:
        if inner_list[len(inner_list) - 1] not in res:
            res.append(inner_list[len(inner_list) - 1])
    res.sort()
    return res


# get the (Tw) in the traces (all transitions in traces)
def getTw(Traces):
    res = []
    for inner_list in Traces:
        for i in inner_list:
            if i not in res:
                res.append(i)
    res.sort()
    return res


def getDirectlyFollow(Traces):
    res = []
    for inner_list in Traces:
        for i in range(len(inner_list) - 1):
            PairItem = (inner_list[i], inner_list[i + 1])
            if PairItem not in res:
                res.append(PairItem)
    res = sorted(res, key=lambda x: (x[0], x[1]))
    return res


def getCausalityAndParallelism(DirectlyFollows):
    Df = DirectlyFollows
    parallelism = []

    for x, y in Df:
        Normal = (x, y)
        Reverse = (y, x)
        for i in Df:
            if Reverse == i:
                parallelism.append(Reverse)
                parallelism.append(Normal)
                Df.remove(i)
                Df.remove(Normal)
    parallelism = sorted(parallelism, key=lambda x: (x[0], x[1]))
    return Df, parallelism


def getFootprint(Causality, Parallelism, Transitions):
    res = {}
    for i in Transitions:
        res[i] = {}
    reveredCausality = []
    for x, y in Causality:
        reveredCausality.append((y, x))
    for i in Transitions:
        for j in Transitions:
            if (i, j) in Causality:
                res[i][j] = 1
            elif (i, j) in Parallelism:
                res[i][j] = 3
            elif (i, j) in reveredCausality:
                res[i][j] = 2
            else:
                res[i][j] = 0
    #     dict(sorted(res[i].items()))
    # dict(sorted(res.items()))
    return res


def checkOnFootprint(footprint, task1, task2):
    row = footprint.get(task1)
    value = row.get(task2)
    return value


def getXlAndYl(Causality, Footprint):
    Cap = {False: [], True: []}
    Collected = []
    Checked = []
    Df = []
    Xl = []
    Yl = []
    for x, y in Causality:
        Xl.append([[x], [y]])

    Cap[False].extend(Causality)

    for x, y in Causality:
        Df.append((x, y))

    for pair in Causality:
        one = 1
        for i in Df:
            if i == pair:
                continue
            if i in Checked:
                continue
            if pair[0] == i[0]:
                if not checkOnFootprint(Footprint, pair[1], i[1]):
                    Input = pair[0]
                    Output = [pair[1], i[1]]
                    Collected.append([[Input], Output])
                    Checked.append(pair)
                    negative = Cap[False]
                    positive = Cap[True]
                    if pair in negative:
                        negative.remove(pair)
                        positive.append(pair)
                    if i in negative:
                        negative.remove(i)
                        positive.append(i)

            if pair[1] == i[1]:
                if not checkOnFootprint(Footprint, pair[0], i[0]):
                    Input = [pair[0], i[0]]
                    Output = pair[1]
                    Collected.append([Input, [Output]])
                    Checked.append(pair)
                    negative = Cap[False]
                    positive = Cap[True]
                    if pair in negative:
                        negative.remove(pair)
                        positive.append(pair)
                    if i in negative:
                        negative.remove(i)
                        positive.append(i)
            one += 1
    # print(Cap)
    # print(Checked)
    for k in Cap[False]:
        Yl.append([k[0], k[1]])
    for k in Collected:
        Yl.append(k)
        Xl.append(k)
    # print(Yl)
    return Xl, Yl


def checkPlaces(Yl, search_str, flag):
    res = []
    if flag:
        for sub_list in Yl:
            if not isinstance(sub_list[0], str):
                for nested_list in sub_list[0]:
                    if search_str in nested_list[0]:
                        res.append(sub_list)
            else:
                if search_str in sub_list[0]:
                    res.append(sub_list)
    if not flag:
        for sub_list in Yl:
            for nested_list in sub_list[1]:
                if search_str in nested_list:
                    res.append(sub_list)
    return res


def getOuts(List):
    if not isinstance(List[1], str):
        return List[1]
    else:
        return [List[1]]


def getFlows(Ti, To, Yl):
    res = []
    Inputs = []
    Outputs = []
    Static = []
    StaticO = []
    for i in Ti:
        res.append(["Iw", i])
        Inputs.append(i)
    for i in Yl:
        for j in Inputs:
            Outs = checkPlaces(Yl, j, True)
            for u in Outs:
                Outputs.append(u)
                StaticO.append(u)
            for k in StaticO:
                if k and [j, k] not in res:
                    res.append([j, k])
            Outs.clear()
            StaticO.clear()
        Inputs.clear()
        for y in Outputs:
            Ints = getOuts(y)
            for u in Ints:
                Static.append(u)
                if u not in Inputs:
                    Inputs.append(u)
            for f in Static:
                if f and [y, f] not in res:
                    res.append([y, f])
            Static.clear()
        Outputs.clear()
    for i in To:
        res.append([i, "Ow"])
    return res
import matplotlib.pyplot as plt

from netgraph import Graph

# Traces=[['a','b','c','d'],
#         ['a','c','b','d'],
#         ['a','e','d']]
Traces=[['a','b','c','d'],
        ['a','c','b','d'],
        ['a','b','c','e','f','b','c','d'],
        ['a','b','c','e','f','c','b','d'],
        ['a','c','b','e','f','b','c','d']]
# Traces=[['a','b','e','f'],
#         ['a','b','e','c','d','b','f'],
#         ['a','b','c','e','d','b','f'],
#         ['a','b','c','d','e','b','f'],
#         ['a','e','b','c','d','b','f']]
Traces = []
num_traces = int(input("Enter the number of traces: "))

# # Loop to get each trace from the user
# print(f"Enter trace as a space-separated list of events Like: a b e f")
# for i in range(num_traces):
#     trace_str = input(f"Enter trace {i + 1} : ")
#     trace = trace_str.split()
#     Traces.append(trace)

Inputs = getTI(Traces)
Outputs= getOI(Traces)
Transitions = getTw(Traces)
Follows = getDirectlyFollow(Traces)
print("Directly Follows:")
printPairs(Follows)
Causality, Parallelism = getCausalityAndParallelism(Follows)
print("\nCausality:")
printPairs(Causality)
print("\nParallelism:")
printPairs(Parallelism)
Footprint = getFootprint(Causality, Parallelism, Transitions)
print("\nFootprint:")
print_as_table(Footprint)

print("Tl = {" + ", ".join(f"{i}" for i in Transitions) + "}")
print("Ti = {" + ", ".join(f"{i}" for i in Inputs) + "}")
print("To = {" + ", ".join(f"{i}" for i in Outputs) + "}")

XL, YL = getXlAndYl(Causality,Footprint)

print("\nXl: ")
print_as_sets(XL)
print("\nYl: ")
print_as_sets(YL)
print("\nPlaces: ")
printPlaces(YL)

# checkPlaces(YL, "d", False)
Flows = getFlows(Inputs, Outputs, YL)
print("\nFlows: ")
print(Flows)
print()
Map = printFollows(Flows)
# print(Map)
print("\nModel Map : ")
for key, value in Map.items():
    print(f"{key}: {value}")
graph = printMap(Map, Flows)
# print(graph)
# Graph(graph, node_shape = 'o' ,edge_cmap='RdGy')
Graph(graph,node_labels= True, node_shape = 'o' ,edge_width=3.,edge_cmap='RdGy' ,arrows=True)
plt.show()


