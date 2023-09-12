from sys import stderr

import re
from typing import SupportsIndex
LETTER_DIGIT_UNDERSCORE_PATTERN = re.compile("[a-zA-Z0-9_]")
ALPHABET = "qwertyuiopasdfghjklzxcvbnm" + "qwertyuiopasdfghjklzxcvbnm".capitalize()

def word_at(word:str,at:SupportsIndex) -> tuple[str, SupportsIndex, SupportsIndex] | None:
    if at >= len(word) or at < -len(word) or len(word[at].split()) == 0:
        return None
    start = at if at > 0 else len(word) - at
    end = start
    if (LETTER_DIGIT_UNDERSCORE_PATTERN.search(word[at])):
        while (start > 0 and LETTER_DIGIT_UNDERSCORE_PATTERN.search(word[start-1]) != None):
            start -= 1
        while (end < len(word) and LETTER_DIGIT_UNDERSCORE_PATTERN.search(word[end]) != None):
            end += 1
    if (end - start == 0):
        return word[start:end+1],start,end
    return word[start:end],start,end

def find_vars(code:str) -> list[str]:
    vars = code
    with open('data/keywords.txt', encoding="utf-8") as file:
        keywords = file.readlines()
    keywords = [e.removesuffix("\n").strip() for e in keywords]
    vars = vars.split('\n')
    vars = [i for i in vars if re.compile("/^#/").search(i) == None]
    vars = " ".join(vars)
    instr = False
    strstart = 0
    for x in range(len(vars)):
        if not x < len(vars):
            break
        if (vars[x] != "\""):
            continue
        if not instr:
            strstart = x
        else:
            vars = vars[:strstart]+vars[x:]
        instr = not instr
    for x in range(len(vars)):
        wa = word_at(vars, x)
        if not wa == None:
            vars = vars.replace(wa[0], ' ') if wa[0] in keywords else vars
    vars = list(set(vars.split()))
    for x in range(len(vars)):
        while x < len(vars) and re.compile("^[0-9]+(.[0-9]+)?$").search(vars[x]) != None:
            vars.pop(x)
    return [x for x in vars if not x == ""]

def rand_name() ->str:
    import random
    x = random.randint(0, 2)
    name = ALPHABET[random.randint(0, len(ALPHABET)-1)]
    abc = ALPHABET + "0123456789"
    for i in range(x):
        name += ALPHABET[random.randint(0, len(ALPHABET)-1)]
    return name

#This makes the code unreadable (anonymize function)
def anon(code:str) -> str:
    temp = code.split('\n')
    org = ""
    # removing comments
    for x in temp:
        org += x + '\n' if re.compile("^\/\/").search(x) == None else ''

    # generating new var names
    vars = find_vars(org)
    newnames = list()
    while len(newnames) < len(vars):
        temp = rand_name()
        if temp not in vars and temp not in newnames:
            newnames.append(temp)

    # replacing variables with new names
    x = 0
    while x < len(code):
        wa = word_at(code, x)
        if not wa == None:
            try:
                index = vars.index(wa[0])
            except ValueError:
                pass
            else:
                code = code[:wa[1]] + newnames[index] + code[wa[2]:]
                x += len(newnames[index])
        x += 1

    # splitting fors into multiple lines
    import random
    def _replace_for_loops(match:re.Match) -> str:
        p1, p2, p3, p4 = match.groups()
        if not random.randint(0, 4):
            return f'\n{p1}for(\n\t{p1+p2};\n\t{p1+p3};\n\t{p1+p4}\n{p1})'
        return match.group()
    code = re.sub('\n([ \t]*)for\((.*);(.*);(.*)\)', _replace_for_loops, code)

    # doubling line breaks
    def _replace_line_breaks(match:re.Match) -> str:
        return f'\n\n' if random.randint(0, 2) else '\n'
    code = re.sub('\n', _replace_line_breaks, code)

    return code

#I don't know what that is but Olie exported it
def test ():
    return
