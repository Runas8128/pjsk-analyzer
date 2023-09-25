import os.path
import typing
import json
from util import RegionName, Rect

class Musics:
    __all = []

    @classmethod
    def load(cls):
        cls.__all = []
        with open(os.path.join(os.path.dirname(__file__), '..', 'assets', 'musics.dat'), 'rb') as f:
            s = f.read().decode('utf-8')
            cls.__all = json.loads(s)

    @classmethod
    @property
    def all(cls):
        if not cls.__all: cls.load()
        return cls.getTitle(cls.__all)
    
    @classmethod
    def find(cls, partial: str):
        if not cls.__all: cls.load()
        return cls.getTitle(sorted(cls.__all, key=lambda music: Musics.key(partial.lower(), music), reverse=True)[:3])
    
    @staticmethod
    def key(a: str, b: typing.List[str]):
        return max(
            sum(str(b[1]).lower().count(c) for c in set(a)) / len(str(b[1])),
            sum(str(b[2]).lower().count(c) for c in set(a)) / len(str(b[2]))
        )
    
    @staticmethod
    def getTitle(data: typing.List[typing.List[str]]):
        return list(map(lambda k: k[1], data))

diff = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'MASTER']

regionName: typing.List[RegionName] = [
    'title', 'diff',
    'score', 'maxScore', 'combo',
    'perfect', 'great', 'good', 'bad', 'miss'
]

region: typing.Dict[RegionName, Rect] = {
    'title': { 'left': 226, 'top': 13, 'width': 1266, 'height': 77 },
    'diff': { 'left': 241, 'top': 113, 'width': 247, 'height': 69 },
    'score': { 'left': 180, 'top': 653, 'width': 860, 'height': 200 },
    'maxScore': { 'left': 651, 'top': 882, 'width': 413, 'height': 100 },
    'combo': { 'left': 310, 'top': 1200, 'width': 610, 'height': 300 },
    'perfect': { 'left': 1264, 'top': 1159, 'width': 160, 'height': 80 },
    'great': { 'left': 1264, 'top': 1230, 'width': 160, 'height': 80 },
    'good': { 'left': 1264, 'top': 1306, 'width': 160, 'height': 80 },
    'bad': { 'left': 1264, 'top': 1382, 'width': 160, 'height': 80 },
    'miss': { 'left': 1264, 'top': 1460, 'width': 160, 'height': 80 },
}
