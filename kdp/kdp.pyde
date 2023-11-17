# NOTE

# We decided to eliminate the 
# wall to wall jumping, the spitting
# of the dragons and the chests. We 
# had a lot of features and wanted to
# get the most important ones right. 

import os
import time
import random

path = os.getcwd() # Current working directory

WIN = False

WIDTH = 1280
HEIGHT = 720

hidden = 0
jump_count = 0
ground = 0
direction = "Right"
egg_collision = False
death = 0
T = 0

class Object:
  def __init__(self, x, y, r, g):
    self.x = x
    self.y = y 
    self.vx = 0
    self.vy = 0 
    self.r = r
    self.g = g

# KNIGHT CLASS

# This class describes the knight. 
# It helps with the super powers they 
# many acquire throughout the game, it 
# also helps with the light circle that
# follows it throughout the gamde. 

class Knight(Object):
  def __init__(self, x, y, r, g):
    Object.__init__(self, x, y, r, g)

    # Special Power Indicators

    self.power_start = 0
    self.immunity = False
    self.kill = False
    self.higher_jump = False
    self.fancy_jump = False
    self.sword = False
    self.torch_battery = 10
    self.last_torch = 0

    # Display Details

    self.img_w = 500
    self.img_h = 584
    self.img_right = loadImage(path + "/images/knight_right.png")
    self.img_left = loadImage(path + "/images/knight_left.png")


    self.lc_width = 500
    self.lc_height = 500
    self.light_circle = loadImage(path + "/images/light_circle.png")


    self.fl_width = 243
    self.fl_height = 500
    self.flashlight = loadImage(path + "/images/flashlight1.png")

    self.immunity_img = loadImage(path + "/images/bubble.png")

    self.sword_w = 504
    self.sword_h = 1104
    self.sword_img = loadImage(path + "/images/sword.png")

    self.boots_w = 500
    self.boots_h = 584
    self.fancy_boots_right = loadImage(path + "/images/fancy_boots_right.png")
    self.fancy_boots_left = loadImage(path + "/images/fancy_boots_left.png")
    self.jumping_boots_right = loadImage(path + "/images/jumping_boots_right.png")
    self.jumping_boots_left = loadImage(path + "/images/jumping_boots_left.png")
    

    # Movement Details

    self.key_handler = {LEFT:False, UP:False, RIGHT:False, ENTER:False, "T":False}

  def gravity(self):
    global key_released
    global jump_count
   
   
    global ground
   
    if self.y >= self.g - (self.r / 2): 
      key_released = 0
      jump_count = 0 
      self.vy = 0
      ground = 1                           
      self.y = self.g - (self.r / 2)   
   
    elif self.y < self.g - (self.r / 2): 
      self.vy += 0.2   
      ground = 0

    # WALLS AND SURFACES

    # This code makes sure the character
    # bounces off walls and stays on top
    # of platforms. 
   
    for wall in LEVEL.walls:
      if (self.y + self.vy + self.r / 2 > wall.y1 and self.y - self.r / 2 <= wall.y1 and self.vy > 0) and (wall.x1 < self.x < wall.x2 or wall.x1 < self.x - self.r / 2 < wall.x2 or wall.x1 < self.x + self.r / 2 < wall.x2):
        self.vy = 0
        ground = 1
        jump_count = 0 
        key_released = 0
        self.y = wall.y1 - self.r / 2
   
    for wall in LEVEL.walls:
      if (self.y + self.vy - self.r / 2 < wall.y2 and self.y + self.r / 2 >= wall.y2 and self.vy < 0) and (wall.x1 < self.x < wall.x2 or wall.x1 < self.x + self.r / 2 < wall.x2 or wall.x1 < self.x - self.r / 2 < wall.x2):
        print("SHSH")
        self.vy = 0
        self.y = wall.y2 + self.r / 2 
   
    global LEVEL
    global death
    for lava in LEVEL.lava:
      if (LEVEL.knight.immunity == 0 and self.y + self.vy + self.r / 2 >= lava.y1 and self.y - self.r / 2 <= lava.y1 and self.vy >= 0) and (lava.x1 < self.x < lava.x2):
        LEVEL = LEVELS[LEVELS.index(LEVEL)]
        time.sleep(0.5)
        death += 1
        LEVEL.knight.x = 50
        break
   
    self.y += self.vy

  def display(self): 
    current_time = time.time()

    # CHARACTER


    #fill(65)
    #noStroke()    
    #ellipse(self.x, self.y, self.r, self.r)

    global direction

    # DISPLAYING POWERS

    # The following lines of code help 
    # with displaying each of the powers 
    # For example, if the character were to
    # obtain an immmunity bubble, it would 
    # become enveloped by one

    if self.fancy_jump == True:

      if direction == "Right":

        imageMode(CENTER)
        image(self.fancy_boots_right, self.x, self.y - 7, self.img_w / 5, self.img_h / 5)
        imageMode(CORNER)

      elif direction == "Left":

        imageMode(CENTER)
        image(self.fancy_boots_left, self.x, self.y - 7, self.img_w / 5, self.img_h / 5)
        imageMode(CORNER)


    elif self.higher_jump == True:

      if direction == "Right":

        imageMode(CENTER)
        image(self.jumping_boots_right, self.x, self.y - 7, self.img_w / 5, self.img_h / 5)
        imageMode(CORNER)

      elif direction == "Left":

        imageMode(CENTER)
        image(self.jumping_boots_left, self.x, self.y - 7, self.img_w / 5, self.img_h / 5)
        imageMode(CORNER)

    else:

      if direction == "Right":

        imageMode(CENTER)
        image(self.img_right, self.x, self.y - 7, self.img_w / 5, self.img_h / 5)
        imageMode(CORNER)

      elif direction == "Left":

        imageMode(CENTER)
        image(self.img_left, self.x, self.y - 7, self.img_w / 5, self.img_h / 5)
        imageMode(CORNER)


    # LIGHT CIRCLE AND FLASHLIGHT

    # This code makes sure the light circle
    # is displayed and the flashlight also
    # shows up accordingly when called.

    fill(0,0,0) # Color Fill

    # Position

    global T
    if T == 1 and current_time - self.last_torch <= self.torch_battery: 

      global direction

      if direction == "Right":

        ul_corner_x = self.x - (self.lc_width / 2) 
        ul_corner_y = self.y - (self.lc_height / 2)

      elif direction == "Left":

        ul_corner_x = self.x - self.lc_width 
        ul_corner_y = self.y - (self.lc_height / 2)


      image(self.flashlight, ul_corner_x, ul_corner_y, self.fl_width * 2.94, self.fl_height)

      #Right Border

      rb_ul_corner_x = ul_corner_x + (self.fl_width * 2.94) - 5
      rect(rb_ul_corner_x, ul_corner_y, (WIDTH - rb_ul_corner_x), (HEIGHT - ul_corner_y))

      #Left Border

      rect(0, ul_corner_y, ul_corner_x + 5, (HEIGHT - ul_corner_y))

      #Upper Border

      rect(0, 0, WIDTH, ul_corner_y + 5)

      #Lower Border

      lowb_ul_corner_y = ul_corner_y + self.fl_height
      rect(0, lowb_ul_corner_y - 5, WIDTH, HEIGHT - lowb_ul_corner_y)

    else:

      ul_corner_x = self.x - (self.lc_width / 2) 
      ul_corner_y = self.y - (self.lc_height / 2)


      image(self.light_circle, ul_corner_x, ul_corner_y, self.lc_width, self.lc_height)

        #Right Border

      rb_ul_corner_x = ul_corner_x + self.lc_width
      rect(rb_ul_corner_x, ul_corner_y, (WIDTH - rb_ul_corner_x), (HEIGHT - ul_corner_y))

        #Left Border

      rect(0, ul_corner_y, ul_corner_x, (HEIGHT - ul_corner_y))

        #Upper Border

      rect(0, 0, WIDTH, ul_corner_y + 1)

      #Lower Border

      lowb_ul_corner_y = ul_corner_y + self.lc_height
      rect(0, lowb_ul_corner_y - 1, WIDTH, HEIGHT - lowb_ul_corner_y)


    # SPECIAL POWERS DISPLAYED


    if (self.immunity == True) and (0 < current_time - self.power_start < 10):
      
      imageMode(CENTER)
      image(self.immunity_img, self.x - 5, self.y, self.r * 1.5, self.r * 1.5)
      imageMode(CORNER)

    elif (self.kill == True) and (0 < current_time - self.power_start < 10):
      
      global direction

      imageMode(CENTER)

      if direction == "Right":
        image(self.sword_img, self.x + (self.r / 2), self.y, self.sword_w / 11, self.sword_h / 11)
      elif direction == "Left":
        image(self.sword_img, self.x - (self.r / 2), self.y, self.sword_w / 11, self.sword_h / 11)

      imageMode(CORNER)

    elif (self.fancy_jump == True) and (0 < current_time - self.power_start < 60):
      pass

    elif (self.higher_jump == True) and (0 < current_time - self.power_start < 10):
      pass

    else:
      self.immunity = False
      self.kill = False
      self.fancy_jump = False
      self.higher_jump = False
      self.power_start = 0

    #print(self.immunity)

      #noFill()
      #stroke(125,0,0)
      #ellipse(self.x, self.y, self.r + 40, self.r + 40)



  def distance(self, target):
    return ((self.x - target.x) ** 2 + (self.y - target.y) ** 2) **0.5


  def update(self):
    self.display()
    self.gravity()

    global hidden
    global key_released
    global jump_count
    global ground

    # KEY HANDLER

    # The key handler manages the following operations.

    # RIGHT -> MOVE RIGHT
    # LEFT -> MOVE LEFT
    # ENTER -> ENTER CAVE
    # TAB -> EXIT CAVE
    # "T" -> TURN ON / OFF TORCH 


    if LEVEL.knight.key_handler[RIGHT] == False and LEVEL.knight.key_handler[LEFT] == False:
      self.vx = 0
    if LEVEL.knight.key_handler[RIGHT]:
      self.vx = 5
    if LEVEL.knight.key_handler[LEFT]:
      self.vx = -5
    if LEVEL.knight.key_handler[UP]:
      if self.fancy_jump == True:

        if (key_released == 0) and ground == 1: # If there hasn't been a first jump
          self.vy = -6.3

        elif (key_released == 1) and (jump_count == 0):
          jump_count = 1
          self.vy = -6.3
          key_released = 0

      elif self.fancy_jump == False:
        if ground == 1:
          if self.higher_jump == True:
            self.vy = -8.3
          else:
            self.vy = -6.3

    if LEVEL.knight.key_handler[ENTER]:
      for cave in LEVEL.caves:
        if (LEVEL.knight.x - (cave.x + 150))**2 + (LEVEL.knight.y - (cave.y + 150))**2 <= cave.r**2:
          hidden = 1
          LEVEL.knight.vx = 0
          LEVEL.knight.x = cave.x + 150
          LEVEL.knight.y = cave.y + 150
          LEVEL.knight.vy = 0


    for wall in LEVEL.walls:
      if (wall.x1 <= self.x + self.vx + self.r / 2 <= wall.x2 or wall.x1 <= self.x + self.vx - self.r / 2 <= wall.x2) and (self.x + self.r / 2 <= wall.x1 or self.x - self.r / 2 >= wall.x2) and (wall.y1 <= self.y <= wall.y2 or wall.y1 <= self.y - self.r / 2 <= wall.y2 or wall.y1 <= self.y + self.r / 2 <= wall.y2):
        self.vx = 0
        if self.x - self.r / 2 >= wall.x2:
          self.x = wall.x2 + self.r / 2
        elif self.x + self.r / 2 <= wall.x1:
          self.x = wall.x1 - self.r / 2
          
    self.x += self.vx
    self.y += self.vy

    # DRAGONS AND IMMUNITY

    # These lines of code makes sure that when 
    # the character has immunity it is not 
    # killed by a dragon.


    for dragon in LEVEL.dragons: # Add immunity and sword here
      if self.distance(dragon) <= (self.r / 2) + (dragon.r / 2):
        if self.kill == True:
          del LEVEL.dragons[LEVEL.dragons.index(dragon)]


    # VALIDATING SPECIAL ITEMS

    # These lines of code validate the 
    # special powers and help keep track the time
    # the character can use them for. 

    for specialitem in LEVEL.specialitems:
      if self.distance(specialitem) <= (self.r / 2) + (specialitem.r / 2) - 50:
        self.immunity = False
        self.kill = False
        self.higher_jump = False
        self.fancy_jump = False
        self.sword = False
        if specialitem.power == "Immunity":
          self.immunity = True
          self.power_start = time.time()
          del LEVEL.specialitems[LEVEL.specialitems.index(specialitem)]

        if specialitem.power == "Kill":
          self.kill = True
          self.power_start = time.time()
          del LEVEL.specialitems[LEVEL.specialitems.index(specialitem)]

        if specialitem.power == "Fancy Jump":
          self.fancy_jump = True
          self.power_start = time.time()
          del LEVEL.specialitems[LEVEL.specialitems.index(specialitem)]

        if specialitem.power == "Higher Jump":
          self.higher_jump = True
          self.power_start = time.time()
          del LEVEL.specialitems[LEVEL.specialitems.index(specialitem)]

        if specialitem.power == "Battery":
          self.torch_battery += 5
          self.last_torch = time.time()
          del LEVEL.specialitems[LEVEL.specialitems.index(specialitem)]

        if specialitem.power == "Saved":
          global WIN 
          WIN = True

    # COLLIDING WITH EGGS

    # These lines of code detect if 
    # the player has collided with a 
    # dragon egg.

    for egg in LEVEL.eggs:
      if self.distance(egg) <= (self.r / 2) + (egg.r / 2):
        global egg_collision

        if self.immunity == False:
          egg_collision = True
        elif self.immunity == True:
          egg_collision = False

    # print(str(self.x) + "," + str(self.y)) # aPrint coordinates

class Cave(Object):
  def __init__(self, x, y):
    self.x = x
    self.y = y 
    self.r = 150

    self.img_w = 250
    self.img_h = 248
    self.img = loadImage(path + "/images/cave2.png")

  def display(self):
    image(self.img, self.x, self.y)


class Lava:
  def __init__(self, x, y, w, h):
    self.x1 = x
    self.y1 = y
    self.w = w
    self.h = h
    self.x2 = x + self.w
    self.y2 = y + self.h

  def display(self):
    fill(237,28,36)
    noStroke()
    rect(self.x1, self.y1, self.w, self.h)


class Dragon(Object):
  def __init__(self, x, y, r, g, walk_l, walk_r):
    Object.__init__(self, x, y, r, g)
    self.walk_l = walk_l
    self.walk_r = walk_r
    self.dir = random.randint(0, 1) #0 - left, 1 - right

    self.img_w = 500
    self.img_h = 352
    self.img = loadImage(path + "/images/dragon.png")


  # ANIMATING THE ENEMY

  # These lines of code animate
  # the dragon so that it moves
  # back and forth between two
  # x coordinates.


  def update(self):
    if self.dir == 0: 
      self.vx = -3
    else:
      self.vx = 3
    if not self.walk_l <= self.x + self.vx <= self.walk_r:
      self.dir = 1 - self.dir
      if self.vx == 3:
        self.vx = -3
      else:
        self.vx = 3
    
    self.x += self.vx
    
  def collision(self, other):
    if (self.x - other.x) ** 2 + (self.y - other.y) ** 2 <= (self.r / 2 + other.r / 2) ** 2:
      return True
    return False
      
  def display(self):
    #fill(125,0,0)
    #noStroke()
    #ellipse(self.x, self.y, self.r, self.r)

    imageMode(CENTER)
    image(self.img, self.x, self.y + 15, self.img_w / 3, self.img_h / 3)
    imageMode(CORNER)

    self.update()

    global hidden
    global LEVEL
    if self.collision(LEVEL.knight) == True and LEVEL.knight.immunity == True or hidden == 1 or LEVEL.knight.sword == True:
      pass
    elif self.collision(LEVEL.knight) == True:
      LEVEL = LEVELS[LEVELS.index(LEVEL)]
      time.sleep(0.5)
      global death
      death += 1
      LEVEL.knight.x = 50
      #for now


class SpecialItem(Object):
  def __init__(self, x, y, r, g, power):
    Object.__init__(self, x, y, r, g)
    self.power = power

    self.immunity_img = loadImage(path + "/images/bubble.png")
    self.sword_img = loadImage(path + "/images/sword.png")
    self.fancy_boots_img = loadImage(path + "/images/fancy_boots.png")
    self.jumping_boots_img = loadImage(path + "/images/jumping_boots.png")
    self.princess_img = loadImage(path + "/images/princess.png")
    self.battery_img = loadImage(path + "/images/battery.png")

    self.sword_w = 504
    self.sword_h = 1104

    self.boots_w = 700
    self.boots_h = 441

    self.princess_w = 500
    self.princess_h = 477

    self.battery_w = 500
    self.battery_h = 273

  def display(self):
    #self.gravity()

  
    #fill(0,0,125)
    #noStroke()
    #ellipse(self.x, self.y, self.r, self.r) # Replaced by static image


    # DISPLAYING THE ITEMS

    # These lines display the items before
    # they are grabbed by the character.

    if self.power == "Immunity":
      imageMode(CENTER)
      image(self.immunity_img, self.x, self.y, 100, 100)
      imageMode(CORNER)
    elif self.power == "Kill":
      imageMode(CENTER)
      image(self.sword_img, self.x - 5, self.y, self.sword_w / 10, self.sword_h / 10)
      imageMode(CORNER)
    elif self.power == "Fancy Jump":
      imageMode(CENTER)
      image(self.fancy_boots_img, self.x, self.y, self.boots_w / 5, self.boots_h / 5)
      imageMode(CORNER)
    elif self.power == "Higher Jump":
      imageMode(CENTER)
      image(self.jumping_boots_img, self.x, self.y, self.boots_w / 5, self.boots_h / 5)
      imageMode(CORNER)
    elif self.power == "Battery":
      imageMode(CENTER)
      image(self.battery_img, self.x, self.y, self.battery_w / 5, self.battery_h / 5)
      imageMode(CORNER)
    elif self.power == "Saved":
      imageMode(CENTER)
      image(self.princess_img, self.x, self.y, self.princess_w / 4, self.princess_h / 4)
      imageMode(CORNER)

  # def update(self): -> Bouncing animation

# class HazardousItem:

class DragonEgg(Object):
  def __init__(self, x, y, r, g):
    Object.__init__(self, x, y, r, g)
    self.x = x
    self.y = y

    self.egg_img_w = 442
    self.egg_img_h = 505
    self.egg_img = loadImage(path + "/images/dragon_egg.png")

    self.dragon_img_w = 500
    self.dragon_img_h = 352
    self.dragon_img = loadImage(path + "/images/dragon.png")

    self.r = r

  def display(self):

    global egg_collision

    if egg_collision == True:
      del LEVEL.eggs[LEVEL.eggs.index(self)]
      LEVEL.dragons.append(Dragon(self.x, self.y, 70, self.g, self.dragon_img_w / 3, self.dragon_img_h / 3))
    else:
      imageMode(CENTER)
      image(self.egg_img, self.x, self.y, self.egg_img_w / 5, self.egg_img_h / 5)
      imageMode(CORNER)

      #fill(0,0,125)
      #noStroke()
      #ellipse(self.x, self.y, 101, 101)

class Wall:
  def __init__(self, x1, y1, width, height):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x1 + width
    self.y2 = y1 + height
    self.w = width
    self.h = height

  def display(self):
    fill(0, 0, 0)
    rect(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1)

Knight = Knight(50,50,100,600)


# LEVEL CLASS

# The level class stores everything
# necessary to properly display and 
# work with a level. 

class Level:
  def __init__(self, ground, knight):

    self.background_img = loadImage(path + "/images/background.png")

    self.ground = ground

    self.caves = []
    self.lava = []
    self.dragons = []
    self.specialitems = []
    self.walls = []
    self.eggs = []
    self.battery = []

    self.knight = knight

  def display(self):

    self.knight.g = self.ground

    # Background
    background(255,255,255)
    fill(0,0,0)
    image(self.background_img, 0, 0, WIDTH, HEIGHT)

    # Ground
    #fill(0,0,0)
    #noStroke()
    #rect(0, self.ground, WIDTH, HEIGHT - self.ground)

    global hidden
    
    # Caves
    for cave in self.caves:
      cave.display()

    # Special Items
    for specialitem in self.specialitems:
      specialitem.display()

    # Dragons
    for dragon in self.dragons:
      dragon.display()

    # Walls
    for wall in self.walls:
      wall.display()

    # Eggs
    for egg in self.eggs:
      egg.display()

    # Lava
    for lava in self.lava:
      lava.display()

    # Knight
    if hidden == 0:
      self.knight.update()
    else:
      background(0)


    global T
    textSize(20)
    if T == 0:
      val = self.knight.torch_battery
    else:
      val = max(0, self.knight.torch_battery - time.time() + self.knight.last_torch)

    if LEVEL != Level0:
      fill(255, 255, 255);
      text("Torch Time: " + str(int(val * 100.0) / 100), 1100, 35)
      text("Death Count: " + str(death), 1100, 60)


# DEFINING THE LEVELS

# The following lines of code determine
# what is in each level and where.


Level0 = Level(600,Knight)


Level0.walls.append(Wall(-44,0,44,720)) # Left Border
Level0.walls.append(Wall(100,0,1180,450)) # Ceiling


Level0.walls.append(Wall(0, Level0.ground, 1280, 720 - Level0.ground)) # Ground


#######

Level1 = Level(600, Knight)


Level1.walls.append(Wall(313,523,500,80)) # Bottom Set
Level1.walls.append(Wall(813,445,141,80))
Level1.walls.append(Wall(954,366,141,80))

Level1.walls.append(Wall(153,307,487,80)) # Top Set
Level1.walls.append(Wall(640,226,142,80))

Level1.walls.append(Wall(0, Level1.ground, 1280, 720 - Level1.ground)) # Ground

Level1.specialitems.append(SpecialItem(250,530,100,Level1.ground,"Kill"))
Level1.dragons.append(Dragon(558, 460, 50, 600, 450, 700))

#######

Level2 = Level(600, Knight)

Level2.walls.append(Wall(100,373,486,79)) # Bottom Most
Level2.walls.append(Wall(100,208,175,79)) # Tiny
Level2.walls.append(Wall(443,167,837,80)) # Long
Level2.walls.append(Wall(1124,247,156,355)) # Vertical

Level2.specialitems.append(SpecialItem(700,530,100,Level2.ground,"Fancy Jump"))


Level2.walls.append(Wall(0, Level2.ground, 1280, 720 - Level2.ground)) # Ground

#######

Level3 = Level(640, Knight)

Level3.walls.append(Wall(0,167,1005,80)) # First, Top to Bottom
Level3.walls.append(Wall(211,406,989,80)) 
Level3.walls.append(Wall(0,640,1280,80))

Level3.caves.append(Cave(420, 10))
Level3.dragons.append(Dragon(509, 90, 50, 640, 320, 720))
Level3.eggs.append(DragonEgg(902, 345, 50, 640))
Level3.specialitems.append(SpecialItem(1100,335,100,Level3.ground,"Immunity"))
Level3.caves.append(Cave(560, 500))
Level3.dragons.append(Dragon(388, 565, 50, 640, 300, 700))

Level3.walls.append(Wall(1200,0,80,487)) # Right Border

Level3.walls.append(Wall(-44,167,44,552)) # Left Border

Level3.walls.append(Wall(0, Level3.ground, 1280, 720 - Level3.ground)) # Ground


#######

Level4 = Level(640, Knight)

Level4.walls.append(Wall(211,280,249,364))  # Pillar 1
Level4.walls.append(Wall(640,280,249,364))  # Pillar 2
Level4.walls.append(Wall(1033,280,249,364)) # Pillar 3

Level4.walls.append(Wall(-44,0,44,489)) # Left Border

Level4.specialitems.append(SpecialItem(110, 580, 50, 640, "Fancy Jump"))
Level4.specialitems.append(SpecialItem(775, 220, 50, 640, "Battery"))

Level4.lava.append(Lava(460,538,180,102))
Level4.lava.append(Lava(889,538,144,102))

Level4.walls.append(Wall(0, Level4.ground, 1280, 720 - Level4.ground)) # Ground

#######

Level5 = Level(640, Knight)

Level5.walls.append(Wall(0,280,249,215)) # Square
Level5.walls.append(Wall(412,0,249,495)) # Long Rectangle
Level5.walls.append(Wall(807,407,473,233)) # Base
Level5.walls.append(Wall(962,247,318,213)) # Upper

Level5.walls.append(Wall(-44,280,44,440)) # Left Border

Level5.lava.append(Lava(0,640,249,77))

Level5.specialitems.append(SpecialItem(722, 577, 50, 640, "Higher Jump"))

Level5.walls.append(Wall(0, Level5.ground, 1280, 720 - Level5.ground)) # Ground

#######

Level6 = Level(640, Knight)

Level6.walls.append(Wall(0,247,318,113)) # Entrance
Level6.walls.append(Wall(226,528,469,113)) # Step 1
Level6.walls.append(Wall(811,528,469,113)) # Step 2

Level6.walls.append(Wall(566,247,714,113)) # Top Platform
Level6.walls.append(Wall(1150,0,130,248)) # Right Border

Level6.walls.append(Wall(-44,247,44,473)) # Left Border

Level6.specialitems.append(SpecialItem(710, 183, 142, 83, "Immunity"))
Level6.specialitems.append(SpecialItem(120, 570, 141, 83, "Kill"))
Level6.dragons.append(Dragon(334,448,50,640,250,440))

Level6.lava.append(Lava(695,528,115,112))

Level6.walls.append(Wall(0, Level6.ground, 1280, 720 - Level6.ground)) # Ground

#######

Level7 = Level(527, Knight)

Level7.walls.append(Wall(-44,0,44,360)) # Left Border

Level7.walls.append(Wall(100,0,1180,420)) # Ceiling
Level7.caves.append(Cave(500, 400))
Level7.walls.append(Wall(0, Level7.ground, 1280, 720 - Level7.ground)) # Ground

Level7.dragons.append(Dragon(690, 460, 50, 527, 420, 900))

######

Level8 = Level(577, Knight)

Level8.walls.append(Wall(0,527,285,62)) # Tiny First Entrance
Level8.walls.append(Wall(285,435,285,143)) # Second Entrance
Level8.walls.append(Wall(692,360,218,218)) # Big Box Down
Level8.walls.append(Wall(100,0,351,300)) # Big Box Up
Level8.walls.append(Wall(451,0,829,210)) # Long Box Up
Level8.walls.append(Wall(1062,210,218,150)) # Small Box Hanging

Level8.walls.append(Wall(-44,0,44,420)) # Left Border

Level8.lava.append(Lava(570,498,122,80))

Level8.walls.append(Wall(0, Level8.ground, 1280, 720 - Level8.ground)) # Ground

######

Level9 = Level(577, Knight)

Level9.walls.append(Wall(100,0,1180,109)) # Ceiling
Level9.walls.append(Wall(217,502,109,109)) # Box Step
Level9.walls.append(Wall(327,428,327,183)) # Long Step
Level9.walls.append(Wall(763,360,114,250)) # Column

Level9.walls.append(Wall(971,459,114,152)) # Small Step to Out
Level9.walls.append(Wall(1085,271,195,340)) # Big Step to Out

Level9.eggs.append(DragonEgg(818,280,141,83))
Level9.specialitems.append(SpecialItem(715, 505, 100, 577, "Kill"))

Level9.walls.append(Wall(-44,0,44,340)) # Left Border

Level9.walls.append(Wall(0, Level9.ground, 1280, 720 - Level9.ground)) # Ground

######

Level10 = Level(611, Knight)

Level10.walls.append(Wall(0,271,195,453)) # Entrance
Level10.walls.append(Wall(100,0,223,109)) # Small Ceiling

Level10.walls.append(Wall(323,0,196,476)) # Hanging Box

Level10.walls.append(Wall(653,542,627,99)) # Stair 1
Level10.walls.append(Wall(737,476,543,71)) # Stair 2
Level10.walls.append(Wall(815,405,465,71)) # Stair 3
Level10.walls.append(Wall(891,334,389,71)) # Stair 4

Level10.walls.append(Wall(-44,0,44,109)) # Left Border
Level10.walls.append(Wall(1324,0,44,720)) # Right Border

Level10.specialitems.append(SpecialItem(1085,275,100,611,"Saved"))

Level10.walls.append(Wall(0, Level10.ground, 1280, 720 - Level10.ground)) # Ground

LEVELS = [Level0, Level1, Level2, Level3, Level4, Level5, Level6, Level7, Level8, Level9, Level10]

LEVEL = LEVELS[0]

def setup():
  size(WIDTH,HEIGHT)

def mouseClicked():
  print(mouseX, mouseY)

def keyPressed():
  if keyCode == LEFT:
    LEVEL.knight.key_handler[LEFT] = True

    global direction
    direction = "Left"

  elif keyCode == RIGHT:
    LEVEL.knight.key_handler[RIGHT] = True

    global direction
    direction = "Right"

  elif keyCode == UP:
    LEVEL.knight.key_handler[UP] = True
  elif key == ENTER:
    LEVEL.knight.key_handler[ENTER] = True
  elif key == TAB:
    global hidden
    hidden = 0
  elif key == "T" or key == 't':
    global T
    T = 1 - T
    if T == 0:
      LEVEL.knight.torch_battery = max(0, LEVEL.knight.torch_battery - time.time() + LEVEL.knight.last_torch)
    else:
      LEVEL.knight.last_torch = time.time()

global key_released

key_released = 0

def keyReleased():
  if keyCode == LEFT:
    LEVEL.knight.key_handler[LEFT] = False
  elif keyCode == RIGHT:
    LEVEL.knight.key_handler[RIGHT] = False
  elif keyCode == UP:

    global key_released

    if key_released == 0:
      key_released += 1

    LEVEL.knight.key_handler[UP] = False

  elif key == ENTER:
    LEVEL.knight.key_handler[ENTER] = False
  elif key == "T" or "t":
    LEVEL.knight.key_handler["T"] = False

#game = Game(520)

TITLE = loadImage(path + "/images/title.png")
TITLE_W = 500
TITLE_H = 327

ENDING = loadImage(path + "/images/ending.png")
ENDING_W = 500
ENDING_H = 153


def draw():
  LEVEL.display()

  #print(LEVEL.knight.x)
  #print(LEVELS.index(LEVEL))

  if LEVEL == Level0:
    imageMode(CENTER)
    image(TITLE,620,240,TITLE_W / 1.5, TITLE_H / 1.5)
    imageMode(CORNER)

  if WIN == True:
    background(0)
    imageMode(CENTER)
    image(ENDING,620,240,ENDING_W, ENDING_H)
    imageMode(CORNER)

  global LEVEL

  if LEVEL.knight.x > WIDTH + 50:

    LEVEL = LEVELS[LEVELS.index(LEVEL) + 1]

    LEVEL.knight.x = 0


  elif LEVEL.knight.x < 0:

    if LEVELS.index(LEVEL) == 0:
      LEVEL.knight.vx = 0
      LEVEL.knight.x = 60
    else:
      LEVEL = LEVELS[LEVELS.index(LEVEL) - 1]
      LEVEL.knight.x = 1230
    
