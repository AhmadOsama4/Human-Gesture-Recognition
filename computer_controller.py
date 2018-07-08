import pyautogui

class ComputerController:
	def __init__(self, controlWindowWidth = 64, controlWindowHeight = 64):
		self.screenWidth, self.screenHeight = pyautogui.size()
		#opencv's window
		self.controlWindowWidth = controlWindowWidth
		self.controlWindowHeight = controlWindowHeight

	def doubleClick(self):
		pyautogui.doubleClick()

	def leftClick(self):
		pyautogui.click(button = 'left')

	def rightClick(self):
		pyautogui.click(button = 'right')

	def moveCursor(self, dx, dy, scale_x = 4, scale_y = 4):
		# scale can be calculated from screen resolution and opencv's window resolution
		curMouseX, curMouseY = pyautogui.position()
		dx = dx * scale_x
		dy = dy * scale_y

		nextMouseX = curMouseY + dx
		nextMouseY = curMouseY + dy

		if nextMouseX < 0 or nextMouseX >= self.screenWidth or nextMouseY < 0 or nextMouseY >= self.screenHeight:
			print('New position is outside the screen size, move values are modified')
			nextMouseX = max(nextMouseX, 0)
			nextMouseX = min(nextMouseX, self.screenWidth - 1)
			nextMouseY = max(nextMouseY, 0)
			nextMouseY = min(nextMouseY, self.screenHeight - 1)

		pyautogui.moveRel(nextMouseX, nextMouseY)

	def moveCursorToCenter(self):
		pyautogui.moveTo(self.screenWidth / 2, self.screenHeight / 2)
		print(self.screenWidth, self.screenHeight)

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