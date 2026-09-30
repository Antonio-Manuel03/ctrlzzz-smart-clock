from time import sleep_ms

# Oggetto display globale
oled = None

def set_display(d):
    global oled
    oled = d

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ==== CIFRE E DUE PUNTI ====
def zero(p):
    oled.line(p.x+10,p.y+5,p.x+8,p.y+1,1)
    oled.line(p.x+8,p.y+1,p.x+4,p.y+1,1)
    oled.line(p.x+4,p.y+1,p.x+2,p.y+3,1)
    oled.line(p.x+2,p.y+3,p.x+1,p.y+7,1)
    oled.line(p.x+1,p.y+7,p.x+1,p.y+12,1)
    oled.line(p.x+1,p.y+12,p.x+4,p.y+15,1)
    oled.line(p.x+4,p.y+15,p.x+7,p.y+15,1)
    oled.line(p.x+7,p.y+15,p.x+10,p.y+12,1)
    oled.line(p.x+10,p.y+12,p.x+10,p.y+5,1)
    oled.line(p.x+9,p.y+4,p.x+2,p.y+12,1)
    oled.show()

def one(p):
    oled.line(p.x+5,p.y+15,p.x+5,p.y+1,1)
    oled.line(p.x+5,p.y+1,p.x+2,p.y+3,1)
    oled.show()

def two(p):
    oled.line(p.x+1,p.y+3,p.x+2,p.y+1,1)
    oled.line(p.x+2,p.y+1,p.x+7,p.y+1,1)
    oled.line(p.x+7,p.y+1,p.x+9,p.y+3,1)
    oled.line(p.x+9,p.y+3,p.x+9,p.y+6,1)
    oled.line(p.x+9,p.y+6,p.x+2,p.y+13,1)
    oled.line(p.x+2,p.y+13,p.x+1,p.y+15,1)
    oled.line(p.x+1,p.y+15,p.x+10,p.y+15,1)
    oled.show()

def three(p):
    oled.line(p.x+1,p.y+3,p.x+2,p.y+1,1)
    oled.line(p.x+2,p.y+1,p.x+7,p.y+1,1)
    oled.line(p.x+7,p.y+1,p.x+9,p.y+3,1)
    oled.line(p.x+9,p.y+3,p.x+9,p.y+5,1)
    oled.line(p.x+9,p.y+5,p.x+7,p.y+7,1)
    oled.line(p.x+7,p.y+7,p.x+4,p.y+7,1)
    oled.line(p.x+7,p.y+8,p.x+9,p.y+9,1)
    oled.line(p.x+9,p.y+9,p.x+9,p.y+12,1)
    oled.line(p.x+9,p.y+12,p.x+7,p.y+15,1)
    oled.line(p.x+7,p.y+15,p.x+3,p.y+15,1)
    oled.line(p.x+3,p.y+15,p.x+1,p.y+13,1)
    oled.show()

def four(p):
    oled.line(p.x+8,p.y+1,p.x+8,p.y+15,1)
    oled.line(p.x+1,p.y+1,p.x+1,p.y+7,1)
    oled.line(p.x+1,p.y+7,p.x+9,p.y+7,1)
    oled.show()

def five(p):
    oled.line(p.x+9,p.y+1,p.x+1,p.y+1,1)
    oled.line(p.x+1,p.y+1,p.x+1,p.y+7,1)
    oled.line(p.x+7,p.y+7,p.x+1,p.y+7,1)
    oled.line(p.x+7,p.y+8,p.x+9,p.y+9,1)
    oled.line(p.x+9,p.y+9,p.x+9,p.y+12,1)
    oled.line(p.x+9,p.y+12,p.x+7,p.y+15,1)
    oled.line(p.x+7,p.y+15,p.x+3,p.y+15,1)
    oled.line(p.x+3,p.y+15,p.x+1,p.y+13,1)
    oled.show()

def six(p):
    oled.line(p.x+10,p.y+3,p.x+8,p.y+1,1)
    oled.line(p.x+8,p.y+1,p.x+4,p.y+1,1)
    oled.line(p.x+4,p.y+1,p.x+2,p.y+3,1)
    oled.line(p.x+2,p.y+3,p.x+1,p.y+7,1)
    oled.line(p.x+1,p.y+7,p.x+1,p.y+12,1)
    oled.line(p.x+1,p.y+12,p.x+4,p.y+15,1)
    oled.line(p.x+4,p.y+15,p.x+7,p.y+15,1)
    oled.line(p.x+7,p.y+15,p.x+10,p.y+13,1)
    oled.line(p.x+10,p.y+13,p.x+10,p.y+9,1)
    oled.line(p.x+10,p.y+9,p.x+8,p.y+7,1)
    oled.line(p.x+8,p.y+7,p.x+4,p.y+7,1)
    oled.line(p.x+4,p.y+7,p.x+2,p.y+9,1)
    oled.show()

def seven(p):
    oled.line(p.x+1,p.y+1,p.x+10,p.y+1,1)
    oled.line(p.x+10,p.y+1,p.x+3,p.y+15,1)
    oled.show()

def eight(p):
    oled.line(p.x+4,p.y+7,p.x+2,p.y+5,1)
    oled.line(p.x+2,p.y+5,p.x+2,p.y+3,1)
    oled.line(p.x+2,p.y+3,p.x+3,p.y+2,1)
    oled.line(p.x+3,p.y+2,p.x+4,p.y+1,1)
    oled.line(p.x+4,p.y+1,p.x+6,p.y+1,1)
    oled.line(p.x+6,p.y+1,p.x+7,p.y+2,1)
    oled.line(p.x+7,p.y+2,p.x+8,p.y+3,1)
    oled.line(p.x+8,p.y+3,p.x+8,p.y+5,1)
    oled.line(p.x+8,p.y+5,p.x+6,p.y+7,1)
    oled.line(p.x+1,p.y+10,p.x+1,p.y+13,1)
    oled.line(p.x+1,p.y+13,p.x+3,p.y+15,1)
    oled.line(p.x+3,p.y+15,p.x+7,p.y+15,1)
    oled.line(p.x+7,p.y+15,p.x+9,p.y+13,1)
    oled.line(p.x+9,p.y+13,p.x+9,p.y+10,1)
    oled.line(p.x+9,p.y+10,p.x+6,p.y+7,1)
    oled.line(p.x+6,p.y+7,p.x+4,p.y+7,1)
    oled.line(p.x+4,p.y+7,p.x+2,p.y+9,1)
    oled.show()

def nine(p):
    oled.line(p.x+10,p.y+6,p.x+8,p.y+8,1)
    oled.line(p.x+8,p.y+8,p.x+3,p.y+8,1)
    oled.line(p.x+3,p.y+8,p.x+1,p.y+5,1)
    oled.line(p.x+1,p.y+5,p.x+1,p.y+3,1)
    oled.line(p.x+1,p.y+3,p.x+3,p.y+1,1)
    oled.line(p.x+3,p.y+1,p.x+8,p.y+1,1)
    oled.line(p.x+8,p.y+1,p.x+10,p.y+3,1)
    oled.line(p.x+10,p.y+3,p.x+10,p.y+10,1)
    oled.line(p.x+10,p.y+10,p.x+9,p.y+13,1)
    oled.line(p.x+9,p.y+13,p.x+7,p.y+15,1)
    oled.line(p.x+7,p.y+15,p.x+3,p.y+15,1)
    oled.line(p.x+3,p.y+15,p.x+1,p.y+13,1)
    oled.show()

def colon(p):
    oled.line(p.x+1,p.y+6,p.x+2,p.y+6,1)
    oled.line(p.x+1,p.y+5,p.x+2,p.y+5,1)
    oled.line(p.x+1,p.y+14,p.x+2,p.y+14,1)
    oled.line(p.x+1,p.y+15,p.x+2,p.y+15,1)
    oled.show()

# ====== ORARIO =======
def draw_time(time_str, y):
    spacing = 13
    start_x = (128 - len(time_str) * spacing) // 2
    for i, char in enumerate(time_str):
        p = Pos(start_x + i * spacing, y)
        if char == '0': zero(p)
        elif char == '1': one(p)
        elif char == '2': two(p)
        elif char == '3': three(p)
        elif char == '4': four(p)
        elif char == '5': five(p)
        elif char == '6': six(p)
        elif char == '7': seven(p)
        elif char == '8': eight(p)
        elif char == '9': nine(p)
        elif char == ':': colon(p)
