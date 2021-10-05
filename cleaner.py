from mc import *
import time 


x, y, z = 116, 62, 508

size = 32

player.setPos(x + size, y + 7 , z)

world.setCuboid(x - size + 1, y - 2, z - size + 1, x + size - 1, y + 20, z + size - 1, 0)
time.sleep(3)
# world.setCuboid(x - size, y - 1, z - size, x + size, y + 5, z + size, 11)
world.setCuboid(x - size, y - 1, z - size, x + size, y + 5, z + size, 3, 2)
# world.setCuboid(x - size + 1, y - 1, z - size + 1, x + size - 1 , y - 5, z + size - 1, 11)
world.setCuboid(x - size + 1, y - 0, z - size + 1, x + size - 1, y + 20, z + size - 1, 0)
# world.setCuboid(x - size, y - 1, z - size, x + size, y + 5, z + size, 3, 2)

player.setPos(x + 1, y, z)
