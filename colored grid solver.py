import sys
import random
from PIL import Image, ImageTk
import tkinter as tk

# todo
# set x/y button
# select color

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.button_exist = False
        self.available_color = (
            "black",
            "white",
            "green",
            "yellow",
            "red",
            "purple",
            "pink",
            "orange"
        )
        self.maxcolor = 3
        self.color_array = []
        self.X = 3
        self.Y = 3
        self.TILE_SIZE = 16
        self.im = None
        self.photoim = None
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # "create" button.
        self.create = tk.Button(root)
        self.create["text"] = "Generate"
        self.create["command"] = self.gen
        self.create.pack(side="left")

        # Displayed image.
        self.label = tk.Label(root)
        self.label.pack(side="bottom", fill = "both", expand = "yes")

        # Input field.
        l1 = tk.Label(root, text = "X:")
        l1.pack(side = "left")
        self.textx = tk.Entry(root)
        self.textx.pack(side = "left")
        l2 = tk.Label(root, text = "Y:")
        l2.pack(side = "left")
        self.texty = tk.Entry(root)
        self.texty.pack(side = "left")
        l3 = tk.Label(root, text = "# of color:")
        l3.pack(side = "left")
        self.textmc = tk.Entry(root)
        self.textmc.pack(side = "left")

    def neightbors(self, id):
        n = []
        if id % self.X > 0:
            n.append(id - 1)
        if id % self.X < self.X - 1:
            n.append(id + 1)
        if id - self.X >= 0:
            n.append(id - self.X)
        if id + self.X < len(self.color_array):
            n.append(id + self.X)
        return n

    def flood_fill(self, color):
        visited = [False] * len(self.color_array)
        left = len(self.color_array)
        next = []
        current = 0
        biggest = []

        currentcell = []

        while left > 1:
            left -= 1
            visited[current] = True
            currentcell.append(current)

            # Add to next if same color and not visited.
            for i in self.neightbors(current):
                if self.color_array[i] == self.color_array[current]:
                    if not visited[i]:
                        if i not in next:
                            next.append(i)

            if next:
                current = next.pop(-1)
            # Finished this color patch.
            else:
                if len(currentcell) > len(biggest):
                    biggest = list(currentcell)
                currentcell.clear()
                current = visited.index(False)
        return biggest
    
    def draw_scare(self, id, extra_pixel, color):
        change = int(0.5 * extra_pixel)

        left = int((id % self.X) * self.TILE_SIZE)
        upper = int(int(id / self.X) * self.TILE_SIZE)
        right = int(left + self.TILE_SIZE)
        lower = int(upper + self.TILE_SIZE)

        left -= change
        upper -= change
        right += change
        lower += change

        self.im.paste(self.available_color[color], (left, upper, right, lower))
    
    def displayim(self):
        self.photoim = ImageTk.PhotoImage(self.im)
        self.label.config(image = self.photoim)

    def solve(self):
        # Add a black scare on flood_fill result.
        result = self.flood_fill(0)
        for i in result:
            self.draw_scare(i, -8, 0)
        self.displayim()
        
    def generate(self):
        self.color_array.clear()
        colornumber = len(self.available_color) - 1
        try:
            selectmaxcol = int(self.textmc.get()) + 1
        except:
            selectmaxcol = 4
        colornumber = min(colornumber, max(selectmaxcol, 2))
        for _i in range(self.X * self.Y):
            self.color_array.append(random.randint(2, colornumber))
        
        # Make and display the color array.
        self.im = Image.new("RGB", (self.X * self.TILE_SIZE, self.Y * self.TILE_SIZE), "black")
        for i in range(len(self.color_array)):
            self.draw_scare(i, 1.0, self.color_array[i])
        self.displayim()

    def gen(self):
        try:
            inputx = int(self.textx.get())
        except:
            inputx = 3
        try:
            inputy = int(self.texty.get())
        except:
            inputy = 3
        self.X = max(inputx, 3)
        self.Y = max(inputy, 3)
        self.generate()
        if self.button_exist == False:
            self.button_exist = True
            self.solvebutton = tk.Button(self, text="Solve", fg="red", command=self.solve)
            self.solvebutton.pack(side="right")

root = tk.Tk()
root.title("Colored grid solver!")
app = Application(master=root)
app.mainloop()
