import cv2
from handTracker import *
from space import *

def main():
	webcam = cv2.VideoCapture(0)
	detector = handTracker()
	game = Game()
	while True:
		_ , img = webcam.read()
            
		detector.handsFinder(img)
		lmList = detector.positionFinder(img)

		try:
			game.run()
			if lmList != []:
				fingers = detector.fingersUp(lmList)
				if fingers == [0, 1, 0, 0, 0]:
					if game.system[4] == False and game.system[5] == False:
						game.change_mode(1)
					else:
						game = Game()
						game.run()
				elif fingers == [0, 0, 0, 0, 1]:
					pg.quit()
				elif fingers == [1, 0, 0, 0, 0]:
					game.change_mode(0)
				elif fingers == [0, 1, 1, 1, 0]:
					game.change_mode(2)
				elif fingers == [0, 0, 0, 0, 0]:
					game.change_mode(3)
				if fingers.count(1) >= 3:
					game.go_by_motion([lmList[0][1], lmList[0][2]])
				if fingers == [1, 1, 0, 0, 1]:
					game.creat_a_bullet(speed = 50)
				if game.enemyP == [False, 0, 6] * 5:
					game.change_mode(4)
					game.event_sound('bmg_win')
				if game.p[2] == 0:
					game.change_mode(5)
					game.event_sound('bmg_lose')

			pg.display.update()
		except Exception as bug:
			print(bug)

		cv2.imshow("Play Space Shooting Game By AI", img)
		cv2.waitKey(1)

		# Tắt chương trình
		if not cv2.getWindowProperty('Play Space Shooting Game By AI', cv2.WND_PROP_VISIBLE):
			break

if __name__ == "__main__":
	main()