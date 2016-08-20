"""import solutions
import pytest

# 78 Statments in problem 4
@pytest.fixture
def set_linked_list_node():
    integer_node = solutions.LinkedListNode(1)
    string_node = solutions.LinkedListNode("HERE")
    integer_node_2 = solutions.LinkedListNode(2)
    string_node_2 = solutions.LinkedListNode("THERE")
    return integer_node, string_node, integer_node_2, string_node_2

@pytest.fixture
def set_linked_list():
    linked_list = solutions.LinkedList()
    linked_list.add(1)
    linked_list.add(2)
    linked_list.add(3)
    return linked_list

#problem 4 test solutions.py
def test_linked_list_node_init(set_linked_list_node):
    integer_node, string_node, integer_node_2, string_node_2 = set_linked_list_node
    assert integer_node.data==1
    assert string_node.data=="HERE"

def test_linked_list_node_str(set_linked_list_node):
    integer_node, string_node, integer_node_2, string_node_2 = set_linked_list_node
    assert str(integer_node) == "1"
    assert str(integer_node_2) == "2"
    assert str(string_node) == "HERE"

def test_linked_list_node_lt(set_linked_list_node):
    integer_node, string_node, integer_node_2, string_node_2 = set_linked_list_node
    assert (integer_node < integer_node_2) == True
    assert (integer_node_2 < integer_node) == False
    with pytest.raises(Exception) as excinfo:
        string_node < integer_node
    print excinfo.typename
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "To compare nodes with __lt__ they must be of the same type"

def test_linked_list_node_gt(set_linked_list_node):
    integer_node, string_node, integer_node_2, string_node_2 = set_linked_list_node
    assert (integer_node > integer_node_2) == False
    assert (integer_node_2 > integer_node) == True
    with pytest.raises(Exception) as excinfo:
        string_node > integer_node
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "To compare nodes with __gt__ they must be of the same type"

def test_linked_list_node_eq(set_linked_list_node):
    integer_node, string_node, integer_node_2, string_node_2 = set_linked_list_node
    assert (integer_node == integer_node) == True
    assert (integer_node == integer_node_2) == False
    with pytest.raises(Exception) as excinfo:
        string_node == integer_node
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "To compare nodes with __eq__ they must be of the same type"

def test_linked_list_init():
    a = solutions.LinkedList()
    assert a.head == None

def test_linked_list_add(set_linked_list):
    a = set_linked_list
    assert a.head.data == 1
    assert a.head.next.data == 2

def test_linked_list_str(set_linked_list):
    a = set_linked_list
    assert str(a) == str([1,2,3])
    a = solutions.LinkedList()
    assert str(a) == str([])

def test_linked_list_remove(set_linked_list):
    a = set_linked_list

    a.remove(3)
    assert a.head.data == 1

    a.remove(1)
    assert a.head.data == 2

    with pytest.raises(Exception) as excinfo:
        a.remove(4)
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "4 is not in the list."

    a.remove(2)
    with pytest.raises(Exception) as excinfo:
        a.remove(4)
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "4 is not in the list."

def test_linked_list_insert(set_linked_list):
    a = set_linked_list
    print str(a)
    a.insert(-1, 1)
    a.insert(0, 1)
    with pytest.raises(Exception) as excinfo:
        a.insert(5, 6)
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "6 is not in the list."
"""
