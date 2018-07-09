import pyautogui
import math

class ComputerController:
	def __init__(self, controlWindowWidth = 64, controlWindowHeight = 64):
		self.screen_width, self.screen_height = pyautogui.size()
		#opencv's window
		self.controlWindowWidth = controlWindowWidth
		self.controlWindowHeight = controlWindowHeight
		self.cur_mouse_x = int(self.screen_width // 2)
		self.cur_mouse_y = int(self.screen_height // 2)
		self.moveCursorToCenter()

	def doubleClick(self):
		pyautogui.doubleClick()

	def leftClick(self):
		pyautogui.click(button = 'left')

	def rightClick(self):
		pyautogui.click(button = 'right')

	def moveCursor(self, dx, dy, scale_x = 5, scale_y = 5):
		dx = dx * scale_x
		dy = dy * scale_y

		next_mouse_x = int(self.screen_width / 2 + dx)
		next_mouse_y = int(self.screen_height / 2 + dy)

		if next_mouse_x < 0:
			next_mouse_x = 0
		if next_mouse_x > self.screen_width:
			next_mouse_x = self.screen_width
		if next_mouse_y < 0:
			next_mouse_y = 0
		if next_mouse_y > self.screen_height:
			next_mouse_y = self.screen_height
		if math.sqrt((next_mouse_x - self.cur_mouse_x) ** 2 + (next_mouse_y - self.cur_mouse_y) ** 2) > 5:
			pyautogui.moveTo(next_mouse_x, next_mouse_y)
			self.cur_mouse_x, self.cur_mouse_y = next_mouse_x, next_mouse_y

	def moveCursorToCenter(self):
		pyautogui.moveTo(self.screen_width / 2, self.screen_height / 2)
		#print(self.screenWidth, self.screenHeight)

	def clickUp(self, count = 1):
		for i in range(count):
			pyautogui.press('up')

	def clickDown(self, count = 1):
		for i in range(count):
			pyautogui.press('down')

	def forward(self):
		pyautogui.hotkey('alt', 'right')

	def backward(self):
		pyautogui.hotkey('alt', 'left')