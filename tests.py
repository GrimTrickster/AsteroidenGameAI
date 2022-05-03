import numpy
from collections import namedtuple
from collections.abc import Mapping
from recordtype import recordtype


Point = recordtype('Point', 'x, y')


def _generateRow():
    pixelRow = []
    for x in range(0, 10):
        if numpy.random.choice([0, 1], p=[0.8, 0.2]) == 1:
            new_asteroid = Point(x, 0)
            pixelRow.append(new_asteroid)
    return pixelRow


def _generateGame():
    asteroids = []
    for n in range(0, 10):
        new_row = _generateRow()
        # print(new_row)
        for asteroid in range(len(new_row)):
            new_row[asteroid] = new_row[asteroid]._replace(y=n)
        # print(new_row)
        asteroids.append(_generateRow())
    return asteroids


test = [Point(x=0, y=0), Point(x=1, y=0), Point(x=8, y=0), Point(x=9, y=0)]
test[0].y = 10

print(test)