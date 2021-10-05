import random 
import time
from mc import *
from print import post
from cleaner import *


class Move:
	def __init__(self, forward, left, right, snake): 
		self.forward = forward
		self.left = left 
		self.right = right
		self.snake = snake

	def __repr__(self):
		return f'Move(forward_{self.forward}, left_{self.left}, right_{self.right}, {self.snake})'


class Coordinates:
	def __init__(self, x, y, z): 
		self.x = x 
		self.y = y 
		self.z = z

	def __repr__(self):
		return f'Coords({self.x}, {self.y}, {self.z})'

	def get_values(self):
		return self.x, self.y, self.z 

	def __eq__(self, new):
		return self.x == new.x and self.y == new.y and self.z == new.z


class Snake:
	head_list = list(range(16, -1, -1))
	control_list = list()
	

	def __init__(self, x, y, z, control_block=False):
		self.x = x
		self.y = y 
		self.z = z		
		self.pos = [Coordinates(x, y, z)]
		self.length = 3
		self.head = self.init_head() 
		self.body = self.init_body()
		self.spawn(self.head)
		self.point1 = [38, 37]
		self.point2 = [40,]
		self.point3 = [39, 175]
		self.x_dir = 1
		self.z_dir = 0
		# self.grow_3 = 1
		# self.take = 1
		self.control_start = False
		self.score = 0
		if control_block == True:
			self.control = self.control_init()

	def random_step(self, step):
		try: 
			range(step)
		except:
			post("needs to be a number")
			return
		for i in range(step):
			random_num = random.randint(1, 6)
			if random_num == 1:
				self.turn_left()
			elif random_num == 2:
				self.turn_right()
			else:
				self.move(1)

	def __repr__(self):
		return f'Snake({self.x}, {self.y}, {self.z}, head: {list(self.head)[1]})'

	def pop_coordinates(self): 
		return self.pos.pop().get_values()	

	def add_coordinates(self, x, y, z): 
		if Coordinates(x, y, z) not in self.pos:
			return self.pos.insert(0, Coordinates(x, y, z))

	def print_coordinates(self):  
		print(self.pos)

	def init_body(self):		
		a = dict()
		for i in range(16):
			a[blocks.WOOL.withData(i)] = 235 + i
		return a[self.head]

	def is_food(self, block):
		# points_1 = (38, 37)
		# points_2 = (40,)
		# points_3 = (39, 175)
		if block in self.point1:
			# self.score += 1
			return 1
		elif block in self.point2:
			return 2
		elif block in self.point3:
			return 3
		else:
			return 0

	def init_head(self):
		return blocks.WOOL.withData(self.head_list.pop())

	def info(self):
		post('snake {} {} {}'.format(self.x, self.y, self.z))

	def spawn(self, colour):
		try:
			world.setBlock(self.x, self.y, self.z, colour)
		except:
			post("must be number not str")
			return
	
	def start_block_control(self):
		if self.control_start == True:
			post('control was started')
			return
		else:
			self.control_start = True
		while True:  
			for control in self.control_list:
				block_forward_id = world.getBlock(control.forward.x, control.forward.y, control.forward.z)
				block_left_id =  world.getBlock(control.left.x, control.left.y, control.left.z)
				block_right_id =  world.getBlock(control.right.x, control.right.y, control.right.z)
				if block_forward_id == 0:
					control.snake.move(1)
					world.setBlock(control.forward.x, control.forward.y, control.forward.z, control.snake.head)
				if block_left_id == 0:
					control.snake.turn_left()
					world.setBlock(control.left.x, control.left.y, control.left.z, control.snake.body)
					control.snake.move(1)
				if block_right_id == 0:
					control.snake.turn_right()
					world.setBlock(control.right.x, control.right.y, control.right.z, control.snake.body)
					control.snake.move(1)
	
	def control_init(self):
		block_forward = Coordinates(self.x - 2, self.y, self.z)
		block_left = Coordinates(self.x - 3, self.y, self.z - 1)
		block_right = Coordinates(self.x - 3, self.y, self.z + 1)
		world.setBlock(block_forward.x, block_forward.y, block_forward.z, self.head)
		world.setBlock(block_left.x, block_left.y, block_left.z, self.body)
		world.setBlock(block_right.x, block_right.y, block_right.z, self.body)
		control_block = Move(block_forward, block_left, block_right, self)
		self.control_list.append(control_block)
		return control_block

	def grown_up(self, count):
		self.length += count
		if count == 1:
			self.score += 100
		elif count == 2:
			self.score += 300
		elif count == 3:
			self.score += 500

	def show_score(self):
		post(f"your current score is {self.score} ")

	def move(self, step): 
		try:
			int(step)
		except:
			post('step has to be a number or function move')
			return 
		for i in range(step):
			next_block  = world.getBlock(self.x + self.x_dir, self.y, self.z + self.z_dir)
			# post(next_block)
			self.spawn(self.body)
			if next_block == 0 or self.is_food(next_block):				
				self.x += self.x_dir
				self.z += self.z_dir 
			else:
				return 0
			# check for current block
			count = self.is_food(next_block)
			if count:
				# score 
				self.grown_up(count)		
			self.spawn(self.head)
			self.add_coordinates(self.x, self.y, self.z)
			if len(self.pos) > self.length:
				x, y, z = self.pop_coordinates()
				world.setBlock(x, y, z, 0)
		return step

	def turn_left(self):
		if self.x_dir == 1 and self.z_dir == 0:
			self.x_dir = 0
			self.z_dir = -1
		elif self.x_dir == 0 and self.z_dir == -1:
			self.x_dir = -1
			self.z_dir = 0
		elif self.x_dir == -1 and self.z_dir == 0:
			self.x_dir = 0
			self.z_dir = 1
		else:
			self.x_dir = 1
			self.z_dir = 0
		
	def turn_right(self):
		if self.x_dir == 1 and self.z_dir == 0:
			self.x_dir = 0
			self.z_dir = 1
		elif self.x_dir == 0 and self.z_dir == 1:
			self.x_dir = -1
			self.z_dir = 0
		elif self.x_dir == -1 and self.z_dir == 0:
			self.x_dir = 0
			self.z_dir = -1
		else:
			self.x_dir = 1
			self.z_dir = 0	

	def get_colour_body(self): 
		body_dict = {
			blocks.WOOL.withData(0): 235,
			blocks.WOOL.withData(1): 236,
		}

	def start_game(self, spawn_flower=True):
		# todo add list of food from snake object
		if spawn_flower == True:
			post('flowers spawned')
			self.spawn_food()
		if self.control_start == True:
			post('control was started')
			return
		else:
			self.control_start = True
		if len(self.control_list) == 1:
			post("game started")
			step_count = 0
			while True:
				time.sleep(1)
				make_step = self.move(1)
				if make_step == 0:
					post(f'game over. your final score {self.score}')
					break 
				for control in self.control_list:
					block_forward_id = world.getBlock(control.forward.x, control.forward.y, control.forward.z)
					block_left_id =  world.getBlock(control.left.x, control.left.y, control.left.z)
					block_right_id =  world.getBlock(control.right.x, control.right.y, control.right.z)
					if block_left_id == 0:
						control.snake.turn_left()
						world.setBlock(control.left.x, control.left.y, control.left.z, control.snake.body)						
					if block_right_id == 0:
						control.snake.turn_right()
						world.setBlock(control.right.x, control.right.y, control.right.z, control.snake.body)
					if make_step == 1:
						step_count += 1
					if step_count == 10:
						post(f'your score {self.score}')

	def get_size_map(self, x, y, z):
		
		y = y + 1
		for i in range(35):
			is_air = world.getBlock(x + i, y, z)			
			max_x = x + i
			if is_air != 0:
				break			

		for i in range(35):
			is_air = world.getBlock(x, y, z + i)		
			max_z = z + i
			if is_air != 0:		
				break			

		for i in range(35):
			is_air = world.getBlock(x - i, y, z)			
			min_x = x - i
			if is_air != 0:
				break		

		for i in range(35):
			is_air = world.getBlock(x, y, z - i)				
			min_z = z - i
			if is_air != 0:
				break
		
		out_dict = {
			"max_x" : max_x,
			"max_z" : max_z,
			"min_x" : min_x,
			"min_z" : min_z
		}
		return out_dict
	
	def spawn_food(self):
		a = snake.get_size_map(self.x, self.y, self.z)
		max_x = a['max_x']
		max_z = a['max_z']
		min_x = a['min_x']
		min_z = a['min_z']
		self.food_on_map(max_x, max_z, min_x, min_z, self.y)

	def food_on_map(self, max_x, max_z, min_x, min_z, y):
		post(max_x)
		# post(self.point1)
		a = [0] * 8
		b = self.point1 + self.point2 + self.point3 + a
		# post(b)
		for x in range(min_x + 1, max_x):
			for z in range(min_z + 1, max_z):
				world.setBlock(x, y, z, random.choice(b))
				# post(str([x, y, z]))

# post('done')
snake = Snake(116, 62, 510, True)
post(snake.point1)
snake.start_game()
# snake.start_game(spawn_flower=False)


print(dir(snake))

def spawn_food(spawn_flower=True):
	post(f'game started {spawn_flower}')
	if spawn_flower == True:
		post('start_game')
		post("flowers spawned")
	# elif

spawn_food(spawn_flower=False)