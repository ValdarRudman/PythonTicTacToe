from tkinter import *
from tkinter import ttk
from tkinter import messagebox


"""
    a subclass of Canvas for dealing with resizing of windows
"""
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        self.row = kwargs.pop('row', '')
        self.column = kwargs.pop('column', '')
        # Keeps track what is drawn on canvas
        self.drawn = ""

        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    """
        Changes the shapes on the canvas as you resize canvas
    """
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

    def drawX(self):
        self.drawn = "x"
        self.x = self.create_line(20, 20, self.width - 20,  self.height - 20, fill = 'black', width = 10)
        self.x1 = self.create_line(self.width - 20, 20, 20, self.height - 20, fill = 'black', width = 10)

    def drawO(self):
        self.drawn = "o"
        self.o = self.create_oval(20, 20, self.width - 20, self.height - 20, width = 10)

    def deleteX(self):
        self.delete(self.x)
        self.delete(self.x1)

    def deleteO(self):
        self.delete(self.o)

    def resetCanvas(self):
        if self.drawn == "x":
            self.deleteX()
        elif self.drawn == "o":
            self.deleteO()
        self.drawn = ""

    def getDrawn(self):
        return self.drawn

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
canvases = []
# ------------------------

"""
    Draws on canvas clicked on and updates, checkScore
"""
def click(event):
    global turn
    global currentPlayer

    if event.widget.getDrawn() == "":
        makeMove(event.widget.getRow(), event.widget.getColumn())
        if currentPlayer == player1:
            event.widget.drawX()
            currentPlayer = player2
        else:
            event.widget.drawO()
            currentPlayer = player1
        checkScore()

"""
    Updates score
"""
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

"""
    Checks score to see if there is a winner
"""
def checkScore():
    global score
    global moves_left
    print(score)
    for i in score:
        if (grid_size * player1_points) == i:
            messagebox.showinfo("Winner", "Player 1 has won")
            print("Player 1 win")
            clearCanvases()
            score = [0 for i in range(2 * grid_size + 2)]
            moves_left = grid_size * grid_size
            return
        if (grid_size * player2_points) == i:
            messagebox.showinfo("Winner", "Player 2 has won")
            print("PLayer 2 win")
            clearCanvases()
            score = [0 for i in range(2 * grid_size + 2)]
            moves_left = grid_size * grid_size
            return

    if(moves_left == 0):
        messagebox.showinfo("Draw", "Draw")
        print("Draw")
        clearCanvases()
        score = [0 for i in range(2 * grid_size + 2)]

def clearCanvases():
    for canvas in canvases:
         canvas.resetCanvas()

def main():

    root = Tk()
    myframe = Frame(root, bg = 'red')
    myframe.pack(fill=BOTH, expand=YES)

    global canvases

    # Create 9 canvases and appends to canvases list
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
            canvases.append(mycanvas)

    frameDetails = Frame(root, bg='red')
    frameDetails.pack(fill=BOTH, expand=YES)

    frameDetails.grid_rowconfigure(0, weight=1)
    frameDetails.grid_columnconfigure(0, weight=1)
    Label(frameDetails, text ="last winner").grid(row = 0, column = 0)

    root.mainloop()

if __name__ == "__main__":
    main()
