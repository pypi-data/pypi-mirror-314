import tattl
import tomllib

from dataclasses import dataclass, field
from pprint import pp

my_toml = """
title = "TOML Example"

[points]
alice = 17
bob = 12
charlie = 7

[garden]
sunny = true
elevation-map = [
    [1, 1, 1, 2, 1],
    [1, 2, 2, 2, 1],
    [1, 2, 3, 3, 2],
    [1, 2, 2, 3, 1],
    [1, 1, 1, 2, 1],
]

[garden.flowers]
roses = { amount = 7, growth = 0.90 }
daffodils = { amount = 3, growth = 0.54 }
daisies = { amount = 12, growth = 0.21 }

[fruits.apples]
color = "red"
tastes = ["sweet", "sour"]

[fruits.mangoes]
color = "orange"
tastes = ["sweet", "citrus"]
"""


@dataclass
class Structure:
    title: str
    points: dict[str, int]

    @dataclass
    class Garden:
        sunny: bool
        elevation_map: list[list[int]] = field(metadata={"name": "elevation-map"})

        @dataclass
        class Flower:
            amount: int
            growth: float

        flowers: dict[str, Flower]

    garden: Garden

    @dataclass
    class Fruit:
        color: str
        tastes: list[str]

    fruits: dict[str, Fruit]


data = tattl.unpack_dict(tomllib.loads(my_toml), Structure)

pp(data)

# Structure(title='TOML Example',
#           points={'alice': 17, 'bob': 12, 'charlie': 7},
#           garden=Garden(sunny=True,
#                         elevation_map=[[1, 1, 1, 2, 1],
#                                        [1, 2, 2, 2, 1],
#                                        [1, 2, 3, 3, 2],
#                                        [1, 2, 2, 3, 1],
#                                        [1, 1, 1, 2, 1]],
#                         flowers={'roses': Flower(amount=7,
#                                                  growth=0.9),
#                                  'daffodils': Flower(amount=3,
#                                                      growth=0.54),
#                                  'daisies': Flower(amount=12,
#                                                    growth=0.21)}),
#           fruits={'apples': Fruit(color='red',
#                                   tastes=['sweet', 'sour']),
#                   'mangoes': Fruit(color='orange',
#                                    tastes=['sweet', 'citrus'])})
