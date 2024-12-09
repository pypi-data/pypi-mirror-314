"""Module for parsing Python source files and extracting structured information using AST.

Copyright (c) 2024 Neil Schneider
"""

import ast
from pathlib import Path

from slimcontext.parsers.pyparse.assignments import PyAssignment
from slimcontext.parsers.pyparse.classes import PyClass
from slimcontext.parsers.pyparse.functions import PyFunction
from slimcontext.parsers.pyparse.imports import PyImport
from slimcontext.parsers.pyparse.pybase import PyNodeBase
from slimcontext.utils.gitrepo_tools import GitRepository
from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


class PyParser:
    """Parses Python source files and extracts structured information using AST."""

    def __init__(self, root_dir: Path | None = None) -> None:
        """Initialize the PyParser instance.

        Args:
            root_dir (Path, optional): The git repo's root directory. Defaults to None.
        """
        if not root_dir:
            try:
                git_root: Path | None = GitRepository().root
            except ValueError:
                git_root = None
        self.root_dir: Path = root_dir or git_root or Path.cwd()

    def context_header(self, file_path: Path) -> list[str]:
        """Generate the header for the context with the file path.

        Args:
            file_path (Path): The path to the Python source file.

        Returns:
            list[str]: A list of header lines with the file path.
        """
        header: list[str] = []
        try:
            # Compute the relative path from root_dir to file_path
            relative_path = file_path.relative_to(self.root_dir)
        except ValueError:
            # If file_path is not under root_dir, use the absolute path
            relative_path = file_path.resolve()

        header.extend((
            '\n******',
            f'File: {relative_path}\n',
        ))
        return header

    def context_body(self, source: str, file_path: Path) -> list[str]:
        """Extract comprehensive information from a Python source file using AST.

        Args:
            source (str): The raw text of the source file.
            file_path (Path): The path to the Python source file.

        Returns:
            list[str]: A list of all the context from the module.
        """
        try:
            tree = ast.parse(source=source, filename=str(file_path))
        except SyntaxError as e:
            logger.warning('Syntax error in %s: %s', file_path, e)
            tree = None

        all_nodes: list = (
            [self._process_node(node=node, source=source) for node in ast.iter_child_nodes(tree)]
            if tree
            else []
        )
        processed_nodes: list[PyNodeBase] = [node for node in all_nodes if node]

        body: list[str] = []
        module_docstring: str | None = ast.get_docstring(tree) if tree else None
        if module_docstring:
            body.extend([module_docstring])
        for node in processed_nodes:
            body.extend(node.context)

        return body

    @staticmethod
    def _process_node(node: ast.AST, source: str) -> PyNodeBase | None:
        """Process a single AST node and extract relevant information.

        Args:
            node (ast.AST): The AST node to process.
            source (str): The raw text of the source file.

        Returns:
            One of the PyNode objects built from PyNodeBase.
        """
        if isinstance(node, ast.Import | ast.ImportFrom):
            return PyImport(node=node, source=source)
        if isinstance(node, ast.Assign):
            return PyAssignment(node=node, source=source)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            return PyFunction(node=node, source=source)
        if isinstance(node, ast.ClassDef):
            return PyClass(node=node, source=source)
        logger.debug('Found uncategorized node type: %s', type(node))
        return None

    def generate_succinct_context(self, source: str, file_path: Path) -> str:
        """Generate a succinct textual context from the repository information for the LLM.

        Args:
            source (str): The raw text of the source file.
            file_path (Path): The path to the Python source file.

        Returns:
            str: A string representation of the repository context.
        """
        context_lines: list[str] = []
        context_lines.extend(self.context_header(file_path=file_path))
        context_lines.extend(self.context_body(source=source, file_path=file_path))

        logger.debug('Generated succinct context for LLM.')
        return '\n'.join(context_lines)

    def generate_full_context(self, source: str, file_path: Path) -> str:
        """Return the entire content of a Python source file.

        Args:
            source (str): The raw text of the source file.
            file_path (Path): The path to the Python source file.

        Returns:
            str: Full text content of the file.
        """
        context_lines: list[str] = []
        context_lines.extend(self.context_header(file_path=file_path))
        context_lines.append(source)

        return '\n'.join(context_lines)

    def generate_context(
        self,
        file_path: Path,
        *,
        full_text: bool = False,
    ) -> str:
        """Generate a textual context from the repository information for the LLM.

        Args:
            file_path (Path): The path to the Python source file.
            full_text (bool, optional): Whether to return the full text of the file.
                Defaults to False.

        Returns:
            str: A string representation of the repository context.
        """
        try:
            with file_path.open('r', encoding='utf-8') as file:
                source = file.read()
        except (OSError, FileNotFoundError):
            logger.exception('Error reading file %s', file_path)
            source = ''
        if full_text:
            return self.generate_full_context(source=source, file_path=file_path)
        return self.generate_succinct_context(source=source, file_path=file_path)


if __name__ == '__main__':

    def example_use() -> None:
        """Small example of how to use PyParser."""
        logger_ex = setup_logger(f'Example use of {__name__}')
        parser = PyParser()
        # Sample file path for demonstration purposes
        file_path = Path('slimcontext/parsers/pyparse/pyparser.py')
        context = parser.generate_context(file_path)
        logger_ex.info('Example context generated by PyParser: %s', context)
