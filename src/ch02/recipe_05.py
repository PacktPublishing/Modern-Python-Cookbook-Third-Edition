# Python Cookbook, 3rd Ed.
#
# Chapter: Statements and Syntax
# Recipe: Designing complex if...elif chains


from enum import Enum
class Weather(Enum):
    FAIR = "fair"
    RAIN = "rain"

class Plan(Enum):
    STAY_IN = "home"
    GO_OUT = "park"

weather = Weather.FAIR
plan = Plan.STAY_IN

def bring(item: str) -> None:
    pass

if weather == Weather.RAIN and plan == Plan.GO_OUT:
    bring("umbrella")
else:
    bring("sunglasses")


# Subsection: How to do it...

class Game:
    def craps(self) -> None:
        pass
    def winner(self) -> None:
        pass
    def point(self, point: int) -> None:
        pass

die_1 = 3
die_2 = 3
game = Game()

dice = die_1 + die_2
if dice in (2, 3, 12):
    game.craps()
elif dice in (7, 11):
    game.winner()
elif dice in (4, 5, 6, 8, 9, 10):
    game.point(dice)

else:
    raise Exception('Design Problem')


# Subsection: There's more...

m = 2
a = 1
b = 2

# do something
assert (m == a or m == b) and m >= a and m >= b

del m  # Remove m prior to running the example

if a >= b:
    m = a
elif b >= a:
    m = b
else:
    raise Exception('Design Problem')

assert (m == a or m == b) and m >= a and m >= b



# End of Designing complex if...elif chains

def test_recipe() -> None:
    """It's sufficient to see that this code runs."""
    pass
