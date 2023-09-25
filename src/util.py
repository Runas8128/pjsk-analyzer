import typing
import difflib

RegionName = typing.Literal[
    'title', 'diff',
    'score', 'maxScore', 'combo',
    'perfect', 'great', 'good', 'bad', 'miss'
]

Rect = typing.Dict[typing.Literal['left', 'top', 'width', 'height'], int]

def getClosest(_target, _list):
    p = 1.0
    while True:
        try:
            if p < 0: return ['', -1]
            rst = difflib.get_close_matches(_target, _list, cutoff=p)[0]
            return [rst, p]
        except IndexError:
            p -= 0.01
