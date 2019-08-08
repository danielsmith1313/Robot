import curses
#Create the screen object
stdscr = curses.initscr()
#Does not mirror input, useful as it is being run in python
curses.noecho()
#Change input to overwrite the buffered input. Allows for instant response from the keyboard with enter keys
curses.cbreak()
#Allows curses to take keypad input automatically
stdscr.keypad(1)

print("Running the main program")

begin_x = 20; begin_y = 7
height = 5; width = 40
win = curses.newwin(height, width, begin_y, begin_x)

closeApplication

def closeApplication():
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()