#########################
# TERMINAL MODULE
# (inputting / outputting text on the console)
#########################

import os, sys

#########################
# Terminal Constants
#########################
def is_color_supported():
    if os.name == 'nt':
        return False
    # Try to set the terminal to red
    sys.stdout.write("\x1b[31m")
    sys.stdout.flush()
    # Try to reset the terminal color
    sys.stdout.write("\x1b[0m")
    sys.stdout.flush()
    # Check if the output is different after the color codes
    return sys.stdout.isatty() and sys.stdout.encoding != 'ascii'

COLOR_ENABLED = is_color_supported()
COLORS = {
    "ENDC":         '\033[0m',
    "BOLD":         '\033[1m',
    "ITALIC":       '\033[3m',
    "UNDERLINE":    '\033[4m',
    "BLACK":        '\033[0;30m',
    "GREY":         '\033[1;30m',
    "GRAY":         '\033[1;30m',
    "RED":          '\033[0;31m',
    "LIGHT_RED":    '\033[1;31m',
    "GREEN":        '\033[0;32m',
    "LIGHT_GREEN":  '\033[1;32m',
    "BROWN":        '\033[0;33m',
    "YELLOW":       '\033[1;33m',
    "BLUE":         '\033[0;34m',
    "LIGHT_BLUE":   '\033[1;34m',
    "PURPLE":       '\033[0;35m',
    "LIGHT_PURPLE": '\033[1;35m',
    "CYAN":         '\033[0;36m',
    "LIGHT_CYAN":   '\033[1;36m',
    "LIGHT_GRAY":   '\033[0;37m',
    "WHITE":        '\033[1;37m' ,
}

VERT = '│'
HORZ = '─'
CROS = '┼┌┬┐└┴┘'
NUMS = "₀₁₂₃₄₅₆₇₈₉"


#########################
# Terminal output
#########################

def announce(message, width=40):
    return ANNOUNCE(message, width)

def ANNOUNCE(message, width=40):
    if width<0: width = len(message)*-width
    color("BOLD")
    printLine(width)
    print(message.upper().center(width))
    printLine(width)
    color("ENDC")

def printLine(width=40):
    print("─"*width)

def clear(): clearScreen()
def clearScreen():
    print("\033c", end="")

def clearLine(lineCount=1, width=None):
    for i in range(lineCount):
        sys.stdout.write("\033[K")
        sys.stdout.write("\033[F")
        if width!=None:
            if type(width)==str: width = len(width)
            print(" "*width)
            clearLine(lineCount=1, width=None)

def flush():
    sys.stdout.flush()

def color(colorKey=None):
    if COLOR_ENABLED:
        if colorKey == None:
            print(COLORS["ENDC"], end="")
        elif type(colorKey)==str:
            colorKey = colorKey.strip().upper()
            if colorKey.strip().upper() in COLORS:
                print(COLORS[colorKey], end="")

# print progress to terminal
# returns message length > externally call mio.clearLine(1, msgLength)
def printProgress(level, currentName, currentNumber, currentList, clearLine=True):
    if type(currentList)==list: currentList = len(currentList)
    if type(currentNumber) in [int,float]: currentNumber += 1
    indentation = level * "    "
    progressString = f"{indentation}Processing {currentName:<18}  -  {currentNumber} / {currentList}"
    print(progressString)
    return len(progressString)



#########################
# Terminal Input
#########################

def numInput(prompt, minimum=None, maximum=None, integer=False, failed=False):
    # ARGUMENT SANATATION
    if maximum==None: maximum = float('inf')
    if minimum==None: minimum = float('-inf')
    # input prompt (color red if previous attempt failed)
    if failed: color("LIGHT_RED")
    print(prompt, end="")
    if failed: color("ENDC")
    inp = input()

    # blank input (return default / re-display prompt with default)
    if inp =="":
        if minimum == float('-inf') and maximum > 0: default = 0
        else: default = minimum
        clearLine(1)
        print(f"{prompt} {default}")
        return default

    # INPUT VALIDATION
    try:
        # (if previous attempt failed, recolor default color)
        if failed:
            clearLine()
            print(prompt+inp)
        # cast to number
        if integer:
            numericInput = int(inp)
        else:
            numericInput = float(inp)
        # bound checker
        if numericInput > maximum:
            raise Exception("Input value too high")
        elif numericInput < minimum:
            raise Exception("Input value too low")
        else:
            return numericInput
    # on invalid input... (recursively prompt again)
    except:
        clearLine(width=len(prompt+inp))
        return numInput(prompt,
            failed=True,
            maximum=maximum,
            minimum=minimum,
            integer=integer)


# using a list, print numbered menu
def menu(optionList, reverse=False):
    if reverse: optionList = optionList[::-1]
    # generate prompt
    menuLines = []
    width = len(optionList)//10
    for i,option in enumerate(optionList):
        menuLine = "{:>"+str(width)+"}. {}"
        if callable(option): option = option.__name__
        menuLines.append(menuLine.format(i+1, option))
    # display prompt
    print("\n".join(menuLines))
    menuPrompt = f"Select an option (1-{len(optionList)}): "
    menuSelection = -1 + numInput(menuPrompt,
        minimum=1,
        maximum=len(optionList),
        integer=True
        )
    # return item from list
    return optionList[menuSelection]


if __name__ == "__main__":
    print(f"color support: {is_color_supported()}")