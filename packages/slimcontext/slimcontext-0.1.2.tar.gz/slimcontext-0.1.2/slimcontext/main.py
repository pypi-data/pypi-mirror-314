"""Main entry point for the Git repository structure extraction tool.

This script extracts Python project structure from a Git repository and generates context for an LLM
model.

Copyright (c) 2024 Neil Schneider
"""

import sys
from pathlib import Path

import click

from slimcontext.parsers.pyparse.pyparser import PyParser
from slimcontext.utils.gitrepo_tools import GitRepository
from slimcontext.utils.logger import setup_logger
from slimcontext.utils.token_counter import TokenCounter

logger = setup_logger(__name__)


def initialize_git_repo(repo_path: Path) -> GitRepository:
    """Initialize a Git repository object.

    Args:
        repo_path (Path): Path to the Git repository.

    Returns:
        GitRepository: Initialized Git repository object.
    """
    try:
        return GitRepository(repo_dir=repo_path)
    except ValueError:
        logger.exception('Error initializing Git repository.')
        sys.exit(1)
    except Exception:
        logger.exception('Unexpected error initializing Git repository.')
        sys.exit(1)


def generate_context(py_parser: PyParser, python_files: list[Path], context_level: str) -> str:
    """Generate context for the given Python files.

    Args:
        py_parser (PyParser): Python parser instance.
        python_files (list[Path]): List of Python file paths.
        context_level (str): Context generation level ('full' or 'succinct').

    Returns:
        str: Combined context for all Python files.
    """
    all_contexts = []
    for file_path in python_files:
        try:
            with file_path.open('r', encoding='utf-8') as f:
                source_code = f.read()
            context = (
                py_parser.generate_full_context(source=source_code, file_path=file_path)
                if context_level == 'full'
                else py_parser.generate_succinct_context(source=source_code, file_path=file_path)
            )
            all_contexts.append(context)
        except FileNotFoundError:  # noqa: PERF203
            logger.warning('File not found: %s', file_path)
        except PermissionError:
            logger.warning('Permission denied for file: %s', file_path)
        except UnicodeDecodeError as e:
            logger.warning('Failed to decode file %s: %s', file_path, e)
        except Exception:
            logger.exception('Unexpected error while reading: %s', file_path)
            raise
    return '\n\n'.join(all_contexts)


def count_tokens(context: str, model: str) -> int:
    """Count the tokens in the given context.

    Args:
        context (str): Generated context.
        model (str): Model name for token counting.

    Returns:
        int: Total token count.
    """
    try:
        token_counter = TokenCounter(model=model)
        return token_counter.count_tokens(context)
    except Exception:
        logger.exception('Error during token counting.')
        sys.exit(1)


def write_output(context: str, output_path: Path | None) -> None:
    """Write the generated context to a file or stdout.

    Args:
        context (str): Generated context.
        output_path (Path | None): Path to the output file, or None for stdout.
    """
    if output_path:
        try:
            with output_path.open('w', encoding='utf-8') as f:
                f.write(context)
            logger.info('Context successfully written to %s', output_path)
        except Exception:
            logger.exception('Failed to write to output file: %s', output_path)
            sys.exit(1)
    else:
        sys.stdout.write(context + '\n')


@click.command()
@click.option(
    '--path',
    default='.',
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help='Path to the Git repository. Defaults to the current directory.',
)
@click.option(
    '--context-level',
    default='succinct',
    type=click.Choice(['full', 'succinct'], case_sensitive=False),
    help="Level of context to generate. Choices are 'full' or 'succinct'. Defaults to 'succinct'.",
)
@click.option(
    '--output',
    default=None,
    type=click.Path(file_okay=True, dir_okay=False, writable=True, path_type=Path),
    help='Output file path. If not provided, outputs to stdout.',
)
@click.option(
    '--token-count',
    default='gpt-4',
    help=(
        "Model name to use for token counting. Defaults to 'gpt-4'. Set to 'None' to skip token "
        'counting.'
    ),
)
@click.option(
    '--log-file',
    default=None,
    type=click.Path(file_okay=True, dir_okay=False, writable=True, path_type=Path),
    help='Path to the log file. If not provided, logs are only output to the console.',
)
@click.option(
    '--log-level',
    default='INFO',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False),
    help="Set the logging level. Defaults to 'INFO'.",
)
def main(  # noqa: PLR0913 PLR0917
    path: Path,
    context_level: str,
    output: Path,
    token_count: str,
    log_file: Path,
    log_level: str,
) -> None:
    """Main entry point of the script."""
    logger.setLevel(log_level)
    if log_file:
        setup_logger(__name__, log_file)

    logger.info('Initializing Git repository at: %s', path)
    git_repo = initialize_git_repo(path)

    python_files = git_repo.get_files_by_suffix(['.py'])
    if not python_files:
        logger.warning('No Python files found in the repository.')
        sys.exit(0)

    logger.info('Found %s Python files to process.', len(python_files))
    py_parser = PyParser(root_dir=git_repo.get_git_root())

    resolved_files = [path / file for file in python_files]
    try:
        combined_context = generate_context(py_parser, resolved_files, context_level)
    except Exception:
        logger.exception('Failed to process repository files.')
        sys.exit(1)

    logger.info('Completed context generation.')

    if token_count.lower() != 'none':
        token_count_value = count_tokens(combined_context, token_count)
        logger.info('Total tokens in context: %s', token_count_value)
        combined_context += f'\n\n# Token Count: {token_count_value}'

    write_output(combined_context, output)


if __name__ == '__main__':
    main()
