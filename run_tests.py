import json
import logging
import multiprocessing as mp
import os
import time

from copy import deepcopy

from generate import generate_data
from task import FSM

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)


def run_test_with_data(test_data):
    """
    Запуск теста с даннными в формате test*.json
    :param test_data:
    :return: True если тест пройден успешно, иначе False
    """
    fsm = FSM(
        {aut["name"]: aut for aut in test_data["automates"]}, test_data["start_states"]
    )
    for iteration, expected_result in enumerate(test_data["result"]):
        fsm.next_stage()
        if fsm.value() != expected_result:
            logging.error(f"Test failed on {iteration + 1} iteration")
            return False
    return True


def run_tests_from_path(tests_path):
    """
    Поиск и запуск всех тестов из директории tests_path
    :param tests_path:
    :return:
    """
    for item in os.listdir(tests_path):
        if os.path.splitext(item)[1] == ".json":
            test_path = os.path.join(tests_path, item)
            with open(test_path, "r") as f:
                test_input = json.load(f)
                is_correct = run_test_with_data(test_input)
                if is_correct:
                    logging.info(f"Test {test_path} succeeded")
                else:
                    logging.error(f"Test {test_path} failed")


def get_generation_time(test_data, iterations_count=25, parallel_factor=1):
    """
    Возвращает время генерации на заданном автомате iterations_count членов выходной последовательности
    :param test_data: задание клеточных автоматов
    :param iterations_count: число итераций
    :param parallel_factor: число потоков
    :return:
    """
    fsm = FSM(
        {aut["name"]: aut for aut in test_data["automates"]},
        test_data["start_states"],
        parallel_factor=parallel_factor,
    )

    start_time = time.time()
    for _ in range(iterations_count):
        fsm.next_stage()
        print(fsm.value(), end="", flush=True)
        print(" -> ", end="", flush=True)
    print()
    return time.time() - start_time


def run_speed_check_tests():
    """
    Запуск тестов на проверку скорости обработки в зависимости от количества потоков (задействованных процессов)
    Нужно уметь сочеть с количеством реальных и виртуальных ядер на тачке запуска
    :return:
    """
    start_time = time.time()
    graph_count = 1000
    graph_nodes = 100
    logging.info(f"Start graphs generation for {graph_count} graphs and {graph_nodes} nodes")
    test_data = generate_data(graph_count, graph_nodes)
    logging.info(f"Graphs generation time: {time.time() - start_time} seconds")

    for cores in range(1, 16):
        generation_time = get_generation_time(
            deepcopy(test_data), iterations_count=10, parallel_factor=cores
        )
        logging.info(f"{generation_time} seconds for {cores} cores")


if __name__ == "__main__":
    logging.info(f'System have {mp.cpu_count()} cores (virtual or real)')
    mp.set_start_method("fork")
    run_tests_from_path("./")
    run_speed_check_tests()
