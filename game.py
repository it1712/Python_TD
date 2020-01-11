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
        #tvorba mapy (templatu) - asi nestíhám, bo x == 0 -_-
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
        self.money = 0
        self.image = Image.open("image.jpg")
        self.image = self.image.resize((int(DEFAULT_CONFIG["enemy_size"] / sqrt(2)), int(DEFAULT_CONFIG["enemy_size"] / sqrt(2))), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image)
        self.image = Image.open("image.jpg")
        self.image = self.image.resize((DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"], DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["rows"]), Image.ANTIALIAS)
        self.endimg = ImageTk.PhotoImage(self.image)
        self.file = None
        self.breakloop = False
        self.turrets = []
        self.turret = None
        self.bullets = []
        self.bullet = None
        self.delay_between_spawn = 2000
        self.auto_wave = False

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
        self.wave_number = 0
        self.start_x = 0
        self.start_y = 0
        self.x = 0
        self.y = DEFAULT_CONFIG["side"]
        self.phase = "shopping"
        self.breakloop = False
        self.delay_between_spawn = 2000
        self.auto_wave = False

    def drawWidgets(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        self.container = Frame(self.parent, width=DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"], height=1000, bg="gray")
        self.canvas = Canvas(self.parent, width=DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"], height=DEFAULT_CONFIG["side"] * (DEFAULT_CONFIG["rows"] + 1), bg=self.color_bg)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonPress-3>", self.on_button_press)
        button_rectangle = Button(self.container, text="Turret Big (100$)", command=self.turret_add_big)
        button_rectangle.pack(side=LEFT)
        button_rectangle = Button(self.container, text="Turret Fast (100$)", command=self.turret_add_fast)
        button_rectangle.pack(side=LEFT)
        button_rectangle = Button(self.container, text="Další vlna", command=self.create_wave)
        button_rectangle.pack(side=LEFT)
        button_rectangle = Button(self.container, text="Další vlna automaticky", command=self.auto_new_wave)
        button_rectangle.pack(side=LEFT)
        button_rectangle = Button(self.container, text="Prodat", command=self.turret_sell)
        button_rectangle.pack(side=RIGHT)
        button_rectangle = Button(self.container, text="Vylepšit", command=self.turret_upgrade)
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

    def auto_new_wave(self):
        self.auto_wave = True if not self.auto_wave else False

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
            self.wave_number += 1
            self.current_wave = self.first_wave + self.wave_difference * (self.wave_number - 1)
            self.phase = "wave"
            self.bullets.clear()
            self.create_enemy(100 + 50 * (self.wave_number - 1), 1 + 0.5 * (self.wave_number - 1))

    def add_enemy(self, hp, speed):
        if self.phase == "wave":
            self.enemy = Enemy(self.enemy_start_x, self.enemy_start_y, hp, speed)
            self.enemy.img = self.img
            for square in self.squares:
                if square.path:
                    self.enemy.path.append(square)
            self.enemies.insert(0, self.enemy)
            self.create_enemy(hp, speed)

    def create_enemy(self, hp, speed):
        if self.current_wave > 0:
            self.current_wave -= 1
            self.delay_between_spawn -= self.delay_between_spawn / 100
            root.after(int(self.delay_between_spawn), self.add_enemy, hp, speed)
        else:
            self.phase = "shopping"

    def bullet_hit_enemy(self, bullet):
        for i, enemy in enumerate(self.enemies):

            point = Point(enemy.x, enemy.y)
            dx = point.x - bullet.x
            dy = point.y - bullet.y
            dist = sqrt(pow(dx, 2) + pow(dy, 2))
            if dist < (DEFAULT_CONFIG["enemy_size"] + bullet.side) / 2 and bullet.hits > 0:
                bullet.hits -= 1
                print(bullet.hits)
                print("\n\n\n\n\n")
                bullet.enemies_hit.append(enemy)
                self.enemies[i].hp -= bullet.damage
                print("Enemy hit appended: {}\n".format(bullet.enemies_hit))

    def turret_attack(self, turret):
        if turret.loaded == 1:
            turret.loaded = 0
            root.after(int(turret.load_time), turret.reload)
            turret.in_range = []
            for enemy in self.enemies[::-1]:
                x = enemy.x
                y = enemy.y
                dxc = x - turret.x
                dyc = y - turret.y
                dis = sqrt(pow(dxc, 2) + pow(dyc, 2))
                if dis < turret.range:
                    turret.in_range.append(enemy)
            if len(turret.in_range) > 0:
                enemy = turret.in_range[0]

                dxc = abs(enemy.x - turret.x)
                dyc = abs(enemy.y - turret.y)

                if dxc == 0:
                    vel_x = 0
                else:
                    vel_x = dxc / dxc if dxc > dyc else dxc / dyc
                if enemy.x - turret.x < 0:
                    vel_x *= -1

                if dyc == 0:
                    vel_y = 0
                else:
                    vel_y = dyc / dyc if dyc > dxc else dyc / dxc
                if enemy.y - turret.y < 0:
                    vel_y *= -1

                self.bullet = Bullet(turret.x, turret.y, vel_x, vel_y, turret.damage, turret.bullet_size, turret.bullet_hits)
        else:
            self.bullet = None

    def loop(self):
        for enemy in self.enemies:
            enemy.set_passed()
            enemy.move()
            if enemy.dead():
                self.enemies.remove(enemy)
                self.money += enemy.reward
            if enemy.reached_end():
                self.hp -= 1
                self.enemies.remove(enemy)
        if len(self.enemies) == 0 and self.auto_wave:
            self.create_wave()
            #self.phase = "shopping"

        for turret in self.turrets:
            self.turret_attack(turret)
            if self.bullet:
                self.bullets.append(self.bullet)
        for bullet in self.bullets:
            bullet.move()
            bullet.is_destroyed()
            self.bullet_hit_enemy(bullet)
            bullet.is_destroyed()
            if bullet.destroyed:
                self.bullets.remove(bullet)
                print(self.bullets)
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
            #self.canvas.create_text(turret.x - turret.side / 2 + 5, turret.y + turret.side / 2, fill="black", font="arial 12",
            #                   text="{}".format(turret.level), anchor=SW)
        for bullet in self.bullets:
            bullet.draw(self.canvas)
        if self.turret:
            self.turret.draw_range(self.canvas)
            self.canvas.create_text(DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"] - 10, DEFAULT_CONFIG["side"] * (DEFAULT_CONFIG["rows"] + 1) + 10,
                                    fill="black", font="arial 15", text="Vylepšit za {}$   Prodat za {}$".format(self.turret.cost * 2, self.turret.total_cost / 2), anchor=NE)
        self.canvas.create_text((DEFAULT_CONFIG["side"]*DEFAULT_CONFIG["cols"] - 10), DEFAULT_CONFIG["side"] / 2,
                                fill="yellow", font="times 30 italic bold", text="{}$".format(self.money), anchor=E)
        self.canvas.create_text(10, DEFAULT_CONFIG["side"] / 2, fill="black", font="arial 30",
                                text="Wave: {}".format(self.wave_number), anchor=W)
        self.canvas.create_text(DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"] / 2, DEFAULT_CONFIG["side"] / 2,
                                fill="red", font="arial 30", text="{}".format("♥" * self.hp))
        self.canvas.create_text(10, DEFAULT_CONFIG["side"] * (DEFAULT_CONFIG["rows"] + 1) + 10,
                                fill="black", font="arial 15", anchor=NW,
                                text="Další vlna automaticky - {}".format("ON" if self.auto_wave else "OFF"))
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
        self.canvas.create_image(DEFAULT_CONFIG["side"] * 5, DEFAULT_CONFIG["side"] * 6, image=self.endimg)
        if askyesno('Konec hry', 'Chcete začít novou hru?'):
            self.create_game()
            print("_____________NEW GAME_____________")
        else:
            self.parent.destroy()

    def turret_add_big(self):
        self.turret_add("big")

    def turret_add_fast(self):
        self.turret_add("fast")

    def turret_add(self, type):
        if self.square and not self.square.path:
            if not self.square.turret_built:
                if type == "big":
                    self.turret = TurretBig(self.square.x, self.square.y)
                elif type == "fast":
                    self.turret = TurretFast(self.square.x, self.square.y)
                if self.money >= self.turret.cost:
                    self.money -= self.turret.cost
                    self.turrets.append(self.turret)
                    self.square.turret_built = True
                    print(self.turrets)
                else:
                    self.turret = None

    def turret_sell(self):
        if self.turret:
            self.turrets.remove(self.turret)
            self.money += int(self.turret.total_cost / 2)
            self.square.turret_built = False
            self.turret = None

    def turret_upgrade(self):
        if self.turret:
            if self.money >= 2 * self.turret.cost:
                self.money -= int(2 * self.turret.cost)
                self.turrets.remove(self.turret)
                self.turret.upgrade()
                self.turrets.append(self.turret)

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
                self.turret = turret


root = Tk()
#root.attributes("-fullscreen", True)
root.geometry("{}x{}+0+0".format(DEFAULT_CONFIG["side"] * DEFAULT_CONFIG["cols"], DEFAULT_CONFIG["side"] * (DEFAULT_CONFIG["rows"] + 2)))
root.resizable(0, 0)
myapp = MyApp(root)
#sdfasd
myapp.create_game()
#sdfasd
root.mainloop()