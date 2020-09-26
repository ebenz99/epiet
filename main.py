import pygame
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from painterModules.gridModule import colorPallet
from painterModules.gridModule import pixelArt
from painterModules.gridModule import menu
from painterModules.gridModule import grid
from painterModules.interpreterModule import Interpreter
import sys
import time


sys.setrecursionlimit(1000000)

pygame.init() #initalize pygame
paintBrush = pygame.image.load("imgs/Paintbrush.png")
currentVersion = 1.1

#Set defaults for our screen size and rows and columns
rows = 30
cols = 30
wid = 800
heigh = 800
showGrid = True

colorRows = 5
colorCols = 4
realColors = [(255,0,0),(255,128,0),(204,204,255),(200,50,200),(0,153,153),(255,204,153),(255,255,0),(30,100,100),(0,255,0),(0,255,255),(70,70,70),(0,128,255),(127,0,255),(255,0,255),(229,255,204),(153,0,76),(255,0,127),(128,128,128),(50,90,160),(255,255,255)]
instructions = ["Save R1","Save R2","Save R3","Load R1","Load R2","Load R3","Add","Subtract","Multiply","Divide","Mod","Exit","CastToChar","CastToInt","Pass","Print","strPrint","strAppend","strClear","Pass"]



checked = []
def fill(spot, grid, color, c):
   if spot.color != c:
      pass
   else:
      spot.click(grid.screen, color)
      pygame.display.update()

      i = spot.col #the var i is responsible for denoting the current col value in the grid
      j = spot.row #the var j is responsible for denoting the current row value in the grid

      #Horizontal and vertical neighbors
      if i < cols-1: #Right
         fill(grid.getGrid()[i + 1][j], grid, color, c)
      if i > 0: #Left
         fill(grid.getGrid()[i - 1][j], grid, color, c)
      if j < rows-1: #Up
         fill(grid.getGrid()[i][j + 1], grid, color, c)
      if j > 0 : #Down
         fill(grid.getGrid()[i][j - 1], grid, color, c)


# saves the current project into a text file that contains the size of the screen, if the gird is showing and all the colors of all the pixels
def save(cols, rows, show, grid, path):
   if len(path) >= 4: # This just makes sure we have .txt at the end of our file selection
      if path[-4:] != '.txt':
         path = path + '.txt'
   else:
      path = path + '.txt'

   # Overwrite the current file, or if it doesn't exist create a new one
   file = open(path, 'w')
   file.write(str(cols) + ' ' + str(rows) + ' ' + str(show) +'\n')

   rows = [[] for i in range(len(grid[0]))]

   for pixel in grid:
       for idx,p in enumerate(pixel): #For every pixel write the color in the text file
           rows[idx].append(p)

   for row in rows:
       for p in row:
           wr = str(p.color[0]) + ',' + str(p.color[1]) + ',' + str(p.color[2])
           file.write(wr + '\n')

   # for pixel in grid:
   #     for p in pixel: #For every pixel write the color in the text file
   #         wr = str(p.color[0]) + ',' + str(p.color[1]) + ',' + str(p.color[2])
   #         file.write(wr + '\n')
   file.write(str(currentVersion))

   file.close()
   name = path.split("/")
   changeCaption(name[-1])


#Opens the file from the given path and displays it to the screen
def openFile(path):
    global grid

    file = open(path, 'r')
    f = file.readlines()
    if f[-1] == str(currentVersion):

       dimensions = f[0].split()    #Dimesnions for the rows and cols
       columns = int(dimensions[0])
       rows = int(dimensions[1])

       if dimensions[2] == '0': #If the show grid attribute at the end of our dimensions line is 0 then don't show grid
          v = False
       else:
          v = True
       initalize(columns, rows, v) #Redraw the grid, tool bars, menu bars etc.
       name = path.split("/")
       changeCaption(name[-1])

       line = 0
       for i in range(columns): # For every pixel, read the color and format it into a tuple
          for j in range(rows):
             line += 1
             nColor = []
             for char in f[line].strip().split(','):
                nColor.append(int(char))


             grid.getGrid()[j][i].show(win, tuple(nColor), 0) #Show the color on the grid
    else:
      window = Tk()
      window.withdraw()
      messagebox.showerror("Unsupported Version", "The file you have opened is created using a previous version of this program. Please open it in that version.")


#Change pygame caption
def changeCaption(txt):
   pygame.display.set_caption(txt)


# This shows the file navigator for opening and saving files
def showFileNav(op=False):
   #Op is short form for open as open is a key word
    window = Tk()
    window.attributes("-topmost", True)
    window.withdraw()
    myFormats = [('Windows Text File','*.txt')]
    if op:
       filename = askopenfilename(title="Open File",filetypes=myFormats) # Ask the user which file they want to open
    else:
       filename = asksaveasfilename(title="Save File",filetypes=myFormats) # Ask the user choose a path to save their file to

    if filename: #If the user seletced something
       x = filename[:] # Make a copy
       return x

# Onsubmit function for tkinter form for choosing pixel size
def onsubmit(x=0):
    global cols, rows, wid, heigh

    st = (30,30)
    window.quit()
    window.destroy()
    try: # Make sure both cols and rows are integers
        if st[0].isdigit():
            cols = int(st[0])
            while 600//cols != 600/cols:
               if cols < 300:
                  cols += 1
               else:
                  cols -= 1
        if st[1].isdigit():
            rows = int(st[1])
            while 600//rows != 600/rows:
               if rows < 300:
                  rows += 1
               else:
                  rows -= 1
        if cols > 300:
          cols = 300
        if rows > 300:
          rows = 300

    except:
        pass

# Update the lbale which shows the pixel size by getting input on rows and cols
# def updateLabel(a, b, c):
#    sizePixel = rowsCols.get().split(',') #Get the contents of the label
#    l = 12
#    w = 12
#
#    try:
#       l = 600/int(sizePixel[0])
#    except:
#       pass
#
#    try:
#       w = 600/(int(sizePixel[1]))
#    except:
#       pass
#
#    label1.config(text='Pixel Size: ' + str(l) + ', ' + str(w)) #Change label to show pixel size


#CREATE SCREEN
def initalize(cols, rows, showGrid=False):
   global pallet, grid, win, tools, lineThickness, saveMenu

   #if grid already exsists delete it then recreate it
   try:
      del grid
   except:
      pass

   pygame.display.set_icon(paintBrush)
   win = pygame.display.set_mode((int(wid), int(heigh) + 300))
   pygame.display.set_caption('Untitled')
   win.fill((255,255,255))

   #CREATION OF OBJECTS
   #last argument controls spacing from the left
   grid = pixelArt(win, int(wid)-100, int(heigh)-80, cols, rows, showGrid,40)
   grid.drawGrid()

   pallet = colorPallet(win, 270, 170, colorRows, colorCols, True, 50, grid.height+20)
   pallet.drawGrid()

   #colorList = [(0,0,0), (255,255,255), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,168,0), (244, 66, 173), (65, 244, 226), (255,168,10), (0, 66, 173), (65, 9, 226)]
   colorList = realColors
   pallet.setColor(colorList)
   instGrid = menu(win, 270, 170, colorRows, colorCols, True, 50, grid.height+20)
   instGrid.setCMDText(instructions)

   lineThickness = menu(win, 1, 1, 4, 1, True, grid.width, grid.height)

   saveMenu = menu(win, 230, 100, 3, 1, True, grid.width - 200, grid.height + 25)
   saveMenu.drawGrid()

   buttons = ['Save', 'Open', 'Run']
   saveMenu.setText(buttons)

   pygame.display.update()

#-----------------------------------------------------------------------#
    #TKINTER FORM FOR GETTING INPUT#
window = Tk()
window.title('Paint Program')

t_var = StringVar()
# rowsCols = Entry(window, textvariable=t_var)

var = IntVar()
# c = Checkbutton(window, text="View Grid", variable=var)
submit = Button(window, text='Begin', command=onsubmit)
window.bind('<Return>', onsubmit)

submit.grid(columnspan=1, row=3, column=1,padx=100,pady=100)
# c.grid(column=0, row=3)
# rowsCols.grid(row=0, column=1, pady=3, padx=8)
# label.grid(row=0, pady=3)

window.update()
mainloop()

#------------------------------------------------------------------------#


#MAIN LOOP
initalize(cols, rows, True)
pygame.display.update()
color = (0,0,0) # Current drawing color
thickness = 1
replace = False
doFill = False
savedPath = '' #Current path of file

run = True
path = ""
while run:
    #Main loop for mouse collision
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            window = Tk()
            window.withdraw()
            #Ask the user if they want to save before closing
            if pygame.display.get_caption()[0].count('*') > 0:
               if messagebox.askyesno("Save Work?", "Would you like to save before closing?"):
                  # If they have already saved the file simply save to that path otherwise they need to chose a location
                  if savedPath != "":
                     save(cols, rows, grid.showGrid, grid.getGrid(),savedPath)
                  else:
                     path = showFileNav()
                     if path != "" and path != None:
                        savedPath = path
                        save(cols, rows, grid.showGrid, grid.getGrid(),savedPath)
            run = False

        if pygame.mouse.get_pressed()[0]: #See if the user has clicked or dragged their mouse
            try:
                pos = pygame.mouse.get_pos()
                if pos[1] >= grid.height: # If the mouse is below the main drawing grid
                    #If they click on the color pallet
                    if pos[0] >= pallet.startx and pos[0] <= pallet.startx + pallet.width and pos[1] >= pallet.starty and pos[1] <= pallet.starty + pallet.height:
                        clicked = pallet.clicked(pos)
                        color = clicked.getColor() # Set current drawing color

                        pallet = colorPallet(win, 270, 170, colorRows, colorCols, True, 50, grid.height+20)
                        pallet.drawGrid()

                        #colorList = [(0,0,0), (255,255,255), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,168,0), (244, 66, 173), (65, 244, 226), (255,168,10), (0, 66, 173), (65, 9, 226)]
                        colorList = realColors
                        pallet.setColor(colorList)
                        instGrid = menu(win, 270, 170, colorRows, colorCols, True, 50, grid.height+20)
                        instGrid.setCMDText(instructions)
                        clicked.show(grid.screen, (255,0,0), 3, True)

                    elif pos[0] >= lineThickness.startx and pos[0] <= lineThickness.startx + lineThickness.width and pos[1] >= lineThickness.starty and pos[1] <= lineThickness.starty + lineThickness.height:
                        lineThickness.drawGrid() #Redraw the grid so that we dont see the red highlight
                        buttons = ['1', '2', '3', '4']
                        lineThickness.setText(buttons)

                        clicked = lineThickness.clicked(pos)
                        clicked.show(grid.screen, (255,0,0), 1, True)

                        thickness = int(clicked.text) # set line thickness

                    #If they click on the save menu

                    elif pos[0] >= saveMenu.startx and pos[0] <= saveMenu.startx + saveMenu.width/3 and pos[1] >= saveMenu.starty and pos[1] <= saveMenu.starty + saveMenu.height:
                        clicked = saveMenu.clicked(pos)

                        if clicked.text == 'Save': # save if they click save
                            path = showFileNav()
                            if path != "" and path != None:
                               savedPath = path
                               save(cols, rows, grid.showGrid, grid.getGrid(),savedPath)
                    elif pos[0] >= saveMenu.startx + saveMenu.width/3 and pos[0] <= saveMenu.startx + 2*saveMenu.width/3 and pos[1] >= saveMenu.starty and pos[1] <= saveMenu.starty + saveMenu.height:
                            path = showFileNav(True)
                            if path != "" and path != None:
                               openFile(path)
                               savedPath = path
                    else:
                        if path != "" and path != None:
                           savedPath = path
                           interp = Interpreter(path,instructions)
                           interp.readGrid()
                           interp.execute()
                else:
                    if replace: #If we have the replace tool selected then replace the color
                        clicked = grid.clicked(pos)
                        c = clicked.color
                        replace = False

                        for x in grid.getGrid():
                            for y in x:
                                if y.color == c:
                                    y.click(grid.screen, color)
                    elif doFill:
                       clicked = grid.clicked(pos)
                       if clicked.color != color:
                          fill(clicked, grid, color, clicked.color)
                          pygame.display.update()

                    else:
                        name = pygame.display.get_caption()[0]
                        if name.find("*") < 1:
                           changeCaption(name + '*')

                        clicked = grid.clicked(pos)
                        clicked.click(grid.screen,color)
                        if thickness == 2:
                            for pixel in clicked.neighbors:
                                pixel.click(grid.screen, color)
                        elif thickness == 3:
                            for pixel in clicked.neighbors:
                                pixel.click(grid.screen, color)
                                for p in pixel.neighbors:
                                    p.click(grid.screen, color)
                        elif thickness == 4:
                            for pixel in clicked.neighbors:
                                pixel.click(grid.screen, color)
                                for p in pixel.neighbors:
                                    p.click(grid.screen, color)
                                    for x in p.neighbors:
                                        x.click(grid.screen, color)

                pygame.display.update()
            except AttributeError:
                pass

pygame.quit()
