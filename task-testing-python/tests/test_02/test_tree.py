import os
import shutil
import tempfile
from pathlib import Path

import pytest
from src.tree_utils_02.tree import Tree, FileNode

@pytest.fixture
def temp_tree():
    return Tree()

@pytest.fixture
def temp_dir():
    # Создаем временную директорию
    test_dir = tempfile.mkdtemp()
    yield test_dir
    # Удаляем после тестов
    shutil.rmtree(test_dir)

# для get тестов
@pytest.fixture
def sample_file_structure(temp_dir):
    # файл в корне
    (Path(temp_dir) / 'file1.txt').write_text('test')
    (Path(temp_dir) / 'dir1').mkdir()
    (Path(temp_dir) / 'dir1' / 'subdir1').mkdir()
    (Path(temp_dir) / 'dir1' / 'file2.txt').write_text('test')
    # пустая директория
    (Path(temp_dir) / 'dir2').mkdir()
    return temp_dir


@pytest.fixture
def temp_dir_structure(tmp_path):
    # Создаем временную структуру директорий и файлов
    d = tmp_path / "test_dir"
    d.mkdir()

    # Пустая директория
    empty_dir = d / "empty_dir"
    empty_dir.mkdir()

    # Непустая директория
    non_empty_dir = d / "non_empty_dir"
    non_empty_dir.mkdir()
    (non_empty_dir / "file.txt").write_text("content")

    # Файл в корне
    (d / "root_file.txt").write_text("content")

    return str(d)

def test_get_with_nonexistent_path():
    tree = Tree()
    with pytest.raises(AttributeError, match='Path not exist'):
        tree.get('/nonexistent/path', dirs_only=False)

def test_get_with_file_path(sample_file_structure):
    tree = Tree()
    file_path = os.path.join(sample_file_structure, 'file1.txt')

    # Для dirs_only=False должен вернуть FileNode
    node = tree.get(file_path, dirs_only=False)
    assert isinstance(node, FileNode)
    assert node.name == 'file1.txt'
    assert not node.is_dir
    assert not node.children

    # Для dirs_only=True должен бросить исключение - нарочно кидаем, что путь не является директорией
    with pytest.raises(AttributeError, match='Path is not directory'):
        tree.get(file_path, dirs_only=True)

    node_null = tree.get(file_path, dirs_only=True, recurse_call=True)
    assert node_null is None


def test_root_directory_protection():
    """Тест проверяет защиту от удаления корневой директории"""
    tree = Tree()
    root_node = FileNode(name=".", is_dir=True, children=[])

    with pytest.raises(ValueError, match="Code should not be executed here!"):
        tree.filter_empty_nodes(root_node)

    root_node_file = FileNode(name=".", is_dir=False, children=[])

    result_is_file = tree.filter_empty_nodes(root_node_file)

    assert result_is_file is None

def test_update_filenode_returns_same_node():
    """Тест проверяет, что метод возвращает тот же объект без изменений"""
    tree = Tree()
    node = FileNode(name="test", is_dir=True, children=[])
    result = tree.update_filenode(node)
    assert result is node


def test_filter_empty_nodes_recursive(temp_tree, temp_dir_structure):
    # Создаем вложенную пустую структуру
    nested_dir = os.path.join(temp_dir_structure, "parent_dir", "child_dir")
    os.makedirs(nested_dir)

    # Создаем структуру узлов
    child_node = FileNode(name="child_dir", is_dir=True, children=[])
    parent_node = FileNode(name="parent_dir", is_dir=True, children=[child_node])
    parent_path = os.path.join(temp_dir_structure, "parent_dir")

    temp_tree.filter_empty_nodes(parent_node, parent_path)
    assert os.path.exists(parent_path) is True


def test_get_file_path_dirs_only_false(temp_tree, temp_dir_structure):
    file_path = os.path.join(temp_dir_structure, "root_file.txt")
    node = temp_tree.get(file_path, dirs_only=False)

    assert node.name == "root_file.txt"
    assert not node.is_dir
    assert not node.children

def test_get_file_path_dirs_only_true(temp_tree, temp_dir_structure):
    file_path = os.path.join(temp_dir_structure, "root_file.txt")

    with pytest.raises(AttributeError, match="Path is not directory"):
        temp_tree.get(file_path, dirs_only=True)

def test_get_file_path_dirs_only_recurse(temp_tree, temp_dir_structure):
    file_path = os.path.join(temp_dir_structure, "root_file.txt")
    assert temp_tree.get(file_path, dirs_only=True, recurse_call=True) is None

def test_get_directory_structure(temp_tree, temp_dir_structure):
    node = temp_tree.get(temp_dir_structure, dirs_only=False)

    assert node.is_dir
    # empty_dir, non_empty_dir, root_file.txt
    assert len(node.children) == 3
    assert any(child.name == "non_empty_dir" for child in node.children)

def test_get_dirs_only(temp_tree, temp_dir_structure):
    node = temp_tree.get(temp_dir_structure, dirs_only=True)

    assert node.is_dir
    # только empty_dir и non_empty_dir
    assert len(node.children) == 2
    assert all(child.is_dir for child in node.children)