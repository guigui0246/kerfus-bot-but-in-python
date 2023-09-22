import json
import os
from typing import SupportsIndex

class Replies():
    """What makes the replies for the bots\n
    0lie used a json file parsing instead of hardcoding it\n
    That's just harder for me but better in coding rules\n
    If only she did all of it like that"""
    def __init__(self, name:str, client) -> None:
        self.filename = name
        self.client = client
        self.reload()

    def reload(self) -> None:
        "(Re)load from file"
        with open(os.path.join("data", self.filename), encoding="utf-8") as file:
            self.data = json.load(file)

    def save(self) -> None:
        "Save to file"
        with open(os.path.join("data", self.filename), "w", encoding="utf-8") as file:
            self.data = json.dump(file, indent=2)

    def includes(self, msg:str, x:SupportsIndex) -> bool:
        "Test for the presence of a copypasta in the msg"
        out = False
        for e in self.data[x][2:]:
            out = out or e in msg
        return out

    def allowed(self, x:SupportsIndex, servid:SupportsIndex, chanid:SupportsIndex) -> bool:
        "Test if the server or channel have copypastas enabled"
        "But here 0lie fricking hardcoded a channel as disabled"
        tags = self.data[x][0]
        for a in tags:
            if self.client.misc.hashtag('no'+a, servid):
                return False
        if self.client.misc.hastag('nopastas',servid) or self.client.misc.hastag('nopastas',chanid):
            return False
        return True

    def __len__(self) -> int:
        return len(self.data)

    def get(self, id:SupportsIndex):
        """Get the data for a specific id"""
        return self.data[id][1]

    def add(self, msg, reactions):
        """Add data to an id"""
        self.data.append([[], msg] + reactions)
        self.save()

    def findid(self, msg) -> list:
        """Find the id of a msg"""
        out = []
        for i in range(len(self.data)):
            if self.includes(msg, i):
                out.append(i)
        return out

    def addreact(self, id:SupportsIndex, react) -> None:
        """Add a reaction to a msg"""
        self.data[id].append(react)
        self.save()

    def getreact(self, id:SupportsIndex):
        """Get the reactions to do"""
        return self.data[id][2:]

    def setmsg(self, id:SupportsIndex, msg) -> None:
        """Set and save the msg into the data"""
        self.data[id][1] = msg
        self.save()

    def delet(self, id:SupportsIndex) -> None:
        """Remove and id from the data"""
        self.data.pop(id)
        self.save()