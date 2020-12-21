from random import randrange, sample

_ = {
    "automates": [
        {
            "name": "auto number one",
            "graph": {
                "1": [["2", "3"], "lambda x, y, prev: x + y + prev + 1"],
                "2": [["1"], "lambda x, prev: x + prev + 2"],
                "3": [["1"], "lambda x, prev: x + prev + 3"],
            },
            "result": {"vertices": ["3"], "function": "lambda v3: v3 + 21"},
        }
    ],
    "start_states": [[0, 0, 0]],
    "result": [24, 28],
}

_ = {
    "automates": [
        {
            "name": "0",
            "graph": {"0": [["0"], "sum"], "1": [[], "sum"]},
            "result": {"vertices": [], "function": "sum"},
        }
    ],
    "start_states": [[0, 0]],
}


def generate_graph(sz: int):
    graph = {}
    for i in range(sz):
        # nodes = sample(range(sz), randrange(sz))
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
                    # map(str, sample(range(graph_sz), graph_sz/2))
                    # map(str, range(graph_sz))

                ),
                "function": "lambda *args: sum(args) % 100",
            },
        }
        for i in range(sz)
    ]

    return res


def generate_data(aut_sz, graph_sz):
    return {
        "automates": generate_fsm(aut_sz, graph_sz),
        "start_states": [
            [randrange(2) for _ in range(graph_sz)] for _ in range(aut_sz)
        ],
    }
