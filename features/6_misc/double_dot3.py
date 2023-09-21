def run(msg, client):
    """exec the calculation and return +1"""
    if (msg.content == ':sudo rm -rf /*'):
        try:																# This is so it feals
            import random													# more real
            files = random.randint(6000, 10000)								# The part with comments
            time = random.random() + 1										# can be removed
            msg.reply(f"{files} files deleted ({time:.3f} seconds)")		#
        except:																#
            pass															#
        msg.reply(f"6396 files deleted (1.405 seconds)")
        return
    import re
    cont = msg.content
    if not re.compile("^:-?(\(-?)*(((\(-?)*[0-9]+(\.[0-9]+)?|NaN|Infinity)\)*(\+|\-|\*|\/|\*\*[-]?))*(\(-?)*([0-9]+(\.[0-9]+)?|NaN|Infinity)\)*$").fullmatch(cont):
        return
    #depth = 0						# This is the original code
    #for a in cont:					# It was changed for what's after
    #    if a == '(':				#
    #        depth += 1				#
    #    if a == ')':				#
    #        depth -= 1				#
    #    if depth < 0:				#
    #        return					#
    #if depth != 0:					#
    #    return						#
    if not cont.count("(") == cont.count(")"):			# This is the new code
        return											#
    cont.replace("Infinity", "float('inf')")
    cont.replace("NaN", "float('NaN')")
    msg.reply(f":{str(1+eval(cont[1:])).replace('inf', 'Infinity').replace('nan', 'NaN')}")
