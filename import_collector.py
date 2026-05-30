import ast
import os
from pathlib import Path
from typing import Set, Tuple, Dict


def get_project_modules(project_path: str) -> Set[str]:
    """Получает список всех локальных модулей в проекте"""
    local_modules = set()
    project_root = Path(project_path).resolve()

    for py_file in project_root.rglob('*.py'):
        if 'venv' not in str(py_file) and '__pycache__' not in str(py_file):
            # Получаем путь относительно корня проекта
            rel_path = py_file.relative_to(project_root)
            # Преобразуем путь в имя модуля
            if rel_path.name == '__init__.py':
                module_name = str(rel_path.parent).replace(os.sep, '.')
                if module_name:
                    local_modules.add(module_name)
            else:
                module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
                local_modules.add(module_name)

    return local_modules


def extract_imports_with_type(file_path: Path, local_modules: Set[str]) -> Dict:
    """Извлекает импорты с указанием типа (внешний/локальный)"""
    imports = {'local': set(), 'external': set(), 'all_names': set()}

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        base_module = alias.name.split('.')[0]
                        imports['all_names'].add(alias.name)
                        if base_module in local_modules:
                            imports['local'].add(alias.name)
                        else:
                            imports['external'].add(base_module)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        base_module = node.module.split('.')[0]
                        full_module = node.module
                        imports['all_names'].add(full_module)

                        # Проверяем, является ли это локальным модулем
                        if base_module in local_modules or full_module in local_modules:
                            imports['local'].add(full_module)
                        else:
                            imports['external'].add(base_module)
        except SyntaxError:
            pass

    return imports


def scan_project_detailed(project_path: str) -> Dict:
    """Сканирует проект и разделяет импорты на локальные и внешние"""
    project_root = Path(project_path).resolve()

    # Получаем все локальные модули проекта
    local_modules = get_project_modules(project_root)

    # Сканируем импорты
    all_imports = {'local': set(), 'external': set(), 'by_file': {}}

    for py_file in project_root.rglob('*.py'):
        if 'venv' not in str(py_file) and '__pycache__' not in str(py_file):
            imports = extract_imports_with_type(py_file, local_modules)

            # Сохраняем по файлам
            rel_path = py_file.relative_to(project_root)
            all_imports['by_file'][str(rel_path)] = imports

            all_imports['local'].update(imports['local'])
            all_imports['external'].update(imports['external'])

    all_imports['local'] = sorted(all_imports['local'])
    all_imports['external'] = sorted(all_imports['external'])

    return all_imports


# Использование
project_path = "."  # путь к проекту
result = scan_project_detailed(project_path)

print("=" * 50)
print("ЛОКАЛЬНЫЕ МОДУЛИ (ваши самописные):")
print("=" * 50)
for module in result['local']:
    print(f"{module}")

print("\n" + "=" * 50)
print("ВНЕШНИЕ МОДУЛИ (сторонние библиотеки):")
print("=" * 50)
for module in result['external']:
    print(f"{module}")

print("\n" + "=" * 50)
print("ДЕТАЛИЗАЦИЯ ПО ФАЙЛАМ:")
print("=" * 50)
for file_path, imports in result['by_file'].items():
    print(f"\n{file_path}:")
    if imports['local']:
        print(f"   Локальные: {', '.join(imports['local'])}")
    if imports['external']:
        print(f"   Внешние: {', '.join(imports['external'])}")