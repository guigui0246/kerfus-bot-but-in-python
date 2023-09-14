from typing import SupportsIndex

class Instance(dict):
    def __init__(self, sett:list = [0, 0, 0], data:list=[0], pointer:SupportsIndex=0, command:SupportsIndex=0, output:str="") -> None:
        self.settings:list=sett
        self.data:list=data
        self.pointer:SupportsIndex=pointer
        self.command:SupportsIndex=command
        self.output:str=output

def create(sett:list = [0, 0, 0]) -> Instance:
    return Instance(sett)

createinstance = create

def runframe(instance:Instance, commands:list[str], input:list[str]) -> bool:
    switch = {}
    def case():
        instance.data[instance.pointer] += 1
        if instance.settings[2] == 0:
            instance.data[instance.pointer] %= 256
    switch['+'] = case
    def case():
        instance.data[instance.pointer] -= 1
        if instance.settings[2] == 0:
            instance.data[instance.pointer] %= 256
    switch['-'] = case
    def case():
        instance.pointer += 1
        if len(instance.data < instance.pointer):
            instance.data.append(0)
    switch['>'] = case
    def case():
        instance.pointer -= 1
    switch['<'] = case
    def case():
        if instance.settings[0] == 1:
            instance.data[instance.pointer] = int(input[0].split(' ')[0])
            input[0] = input[0][len(input[0].split(' ')[0])+1:]
        else:
            instance.data[instance.pointer] = ord(input[0][0])
            input[0] = input[0][1:]
    switch[","] = case
    def case():
        if instance.settings[1] == 1:
            instance.output += instance.data[instance.pointer] + " "
        else:
            instance.output += chr(instance.data[instance.pointer])
    switch["."] = case
    def case():
        if not instance.data[instance.pointer]:
            depth = 1
            while depth > 0:
                instance.command += 1
                depth += commands[instance.command] == '['
                depth -= commands[instance.command] == ']'
    switch["["] = case
    def case():
        if instance.data[instance.pointer]:
            depth = 1
            while depth > 0:
                instance.command -= 1
                depth -= commands[instance.command] == '['
                depth += commands[instance.command] == ']'
    switch["]"] = case
    del case
    switch[commands[instance.command]]()
    del switch
    #print(instance.data, instance.command, instance.pointer)
    instance.command += 1
    return instance.command < len(commands)

def wholesim(settings, runtime, input, code) -> str:
    instance:Instance = create(settings)
    cont = True
    x = 0
    while (x < runtime or runtime == -1) and cont:
        runframe(instance, code, input)
        x += 1
    return instance.output
