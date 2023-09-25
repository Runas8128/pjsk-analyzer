import discord

import asyncio
import numpy as np
import cv2
import getText
from mongoose import Mongoose

accMap = [
    ('perfect', 100),
    ('great', 75),
    ('good', 50),
    ('bad', 25),
    ('miss', 0),
]

class Uploader:
    reply: discord.Message
    def __init__(self, message: discord.Message):
        self.message = message
        self.uid = str(message.author.id)
        self.atts = message.attachments

        self.add = 0
        self.uploadCount = 0
        self.total = len(self.atts)
        
        self.reply = None

        self.lock = asyncio.Lock()
    
    def hasRedundant(self, rst):
        return Mongoose.has(self.uid, { 'title': rst['title'], 'diff': rst['diff'], 'score': rst['score'] })

    async def upload(self, att: discord.Attachment):
        buf = await att.read()
        rst = Uploader.analyze(buf)
        if not self.hasRedundant(rst):
            Mongoose.upload(self.uid, rst) # add new
            self.add += 1
        async with self.lock:
            self.uploadCount += 1
            await self.reply.edit(
                content=f'analyzing... ({self.uploadCount}/{self.total})',
                allowed_mentions=discord.AllowedMentions.none()
            )
    
    async def start(self):
        self.reply = await self.message.reply(
            content=f'analyzing... (0/{self.total})',
            allowed_mentions=discord.AllowedMentions.none()
        )
        await asyncio.gather(*list(map(lambda img: self.upload(img), self.atts)))
        await self.reply.edit(
            content=f'all image analyzed. ' + \
                    f'{self.add} data added, ' + \
                    f'{self.uploadCount - self.add} redundant data ignored',
            allowed_mentions=discord.AllowedMentions.none()
        )

    @staticmethod
    def analyze(buf: bytes):
        nparr = np.fromstring(buf, np.uint8)
        img_np = cv2.imdecode(nparr, 1)
        img = getText.Image(img_np)
        judges = dict([judge, img.get(judge)] for (judge, _) in accMap)

        return {
            'title': img.get('title'),
            'diff': img.get('diff'),
            'score': img.get('score'),
            'combo': img.get('combo'),
            'judge': judges,
            'acc': sum(judges[judge] * score for (judge, score) in accMap) / sum(judges.values())
        }
