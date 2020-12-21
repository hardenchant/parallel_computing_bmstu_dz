import copy
import multiprocessing as mp
from collections import namedtuple

from typing import Generator, KeysView


class Task(namedtuple("Task", ["graph_id", "node_id", "result"])):
    def run(self, graph: KeysView):
        neighbours, function_str, value = graph[self.node_id]
        f = eval(function_str)

        return Task(
            self.graph_id,
            self.node_id,
            f(*[graph[neighbour][2] for neighbour in neighbours], value),
        )


class FSM:
    def __init__(self, automates, start_states, parallel_factor=mp.cpu_count()):
        self._FSMs = automates
        self.parallel_factor = parallel_factor

        for auto_start_states, fsm in zip(start_states, self._FSMs.values()):
            for auto_start_state, node in zip(auto_start_states, fsm["graph"].values()):
                node.append(auto_start_state)

    def _gen_tasks(self) -> Generator:
        for name, fsm in self._FSMs.items():
            for node_id in fsm["graph"]:
                yield (Task(name, node_id, None), fsm["graph"])

    def next_stage(self, inplace=True):
        ng = self if inplace else copy.deepcopy(self)

        tasks = ng._gen_tasks()
        with mp.Pool(self.parallel_factor) as p:
            results = p.starmap(Task.run, tasks)

        for res in results:
            ng._FSMs[res.graph_id]["graph"][res.node_id][2] = res.result

        return ng

    def _value(self, graph_id: str):
        graph = self._FSMs[graph_id]
        result = graph["result"]
        return eval(result["function"])(
            *[graph["graph"][k][2] for k in result["vertices"]]
        )

    def value(self):
        return sum([self._value(gid) for gid in self._FSMs])
