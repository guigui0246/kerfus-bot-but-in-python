import os
import json
from typing import Any

class Database():
    """Probably a database for everything the bot needs"""
    def __init__(self, name:str) -> None:
        self.dirname = name
        self.v2get = self.nget
        self.v2set = self.nset
        self.v2del = self.ndel

    def get_user(self, type, id, defi:Any = False) -> str:
        """\"v1 - depracted, don't use\" -0lie\n
        It's deprecated not depracted but ok, I'll still doing it tho\n
        It gives the data from the file => .get()"""
        dir = os.path.join(self.dirname, str(type))
        path = os.path.join(dir, str(id))
        if os.path.exists(path):
            with open(path) as file:
                return file.read()
        else:
            if defi:
                if not os.path.exists(dir):
                    os.makedirs(dir)
                with open(path, "w") as file:
                    json.dump(defi, file)
            return json.dumps(defi)

    def setuser(self, type, id, setto) -> None:
        """Set something to the user file
        Also v1 deprecated but 0lie didn't write it"""
        dir = os.path.join(self.dirname, str(type))
        path = os.path.join(dir, str(id))
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, "w") as file:
            json.dump(setto, file)

    def deluser(self, type, id) -> None:
        """Probably delete a user
        Also v1 deprecated but 0lie didn't write it"""
        dir = os.path.join(self.dirname, str(type))
        path = os.path.join(dir, str(id))
        try:
            os.unlink(path)
        except:
            try:
                os.remove(path)
            except:
                pass

    def get(self, id, defi) -> str:
        """Get the data from the file
        Also v1 deprecated but 0lie didn't write it"""
        dir = os.path.join(self.dirname, "other")
        path = os.path.join(dir, str(id))
        if not os.path.exists(path):
            with open(path) as file:
                return file.read()
        else:
            if not os.path.exists(dir):
                os.makedirs(dir)
            with open("path", "w") as file:
                json.dump(defi, file)
            return json.dumps(defi)

    def set(self, id, setto) -> None:
        """Set the data into the file
        Also v1 deprecated but 0lie didn't write it"""
        dir = os.path.join(self.dirname, "other")
        path = os.path.join(dir, str(id))
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, "w") as file:
            if isinstance(setto, str) and setto.startswith('['):
                json.dump(setto, file)
            else:
                file.write(str(setto))

    def gettype(self, type, id, defi:Any = False):
        """Get the type using the type ?\n
        You should use better variable names 0lie"""
        dir = os.path.join(self.dirname, str(type))
        path = os.path.join(dir, str(id))
        if not os.path.exists(path):
            with open(path) as file:
                return file.read()
        else:
            if defi:
                if not os.path.exists(dir):
                    os.makedirs(dir)
                with open("path", "w") as file:
                    json.dump(defi, file)
            return defi

    def settype(self, type, id, setto) -> None:
        """Set the type"""
        dir = os.path.join(self.dirname, str(type))
        path = os.path.join(dir, str(id))
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, "w") as file:
            json.dump(setto, file)

    def deltype(self, type, id) -> None:
        """Delete a type"""
        dir = os.path.join(self.dirname, str(type))
        path = os.path.join(dir, str(id))
        try:
            os.unlink(path)
        except:
            try:
                os.remove(path)
            except:
                pass

    def nget(self, id, defi:Any = False):
        """\"v2\" - 0lie
        Can you please say v2 of what ????"""
        path = os.path.join(self.dirname, id)
        dir = os.path.split()[0]
        if os.path.exists(path):
            with open(path) as file:
                return file.read()
        else:
            if defi:
                if not os.path.exists(dir):
                    os.makedirs(dir)
                with open(path, "w") as file:
                    file.write(defi)
            return defi

    def nset(self, id, setto):
        """Set the data into the file
        Also v2 but 0lie didn't write it"""
        path = os.path.join(self.dirname, str(id))
        dir = os.path.split()[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, "w") as file:
            file.write(str(setto))
        return self

    def ndel(self, id):
        path = os.path.join(self.dirname, str(id))
        if os.path.exists(path):
            try:
                os.unlink(path)
            except:
                try:
                    os.remove(path)
                except:
                    pass
        return self

    def v2_loaduser(self, type, id):
        dir = os.path.join(self.dirname, "users/")
        path = os.path.join(dir, f"{id}.json")
        if not os.path.exists(dir):
            os.makedirs(dir)
        try:
            module_name = os.path.normpath(path).replace("/", ".").removeprefix("..").removeprefix(".")
            module = {}
            exec("import "+module_name+"\nmodule="+module_name, module, module)
            module[module]
        except:
            pass
        if not os.path.exists(path) or not (type in module or type in module[module]):
            #moving data from v1 to v2
            from_v1 = self.get_user(type, id)
            if from_v1 == "false" or from_v1 == "False":
                from_v1 = self.get_user(type, id + ".json")
            if from_v1 != "false" and from_v1 != "False":
                self.deluser(type, id)
                data = module[module] if os.path.exists(path) else {}
                data[type] = from_v1
                with open(path, "r") as file:
                    json.dump(data, file)
                return data
            else:
                #</moving data>
                data = module[module] if os.path.exists(path) else {}
                with open(path, "w") as file:
                    json.dump(data, file)
        return module[module]

    def v2getuser(self, type, id, defi:Any = False):
        data = self.v2_loaduser(type, id)
        if type is data:
            return data[type]
        if defi:
            data[type] = defi
            path = os.path.join(self.dirname, "users", f"{id}.json")
            with open(path, "w") as file:
                json.dump(data, file)
            return defi
        return None

    def v2setuser(self, type, id, setto):
        data = self.v2_loaduser(type, id)
        data[type] = setto
        path = os.path.join(self.dirname, "users", f"{id}.json")
        with open(path, "w") as file:
            json.dump(data, file)
        return self

    def v2deluser(self, type, id):
        data = self.v2_loaduser(type, id)
        if type in data:
            del data[type]
            path = os.path.join(self.dirname, "users", f"{id}.json")
            with open(path) as file:
                json.dump(data, file)
        return self