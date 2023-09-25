import typing
import cv2
import cv2.typing
import easyocr

import util
import data

en_ja_reader = easyocr.Reader(['en', 'ja'])
en_reader = easyocr.Reader(['en'])

readText = lambda reader, target: reader.readtext(target)[0][1]
readInt = lambda target: int(en_reader.readtext(target, allowlist='0123456789')[0][1])

class Image:
    def __init__(self, url_or_image: typing.Union[str, cv2.typing.MatLike]):
        if isinstance(url_or_image, str):
            self.image = cv2.imread(url_or_image)
        else:
            self.image = url_or_image

    def get(self, name: util.RegionName):
        ratio = len(self.image) / 2048
        left, top, width, height = map(lambda l: int(l[1] * ratio), data.region[name].items())
        tar = self.image[top:top+height, left:left+width]
        tar = cv2.cvtColor(tar, cv2.COLOR_BGR2GRAY)

        if name == 'title':
            return util.getClosest(readText(en_ja_reader, tar), data.Musics.all())[0]
        elif name == 'diff':
            return util.getClosest(readText(en_reader, tar), data.diff)[0]
        else:
            return readInt(tar)
