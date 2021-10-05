import mcpi.minecraft as minecraft
import mcpi.block as blocks
import mcpi.entity as entity
import mcpi.entity as creatures
import config
from mcpi.connection import RequestError


class ConnectPlayer:
    def __init__(self, minecraft_obj, nick):
        self.mc = minecraft_obj
        self.player_id = minecraft_obj.getPlayerEntityId(nick)

    def getDirection(self):
        return self.mc.entity.getDirection(self.player_id)

    def getPitch(self):
        return self.mc.entity.getPitch(self.player_id)

    def getTilePos(self):
        return self.mc.entity.getTilePos(self.player_id)

    def getPos(self):
        return self.mc.entity.getPos(self.player_id)

    def getAccPos(self):
        return self.mc.entity.getPos(self.player_id)

    def getRotation(self):
        return self.mc.entity.getRotation(self.player_id)

    def getTilePos(self):
        return self.mc.entity.getTilePos(self.player_id)

    def setPos(self, x, y, z):
        return self.mc.entity.setPos(self.player_id, x, y, z)

    def setTilePos(self, x, y, z):
        return self.mc.entity.setTilePos(self.player_id, x, y, z)


class World:
    def __init__(self, minecraft_obj):
        self.mc = minecraft_obj

    def camera(self, *args):
        return self.mc.camera(args)

    def create(self, *args):
        return self.mc.create(args)

    def entity(self, *args):
        return self.mc.entity(args)

    def events(self, *args):
        return self.mc.events(args)

    def getBlock(self, *args):
        return self.mc.getBlock(args)

    def getBlockWithData(self, *args):
        return self.mc.getBlockWithData(args)

    def getBlocks(self, *args):
        return self.mc.getBlocks(args)

    def getEntities(self, *args):
        return self.mc.getEntities(args)

    def getEntityTypes(self, *args):
        return self.mc.getEntityTypes(args)

    def getHeight(self, *args):
        return self.mc.getHeight(args)

    def postToChat(self, *args):
        return self.mc.postToChat(args)

    def removeEntities(self, *args):
        return self.mc.removeEntities(args)

    def removeEntity(self, *args):
        return self.mc.removeEntity()

    def setBlock(self, x, y, z, blockType, *args):
        return self.mc.setBlock(x, y, z, blockType, args)

    def setBlocks(self, x0, y0, z0, x, y, z, blockType, *args):
        return self.mc.setBlocks(x0, y0, z0, x, y, z, blockType, args)

    def setCuboid(self, x0, y0, z0, x, y, z, blockType, *args):
        return self.mc.setBlocks(x0, y0, z0, x, y, z, blockType, args)

    def setSign(self, *args):
        return self.mc.setSign(args)

    def setting(self, *args):
        return self.mc.settings(args)

    def spawnEntity(self, *args):
        return self.mc.spawnEntity(args)

    def spawnCreature(self, x, y, z, creature_id, *args):
        return self.mc.spawnEntity(x, y, z, creature_id, args)

    def buildColumn(self, x, y, z, h, block_type):
        return self.mc.setBlocks(x, y, z, x, y + h - 1, z, block_type)

    def _buildDoor(self, x, y, z, direction=0):
        self.mc.setBlock(x, y, z, 64, direction)
        self.mc.setBlock(x, y + 1, z, 64, 8)

    def buildHome(self, x, y, z, width=5, length=5, height=5, block_type=5, direction=0):
        """ build home on x, y, z with width, length, height from block_type """

        if length < 3 or width < 3 or height < 3:
            raise ValueError

        if type(block_type) == 'mcpi.block.Block':
            block_type = list(block_type)[0]

        x_start = x - width // 2
        y_start = y - 1
        z_start = z - length // 2
        x_end = x_start + width
        y_end = y_start + height
        z_end = z_start + length

        # make box
        self.mc.setBlocks(x_start, y_start, z_start, x_end - 1, y_end - 1,
                          z_end - 1, block_type)

        if block_type != 0:
            # make glasses
            self.mc.setBlocks( x_start + 1, y_start + 2, z_start, x_end - 2,
                              y_start + 2, z_end - 1, 20)
            self.mc.setBlocks(x_start, y_start + 2, z_start + 1, x_end - 1 ,
                              y_start + 2, z_end - 2, 20)

            # make air in box
            self.mc.setBlocks(x_start + 1, y_start + 1, z_start + 1, x_end - 2,
                              y_end - 2, z_end - 2, 0)

            # make floor
            self.mc.setBlocks(x_start + 1, y_start, z_start + 1, x_end - 2,
                              y_start, z_end - 2, 5)

            # make doors
            flag = 1
            if width <= 7 and (direction == 1 or direction == 3):
                if width % 2 == 1:
                    flag = 0
            if length <= 7 and (direction == 0 or direction == 2):
                if length % 2 == 1:
                    flag = 0
            if direction == 0:
                self._buildDoor(x_start, y_start + 1, z, 7)
                if flag:
                    self._buildDoor(x_start, y_start + 1, z - 1, 0)
            elif direction == 1:
                self._buildDoor(x, y_start + 1, z_start, 1)
                if flag:
                    self._buildDoor(x - 1, y_start + 1, z_start, 4)
            elif direction == 2:
                self._buildDoor(x_end - 1, y_start + 1, z, 2)
                if flag:
                    self._buildDoor(x_end - 1, y_start + 1, z - 1, 5)
            elif direction == 3:
                self._buildDoor(x, y_start + 1, z_end - 1, 6)
                if flag:
                    self._buildDoor(x - 1, y_start + 1, z_end - 1, 3)



mc = minecraft.Minecraft.create(address = config.server)

player = ConnectPlayer(mc, config.nickname)
world = World(mc)
