import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.tree_utils_02.size_tree import SizeTree, FileSizeNode


@pytest.fixture
def temp_dir():
    # Создаем временную директорию
    test_dir = tempfile.mkdtemp()
    yield test_dir
    # Удаляем после тестов
    shutil.rmtree(test_dir)


@pytest.fixture
def sample_file_structure(temp_dir):
    # Создаем тестовую структуру файлов и папок
    file1 = Path(temp_dir) / 'file1.txt'
    file1.write_text('test content')  # ~12 bytes

    dir1 = Path(temp_dir) / 'dir1'
    dir1.mkdir()

    file2 = dir1 / 'file2.txt'
    file2.write_text('more content')  # ~12 bytes

    subdir1 = dir1 / 'subdir1'
    subdir1.mkdir()

    dir2 = Path(temp_dir) / 'dir2'
    dir2.mkdir()

    return {
        'root': temp_dir,
        'file1': file1,
        'dir1': dir1,
        'file2': file2,
        'subdir1': subdir1,
        'dir2': dir2
    }


def test_construct_filenode_for_file(sample_file_structure):
    tree = SizeTree()
    file_path = str(sample_file_structure['file1'])
    node = tree.construct_filenode(file_path, is_dir=False)

    assert isinstance(node, FileSizeNode)
    assert node.name == 'file1.txt'
    assert not node.is_dir
    assert node.size == os.path.getsize(file_path)
    assert node.children == []


def test_construct_filenode_for_directory():
    tree = SizeTree()
    with tempfile.TemporaryDirectory() as temp_dir:
        node = tree.construct_filenode(temp_dir, is_dir=True)

        assert isinstance(node, FileSizeNode)
        assert node.name == os.path.basename(temp_dir)
        assert node.is_dir
        assert node.size == 4096  # BLOCK_SIZE
        assert node.children == []


def test_update_filenode_with_children():
    tree = SizeTree()

    # Создаем mock-узлы
    parent = FileSizeNode(name='parent', is_dir=True, children=[], size=4096)
    child1 = FileSizeNode(name='child1', is_dir=False, children=[], size=1024)
    child2 = FileSizeNode(name='child2', is_dir=False, children=[], size=2048)
    parent.children = [child1, child2]

    updated_node = tree.update_filenode(parent)

    assert updated_node.size == 4096 + 1024 + 2048  # parent + child1 + child2


def test_get_file_size_calculation(sample_file_structure):
    tree = SizeTree()
    file_path = str(sample_file_structure['file1'])
    node = tree.get(file_path, dirs_only=False)

    assert node.size == os.path.getsize(file_path)
