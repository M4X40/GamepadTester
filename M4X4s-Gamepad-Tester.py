#############
## IMPORTS ##
#############

try:
    from inputs import devices, get_gamepad
    import curses
    import os
except:
    import sys, subprocess
    print('Installing Inputs')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'inputs'])
    print('Installing Curses')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'windows-curses'])
    from inputs import devices, get_gamepad
    import curses

##########
## VARS ##
##########

FullKeyMap = {
    "BTN_NORTH":  "Y             ", #0
    "BTN_SOUTH":  "A             ", #1
    "BTN_EAST":   "B             ", #2
    "BTN_WEST":   "X             ", #3
    "BTN_START":  "Start         ", #5
    "BTN_SELECT": "Select        ", #6
    "BTN_TL":     "Left Bumper   ", #8
    "BTN_TR":     "Right Bumper  ", #9
    "BTN_THUMBL": "Left Stick    ", #11
    "BTN_THUMBR": "Right Stick   ", #12
    "ABS_HAT0X":  "D-Pad LR",
    "ABS_HAT0Y":  "D-Pad UD",
    "ABS_X":      "Left Stick LR",
    "ABS_Y":      "Left Stick UD",
    "ABS_RX":     "Right Stick LR",
    "ABS_RY":     "Right Stick UD",
    "ABS_Z":      "Left Trigger  ",
    "ABS_RZ":     "Right Trigger ",
}
LineMap = {
    "A             ": 0,
    "B             ": 1,
    "X             ": 2,
    "Y             ": 3,
    # Line 4 is blank
    "D-Pad Up      ": 5,
    "D-Pad Down    ": 6,
    "D-Pad Left    ": 7,
    "D-Pad Right   ": 8,
    # Line 9 is blank
    "Start         ": 10,
    "Select        ": 11,
    # Line 12 is blank
    "Left Bumper   ": 13,
    "Right Bumper  ": 14,
    # Line 15 is blank
    "Left Trigger  ": 16,
    "Right Trigger ": 17,
    # Line 18 is blank
    "Left Stick    ": 19,
    "Right Stick   ": 20,
    # Line 21 is blank
    "Left Stick X  ": 22,
    "Left Stick Y  ": 23,
    "Right Stick X ": 24,
    "Right Stick Y ": 25,
}
StickNames = [
    "ABS_X",
    "ABS_Y",
    "ABS_RX",
    "ABS_RY"
]
TriggerNames = [
    "ABS_Z",
    "ABS_RZ"
]
BreakButton = False
canrun = False

###################
## GAMEPAD CHECK ##
###################

def TestForGamepad():
    for d in devices:
        if "pad" in str(d):
            print("Gamepad Found! Detecting Inputs:")
            return True
        else:
            pass
    return False

found = False
found = TestForGamepad()
if found:
    canrun = True
else:
    print("Gamepad not found. Try restarting the script.")
    os.system("pause")

############
## CURSES ##
############

#Init
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(False)

#Labels
stdscr.addstr(LineMap["Y             "],0, "Y             |   Released")
stdscr.addstr(LineMap["A             "],0, "A             |   Released")
stdscr.addstr(LineMap["B             "],0, "B             |   Released")
stdscr.addstr(LineMap["X             "],0, "X             |   Released")

stdscr.addstr(LineMap["Start         "],0, "Start         |   Released")
stdscr.addstr(LineMap["Select        "],0, "Select        |   Released")

stdscr.addstr(LineMap["Left Bumper   "],0, "Left Bumper   |   Released")
stdscr.addstr(LineMap["Right Bumper  "],0, "Right Bumper  |   Released")

stdscr.addstr(LineMap["Left Stick    "],0,"Left Stick    |   Released")
stdscr.addstr(LineMap["Right Stick   "],0,"Right Stick   |   Released")

stdscr.addstr(LineMap["D-Pad Up      "],0,"D-Pad Up      |   Released")
stdscr.addstr(LineMap["D-Pad Down    "],0,"D-Pad Down    |   Released")
stdscr.addstr(LineMap["D-Pad Right   "],0,"D-Pad Right   |   Released")
stdscr.addstr(LineMap["D-Pad Left    "],0,"D-Pad Left    |   Released")

stdscr.addstr(LineMap["Left Trigger  "],0,"Left Trigger  |   0%")
stdscr.addstr(LineMap["Right Trigger "],0,"Right Trigger |   0%")

stdscr.addstr(LineMap["Left Stick X  "],0,"Left Stick X  |   0%")
stdscr.addstr(LineMap["Left Stick Y  "],0,"Left Stick Y  |   0%")
stdscr.addstr(LineMap["Right Stick X "],0,"Right Stick X |   0%")
stdscr.addstr(LineMap["Right Stick Y "],0,"Right Stick Y |   0%")

stdscr.refresh()

############
## INPUTS ##
############

def StickInput(name, state):
    state = round(round(state/32767, 2) * 100)
    match name:
        case "ABS_X":
            name = "Left Stick X  "
        case "ABS_Y":
            name = "Left Stick Y  "
        case "ABS_RX":
            name = "Right Stick X "
        case "ABS_RY":
            name = "Right Stick Y "
    line = LineMap[name]
    stdscr.addstr(line,0,f"{name}|   {state}%     ")
    stdscr.refresh()
def TriggerInput(name, state):
    state = round(round(state/255, 2) * 100)
    line = LineMap[name]
    stdscr.addstr(line,0,f"{name}|   {state}%     ")
    stdscr.refresh()
def BTNPrint(name, state):
    match state:
        case 1:
            state = "Pressed"
        case 0:
            state = "Released"
    line = LineMap[name]
    stdscr.addstr(line,0,f"{name}|   {state}     ")
    stdscr.refresh()
def DPadInput(name, state):
    if "X" in name:
        match state:
            case -1:
                name = "D-Pad Left    "
                state = "Pressed"
            case 0:
                stdscr.addstr(LineMap["D-Pad Left    "],0,f"D-Pad Left    |   Released     ")
                name = "D-Pad Right   "
                state = "Released"
            case 1:
                name = "D-Pad Right   "
                state = "Pressed"
    else:
        match state:
            case -1:
                name = "D-Pad Up      "
                state = "Pressed"
            case 0:
                stdscr.addstr(LineMap["D-Pad Up      "],0,f"D-Pad Up      |   Released     ")
                name = "D-Pad Down    "
                state = "Released"
            case 1:
                name = "D-Pad Down    "
                state = "Pressed"
    line = LineMap[name]
    stdscr.addstr(line,0,f"{name}|   {state}     ")
    stdscr.refresh()

def NameInput(name):
    return FullKeyMap[name]

def MainLoop():
    global canrun
    while canrun:
        try:
            events = get_gamepad()
            for event in events: 
                if event.ev_type == "Sync": # Filters unneeded returns
                    continue
                name = event.code
                RealName = NameInput(name)
                state = event.state

                if name in StickNames:
                    StickInput(name, state)
                    continue
                elif name in TriggerNames:
                    TriggerInput(RealName, state)
                    continue
                elif "BTN" in name:
                    BTNPrint(RealName, state)
                elif "HAT0" in name:
                    DPadInput(name, state)

                if not BreakButton == False and name == BreakButton: # Debug break button
                    canrun = False
                    break
        except Exception as e:
            print(f"[ERR] {e}")
            canrun = False

if __name__ == "__main__":
    MainLoop()