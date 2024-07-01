# Python Cookbook, 3rd Ed.
#
# Chapter: User Inputs and Outputs
# Recipe: Using cmd to create command-line applications

import builtins
import random
from unittest.mock import Mock

import pytest

import ch06.recipe_05 as recipe_05

@pytest.fixture()
def mock_input() -> Mock:
    return Mock(
        name="input",
        side_effect=["help", "help dice", "dice 5", "roll", "quit"]
    )

@pytest.fixture()
def known_seed() -> None:
    random.seed(42)

def test_dice_cli(
        mock_input: Mock,
        known_seed: None,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(builtins, 'input', mock_input)

    game = recipe_05.DiceCLI()
    game.cmdloop()

    out, err = capsys.readouterr()
    terminal_output = out.splitlines()
    assert 'Documented commands (type help <topic>):' in terminal_output
    assert 'Sets the number of dice to roll.' in terminal_output
    assert 'Rolling 5 dice' in terminal_output
    assert '[6, 1, 1, 6, 3]' in terminal_output, f"Not found in {terminal_output!r}"
