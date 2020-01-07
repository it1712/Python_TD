# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox, colorchooser
from objects import *

class MyApp:
    def __init__(self, parent):
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.start_x = 0
        self.start_y = 0
        self.x = 0
        self.y = 0
        self.first_wave = 10
        self.wave_difference = 2
        self.current_wave = self.first_wave
        self.wave_number = 1
        #self.template = [[1]*DEFAULT_CONFIG["cols"]]*DEFAULT_CONFIG["rows"]
        self.template = [
            [1,1,1,1,1,1,1,1,1,1],
            [3,2,2,1,1,2,2,2,1,1],
            [1,1,2,1,1,2,1,2,1,1],
            [1,1,2,1,1,2,1,2,2,1],
            [1,1,2,1,1,2,1,1,2,1],
            [1,1,2,2,2,2,1,1,2,1],
            [1,1,1,1,1,1,1,1,2,1],
            [1,1,1,1,1,1,1,1,2,1],
            [4,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1],
        ]
        self.squares = []
        self.square = None
        self.phase = "build"
        self.parent = parent
        self.drawWidgets()
        self.enemy = None
        self.enemys = []
        self.enemy_start_x = None
        self.enemy_start_y = None

    def drawWidgets(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        self.container = Frame(self.parent, width=screen_width - 50, height=300, bg="gray")
        self.canvas = Canvas(self.parent, width=screen_width - 50, height=screen_height - 350, bg=self.color_bg)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonPress-3>", self.on_button_press)
        #self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        #self.canvas.bind("<B1-Motion>", self.on_move_press)


        #Vybrat věž, do proměnné self.currentturretasivole -> vybranou turretu -> podle toho vybrat
        #Hlavně pak udělat nahrazení v self.squares na správné pozici
        button_rectangle = Button(self.container, text="Turret 1", command=self.p)
        button_rectangle.pack(side=LEFT)
        button_rectangle = Button(self.container, text="Turret 2", command=self.p)
        button_rectangle.pack(side=LEFT)
        button_rectangle = Button(self.container, text="add", command=self.add_enemy)
        button_rectangle.pack(side=LEFT)
        button_rectangle = Button(self.container, text="Next wave", command=self.create_wave)
        button_rectangle.pack(side=LEFT)
        button_rectangle = Button(self.container, text="Prodat", command=self.p)
        button_rectangle.pack(side=RIGHT)
        button_rectangle = Button(self.container, text="Vylepšit", command=self.p)
        button_rectangle.pack(side=RIGHT)
        self.container.pack(fill=BOTH)

        self.canvas.focus_set()

        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='Soubor', menu=filemenu)
        filemenu.add_command(label='Konec', command=self.parent.destroy)
        canvasmenu = Menu(menu)
        menu.add_cascade(label='Plátno', menu=canvasmenu)
        canvasmenu.add_command(label='Vyčistit plátno', command=self.clear_canvas)
        canvasmenu.add_command(label='Překreslit plátno', command=self.redraw_canvas)
        objectsmenu = Menu(menu)
        menu.add_cascade(label='Věž', menu=objectsmenu)
        objectsmenu.add_command(label='Vylepšit', command=self.p)
        objectsmenu.add_command(label='Prodat', command=self.p)


    def p(self):
        pass

    def create_wave(self):
        #root.after(2000, self.create_wave, self)
        self.current_wave = self.first_wave + self.wave_difference * self.wave_number
        self.create_enemy()
        self.wave_number += 1

    def add_enemy(self):
        self.enemy = Enemy(self.enemy_start_x, self.enemy_start_y)
        self.enemys.append(self.enemy)
        #self.create_enemy()

    def create_enemy(self):
        if self.current_wave > 0:
            self.current_wave -= 1
            root.after(2000, self.add_enemy)

    def loop(self):
        for enemy in self.enemys:
            enemy.set_passed(self.squares)
            enemy.set_dir(self.squares)
            enemy.move()
            self.redraw_canvas()
        root.after(10, MyApp.loop, self)

    def change_fill_color(self):  # changing the fill color
        if self.square:
            #            self.square.fill_color = colorchooser.askcolor(color=self.square.fill_color)[1]
            self.square.fill_color = "green"
            self.redraw_canvas()
        else:
            print("Objekt neexistuje")

    def clear_canvas(self):
        self.canvas.delete("all")
        print("Vyčistit canvas")

    def redraw_canvas(self):
        self.clear_canvas()
        for square in self.squares:
            square.draw(self.canvas)
        for enemy in self.enemys:
            enemy.draw(self.canvas)
        print("Překreslit canvas")

    def create_game(self):
        self.x = 0
        self.y = 0
        for i in range(len(self.template)):
            for j in range(len(self.template[i])):
                print(self.template[i][j], end=" ")
                if self.template[i][j] >= 2:
                    self.square = Path(self.x, self.y)
                    if self.template[i][j] == 3:
                        self.square.start = True
                        self.enemy_start_x = self.square.x + DEFAULT_CONFIG["side"] / 2
                        self.enemy_start_y = self.square.y + DEFAULT_CONFIG["side"] / 2
                    if self.template[i][j] == 4:
                        self.square.end = True
                if self.template[i][j] == 1:
                    self.square = Build(self.x, self.y)
                self.squares.append(self.square)
                self.x += DEFAULT_CONFIG["side"]
            print("\n")
            self.y += DEFAULT_CONFIG["side"]
            self.x -= DEFAULT_CONFIG["side"] * len(self.template[i])
        self.redraw_canvas()

    # def info_box(self):
    #      messagebox.showinfo('Message title', 'Message content')
    #       print("Zobrazí info")

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        point = Point(self.start_x, self.start_y)
        #self.action = ""
        print(event)
        for i, s in enumerate(self.squares):
            if s.detect_cursor(point):
                if event.num == 1:
                    pass
                    # print("Path")
                    #self.squares[i] = Path(s.x, s.y)
            # if event.num == 3:
            #print("Build")
            # self.squares[i] = Build(s.x, s.y)
            #self.redraw_canvas()

  #  def on_move_press(self, event):
  #      cur_x = self.canvas.canvasx(event.x)
   #     cur_y = self.canvas.canvasy(event.y)
  #      if self.phase == "build":
 #           pass
#
#        if (self.action == "new"):
#            self.square.x = self.start_x if self.start_x <= cur_x else cur_x
#            self.square.y = self.start_y if self.start_y <= cur_y else cur_y
#            self.square.width = abs(self.start_x - cur_x)
#            self.square.height = abs(self.start_y - cur_y)
#
#       if (self.action == "edit"):
#            self.square.x = cur_x - self.start_x + self.old_x
#            self.square.y = cur_y - self.start_y + self.old_y
#
#        if event.state & 0x00001 and self.square:
#            print('SHIFT')
#
#        if event.state & 0x00004 and (self.action == "edit"):
#            print('CTRL')
#
#        if event.state & 0x20000:
#            print('ALT')
#
#        self.redraw_canvas()
#        print("Tažení myši nad plátnem (drag)")

    # def on_ctrl_move_press(self, event):
    #     print("Tažení myši nad plátnem (drag) + CTRL")

#    def on_button_release(self, event):
#        self.action = ""
#        print("Uvolnění tlačítka myši nad plátnem (drop)")


root = Tk()
#root.attributes("-fullscreen", True)
myapp = MyApp(root)
#sdfasd
myapp.create_game()
myapp.loop()
#sdfasd
root.mainloop()