import platform

if platform.system() != "Windows":
    print("Tamagotchi can only run on Windows. Quitting.")
    quit()

import base64
import threading
import tkinter as tk
import winsound
import random
import time
import os


class Pet:
    def __init__(self):
        self.health = random.randrange(70, 100)
        self.mood = random.randrange(50, 100)
        self.full = random.randrange(60)
        self.action = "sleep"
        self.delta_health = 0
        self.delta_mood = 0
        self.delta_full = 0
        self._last_alone = time.time()
        threading.Timer(1, self.update).start()

    def leave_alone(self, force=False):
        if time.time() - self._last_alone > 5 or force:
            self._last_alone = time.time()
            self.delta_full = 0
            self.delta_health = 0
            self.delta_mood = 0
            choice = random.choice([
                "sleep",
                "sleep",
                "T&J",
                "hurt"
            ])
            self.action = choice
            if choice == "sleep":
                self.delta_health = 2
                self.delta_mood = 2
                self.health += self.delta_health
                self.mood += self.delta_mood
                if self.health > 100:
                    self.health = 100
                if self.mood > 100:
                    self.mood = 100
            elif choice == "T&J":
                self.delta_mood = 10
                self.mood += self.delta_mood
                if self.mood > 100:
                    self.mood = 100
            elif choice == "hurt":
                self.delta_health = -20
                self.delta_mood = random.randrange(-10, -5)
                self.health += self.delta_health
                if self.health < 0:
                    self.health = 0
                self.mood += self.delta_mood
                if self.mood < 0:
                    self.mood = 0

    def feed(self):
        self.delta_full = random.randrange(20, 35)
        self.delta_health = 0
        self.delta_mood = 0
        self.full += self.delta_full
        if self.full > 100:
            self.delta_health = random.randrange(-15, -5)
            self.health += self.delta_health
            if self.health < 0:
                self.health = 0
            self.delta_mood = random.randrange(-15, -5)
            self.mood += self.delta_mood
            if self.mood < 0:
                self.mood = 0
            self.full = 100
        else:
            self.delta_mood = random.randrange(5, 10)
            self.mood += self.delta_mood
            if self.mood > 100:
                self.mood = 100

    def play(self):
        self.delta_full = 0
        self.delta_health = 0
        self.delta_mood = 0
        if self.full >= 30 and self.mood >= 30:
            self.action = random.choice([
                "fishing",
                "hiking",
                "reading"
            ])
            self.delta_mood = random.randrange(10, 20)
            self.mood += self.delta_mood
            if self.mood > 100:
                self.mood = 100
        else:
            self.action = "404"

    def take_to_vet(self):
        self.delta_full = 0
        self.delta_health = random.randrange(30, 50)
        self.delta_mood = random.randrange(-15, -5)
        self.health += self.delta_health
        if self.health > 100:
            self.health = 100
        self.mood += self.delta_mood
        if self.mood < 0:
            self.mood = 0

    def update(self):
        threading.Timer(1, self.update).start()
        self.full += random.randrange(-2, 0)
        if self.full < 0:
            self.full = 0
            self.health += random.randrange(-3, -1)
            if self.health < 0:
                self.health = 0
        if self.mood == 0:
            self.health += random.randrange(-3, -1)
            if self.health < 0:
                self.health = 0
        if self.status() == "sick":
            if self.mood > 70:
                self.mood = 70
        if self.status() == "dying":
            if self.mood > 30:
                self.mood = 30

    def status(self):
        if self.health >= 70:
            return "health"
        elif self.health >= 30:
            return "sick"
        elif self.health > 0:
            return "dying"
        else:
            return "dead"


class Renderer:
    def __init__(self):
        self._width = 144
        self._height = 144
        self._gram = [[0 for _ in range(self._height)] for _ in range(self._width)]
        self._anime_pos = 0
        self._anime_last = 0
        self._font = {}
        self._light = {}
        self._anime = {}
        self._init_lib()

    def _init_lib(self):
        self._font = {
            'A': self._construct_map([
                "  X  ",
                " XXX ",
                "X   X",
                "XXXXX",
                "X   X",
            ]),
            'B': self._construct_map([
                "XXXX ",
                "X  XX",
                "XXXX ",
                "X   X",
                "XXXXX",
            ]),
            'C': self._construct_map([
                " XXXX",
                "X    ",
                "X    ",
                "X    ",
                " XXXX",
            ]),
            'D': self._construct_map([
                "XXXX ",
                "X   X",
                "X   X",
                "X   X",
                "XXXX ",
            ]),
            'E': self._construct_map([
                "XXXXX",
                "X    ",
                "XXXX ",
                "X    ",
                "XXXXX",
            ]),
            'F': self._construct_map([
                "XXXXX",
                "X    ",
                "XXXX ",
                "X    ",
                "X    ",
            ]),
            'G': self._construct_map([
                "XXXXX",
                "X    ",
                "X  XX",
                "X   X",
                "XXXXX",
            ]),
            'H': self._construct_map([
                "X   X",
                "X   X",
                "XXXXX",
                "X   X",
                "X   X",
            ]),
            'I': self._construct_map([
                " XXX ",
                "  X  ",
                "  X  ",
                "  X  ",
                " XXX ",
            ]),
            'J': self._construct_map([
                " XXXX",
                "   X ",
                "   X ",
                " X X ",
                " XXX ",
            ]),
            'K': self._construct_map([
                "X   X",
                "X  X ",
                "XXX  ",
                "X  XX",
                "X   X",
            ]),
            'L': self._construct_map([
                "X    ",
                "X    ",
                "X    ",
                "X    ",
                "XXXXX",
            ]),
            'M': self._construct_map([
                "X   X",
                "XX XX",
                "X X X",
                "X   X",
                "X   X",
            ]),
            'N': self._construct_map([
                "X   X",
                "XX  X",
                "X X X",
                "X  XX",
                "X   X",
            ]),
            'O': self._construct_map([
                " XXX ",
                "X   X",
                "X   X",
                "X   X",
                " XXX ",
            ]),
            'P': self._construct_map([
                "XXXX ",
                "X   X",
                "XXXX ",
                "X    ",
                "X    ",
            ]),
            'Q': self._construct_map([
                " XXX ",
                "X   X",
                "X   X",
                "X  X ",
                " XX X",
            ]),
            'R': self._construct_map([
                "XXXX ",
                "X   X",
                "XXXX ",
                "X   X",
                "X   X",
            ]),
            'S': self._construct_map([
                " XXXX",
                "X    ",
                " XXX ",
                "    X",
                "XXXX ",
            ]),
            'T': self._construct_map([
                "XXXXX",
                "  X  ",
                "  X  ",
                "  X  ",
                "  X  ",
            ]),
            'U': self._construct_map([
                "X   X",
                "X   X",
                "X   X",
                "X   X",
                " XXX ",
            ]),
            'V': self._construct_map([
                "X   X",
                "X   X",
                "X   X",
                " X X ",
                "  X  ",
            ]),
            'W': self._construct_map([
                "X   X",
                "X   X",
                "X X X",
                "XX XX",
                "X   X",
            ]),
            'X': self._construct_map([
                "X   X",
                " X X ",
                "  X  ",
                " X X ",
                "X   X",
            ]),
            'Y': self._construct_map([
                "X   X",
                " X X ",
                "  X  ",
                "  X  ",
                "  X  ",
            ]),
            'Z': self._construct_map([
                "XXXXX",
                "   X ",
                "  X  ",
                " X   ",
                "XXXXX",
            ]),
            '1': self._construct_map([
                " XX  ",
                "  X  ",
                "  X  ",
                "  X  ",
                "XXXXX",
            ]),
            '2': self._construct_map([
                " XXX ",
                "X   X",
                "  XX ",
                " X   ",
                "XXXXX",
            ]),
            '3': self._construct_map([
                "XXXX ",
                "    X",
                " XXX ",
                "    X",
                "XXXX ",
            ]),
            '4': self._construct_map([
                "X  X ",
                "X  X ",
                "XXXXX",
                "   X ",
                "   X ",
            ]),
            '5': self._construct_map([
                "XXXXX",
                "X    ",
                "XXXX ",
                "    X",
                "XXXX ",
            ]),
            '6': self._construct_map([
                " XXX ",
                "X    ",
                "XXXX ",
                "X   X",
                " XXX ",
            ]),
            '7': self._construct_map([
                "XXXXX",
                "   X ",
                "  X  ",
                "  X  ",
                "  X  ",
            ]),
            '8': self._construct_map([
                " XXX ",
                "X   X",
                " XXX ",
                "X   X",
                " XXX ",
            ]),
            '9': self._construct_map([
                " XXX ",
                "X   X",
                " XXXX",
                "    X",
                " XXX ",
            ]),
            '0': self._construct_map([
                " XXX ",
                "X  XX",
                "X X X",
                "XX  X",
                " XXX ",
            ]),
            ':': self._construct_map([
                "     ",
                "  X  ",
                "     ",
                "  X  ",
                "     ",
            ]),
            '>': self._construct_map([
                " X   ",
                "  X  ",
                "   X ",
                "  X  ",
                " X   ",
            ]),
            '+': self._construct_map([
                "     ",
                "  X  ",
                " XXX ",
                "  X  ",
                "     ",
            ]),
            '-': self._construct_map([
                "     ",
                "     ",
                " XXX ",
                "     ",
                "     ",
            ]),
            '.': self._construct_map([
                "     ",
                "     ",
                "     ",
                "  X  ",
                "     ",
            ]),
            '&': self._construct_map([
                "  X  ",
                " X X ",
                "  X  ",
                " X X ",
                "  X X",
            ])
        }
        self._light = {
            "alone": self._construct_map([
                "                    ",
                "                    ",
                "       XXXXXX       ",
                "      X      X      ",
                "     X  X  X  X     ",
                "     X        X     ",
                "      X      X      ",
                "       XX  XX       ",
                "      X      X      ",
                "     X        X     ",
                "    X  X    X  X    ",
                "    X  X    X  X    ",
                "    X  X    X  X    ",
                "    XXX      XXX    ",
                "     X        X     ",
                "     X   XX   X     ",
                "     X  X  X  X     ",
                "      XXX  XXX      ",
                "                    ",
                "                    "
            ]),
            "feed": self._construct_map([
                "                    ",
                "        XXX         ",
                "      XX   XX       ",
                "     X       X      ",
                "    X   XXX   X     ",
                "    X         X     ",
                "    X         X     ",
                "   X    XXX    X    ",
                "   X  XX   XX  X    ",
                "   X           X    ",
                "   X           X    ",
                "   X    XXX    X    ",
                "   X  XX   XX  X    ",
                "    X         X     ",
                "    X         X     ",
                "    X   XXX   X     ",
                "     X       X      ",
                "      XX   XX       ",
                "        XXX         ",
                "                    "
            ]),
            "play": self._construct_map([
                "                    ",
                "                    ",
                "                    ",
                "                    ",
                "                    ",
                "  XXXXXXXXXXXXXXXX  ",
                "  X              X  ",
                "  X              X  ",
                "  X              X  ",
                "  X              X  ",
                "  X     XXXX     X  ",
                "  X    X    X    X  ",
                "  X   X      X   X  ",
                "  X   X      X   X  ",
                "  X   X      X   X  ",
                "  XXXXX      XXXXX  ",
                "                    ",
                "                    ",
                "                    ",
                "                    "
            ]),
            "vet": self._construct_map([
                "                    ",
                "                    ",
                "                    ",
                "      XX     XX     ",
                "     X  X   X  X    ",
                "    X    X X    X   ",
                "   X      X      X  ",
                "   X             X  ",
                "   X             X  ",
                "    X           X   ",
                "     X         X    ",
                "      X       X     ",
                "       X     X      ",
                "        X   X       ",
                "         X X        ",
                "          X         ",
                "                    ",
                "                    ",
                "                    ",
                "                    "
            ])
        }
        self._anime = {
            "sleep": [
                self._construct_map([
                    "                    ",
                    "                    ",
                    "XX     XXXXXX       ",
                    " X    X      X      ",
                    " XX  X  X  X  X     ",
                    "     X        X     ",
                    "      X      X      ",
                    "       XX  XX       ",
                    "     XX      XX     ",
                    "   XX   XXXX   XX   ",
                    "  X X  X    X  X X  ",
                    "  X X  X    X  X X  ",
                    "  X XXXX     XXX X  ",
                    "  X              X  ",
                    "  X              X  ",
                    "  X              X  ",
                    "   XXXXXXXXXXXXXX   ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ]),
                self._construct_map([
                    "  XX                ",
                    "   X                ",
                    "   XX  XXXXXX       ",
                    " XX   X      X      ",
                    "  X  X  X  X  X     ",
                    "  XX X        X     ",
                    "      X      X      ",
                    "       XX  XX       ",
                    "     XX      XX     ",
                    "   XX   XXXX   XX   ",
                    "  X X  X    X  X X  ",
                    "  X X  X    X  X X  ",
                    "  X XXXX     XXX X  ",
                    "  X              X  ",
                    "  X              X  ",
                    "  X              X  ",
                    "   XXXXXXXXXXXXXX   ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ]),
                self._construct_map([
                    "   XX               ",
                    "    X               ",
                    "    XX XXXXXX       ",
                    " XX   X      X      ",
                    "  X  X  X  X  X     ",
                    "  XX X        X     ",
                    "XX    X      X      ",
                    " X     XX  XX       ",
                    " XX  XX      XX     ",
                    "   XX   XXXX   XX   ",
                    "  X X  X    X  X X  ",
                    "  X X  X    X  X X  ",
                    "  X XXXX     XXX X  ",
                    "  X              X  ",
                    "  X              X  ",
                    "  X              X  ",
                    "   XXXXXXXXXXXXXX   ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ])
            ],
            "hurt": [
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X      X      ",
                    "      XXX  XXX      ",
                    "     X   XX   X     ",
                    "    X   X X    X    ",
                    "    X  X   X   X    ",
                    "     X  X   X  X    ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X   XX   X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ]),
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X      X      ",
                    "      X X  X X      ",
                    "     XXX    XX      ",
                    "    X   X  X  X     ",
                    "   X    X  X   X    ",
                    "   X   X   X   X    ",
                    "    X       X  X    ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X   XX   X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ])
            ],
            "T&J": [
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X      X      ",
                    "  X  X  X  X  X     ",
                    " X   X        X     ",
                    "  X   X      X      ",
                    "   XX  XX  XX       ",
                    "  X  XX      X      ",
                    "  X           X     ",
                    "   XX          X    ",
                    "     X      X   X   ",
                    "     X       X  X   ",
                    "     X        XX    ",
                    "     X        X     ",
                    "     X   XX   X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ]),
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X      X      ",
                    "     X  X  X  X     ",
                    "     X        X     ",
                    "      X      X      ",
                    "       XX  XX       ",
                    " X   XX      X      ",
                    "X   X         X     ",
                    " X X           X    ",
                    "  X  X      X   X   ",
                    "  X  X       X  X   ",
                    "   XX         XX    ",
                    "     X        X     ",
                    "     X   XX   X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ])
            ],
            "feed": [
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X      X      ",
                    "     X  X  X  X     ",
                    "     X        X     ",
                    "      X      X      ",
                    "       XX  XX       ",
                    "      X      X      ",
                    "     X        X     ",
                    "    X  X    X  X    ",
                    "    X  X XX X  X    ",
                    "    X  XXXXXX  X    ",
                    "     XX      XX     ",
                    "     X        X     ",
                    "     X   XX   X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ]),
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X      X      ",
                    "     X  X  X  X     ",
                    "     X        X     ",
                    "      XXXXXXXXX      ",
                    "     X   XX   X     ",
                    "    X   X  X   X    ",
                    "    X   X  X  XX    ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X        X     ",
                    "     X   XX   X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ])
            ],
            "play": [
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X      X      ",
                    "     X  X  X  X     ",
                    "     X        X     ",
                    "      X      X      ",
                    "       XX  XX       ",
                    "      X      X      ",
                    "     X        X     ",
                    "    X  X    X  X    ",
                    "    X  X    X  X    ",
                    "    X  X    X  X    ",
                    "    XXX      XXX    ",
                    "     X        X     ",
                    "     X   XX   X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ]),
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X      X      ",
                    "     X  X  X  X     ",
                    "     X        X     ",
                    "      X      X      ",
                    "       XX  XX       ",
                    "      X      X      ",
                    "     X        X     ",
                    "    X          X    ",
                    "   X   X    X   X   ",
                    "   X  X      X  X   ",
                    "    XX        XX    ",
                    "     X        X     ",
                    "     X   XX   X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ])
            ],
            "vet": [
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X      X      ",
                    "     X  X  X  X     ",
                    "     X        X     ",
                    "      X      X      ",
                    "       XX  XX       ",
                    "      X      X      ",
                    "     X        X     ",
                    "    X  X    X  X    ",
                    "    X  X    X  X    ",
                    "    X  X    X  X    ",
                    "    XXX      XXX    ",
                    "     X        X     ",
                    "     X   XX   X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ]),
                self._construct_map([
                    "                    ",
                    "                    ",
                    "       XXXXXX       ",
                    "      X  XX  X      ",
                    "     X  X  X  X     ",
                    "     X   XX   X     ",
                    "      X  XX  X      ",
                    "       XXXXXX       ",
                    "      X XXXX X      ",
                    "     X X XX X X     ",
                    "    X XX XX XX X    ",
                    "    XX X XX X XX    ",
                    "    X  X XX X  X    ",
                    "    XXX  XX  XXX    ",
                    "     X  X  X  X     ",
                    "     X X XX X X     ",
                    "     X  X  X  X     ",
                    "      XXX  XXX      ",
                    "                    ",
                    "                    "
                ])
            ],
            "dead": [
                self._construct_map([
                    "                    ",
                    "                    ",
                    "                    ",
                    "                    ",
                    "        XXXX        ",
                    "    X   XXXX XX     ",
                    "    X   XXXX   X    ",
                    "X  X XXXXXXXXXX X   ",
                    " XX  XXXXXXXXXX  X  ",
                    "  X  XXXXXXXXXX X XX",
                    "  X X   XXXX   X X  ",
                    "   X X  XXXX    X X ",
                    "   XX X XXXX X XXX  ",
                    "  X  XX XXXXXXX X   ",
                    "      XX  XX  X X   ",
                    "    XX         XX   ",
                    "  XX             X  ",
                    "XX                XX",
                    "                    ",
                    "                    "
                ])
            ]
        }

    @staticmethod
    def _construct_map(arr):
        return [(lambda row: [(lambda c: 0 if c == ' ' else 1)(char) for char in row])(line) for line in arr]

    def draw_clear(self):
        self._gram = [[0 for _ in range(self._height)] for _ in range(self._width)]

    def _draw_pixel(self, x, y, on, reverse=False):
        i_x = x - 1
        i_y = y - 1
        if 0 <= i_x <= self._width - 1:
            if 0 <= i_y <= self._height - 1:
                if not reverse:
                    self._gram[i_x][i_y] = 1 if on else 0
                else:
                    self._gram[i_x][i_y] = -1 if on else 0

    def render_light(self, status):
        assert len(status) == 4
        light_pos = [(8, 2), (44, 2), (80, 2), (116, 2)]
        light_name = ["alone", "feed", "play", "vet"]
        for i in range(len(light_pos)):
            if status[i]:
                start_pos = light_pos[i]
                for x in range(20):
                    for y in range(20):
                        self._draw_pixel(x + start_pos[0], y + start_pos[1], self._light[light_name[i]][y][x])
            else:
                start_pos = light_pos[i]
                for x in range(20):
                    for y in range(20):
                        self._draw_pixel(x + start_pos[0], y + start_pos[1], self._light[light_name[i]][y][x],
                                         reverse=True)

    def render_anime(self, name):
        if name in self._anime.keys():
            frame = self._anime_pos % len(self._anime[name])
            for x in range(20):
                for y in range(20):
                    if self._anime[name][frame][y][x]:
                        for r in range(3):
                            for c in range(3):
                                self._draw_pixel(42 + x * 3 + r, 30 + y * 3 + c, self._anime[name][frame][y][x])

            if time.time() - self._anime_last > 0.8:
                self._anime_last = time.time()
                self._anime_pos += 1

    def render_text(self, text, pos_x, pos_y):
        s_x = pos_x * 3
        s_y = 24 + pos_y * 3
        for c in text:
            if c in self._font.keys():
                for x in range(len(self._font[c][0])):
                    for y in range(len(self._font[c])):
                        if self._font[c][y][x]:
                            for row in range(3):
                                for col in range(3):
                                    self._draw_pixel(s_x + x * 3 + row, s_y + y * 3 + col, self._font[c][y][x])
                s_x += len(self._font[c][0] * 3) + 3

    def get_gram(self):
        return self._gram


class Page:
    def __init__(self):
        self._renderer = Renderer()


class IndexPage(Page):
    def render(self):
        self._renderer.draw_clear()
        self._renderer.render_light((1, 1, 1, 1))
        self._renderer.render_anime("play")
        self._renderer.render_text("TAMA", 7, 25)
        self._renderer.render_text("GOTCHI", 7, 32)
        return self._renderer.get_gram()


class AlonePage(Page):
    def render(self, status, doing, t):
        self._renderer.draw_clear()
        self._renderer.render_light((1, 0, 0, 0))
        self._renderer.render_anime(status)
        self._renderer.render_text(doing, 10, 25)
        self._renderer.render_text(t, 10, 32)
        return self._renderer.get_gram()


class StatusPage(Page):
    def render(self, status, health, mood, hunger):
        self._renderer.draw_clear()
        self._renderer.render_light((0, 0, 0, 0))
        self._renderer.render_text(status.upper(), 2, 8)
        self._renderer.render_text("HP:" + str(health), 2, 15)
        self._renderer.render_text("MOOD:" + str(mood), 2, 22)
        self._renderer.render_text("FULL:" + str(hunger), 2, 29)
        return self._renderer.get_gram()


class MenuPage(Page):
    def render(self, select):
        assert select in [0, 1, 2]
        self._renderer.draw_clear()
        self._renderer.render_light([1 if i == select + 1 else 0 for i in range(4)])
        self._renderer.render_text("FEED", 14, 13)
        self._renderer.render_text("PLAY", 14, 20)
        self._renderer.render_text("VET", 14, 27)
        select_pos = [(7, 13), (7, 20), (7, 27)]
        self._renderer.render_text(">", select_pos[select][0], select_pos[select][1])
        return self._renderer.get_gram()


class FeedPage(Page):
    def render(self, full, mood):
        self._renderer.draw_clear()
        self._renderer.render_light((0, 1, 0, 0))
        self._renderer.render_anime("feed")
        self._renderer.render_text("FULL" + ("+" if full >= 0 else '') + str(full), 4, 25)
        self._renderer.render_text("MOOD" + ("+" if mood >= 0 else '') + str(mood), 4, 32)
        return self._renderer.get_gram()


class PlayPage(Page):
    def render(self, status, mood):
        self._renderer.draw_clear()
        self._renderer.render_light((0, 0, 1, 0))
        if status != "404":
            self._renderer.render_anime("play")
            self._renderer.render_text(status, 4, 25)
        else:
            self._renderer.render_text("NO", 4, 25)
        self._renderer.render_text("MOOD" + ("+" if mood >= 0 else '') + str(mood), 4, 32)
        return self._renderer.get_gram()


class VetPage(Page):
    def render(self, hp, mood):
        self._renderer.draw_clear()
        self._renderer.render_light((0, 0, 0, 1))
        self._renderer.render_anime("vet")
        self._renderer.render_text("HP" + ("+" if hp >= 0 else '') + str(hp), 4, 25)
        self._renderer.render_text("MOOD" + ("+" if mood >= 0 else '') + str(mood), 4, 32)
        return self._renderer.get_gram()


class DeadPage(Page):
    def render(self, t):
        self._renderer.draw_clear()
        self._renderer.render_light((0, 0, 0, 0))
        self._renderer.render_anime("dead")
        self._renderer.render_text("R.I.P.", 9, 23)
        self._renderer.render_text(t, 9, 32)
        return self._renderer.get_gram()


class GamePlay:
    def __init__(self):
        self._pet = Pet()
        self._state = "index"
        self._pindex = IndexPage()
        self._palone = AlonePage()
        self._pstatus = StatusPage()
        self._pmenu = MenuPage()
        self._pfeed = FeedPage()
        self._pplay = PlayPage()
        self._pvet = VetPage()
        self._pdead = DeadPage()
        self._menu_select = 0
        self._start_time = time.time()
        self._life_time = ""
        self._when_alone()
        threading.Timer(2, self._to_alone).start()

    def get_time(self):
        time_past = (time.time() - self._start_time)
        second = int(time_past % 60)
        minute = int((time_past - second) // 60)
        return ("0" if minute < 10 else "") + str(minute) + ":" + ("0" if second < 10 else "") + str(second)

    def render(self):
        if self._pet.health == 0:
            self._state = "dead"
        else:
            self._life_time = self.get_time()
        if self._state == "index":
            return self._pindex.render()
        elif self._state == "alone":
            return self._palone.render(self._pet.action, self._pet.action.upper(), self.get_time())
        elif self._state == "status":
            return self._pstatus.render(self._pet.status(), self._pet.health, self._pet.mood, self._pet.full)
        elif self._state == "menu":
            return self._pmenu.render(self._menu_select)
        elif self._state == "feed":
            return self._pfeed.render(self._pet.delta_full, self._pet.delta_mood)
        elif self._state == "play":
            return self._pplay.render(self._pet.action.upper(), self._pet.delta_mood)
        elif self._state == "vet":
            return self._pvet.render(self._pet.delta_health, self._pet.delta_mood)
        elif self._state == "dead":
            return self._pdead.render(self._life_time)

    def _when_alone(self):
        threading.Timer(1, self._when_alone).start()
        if self._state == "alone":
            self._pet.leave_alone()

    def _to_alone(self):
        self._state = "alone"
        self._pet.leave_alone(force=True)

    def interact(self, btn):
        if self._state == "alone":
            if btn == "select":
                self._menu_select = 0
                self._state = "menu"
            elif btn == "confirm":
                self._state = "status"
        elif self._state == "status":
            if btn == "cancel":
                self._state = "alone"
                self._pet.leave_alone()
        elif self._state == "menu":
            if btn == "cancel":
                self._state = "alone"
                self._pet.leave_alone()
            elif btn == "select":
                self._menu_select += 1
                self._menu_select %= 3
            elif btn == "confirm":
                if self._menu_select == 0:
                    self._state = "feed"
                    self._pet.feed()
                    threading.Timer(2, self._to_alone).start()
                elif self._menu_select == 1:
                    self._state = "play"
                    self._pet.play()
                    threading.Timer(2, self._to_alone).start()
                elif self._menu_select == 2:
                    self._state = "vet"
                    self._pet.take_to_vet()
                    threading.Timer(2, self._to_alone).start()


class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        self._ori_x = 0
        self._ori_y = 0
        self._last_click = 0
        self._dragging = 0
        self._bgImg = tk.PhotoImage(
            data="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")
        self._pressSnd = base64.b64decode(
            "UklGRvhdAABXQVZFZm10IBAAAAABAAIARKwAABCxAgAEABAAZGF0YehEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP//AAAAAAAAAAAAAAAAAQABAAAAAAAAAAAAAAD//wAA//8AAAAAAAABAAEAAQAAAAAA//8AAAAA//8AAAAAAAAAAAAAAAABAAEAAAABAAAAAAAAAP//AAD/////AAAAAAAAAQABAAEAAQAAAAAAAAD//////////wAAAAAAAAEAAQABAAEA//8AAAAA//////////8AAAEAAQABAAEAAAABAP////////7/AAD/////AAABAAEAAgABAAAAAQD//wAA/v/9/wAA/v8AAAEAAQACAAMAAwABAAEA/v////7//f////3///8AAAEAAgADAAMAAgACAP//AAD///3////9//7//v///wEABAADAAMAAwD//wEA/v/9/////P/+//7/AAACAAUABQADAAMA/v8AAP3//P////v//v/9////AgAEAAUABQAEAAAAAQD9//3//v/6//3//P/+/wEABAAFAAYABAAAAAIA/f/+//7/+v/+//z///8BAAMABAAFAAMAAQACAP3///////z//v/7//3/AAABAAMABAACAAIAAwD+/wEA/v/8////+//+/wAAAgAEAAQAAgACAAEA/f8BAP7//f8AAPv///8AAAEAAwADAAEAAgABAAAAAwD////////7//3//v/+/wIAAwABAAQAAQABAAQA//8AAP//+v/+//3///8DAAIAAQACAAAAAAADAP//AgAAAPz////9////AgAAAAEAAgD//wEAAwD//wMA///9//7//P/+/wEAAQACAAQA//8CAAMA//8DAP7//f/+//z//v8BAP//AgACAP//AgABAAAABQABAAEAAQD8//z//f/9////AQD//wUAAwABAAYAAAACAAAA+//8//v//v///wEAAAAGAAMAAQAFAAAABAAAAP3//P/7//z//f/+//3/BQACAAMACAADAAcAAwAAAPz/+v/3//j/+v/6/wYAAwAJAAwAAQAKAAAAAAD9//j/+P/3//v/9/8HAAIABwALAAEACwACAAIA///7//j/9f/0//T/AAD//woACgAEAAsABQAEAP///P/7//b/9v/4/wMAAAAJAAkA//8GAAAAAwAAAAIA+//4//j/9f8AAPn/BwAIAAUACgAEAAoAAwAGAP3/+P/v/+z/+//3/woABAAGAA8ACgAPAAMAAwD2//P/+f/x//3/+v8OAAcA+f8GAP//CQAMAAwA/f/1//3/9//1//j/CgD//wMACQANAA8ACAAQAPL/+f/7//D/9//0/w8AAgABAAYABwANAAQACADy//v//P/v//7/8v8KAAIADAAPAPn/EQADAAoA+v/y//T/9P8BAOr/EwAFAAwAFgAEABoABgAAAOD/5v/y/+b/AQACABYAGwAbAAsA8/8CAP7/9f/n//P/DAAFAAsAEwAEAPv/AgD2//j/+f8NAAMA/f8cAP//EwALAAYA7v/K//L/4/8BAP7/GwAfAAsANAAVACAAGgD+/9b/2//6/+H/6//3//r/AAAYAAMA/f8dAAwAEQANAAgADQDq/xAAFgADABQA5f/k//D/BAD8/+H///8RAAQAAgAHAPD/FAAoAPv/8v8EAAkAGAAKAAgAFgDq//j/8P/2/wYA6P8MABQA+//4/wcAAgDu/xYAAQDO/wIAEAAfADkAEgAAABsAHQD0/+L/4P/9/9T/4v/z/83/HwA6ABsA5//4/wAAFQBAACEAAADr/xIA/f/m/+j/7P8aAA8AAwARAPr/2P/g//P/9P/w/y0ADQDy/0gA8v/V/xUAJgA7AC0ABADJ/+//EQDL/9r/9//4//7/AQAWAPr/JQBNAP//4f/v/+D//v8rAAYA7v8RACcAHQALAP//5f/j/9r/6P8KAB0AHgAJAB0A5P/W/+j/8v8VAB8ABgDC/zwAeQAqAPz/HwAcANz/8v+6/67/7f8XAO//3//1/+T/NAAVAAwAMQApAEcA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/f8AAAAAAAD//wEAAAAAAAIA///9//////8AAAEA//8AAAAAAQABAAAAAgABAAMA//8BAP7/AgD+/wIA/////wAA/v8BAAAAAAABAP///v8AAAIA/v8CAP3//v///wAA/f///wAAAQD//wEA//8AAAEAAAD+////AAAAAAAAAAD//wEAAAD///7//////wEAAAAAAAEAAQAAAAAAAQABAAEAAAACAAIAAwADAP//AAAAAAEA//8BAP//AQACAAEAAAD//wIA//8BAP3/AAAAAAMAAwACAAMAAwACAAEAAAAAAAAAAgAAAAMAAQABAAEAAQAAAAIAAAAAAP//AwABAAEAAQABAAEABQACAAEAAQAEAAEAAwACAAAAAwADAAAAAQAAAAEAAQACAAAAAgABAAEAAAD//wEAAQABAAIAAAABAAEAAAABAAEAAgAAAAAAAAABAAIAAgD+//7/////////AAD+////AgD///3/AAD//wAA//8AAP3/AgAAAAIA//8DAAEAAQAAAAEAAAABAAAAAAD//wEA/f////3/AQD+/wEA/P///wAAAAAAAAAA/v8AAAEAAQD//wAAAQABAP//AQD9////AQD///z/AAD+/wAA//8BAP7//////////v///wEA/v8CAAAAAgAAAAAAAAABAAEAAAAAAP7/AAABAP///////wEAAQAAAAAAAAD//wMAAQAAAAEAAwAAAAIAAAAAAAAAAgACAAAAAgAAAAEA//8CAAAAAAD//wIAAAACAAEAAQAAAAIAAAACAP7/AwD//wIA//8BAP7/AgAAAAAA/f/+//7/AAD+/wEA/v///wAAAAD//////v8AAP//AQAAAP7//////////v8AAP7//v///wAA/v////7////9/wAA////////AQD//wAAAAACAP//AwD//wEA/v8CAP//AQD+/wMA//8CAP//AQD//wIAAgADAAAAAwAAAAMAAgAEAAEAAgACAAMAAQADAAEAAQAAAAIAAQABAAIAAAAAAAEAAwACAAIAAwACAAIAAgABAAIAAgACAAEAAQAAAAEAAAAAAP//AQD//wIA/////wAAAAABAP//AAAAAAAAAAABAAAAAAAAAAEA//8BAAEA//8AAAAAAQD//wEA/v/////////+/////v8AAP//////////AAAAAP///////wIAAAAAAP7/AQD+/wIA//8BAP7/AQD//wEA/v8AAP7///8AAAIA//8BAP//AQAAAAMA//8AAP//AQD//wEA/v8AAAEAAQABAAEAAAACAP//AAD//wEAAQABAAEAAAAAAAAAAQABAAAAAAAAAP//AQD//wEA/v8BAP//AQAAAAEA/v8CAAAAAQAAAAEA//8BAP//AAD+/wAA//8BAP//AAD+/wAA/f/+//7//v8AAAAA/v///////v8BAAAAAAAAAP//AAABAAAAAAD///7///8BAAAA///+/////v8CAP//AQD//wEA/v8AAAAAAQAAAAEAAQABAAIAAgAAAAAAAAAAAAAAAAD//wEA//8CAAAAAgABAAEAAQAAAAAAAQAAAAAAAQAAAAEAAQACAP//AgABAAEAAQABAAEAAAABAAAAAQAAAAIAAAABAAEAAQAAAAAA//8AAAAAAAAAAAAA//8AAP//AAD//wEAAAABAP//AQD//wIA//8BAP7/AQD//wAA//8BAP7/AAD//wAA/v8BAP3/AAD//wAA//8AAP//AgAAAAEAAAAAAAAAAQAAAAEA//8BAAAAAAAAAAAAAAAAAAAAAAD//wEAAAAAAAEAAAAAAAAAAAABAP//AAD/////AQAAAP//////////AQAAAAAAAAABAAAAAAD///////8BAP//AAD//wEA//8BAP7//////wAA/v8AAP/////+/wEA/v8BAP7/AQD//wIAAAAAAP7/AQD//wIAAAAAAP7/AQD//wAAAABfUE1Y4xgAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDAyIDc5LjE2NDM2MCwgMjAyMC8wMi8xMy0wMTowNzoyMiAgICAgICAgIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgICAgICAgICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgICAgICAgICAgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiCiAgICAgICAgICAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgICAgICAgICAgeG1sbnM6eG1wRE09Imh0dHA6Ly9ucy5hZG9iZS5jb20veG1wLzEuMC9EeW5hbWljTWVkaWEvIj4KICAgICAgICAgPHhtcDpNZXRhZGF0YURhdGU+MjAyMS0wNC0yNlQyMDowNToxOSswODowMDwveG1wOk1ldGFkYXRhRGF0ZT4KICAgICAgICAgPHhtcDpNb2RpZnlEYXRlPjIwMjEtMDQtMjZUMjA6MDU6MTkrMDg6MDA8L3htcDpNb2RpZnlEYXRlPgogICAgICAgICA8eG1wTU06SW5zdGFuY2VJRD54bXAuaWlkOmRmMjE4ZjY5LWEyNTQtYWM0MC1iN2Y5LTZhZWM4ODRlYjdhODwveG1wTU06SW5zdGFuY2VJRD4KICAgICAgICAgPHhtcE1NOkRvY3VtZW50SUQ+eG1wLmRpZDo2NjgwOWQ3NS1hYWJkLWE2NGUtYmNlZS01YzVlNTZhN2E2ZWQ8L3htcE1NOkRvY3VtZW50SUQ+CiAgICAgICAgIDx4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ+eG1wLmRpZDo1MGUzNjliMi1kMDExLWRlNGMtOWJkZC1kZjg0NGYwMzQyNGE8L3htcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD4KICAgICAgICAgPHhtcE1NOkhpc3Rvcnk+CiAgICAgICAgICAgIDxyZGY6U2VxPgogICAgICAgICAgICAgICA8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OmFjdGlvbj5zYXZlZDwvc3RFdnQ6YWN0aW9uPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6aW5zdGFuY2VJRD54bXAuaWlkOjUwZTM2OWIyLWQwMTEtZGU0Yy05YmRkLWRmODQ0ZjAzNDI0YTwvc3RFdnQ6aW5zdGFuY2VJRD4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OndoZW4+MjAyMS0wNC0yNlQyMDowMDo1OSswODowMDwvc3RFdnQ6d2hlbj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OnNvZnR3YXJlQWdlbnQ+QWRvYmUgQXVkaXRpb24gMTMuMCAoV2luZG93cyk8L3N0RXZ0OnNvZnR3YXJlQWdlbnQ+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDpjaGFuZ2VkPi9tZXRhZGF0YTwvc3RFdnQ6Y2hhbmdlZD4KICAgICAgICAgICAgICAgPC9yZGY6bGk+CiAgICAgICAgICAgICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6YWN0aW9uPnNhdmVkPC9zdEV2dDphY3Rpb24+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDppbnN0YW5jZUlEPnhtcC5paWQ6NjY4MDlkNzUtYWFiZC1hNjRlLWJjZWUtNWM1ZTU2YTdhNmVkPC9zdEV2dDppbnN0YW5jZUlEPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6d2hlbj4yMDIxLTA0LTI2VDIwOjAwOjU5KzA4OjAwPC9zdEV2dDp3aGVuPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6c29mdHdhcmVBZ2VudD5BZG9iZSBBdWRpdGlvbiAxMy4wIChXaW5kb3dzKTwvc3RFdnQ6c29mdHdhcmVBZ2VudD4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OmNoYW5nZWQ+Lzwvc3RFdnQ6Y2hhbmdlZD4KICAgICAgICAgICAgICAgPC9yZGY6bGk+CiAgICAgICAgICAgICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6YWN0aW9uPnNhdmVkPC9zdEV2dDphY3Rpb24+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDppbnN0YW5jZUlEPnhtcC5paWQ6YzAyOTZlZjItNzYyYy1jMDQwLTk5OGMtNTFlYjJhMjUzNmNlPC9zdEV2dDppbnN0YW5jZUlEPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6d2hlbj4yMDIxLTA0LTI2VDIwOjA1OjE5KzA4OjAwPC9zdEV2dDp3aGVuPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6c29mdHdhcmVBZ2VudD5BZG9iZSBBdWRpdGlvbiAxMy4wIChXaW5kb3dzKTwvc3RFdnQ6c29mdHdhcmVBZ2VudD4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OmNoYW5nZWQ+L21ldGFkYXRhPC9zdEV2dDpjaGFuZ2VkPgogICAgICAgICAgICAgICA8L3JkZjpsaT4KICAgICAgICAgICAgICAgPHJkZjpsaSByZGY6cGFyc2VUeXBlPSJSZXNvdXJjZSI+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDphY3Rpb24+c2F2ZWQ8L3N0RXZ0OmFjdGlvbj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0Omluc3RhbmNlSUQ+eG1wLmlpZDpkZjIxOGY2OS1hMjU0LWFjNDAtYjdmOS02YWVjODg0ZWI3YTg8L3N0RXZ0Omluc3RhbmNlSUQ+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDp3aGVuPjIwMjEtMDQtMjZUMjA6MDU6MTkrMDg6MDA8L3N0RXZ0OndoZW4+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDpzb2Z0d2FyZUFnZW50PkFkb2JlIEF1ZGl0aW9uIDEzLjAgKFdpbmRvd3MpPC9zdEV2dDpzb2Z0d2FyZUFnZW50PgogICAgICAgICAgICAgICAgICA8c3RFdnQ6Y2hhbmdlZD4vPC9zdEV2dDpjaGFuZ2VkPgogICAgICAgICAgICAgICA8L3JkZjpsaT4KICAgICAgICAgICAgPC9yZGY6U2VxPgogICAgICAgICA8L3htcE1NOkhpc3Rvcnk+CiAgICAgICAgIDx4bXBNTTpEZXJpdmVkRnJvbSByZGY6cGFyc2VUeXBlPSJSZXNvdXJjZSI+CiAgICAgICAgICAgIDxzdFJlZjppbnN0YW5jZUlEPnhtcC5paWQ6NTBlMzY5YjItZDAxMS1kZTRjLTliZGQtZGY4NDRmMDM0MjRhPC9zdFJlZjppbnN0YW5jZUlEPgogICAgICAgICAgICA8c3RSZWY6ZG9jdW1lbnRJRD54bXAuZGlkOjUwZTM2OWIyLWQwMTEtZGU0Yy05YmRkLWRmODQ0ZjAzNDI0YTwvc3RSZWY6ZG9jdW1lbnRJRD4KICAgICAgICAgICAgPHN0UmVmOm9yaWdpbmFsRG9jdW1lbnRJRD54bXAuZGlkOjUwZTM2OWIyLWQwMTEtZGU0Yy05YmRkLWRmODQ0ZjAzNDI0YTwvc3RSZWY6b3JpZ2luYWxEb2N1bWVudElEPgogICAgICAgICA8L3htcE1NOkRlcml2ZWRGcm9tPgogICAgICAgICA8ZGM6Zm9ybWF0PmF1ZGlvL3gtd2F2PC9kYzpmb3JtYXQ+CiAgICAgICAgIDx4bXBETTpUcmFja3M+CiAgICAgICAgICAgIDxyZGY6QmFnPgogICAgICAgICAgICAgICA8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KICAgICAgICAgICAgICAgICAgPHhtcERNOnRyYWNrTmFtZT5DdWVQb2ludCBNYXJrZXJzPC94bXBETTp0cmFja05hbWU+CiAgICAgICAgICAgICAgICAgIDx4bXBETTp0cmFja1R5cGU+Q3VlPC94bXBETTp0cmFja1R5cGU+CiAgICAgICAgICAgICAgICAgIDx4bXBETTpmcmFtZVJhdGU+ZjQ0MTAwPC94bXBETTpmcmFtZVJhdGU+CiAgICAgICAgICAgICAgIDwvcmRmOmxpPgogICAgICAgICAgICAgICA8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KICAgICAgICAgICAgICAgICAgPHhtcERNOnRyYWNrTmFtZT5DRCBUcmFjayBNYXJrZXJzPC94bXBETTp0cmFja05hbWU+CiAgICAgICAgICAgICAgICAgIDx4bXBETTp0cmFja1R5cGU+VHJhY2s8L3htcERNOnRyYWNrVHlwZT4KICAgICAgICAgICAgICAgICAgPHhtcERNOmZyYW1lUmF0ZT5mNDQxMDA8L3htcERNOmZyYW1lUmF0ZT4KICAgICAgICAgICAgICAgPC9yZGY6bGk+CiAgICAgICAgICAgICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICAgICAgICA8eG1wRE06dHJhY2tOYW1lPlN1YmNsaXAgTWFya2VyczwveG1wRE06dHJhY2tOYW1lPgogICAgICAgICAgICAgICAgICA8eG1wRE06dHJhY2tUeXBlPkluT3V0PC94bXBETTp0cmFja1R5cGU+CiAgICAgICAgICAgICAgICAgIDx4bXBETTpmcmFtZVJhdGU+ZjQ0MTAwPC94bXBETTpmcmFtZVJhdGU+CiAgICAgICAgICAgICAgIDwvcmRmOmxpPgogICAgICAgICAgICA8L3JkZjpCYWc+CiAgICAgICAgIDwveG1wRE06VHJhY2tzPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+AA==")
        self._game = GamePlay()
        self._init_window()
        self.after(500, self._render)

    def _init_window(self):
        self._bg = tk.Label(self, image=self._bgImg, bg="white")
        self._canvas = tk.Canvas(self, bg="#9c9a74", width=144, height=144)
        self._canvas.config(highlightthickness=0)
        self._canvas.place(x=128, y=150)
        self._canvas.create_rectangle(0, 24, 144, 144, fill="#918f6c", width=0)
        self.overrideredirect(True)
        self.geometry("+600+250")
        self.lift()
        self.resizable(width=False, height=False)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "white")
        self._bg.focus_set()
        self._bg.pack()
        self._bg.bind("<ButtonPress-1>", self._on_click)
        self._bg.bind("<B1-Motion>", self._on_move)
        self._bg.bind("<Key>", self._on_key)

    def _render(self):
        self.after(100, self._render)
        self._canvas.delete(tk.ALL)
        gram = self._game.render()
        self._canvas.create_rectangle(0, 24, 144, 144, fill="#918f6c", width=0)
        for x in range(len(gram)):
            for y in range(len(gram[0])):
                if gram[x][y] == 1:
                    self._canvas.create_rectangle(x, y, x + 1, y + 1, outline="#222222", width=1)
                elif gram[x][y] == -1:
                    self._canvas.create_rectangle(x, y, x + 1, y + 1, outline="#918f6c", width=1)

    def _on_click(self, event):
        buttons = {
            "select": (136, 317, 159, 338),
            "confirm": (187, 326, 209, 347),
            "cancel": (238, 316, 260, 337)
        }
        for button in buttons.keys():
            if self._in_region((event.x, event.y), buttons[button]):
                if time.time() - self._last_click >= 0.2:
                    self._last_click = time.time()
                    self._on_press(button)
                    self._dragging = False
                    return
        self._dragging = True
        self._ori_x = event.x
        self._ori_y = event.y

    @staticmethod
    def _in_region(point, region):
        if region[0] <= point[0] <= region[2]:
            if region[1] <= point[1] <= region[3]:
                return True
        return False

    def _on_key(self, event):
        keysym = event.keysym
        if time.time() - self._last_click >= 0.2:
            self._last_click = time.time()
            if keysym == "Escape":
                self._on_quit()
            if keysym == "Left":
                self._on_press("select")
            if keysym == "Down":
                self._on_press("confirm")
            if keysym == "Right":
                self._on_press("cancel")

    def _on_press(self, btn):
        t = threading.Thread(target=winsound.PlaySound, args=(self._pressSnd, winsound.SND_MEMORY))
        t.setDaemon(True)
        t.start()
        self._game.interact(btn)

    def _on_move(self, event):
        if self._dragging:
            delta_x = event.x - self._ori_x
            delta_y = event.y - self._ori_y
            target_x = self.winfo_x() + delta_x
            target_y = self.winfo_y() + delta_y
            self.geometry(f"+{target_x}+{target_y}")

    @staticmethod
    def _on_quit():
        os._exit(0)


App().mainloop()
