"""
Cli/Main Tests
"""

import os.path
import subprocess  # nosec
import sys
from typing import Any, List, Union

import pytest
from _pytest.capture import CaptureFixture, CaptureResult

# Our Project
from pytodo import main as cli

unit_test_data: List[List[str]] = [
    [
        "input",
        r"""
    output
    """,
    ],
    [
        "input",
        r"""
    output
    """,
    ],
]

# [[input, expected], ...]
integration_test_data: List[List[Union[str, List[str]]]] = [
    [
        "input",
        r"""
    output
    """.strip(),
    ],
]


@pytest.mark.parametrize("message,expected", unit_test_data)
def test_method_with_input(message: str, expected: List[str], capsys: CaptureFixture) -> None:
    """Runs the class methods against all of our test data."""

    captured_out: List[str]
    expected_out: List[str]

    sys.argv = ["pytodo"] + message.split(" ")

    # discard previous output
    captured: CaptureResult[Any] = capsys.readouterr()
    cli()
    captured = capsys.readouterr()  # capture new output

    # captured_out = captured.out.split("\n")
    captured_out = [*captured.out]
    # expected_out = [str(number) for number in expected]
    expected_out = [*expected]

    print(f"{captured_out} == {expected_out}")
    assert all(e == o for e, o in zip(captured_out, expected_out))


@pytest.mark.parametrize("message,expected", integration_test_data)
def test_script(message: str, expected: List[str]) -> None:
    """Runs the main script against all of our test data."""

    program_input: str = ""

    process: subprocess.CompletedProcess = subprocess.run(
        [
            "python",
            os.path.dirname("src/pytodo/"),
            message,
        ],
        check=False,
        input=program_input,
        stdout=subprocess.PIPE,
    )

    program_output: str = process.stdout.decode("utf-8").strip()
    # program_output: str = process.stdout.decode("utf-8")
    # program_out: List[str] = program_output.split("\n")
    program_out: List[str] = [*program_output]

    # expected_out: List[int] = [str(number) for number in expected]
    expected_out: List[str] = [*expected]

    print(f" program_out: {program_out}\n==\nexpected_out: {expected_out}")
    assert all(e == o for e, o in zip(program_out, expected_out))
