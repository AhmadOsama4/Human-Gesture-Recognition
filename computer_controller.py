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

	def moveCursor(self, dx, dy, scale_x = 1, scale_y = 1):
		# scale can be calculated from screen resolution and opencv's window resolution
		cur_mouse_x, cur_mouse_y = pyautogui.position()
		dx = dx * scale_x
		dy = dy * scale_y

		next_mouse_x = int(cur_mouse_x + dx)
		next_mouse_y = cur_mouse_y + dy

		if next_mouse_x < 0:
			dx = -cur_mouse_x
		if next_mouse_x > self.screenWidth:
			dx = self.screenWidth - cur_mouse_x
		if next_mouse_y < 0:
			dy = -cur_mouse_y
		if next_mouse_y > self.screenHeight:
			dx = self.screenHeight - cur_mouse_y

		# if nextMouseX < 0 or nextMouseX >= self.screenWidth or nextMouseY < 0 or nextMouseY >= self.screenHeight:
		# 	print('New position is outside the screen size, move values are modified')
		# 	nextMouseX = max(nextMouseX, 0)
		# 	nextMouseX = min(nextMouseX, self.screenWidth - 1)
		# 	nextMouseY = max(nextMouseY, 0)
		# 	nextMouseY = min(nextMouseY, self.screenHeight - 1)

		pyautogui.moveRel(dx, dy)

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