from tkinter import *
from tkinter import ttk

# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self,parent, **kwargs):
        self.row = kwargs.pop('row', '')
        self.column = kwargs.pop('column', '')

        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # Determine oldWidth: newWidth
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width = self.width, height = self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)

    def getRow(self):
        return self.row
    def getColumn(self):
        return self.column

# ------------------------
player1 = "X"
player1_points = 1
Total_player1_Wins = 0

player2 = "O"
player2_points = -1
Total_player2_Wins = 0

currentPlayer = player1

grid_size = 3
grid = [["" for i in range(grid_size)] for j in range(grid_size)]
score = [0 for i in range(2 * grid_size + 2)]

moves_left = grid_size * grid_size
# ------------------------

def click(event):
    global turn
    global currentPlayer

    makeMove(event.widget.getRow(), event.widget.getColumn())

    if currentPlayer == player1:
        event.widget.create_line(20, 20, event.widget.winfo_width() - 20,  event.widget.winfo_height() - 20, fill = 'black', width = 10)
        event.widget.create_line(event.widget.winfo_width() - 20, 20, 20, event.widget.winfo_height() - 20, fill = 'black', width = 10)
        currentPlayer = player2
    else:
        event.widget.create_oval(20, 20, event.widget.winfo_width() - 20,  event.widget.winfo_height() - 20, width = 10)
        currentPlayer = player1
    checkScore()

def makeMove(row, column):
    global moves_left

    grid[row][column] = currentPlayer
    moves_left -= 1

    if currentPlayer == player1:
        points = player1_points
    else:
        points = player2_points

    score[row] += points
    score[grid_size + column] += points

    if row == column:
        score[2 * grid_size] += points
    if grid_size - 1 - column == row:
        score[2 * grid_size + 1] += points

def checkScore():
    print(score)
    for i in score:
        if (grid_size * player1_points) == i:
            print("Player 1 win")
        if (grid_size * player2_points) == i:
            print("PLayer 2 win")

    if(moves_left == 0):
        print("Draw")

def main():

    root = Tk()
    myframe = Frame(root, bg = 'red')
    myframe.pack(fill=BOTH, expand=YES)

    for i in range(3):
        for j in range(3):
            myframe.grid_rowconfigure(i, weight=1)
            myframe.grid_columnconfigure(j, weight=1)
            mycanvas = ResizingCanvas(myframe, width=100, height=100, bg='white', highlightthickness=0, row = i, column = j)
            mycanvas.grid(column = j, row = i, sticky = N+S+E+W) #fill=BOTH  expand=YES
            mycanvas.bind("<Button-1>", click)

            if i != 0:
                mycanvas.create_line(0, 0, 100, 0, fill = 'black', width = 5)
            if j != 0:
                mycanvas.create_line(0, 0, 0, 100, fill = 'black', width = 5)

    frameDetails = Frame(root, bg='red')
    frameDetails.pack(fill=BOTH, expand=YES)

    frameDetails.grid_rowconfigure(0, weight=1)
    frameDetails.grid_columnconfigure(0, weight=1)
    Label(frameDetails, text ="last winner").grid(row = 0, column = 0)

    root.mainloop()

if __name__ == "__main__":
    main()
