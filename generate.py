from random import randrange, sample


def generate_graph(sz: int):
    graph = {}
    for i in range(sz):
        nodes = sample(range(sz), 5)
        graph[str(i)] = [list(map(str, nodes)), "lambda *args: sum(args) % 100"]
    return graph


def generate_fsm(sz: int, graph_sz: int):
    res = [
        {
            "name": str(i),
            "graph": generate_graph(graph_sz),
            "result": {
                "vertices": list(
                    map(str, sample(range(graph_sz), randrange(graph_sz)))
                ),
                "function": "lambda *args: sum(args) % 100",
            },
        }
        for i in range(sz)
    ]

    return res


def generate_data(aut_sz, graph_sz, max_start_value=2):
    return {
        "automates": generate_fsm(aut_sz, graph_sz),
        "start_states": [
            [randrange(max_start_value) for _ in range(graph_sz)] for _ in range(aut_sz)
        ],
    }
