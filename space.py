import pygame as pg
from pygame.locals import *
from time import *

pg.init()
pg.mixer.init()

def blit_text(surface, text, max_width, max_height, pos, font = pg.font.SysFont('Arial', 28), color = (255, 255, 255)):
	words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
	space = font.size(' ')[0]  # The width of a space.
	x, y = pos
	for line in words:
		for word in line:
			word_surface = font.render(word, 0, color)
			word_width, word_height = word_surface.get_size()
			if x + word_width >= max_width:
				x = pos[0]  # Reset the x.
				y += word_height  # Start on new row.
			surface.blit(word_surface, (x, y))
			x += word_width + space
		x = pos[0]  # Reset the x.
		y += word_height  # Start on new row.

class Information:
	def __init__(self):
		pg.key.set_repeat(100, 500)
		self.creat_a_screen()
		self.load_image()
		self.creat_position()
		self.key_word()
		self.pTime, self.cTime = 0, 0
		self.help_text = ['Raise at least 3 fingers to move the rocket',
						  'Use Metal (Thumb, Index Finger and Pinky Finger) to shoot',
						  'Raise only the Thumb to Back to Start',
						  'No finger to Pause Game']

	def creat_a_screen(self):
		self.size = [425, 750]
		self.scr = pg.display.set_mode(self.size)
		pg.display.set_caption('Space Shooting')

	def load_image(self):
		self.plane = [pg.transform.scale(pg.image.load(f'E:\ThisPC\Desktop\Other\DoAnCoSo4\Pic\P ({x + 1}).png'), (40, 80)) for x in range(3)]
		self.bg = [pg.transform.scale(pg.image.load(f'E:\ThisPC\Desktop\Other\DoAnCoSo4\Pic\BG{x}.png'), self.size) for x in range(2)]
		self.bullet = [pg.transform.scale(pg.image.load(f'E:\ThisPC\Desktop\Other\DoAnCoSo4\Pic\B ({x + 1}).png'), [10, 10]) for x in range(7)]
		self.enemy = [pg.transform.scale(pg.image.load(f'E:\ThisPC\Desktop\Other\DoAnCoSo4\Pic\E ({x + 1}).png'), [80, 80]) for x in range(6)]
		self.status = [pg.transform.scale(pg.image.load(f'E:\ThisPC\Desktop\Other\DoAnCoSo4\Pic\S{i + 1}.png'), (200, 80)) for i in range(4)]
		self.finger = [pg.transform.scale(pg.image.load(f'E:\ThisPC\Desktop\Other\DoAnCoSo4\Pic\{i}.png'), (80, 80)) for i in range(4, 8)]
		self.star = pg.transform.scale(pg.image.load(f'E:\ThisPC\Desktop\Other\DoAnCoSo4\Pic\star.png'), (300, 100))

	def creat_position(self):
		self.bgPos = [0, - self.size[1], 8]
		self.p = [(self.size[0] - self.plane[0].get_width()) // 2, self.size[1] - self.plane[0].get_height(), 500]
		self.pdx, self.pdy = [], []
		self.bPos = []
		self.ebPos = []
		self.columns = [0] * 5
		self.enemyP = [[True, 250.0, 0] for i in range(5)]
		self.reset_e = [[True, 250.0, 0] for i in range(5)]

	def key_word(self):
		self.system = [False] * 6 # 0:Start, 1:Play, 2:Help, 3:Pause, 4:Win, 5:Lose
		self.system[0] = True

	def font(self, size):
		f = pg.font.SysFont('Time New Roman', size)
		return f

class Game(Information):
	def __init__(self):
		super().__init__()

	def play_background_music(self, music_name):
		pg.mixer.music.load(r'E:\\ThisPC\\Desktop\\Other\\DoAnCoSo4\\Music\\'+music_name+'.mp3')
		pg.mixer.music.play()

	def event_sound(self, sound_name):
		sound = pg.mixer.Sound(r'E:\\ThisPC\\Desktop\\Other\\DoAnCoSo4\\Music\\'+sound_name+'.mp3')
		pg.mixer.Sound.play(sound)

	def BG(self):
		self.scr.blit(self.bg[0], (0, self.bgPos[0]))
		self.scr.blit(self.bg[1], (0, self.bgPos[1]))
		self.bgPos[0] += self.bgPos[2]
		self.bgPos[1] += self.bgPos[2]
		if self.bgPos[0] > self.size[1] + self.bgPos[2]:
			self.bgPos[0] = - self.size[1]
		elif self.bgPos[1] > self.size[1] + self.bgPos[2]:
			self.bgPos[1] = - self.size[1]

	def PLANE(self):
		self.scr.blit(self.plane[0], (self.p[0], self.p[1]))

	def go_by_motion(self, pos):
		self.pdx.append(pos[0])
		self.pdy.append(pos[1])
		if len(self.pdx) == 2:
			if 0 <= self.p[0] + self.pdx[1] - self.pdx[0] <= self.size[0] - self.plane[0].get_width():
				self.p[0] += self.pdx[1] - self.pdx[0]
			if self.enemy[0].get_height() + 20 <= self.p[1] + self.pdy[1] - self.pdy[0] <= self.size[1] - self.plane[0].get_height():
				self.p[1] += self.pdy[1] - self.pdy[0]
			del self.pdx[0], self.pdy[0]

	def creat_a_bullet(self, speed = 5):
		if self.bPos != []:
			self.bPos[0] = speed
		else:
			self.bPos.append(speed)
		bx = self.p[0] + (self.plane[0].get_width() - self.bullet[0].get_width()) // 2
		by = self.p[1] - self.bullet[0].get_height()
		column = bx // (5 + self.enemy[-1].get_width())
		self.bPos.insert(1, [bx, by])

	def shooting(self):
		for i in range(1, len(self.bPos)):
			self.scr.blit(self.bullet[6], self.bPos[i])
			self.bPos[i][1] -= self.bPos[0]
		if len(self.bPos) > 1:
			if self.bPos[-1][1] < - self.bullet[0].get_height():
				del self.bPos[-1]

	def ENEMY(self):
		for i in range(5):
			if self.enemyP[i][0]:
				self.scr.blit(self.enemy[self.enemyP[i][2]], (i * (5 + self.enemy[-1].get_width()), 0))
		self.enemy_shoot()
		self.hit()

	def hit(self):
		for i in self.bPos[1:]:
			if i[1] < self.enemy[-1].get_height():
				x = i[0] // (5 + self.enemy[-1].get_width())
				if self.enemyP[x][1] > 0:
					self.enemyP[x][1] -= 0.25
					self.event_sound('hit')
				if self.enemyP[x][1] == 0:
					self.enemyP[x][0] = False
				if self.enemyP[x][0] == False and self.enemyP[x][2] < 6:
					self.enemyP[x] = [True, self.reset_e[x][1] * 2, self.reset_e[x][2] + 1]
					self.reset_e[x] = [True, self.reset_e[x][1] * 2, self.reset_e[x][2] + 1]

		for i in self.ebPos:
			if self.p[0] <= i[0] <= self.p[0] + self.plane[0].get_width():
				if self.p[1] <= i[1] <= self.p[1] + self.plane[0].get_height():
					if self.p[2] > 0:
						self.event_sound('hitted')
						self.p[2] -= 1

	def enemy_creat_bullets(self, n = 1000, overtime = 1):
		self.cTime = time()
		if self.cTime - self.pTime > overtime:
			c = 5 + self.enemy[-1].get_width()
			for i in range(5):
				x = i * c + (c - self.bullet[1].get_width()) / 2
				y = self.enemy[-1].get_height()
				dx = (self.p[0] + self.plane[0].get_width() / 2 - x) / n
				dy = (self.p[1] - y) / n
				self.ebPos.append([x, y, dx, dy])
			self.pTime = self.cTime

	def enemy_shoot(self):
		if self.ebPos != []:
			for i in self.ebPos:
				self.scr.blit(self.bullet[2], i[:2])
				i[0] += i[2]
				i[1] += i[3]
			if self.ebPos[0][0] > self.size[0] or self.ebPos[0][0] < 0 or self.ebPos[0][1] > self.size[1]:
				del self.ebPos[0]

	def start_mode(self):
		if self.system[0]:
			if not pg.mixer.music.get_busy():
				self.play_background_music('bmg_start')
			self.PLANE()
			self.scr.blit(self.star, ((self.size[0] - self.star.get_width()) // 2, 50))
			for x, i in enumerate(self.status[:3]):
				self.scr.blit(i, ((self.size[0] - i.get_width()) // 2, (self.size[1] - 3 * i.get_height() - 40) // 2 + x * (i.get_height() + 20)))

	def win_mode(self):
		if self.system[4]:
			you_win = self.font(100).render('YOU WIN !!', True, (255, 255, 255))
			self.PLANE()
			self.scr.blit(you_win, ((self.size[0] - you_win.get_width()) // 2, 80))
			for x, i in enumerate(self.status[:3]):
				self.scr.blit(i, ((self.size[0] - i.get_width()) // 2, (self.size[1] - 3 * i.get_height() - 40) // 2 + x * (i.get_height() + 20)))

	def lose_mode(self):
		if self.system[5]:
			you_lose = self.font(70).render('YOU LOSE !!', True, (255, 255, 255))
			self.PLANE()
			self.scr.blit(you_lose, ((self.size[0] - you_lose.get_width()) // 2, 80))
			for x, i in enumerate(self.status[:3]):
				self.scr.blit(i, ((self.size[0] - i.get_width()) // 2, (self.size[1] - 3 * i.get_height() - 40) // 2 + x * (i.get_height() + 20)))

	def pause_mode(self):
		if self.system[3]:
			if not pg.mixer.music.get_busy():
				self.play_background_music('bmg_help')
			you_pause = self.font(70).render("You've Paused !!", True, (255, 255, 255))
			self.PLANE()
			self.scr.blit(you_pause, ((self.size[0] - you_pause.get_width()) // 2, 80))
			a = self.status.copy()
			a.reverse()
			t = a[1]
			a[1] = a[2]
			a[2] = t
			for x, i in enumerate(a[:3]):
				self.scr.blit(i, ((self.size[0] - i.get_width()) // 2, (self.size[1] - 3 * i.get_height() - 40) // 2 + x * (i.get_height() + 20)))

	def help_mode(self):
		if self.system[2]:
			if not pg.mixer.music.get_busy():
				self.play_background_music('bmg_help')
			your_help = self.font(35).render('Use Your Right Hand To Control', True, (255, 0, 0))
			self.scr.blit(your_help, ((self.size[0] - your_help.get_width()) // 2, 80))
			self.PLANE()
			for x, i in enumerate(self.finger):
				self.scr.blit(i, (20, (self.size[1] - 4 * i.get_height() - 120) // 2 + x * (i.get_height() + 40)))
				blit_text(self.scr, self.help_text[x], self.size[0] - 40, self.size[1], 
						  [50 + i.get_width(), (self.size[1] - 4 * i.get_height() - 120) // 2 + x * (i.get_height() + 40)])

	def play_mode(self):
		if self.system[1]:
			if not pg.mixer.music.get_busy():
				self.play_background_music('bmg_play')
			life = self.font(30).render(f'Life : {self.p[2]}', True, (255, 255,0))
			self.scr.blit(life, (10, self.size[1] - 10 - life.get_height()))
			self.PLANE()
			self.shooting()
			self.ENEMY()
			self.enemy_creat_bullets(500, 1)

	def change_mode(self, n):
		self.system = [False] * 6
		self.system[n] = True
		pg.mixer.music.pause()

	def run(self):
		self.BG()
		self.start_mode()
		self.help_mode()
		self.play_mode()
		self.pause_mode()
		self.win_mode()
		self.lose_mode()