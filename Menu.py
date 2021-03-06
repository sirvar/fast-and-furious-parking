#main menu screen

from pygame import *
from Level import *
from Store import *
from Popup import *

class Menu():
	#initialize pygame
	init()
	def __init__(self, surface):
		"Initialize variables, load images, set flags, and fonts"
		self.surface = surface
		self.bg = transform.scale(image.load("res/main_bg.jpg").convert(), (surface.get_width(), surface.get_height()))
		self.carImage = image.load("res/front_car.png")
		self.arrow_left = image.load("res/arrow_left.png")
		self.carImageSized = transform.scale(self.carImage, (150, 100))
		self.carX, self.carY = 437,290
		self.width = self.carImageSized.get_width()
		self.height = self.carImageSized.get_height()
		self.logo = image.load("res/logo_perspective.png")
		self.running = True
		self.rightMenu = image.load("res/menu_right.png")
		self.rightMenuX, self.rightMenuY = 1024, 768
		self.menuFont = font.Font("res/fonts/pricedown.ttf", 35)
		#menu options with color, rects, text, and action on click
		self.optionColors = [(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255)]
		self.optionRects = [Rect(825,455,self.menuFont.size("Start Game")[0]+10,self.menuFont.size("Start Game")[1]),Rect(825,505,self.menuFont.size("Store")[0]+10,self.menuFont.size("Store")[1]),Rect(825,555,self.menuFont.size("Options")[0]+10,self.menuFont.size("Options")[1]),Rect(825,605,self.menuFont.size("Help")[0]+10,self.menuFont.size("Help")[1]),Rect(825,655,self.menuFont.size("About")[0]+10,self.menuFont.size("About")[1])]
		self.options = ["Start Game", "Store", "Help", "About"]
		self.optionResults = [self.levelRunning,self.storeRunning,self.setHelp,self.setAbout]
		self.store = Store(surface)
		self.level = Level(surface)
		self.about = Popup(surface, "About", ["Developed By Rikin Katyal", "ICS3U Final Project 2015", "Made Using Python and Pygame"])
		self.help = Popup(surface, "Help", ["Use arrow keys or WASD to move.", "Press Space for emergency break.", "Earn coins to spend in the store.", "Drive through obstacles and park", "in marked parking spot."])
		self.help.images([image.load("res/arrows.png"), image.load("res/wasd.png"), image.load("res/coin_medium.png")],[(310,456),(470,450),(660,475)])
		self.settings = Popup(surface, "Settings", ["Sound Effects (SFX)", "Music"])
		self.aboutRunning = False
		self.helpRunning = False
		self.settingsRunning = False

	def render(self, down):
		"Main function to render menu"
		mx, my = mouse.get_pos()
		mb = mouse.get_pressed()
		self.pressed = key.get_pressed()
		# blit menu if not store adn not level
		if not self.store.isRunning() and not self.level.isRunning():
			self.surface.blit(self.bg, (0,0))
			self.width += 16
			self.height += 12
			self.carY += 6
			self.carX -= 8
			self.carImageSized = transform.scale(self.carImage, (self.width, self.height))
			#blit logo and move car down road
			if self.carY > 320:
				self.surface.blit(self.logo, (512-100,380))
			if self.carY < 768:
				self.surface.blit(self.carImageSized, (self.carX, self.carY))
			else:
				self.surface.blit(self.rightMenu, (self.rightMenuX, self.rightMenuY))
				if self.rightMenuX >= 590:
					self.rightMenuX -= 30
				if self.rightMenuY >= 350:
					self.rightMenuY -= 30
				if self.rightMenuX <= 590 and self.rightMenuY <= 350:
					for r in range(len(self.options)):
						# draw.rect(self.surface, (255,255,0), self.optionRects[r])
						if self.optionRects[r].collidepoint((mx,my)) and not self.aboutRunning and not self.helpRunning:
							self.optionColors[r] = (0,0,0)
							if mb[0]:
								self.optionResults[r]()
						else:
							self.optionColors[r] = (255,255,255)
						self.surface.blit(self.menuFont.render(self.options[r], 1, self.optionColors[r]), (830, 450+(r*50)))
		#blit store instead of menu
		elif self.store.isRunning():
			self.store.render(down)
		#blit level screen instead of menu
		elif self.level.isRunning():
			self.level.render()
		#if level is chosen, end menu screen
		if self.level.choseLevel:
			self.running = False
		#about popup
		if self.aboutRunning:
			self.about.render()
			self.aboutRunning = self.about.isRunning()
		#help popup
		elif self.helpRunning:
			self.help.render()
			self.helpRunning = self.help.isRunning()

	def isRunning(self):
		"Check if menu is running"
		return self.running

	def notRunning(self):
		"Stop running menu"
		self.running = False

	def storeRunning(self):
		"Check if store is running"
		self.store.running = True

	def levelRunning(self):
		"Check if level screen is running"
		self.level.running = True

	def setAbout(self):
		"Start about popup"
		self.aboutRunning = True

	def setHelp(self):
		"Start help popup"
		self.helpRunning = True