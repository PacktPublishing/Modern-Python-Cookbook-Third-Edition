# Python Cookbook, 3rd Ed.
#
# Chapter: User Inputs and Outputs
# Recipe: Using cmd to create command-line applications


bash_example_1_1 = """
% python src/ch06/recipe_05.py
A dice rolling tool. ? for help.
] help

Documented commands (type help <topic>):
========================================
dice  help  reroll  roll

Undocumented commands:
======================
EOF  quit

] help roll
Roll the dice. Use the dice command to set the number of dice.
] help dice
Sets the number of dice to roll.
] dice 5
Rolling 5 dice
] roll
[5, 6, 6, 1, 5]
] 
"""

# Subsection: Getting ready

bash_example_1_2 = """
] roll
[4, 2, 2, 1, 4]
] reroll 1 2 3
[4, 6, 3, 6, 4] (reroll 1)
] reroll 1 2 3
[4, 5, 3, 6, 4] (reroll 2)
] 
"""


# Subsection: How to do it...

import cmd
import random

class DiceCLI(cmd.Cmd):
    prompt = "] "
    intro = "A dice rolling tool. ? for help."

    def preloop(self) -> None:
        self.n_dice = 6
        self.dice: list[int] | None = None  # no roll has been made.
        self.reroll_count = 0

    def do_roll(self, arg: str) -> bool:
        """Roll the dice. Use the dice command to set the number of dice."""
        self.dice = [random.randint(1, 6) for _ in range(self.n_dice)]
        print(f"{self.dice}")
        return False

    def do_reroll(self, arg: str) -> bool:
        """Reroll selected dice. Provide the 0-based positions."""
        try:
            positions = map(int, arg.split())
        except ValueError as ex:
            print(ex)
            return False
        if self.dice is None:
            print("Dice haven't been rolled")
            return False
        for p in positions:
            self.dice[p] = random.randint(1, 6)
        self.reroll_count += 1
        print(f"{self.dice} (reroll {self.reroll_count})")
        return False

    def do_dice(self, arg: str) -> bool:
        """Sets the number of dice to roll."""
        try:
            self.n_dice = int(arg)
        except ValueError:
            print(f"{arg!r} is invalid")
            return False
        self.dice = None
        print(f"Rolling {self.n_dice} dice")
        return False

    def do_EOF(self, arg: str) -> bool:
        return True

    def do_quit(self, arg: str) -> bool:
        return True

    def emptyline(self) -> bool:
        """Shows current state of the dice."""
        # There a number of ways to make this easier to understand.
        if self.dice:
            print(f"{self.dice} (roll {self.reroll_count})")
        return False


if __name__ == "__main__":
    game = DiceCLI()
    game.cmdloop()

# Subsection: There's more...

class DiceCLI2(cmd.Cmd):
    prompt = "] "
    intro = "A dice rolling tool. ? for help."


test_dice = """
>>> import random
>>> random.seed(42)
>>> c = DiceCLI()
>>> c.preloop()
>>> c.do_roll('')
[6, 1, 1, 6, 3, 2]
False
>>> c.do_reroll('1 2 4 5')
[6, 2, 2, 6, 6, 1] (reroll 1)
False
>>> c.do_dice('3')
Rolling 3 dice
False
>>> c.do_quit('')
True
"""

# End of Using cmd to create command-line applications

__test__ = {name: code for name, code in locals().items() if name.startswith("test_")}
