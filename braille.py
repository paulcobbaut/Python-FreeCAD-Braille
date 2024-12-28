#!/usr/bin/python
# braille.py -- Paul Cobbaut, 2022-07-05 and 2024-08-20
# Braille has many different dialects. This script is for Flemish!
# Some characters will be identical in French, Dutch, German, English... but not all.

import FreeCAD
from FreeCAD import Base, Vector
import Part

# These four define the size of the dots in mm
dot_size        =  1.0  # diameter of a dot
dot_separation  =  2.5  # space between center of dots
char_separation =  6.0  # space between center of characters
line_separation = 10.0  # space between center of lines

# position of Braille dots
# 14
# 25
# 36
# list of supported characters is a dictionary {character : dots printed}
braille = {
  "a" : "1",        # ⠁
  "b" : "12",       # ⠃
  "c" : "14",       # ⠉ 
  "d" : "145",      # ⠙
  "e" : "15",       # ⠑
  "f" : "124",      # ⠋
  "g" : "1245",     # ⠛
  "h" : "125",      # ⠓
  "i" : "24",       # ⠊
  "j" : "245",      # ⠚
  "k" : "13",       # ⠅
  "l" : "123",      # ⠇
  "m" : "134",      # ⠍
  "n" : "1345",     # ⠝
  "o" : "135",      # ⠕
  "p" : "1234",     # ⠏
  "q" : "12345",    # ⠟
  "r" : "1235",     # ⠗
  "s" : "234",      # ⠎
  "t" : "2345",     # ⠞
  "u" : "136",      # ⠥
  "v" : "1236",     # ⠧
  "w" : "2456",     # ⠺
  "x" : "1346",     # ⠭
  "y" : "13456",    # ⠽
  "z" : "1356",     # ⠵
  #uppercase "45"   # ⠨ # 'permanent' uppercase series
  "`" : "45",       # ⠨ This is a hack, enables using the funtion to insert this character
  #uppercase "45"   # ⠨
  #uppercase "46"   # ⠨ # one uppercase character
  "~" : "46",       # ⠨ This is a hack, enables using the funtion to insert this character
  #uppercase "46"   # ⠨
  "A" : "1",        # ⠨⠁
  "B" : "12",       # ⠨⠃
  "C" : "14",       # ⠨⠉ 
  "D" : "145",      # ⠨⠙
  "E" : "15",       # ⠨⠑
  "F" : "124",      # ⠨⠋
  "G" : "1245",     # ⠨⠛
  "H" : "125",      # ⠨⠓
  "I" : "24",       # ⠨⠊
  "J" : "245",      # ⠨⠚
  "K" : "13",       # ⠨⠅
  "L" : "123",      # ⠨⠇
  "M" : "134",      # ⠨⠍
  "N" : "1345",     # ⠨⠝
  "O" : "135",      # ⠨⠕
  "P" : "1234",     # ⠨⠏
  "Q" : "12345",    # ⠨⠟
  "R" : "1235",     # ⠨⠗
  "S" : "234",      # ⠨⠎
  "T" : "2345",     # ⠨⠞
  "U" : "136",      # ⠨⠥
  "V" : "1236",     # ⠨⠧
  "W" : "2456",     # ⠨⠺
  "X" : "1346",     # ⠨⠭
  "Y" : "13456",    # ⠨⠽
  "Z" : "1356",     # ⠨⠵
  #number : "3456"  # ⠼ Precedes a number
  "#" : "3456",     # ⠼ This is a hack, enables using the funtion to insert this character
  #number : "3456"  # ⠼
  "1" : "1",        # ⠼⠁
  "2" : "12",       # ⠼⠃
  "3" : "14",       # ⠼⠉
  "4" : "145",      # ⠼⠙
  "5" : "15",       # ⠼⠑
  "6" : "124",      # ⠼⠋
  "7" : "1245",     # ⠼⠛
  "8" : "125",      # ⠼⠓
  "9" : "24",       # ⠼⠊
  "0" : "245",      # ⠼⠚
  " " : "",         #  spatie
  "-" : "36",       # ⠤ min en streepje zijn hetzelfde
  "," : "2",        # ⠂
  ";" : "23",       # ⠆
  "'" : "3",        # ⠄
  ":" : "25",       # ⠒
  "!" : "235",      # ⠖
  "(" : "236",      # ⠦
  ")" : "356",      # ⠴
  '"' : "2356",     # ⠶
  "?" : "26",       # ⠢
  "." : "256",      # ⠲
  "*" : "35",       # ⠔
  "@" : "345",      # ⠜
  "€" : "15",       # ⠑
  "/" : "34",       # ⠌ schuine streep
  "+" : "235",      # ⠖
  "=" : "2356"     # ⠶
  #"/" : "356"       # ⠴ deelteken, we doen geen wiskunde 
}

# create the template dot that is always copied
def create_template_dot():
    dot = doc.addObject("Part::Sphere", "dot")
    dot.Radius = dot_size
    dot.Angle1 = -90
    dot.Angle2 = 90
    dot.Angle3 = 180
    dot.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(180, 0, 90))
    dot.ViewObject.hide()
    doc.recompute()	
    return dot

# place a dot in the correct position
def place_a_dot(dot_number, char_count, line_count):		# dot_number is Braille dot 1, 2, 3, 4, 5 or 6
    obj = doc.addObject('Part::Feature','dot')			# copy the template dot
    obj.Shape = doc.dot.Shape
    obj.Label = "dot_" + str(line_count) + "_" + str(char_count) + "_" + str(dot_number)	# name has 'some' meaning: dot + character position + Braille dot
    # Get X coordinate
    left_right = dot_number >> 2				# 0 if 1,2 or 3, 1 if 4, 5 or 6 (zero means dot on the left, one means dot on the right)
    char_position = char_count * char_separation		# this is the n-th character (n = char_count + 1 )
    dot_position = dot_separation * left_right                  # this is either a 123 dot on the left, or a 456 dot on the right
    x = char_position + dot_position
    # Get Y coordinate
    line_position = line_separation * line_count
    y = dot_separation * (- dot_number % 3) - line_position	# negative modulo 3 gives Y coordinate (three dots above each other)
    # Finale position for this dot
    position = FreeCAD.Vector(x, y, 0)
    rotation = FreeCAD.Rotation(180, 0, 90)
    obj.Placement = FreeCAD.Placement(position, rotation)	# put copied and named dot in correct location
    return obj

def create_character(char, char_count, line_count):
    dotlist = [] # all dots of this character in one list
    for i in range(1,7):
        if str(i) in braille[char]:
            dotobj = place_a_dot(i, char_count, line_count)
            dotlist.append(dotobj)
    obj = doc.addObject("Part::Compound",str(line_count) + ' ' + str(char_count) + ' ' + char)
    obj.Links = dotlist
    doc.recompute()
    return obj # returns up to six dots as one object

def create_braille_string(string, line_count):
    string = ' ' + string + ' ' # thus there is always a previous_char and next_char
    char_count = 0  # keeps track of the n-th character on each line, used for the position of the current character
    inserted_char_count = 0 # counts special inserted characters like "45" "46" and "3456"
    line_list = []  # list to create compound of this line
    for current_char in string: 
        if current_char != " ":                     # space only ups char_count with one
            previous_char = string[char_count - inserted_char_count - 1]
            next_char     = string[char_count - inserted_char_count + 1]
            if current_char.isupper():
                if not previous_char.isupper():     # This is the first uppercase letter
                    if not next_char.isupper():     # This is not a series of uppercase letters
                        obj46 = create_character("~", char_count, line_count) # hack for "46"
                        char_count = char_count + 1
                        inserted_char_count = inserted_char_count + 1
                        line_list.append(obj46)
                    else:                           # This is a series of uppercase letters
                        obj45 = create_character("`", char_count, line_count) # hack for "45"
                        char_count = char_count + 1
                        inserted_char_count = inserted_char_count + 1
                        line_list.append(obj45)
            if current_char.isdigit():
                if not previous_char.isdigit() and not previous_char == ',': # This is the first or the only digit
                    obj3456 = create_character("#", char_count, line_count)
                    char_count = char_count + 1
                    inserted_char_count = inserted_char_count + 1
                    line_list.append(obj3456)
            objchar = create_character(current_char, char_count, line_count)
            line_list.append(objchar)
        char_count = char_count + 1
    line_name = "line" + string 
    obj = doc.addObject("Part::Compound",line_name)
    obj.Links = line_list
    obj.Label = line_name
    doc.recompute()
    return

# START
doc = FreeCAD.newDocument("Braille demo")
dot = create_template_dot()
# line_count keeps track of the n-th line
# is used for the position of the current line
line_count = 0

create_braille_string("quick brown fox jumps", line_count)
line_count = line_count + 1
create_braille_string("Over The laZy doG", line_count)
line_count = line_count + 1
create_braille_string("(haakjes) komma, punt.", line_count)
line_count = line_count + 1
create_braille_string("quote' dub: pkom; vr?", line_count)
line_count = line_count + 1
create_braille_string("ALLES HOOFDLETTERS!!!", line_count)
line_count = line_count + 1
create_braille_string("tel 1 2 3 of 1,2,3", line_count)
line_count = line_count + 1
create_braille_string("4+2=6 zwart/wit **", line_count)
line_count = line_count + 1
create_braille_string("pol@brol 1/2 €9.50", line_count)
line_count = line_count + 1

# visualise all in FreeCAD GUI
doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
