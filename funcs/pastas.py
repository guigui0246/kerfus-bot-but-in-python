import misc
import json
import os
from typing import SupportsIndex

class Replies():
    def __init__(self, name:str, client) -> None:
        self.filename = name
        self.client = client
        self.reload()

    def reload(self) -> None:
        with open(os.path.join("data", self.filename), encoding="utf-8") as file:
            self.data = json.load(file)

    def save(self) -> None:
        with open(os.path.join("data", self.filename), "w", encoding="utf-8") as file:
            self.data = json.dump(file)

    def includes(self, msg:str, x:SupportsIndex) -> bool:
        out = False
        for e in self.data[x][2:]:
            out = out or e in msg
        return out

    def allowed(self, x:SupportsIndex, servid:SupportsIndex, chanid:SupportsIndex) -> bool:
        tags = self.data[x][0]
        for a in tags:
            if self.client.misc.hashtag('no'+a, servid):
                return False
        if chanid == 1063934412053557310:
            return False
        return True

    def __len__(self) -> int:
        return len(self.data)

    def get(self, id:SupportsIndex):
        return self.data[id][1]

    def add(self, msg, reactions):
        self.data.append([[], msg] + reactions)
        self.save()

    def findid(self, msg) -> list:
        out = []
        for i in range(len(self.data)):
            if self.includes(msg, i):
                out.append(i)
        return out

    def addreact(self, id:SupportsIndex, react) -> None:
        self.data[id].append(react)
        self.save()

    def getreact(self, id:SupportsIndex):
        return self.data[id][2:]

    def setmsg(self, id:SupportsIndex, msg) -> None:
        self.data[id][1] = msg
        self.save()

    def delet(self, id:SupportsIndex) -> None:
        self.data.pop(id)
        self.save()