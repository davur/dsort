# content of test_sysexit.py
import pytest

from dsort import *


# def add(a, b):
#     return a + b


@pytest.fixture
def dsort():
    return DSort()

@pytest.fixture
def dsort_name():
    dsort = DSort()
    dsort.key_sort_order = ["city", "name"]
    return dsort

@pytest.fixture
def people():
    a = {
        'name': "Al",
        'age': 33
    }
    b = {
        'name': "Bob",
        'age': 30
    }
    c = {
        'name': "Cin",
        'age': 40
    }
    d = {
        'name': "Dee",
        'age': 34
    }
    return [b, d, c, a] 



def test_compare_no_order_preference(dsort):
    assert dsort.compare("age", "name") == -1
    assert dsort.compare("name", "age") == 1
    assert dsort.compare("name", "name") == 0


def test_compare_with_order_preference(dsort_name):
    assert dsort_name.compare("age", "name") == 1
    assert dsort_name.compare("name", "age") == -1
    assert dsort_name.compare("name", "name") == 0


def test_compare_no_matching_order_preference(dsort):
    dsort.key_sort_order = ["city", "state"]

    assert dsort.compare("age", "name") == -1
    assert dsort.compare("name", "age") == 1


def test_sort_list(dsort, people):
    people = sorted(people, key=dsort.sort_list_cmp)

    assert people[0]["name"] == "Al"


def test_sort_list_by_age(dsort):
    names = ["Bob", "Dee", "Cin", "Al"]
    names = sorted(names, key=dsort.sort_list_cmp)

    sorted_names = ["Al", "Bob", "Cin", "Dee"]

    assert(names[0] == "Al")
    assert(names[-1] == "Dee")
    assert(names == sorted_names)


def test_sort_keys(dsort, people):


    p1 = dsort.sort_keys(people[0])
    keys = list(p1.keys())
    assert(keys == ['age', 'name'])


def test_sort_keys_name(dsort_name, people):
    p1 = dsort_name.sort_keys(people[0])
    keys = list(p1.keys())

    assert(keys == ['name', 'age'])



def test_file_1(dsort, capfd):
    dsort.infiles=["./tests/1/in.yaml"]
    dsort.key_sort_order = ['apiVersion', 'kind', 'metadata', 'name', 'namespace']
    dsort.main(outform="yaml")

    with open("./tests/1/out.yaml", 'r', encoding='UTF-8') as file:
        expected = file.read()

    out, _ = capfd.readouterr()

    assert out == expected



def test_file_2(dsort, capfd):
    dsort.infiles=["./tests/2/in.yaml"]
    dsort.sort_lists = ['env', 'containers']
    dsort.key_sort_order = ['apiVersion', 'kind', 'metadata', 'name', 'namespace', 'image']
    dsort.main(outform="yaml")

    with open("./tests/2/out.yaml", 'r', encoding='UTF-8') as file:
        expected = file.read()

    out, _ = capfd.readouterr()

    assert out == expected


def test_file_3(dsort, capfd):
    dsort.infiles=["./tests/3/in.yaml"]
    dsort.sort_all_lists = True
    dsort.key_sort_order = ['apiVersion', 'kind', 'metadata', 'name', 'namespace', 'image']
    dsort.main(outform="yaml")

    with open("./tests/3/out.yaml", 'r', encoding='UTF-8') as file:
        expected = file.read()

    out, _ = capfd.readouterr()

    assert out == expected


def test_file_4(dsort, capfd):
    dsort.infiles=["./tests/4/in.yaml"]
    dsort.main(outform="yaml")

    with open("./tests/4/out.yaml", 'r', encoding='UTF-8') as file:
        expected = file.read()

    out, _ = capfd.readouterr()

    assert out == expected
