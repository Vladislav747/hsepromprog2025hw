import os
import shutil

from .node import FileNode

# Утилита аналог команды tree
class Tree:

    def get(self, current_path: str, dirs_only: bool, recurse_call=False):
        # проверка что вообще путь существует
        if not os.path.exists(current_path):
            raise AttributeError('Path not exist')

    # Если это не директория и не включен режим dirs_only, вернуть FileNode(файл)
        if not os.path.isdir(current_path):
            if not dirs_only:
                return self.construct_filenode(
                    current_path,
                    is_dir=False
                )
            else:
                if recurse_call:
                    return None
                else:
                    raise AttributeError('Path is not directory')

        answer = self.construct_filenode(
            current_path,
            is_dir=True
        )

        for child_filename in sorted(os.listdir(current_path)):
            child_path = os.path.join(current_path, child_filename)

            child_node = self.get(
                child_path,
                dirs_only=dirs_only,
                recurse_call=True
            )

            if child_node is not None:
                answer.children.append(child_node)

        return self.update_filenode(answer)

    def construct_filenode(self, path, is_dir):
        # получить имя файла или директории
        filename = os.path.basename(path)
        # По сути это файл
        return FileNode(
            name=filename,
            is_dir=is_dir,
            children=[]
        )

    # Обновить информацию о файле
    def update_filenode(self, file_node):
        return file_node

    # Удаление пустых директорий
    def filter_empty_nodes(self, node: FileNode, current_path='.'):
        if not node.is_dir:
            return

        if len(node.children) == 0:
            if current_path == '.':
                raise ValueError('Code should not be executed here!')
            shutil.rmtree(current_path)

        # рекурсивно проходим по дочерним узлам и там тоже удаляем пустые директории
        for child in node.children:
            self.filter_empty_nodes(
                child, os.path.join(current_path, child.name)
            )
