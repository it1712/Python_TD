# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from objects import *
from json import dumps
from ast import literal_eval
from PIL import Image, ImageTk

class MyApp:
    def __init__(self, parent):
        self.color_fg = 'black'
        self.color_bg = 'grey'
        self.start_x = 0
        self.start_y = 0
        self.x = 0
        self.y = 0
        self.width = DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"]
        self.height = DEFAULT_CONFIG["side"] * (DEFAULT_CONFIG["rows"] + 1)
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
        self.phase = ""
        self.parent = parent
        self.drawWidgets()
        self.enemy = None
        self.enemies = []
        self.enemy_start_x = None
        self.enemy_start_y = None
        self.hp = 5
        self.money = 500
        self.image = Image.open("image.jpg")
        self.image = self.image.resize((int(DEFAULT_CONFIG["enemy_size"] / sqrt(2)), int(DEFAULT_CONFIG["enemy_size"] / sqrt(2))), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image)
        self.file = None
        self.breakloop = False
        self.turrets = []
        self.turret = None
        self.bullets = []
        self.bullet = None

    def set_default(self):
        self.bullets = []
        self.bullet = None
        self.turret = None
        self.turrets = []
        self.enemy = None
        self.enemies = []
        self.enemy_start_x = None
        self.enemy_start_y = None
        self.hp = 5
        self.money = 500
        self.squares = []
        self.square = None
        self.current_wave = 0
        self.wave_number = 1
        self.start_x = 0
        self.start_y = 0
        self.x = 0
        self.y = DEFAULT_CONFIG["side"]
        self.phase = "shopping"
        self.breakloop = False

    def drawWidgets(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        self.container = Frame(self.parent, width=DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"], height=169999, bg="gray")
        self.canvas = Canvas(self.parent, width=DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"], height=DEFAULT_CONFIG["side"] * (DEFAULT_CONFIG["rows"] + 1), bg=self.color_bg)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonPress-3>", self.on_button_press)
        #self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        #self.canvas.bind("<B1-Motion>", self.on_move_press)


        #Vybrat věž, do proměnné self.currentturretasivole -> vybranou turretu -> podle toho vybrat
        #Hlavně pak udělat nahrazení v self.squares na správné pozici
        button_rectangle = Button(self.container, text="Turret 1", command=self.turret_add)
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
        gamemenu = Menu(menu)
        menu.add_cascade(label='Hra', menu=gamemenu)
        gamemenu.add_command(label='Nová hra', command=self.create_game)
        gamemenu.add_command(label='Konec', command=self.parent.destroy)
        filemenu = Menu(menu)
        menu.add_cascade(label='Soubor', menu=filemenu)
        filemenu.add_command(label='Uložit herní pole', command=self.save_template)
        filemenu.add_command(label='Načíst herní pole', command=self.load_template)

    def p(self):
        pass

    def load_template(self):
        self.breakloop = True
        self.file = askopenfile(mode="r", initialdir="./templates/", title="Vyber soubor", filetypes=(("PythonTowerDefense Template", "*.temp"), ("Všechny soubory", "*.*")))
        file_content = self.file.read()
        #file_content = self.file
        print(file_content)
        self.template = literal_eval(file_content)
        print(self.template)
        self.file.close()
        self.file = None
        self.create_game()

    def save_template(self):
        self.file = asksaveasfile(mode="w", defaultextension=".temp", initialdir="./templates/", title="Uložit soubor")
        self.file.write(dumps(self.template))
        self.file.close()
        self.file = None

    def create_wave(self):
        #root.after(2000, self.create_wave, self)
        if self.phase != "wave":
            self.current_wave = self.first_wave + self.wave_difference * (self.wave_number - 1)
            self.phase = "wave"
            self.create_enemy()
            self.wave_number += 1

    def add_enemy(self):
        if self.phase == "wave":
            self.enemy = Enemy(self.enemy_start_x, self.enemy_start_y)
            self.enemy.img = self.img
            for square in self.squares:
                if square.path:
                    self.enemy.path.append(square)
            self.enemies.insert(0,self.enemy)
            self.create_enemy()

    def create_enemy(self):
        if self.current_wave > 0:
            self.current_wave -= 1
            root.after(2000, self.add_enemy)
        else:
            self.phase = "shopping"

    def bullet_hit_enemy(self):
        for bullet in self.bullets:
            for i, enemy in enumerate(self.enemies):

                point = Point(enemy.x, enemy.y)
                dx = point.x - bullet.x
                dy = point.y - bullet.y
                dist = sqrt(pow(dx, 2) + pow(dy, 2))
                if dist < (DEFAULT_CONFIG["enemy_size"] + bullet.side) / 2 and bullet.hits > 0:
                    bullet.hits -= 1
                    bullet.enemies_hit.append(enemy)
                    self.enemies[i].hp -= bullet.damage
                    print("Enemy hit appended: {}\n".format(bullet.enemies_hit))

    def loop(self):
        for enemy in self.enemies:
            enemy.set_passed()
            enemy.move()
            if enemy.dead():
                self.enemies.remove(enemy)
            if enemy.reached_end():
                self.hp -= 1
                self.enemies.remove(enemy)
        #if len(self.enemies) == 0:
        #    self.phase = "shopping"
        for bullet in self.bullets:
            bullet.enemies = self.enemies
            bullet.move()
            bullet.hit_enemy()
            if bullet.x < 0 or bullet.y < DEFAULT_CONFIG["side"] or bullet.x > self.width or bullet.y > DEFAULT_CONFIG["side"] * (DEFAULT_CONFIG["rows"] + 1) or bullet.destroyed:
                self.bullets.remove(bullet)
        self.redraw_canvas()
        if self.hp > 0:
            if not self.breakloop:
                root.after(int(1000/24), self.loop)
        else:
            self.end_game_dialog()

    def clear_canvas(self):
        self.canvas.delete("all")
        print("Vyčistit canvas")

    def redraw_canvas(self):
        self.clear_canvas()
        for square in self.squares:
            square.draw(self.canvas)
        for enemy in self.enemies:
            enemy.draw(self.canvas)
        for turret in self.turrets:
            turret.draw(self.canvas)
        for bullet in self.bullets:
            bullet.draw(self.canvas)
        if self.turret:
            self.turret.draw_range(self.canvas)
        print("Překreslit canvas")

    def create_game(self):
        self.set_default()
        for i in range(len(self.template)):
            for j in range(len(self.template[i])):
                print(self.template[i][j], end=" ")
                if self.template[i][j] >= 2:
                    self.square = Path(self.x, self.y)
                    if self.template[i][j] == 3:
                        self.square.start = True
                        self.square.fill_color = "green"
                        self.enemy_start_x = self.square.x + DEFAULT_CONFIG["side"] / 2
                        self.enemy_start_y = self.square.y + DEFAULT_CONFIG["side"] / 2
                    if self.template[i][j] == 4:
                        self.square.end = True
                        self.square.fill_color = "red"
                if self.template[i][j] == 1:
                    self.square = Build(self.x, self.y)
                self.squares.append(self.square)
                self.x += DEFAULT_CONFIG["side"]
            print("\n")
            self.y += DEFAULT_CONFIG["side"]
            self.x -= DEFAULT_CONFIG["side"] * len(self.template[i])
            self.square = None
        self.redraw_canvas()
        self.breakloop = False
        self.loop()

    def end_game_dialog(self):
        print("Konec hry")
        if askyesno('Konec hry', 'Chcete začít novou hru?'):
            self.create_game()
            print("_____________NEW GAME_____________")
        else:
            self.parent.destroy()

    def turret_add(self):
        if self.square and not self.square.path:
            if not self.square.turret_built:
                self.turret = Turret(self.square.x, self.square.y)
                self.turret.enemies = self.enemies
                self.bullet = self.turret.attack()
                if self.bullet:
                    self.bullets.append(self.bullet)
                self.turrets.append(self.turret)
                self.square.turret_built = True
                print(self.turrets)

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        point = Point(self.start_x, self.start_y)
        #self.action = ""
        print(event)
        self.square = None
        for idx, square in enumerate(self.squares):
            if not square.path and square.fill_color != DEFAULT_CONFIG["fill"]:
                self.squares[idx].fill_color = DEFAULT_CONFIG["fill"]
            if square.detect_cursor(point):
                self.square = None
                if event.num == 1:
                    if not square.path:
                        self.square = square
                        self.squares[idx].fill_color = "pink"
                    # print("Path")
                    #self.squares[i] = Path(s.x, s.y)

            # if event.num == 3:
            #print("Build")
            # self.squares[i] = Build(s.x, s.y)
            #self.redraw_canvas()

        self.turret = None

        for idx, turret in enumerate(self.turrets):
            if turret.detect_cursor(point) and event.num == 1:
                self.square = None
                self.turret = turret

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
root.geometry("{}x{}+0+0".format(DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"], DEFAULT_CONFIG["side"] * (DEFAULT_CONFIG["rows"] + 2)))
root.resizable(0, 0)
myapp = MyApp(root)
#sdfasd
myapp.create_game()
#sdfasd
root.mainloop()