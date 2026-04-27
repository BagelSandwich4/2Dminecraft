import unittest
from unittest.mock import patch, Mock
from collisions import solid_mask

class Testsolid_mask(unittest.TestCase):
    def setUp(self):

        # create a fake player to mock
        self.player = Mock()
        self.player.pos = Mock()
        self.player.pos.x = 0
        self.player.pos.y = 0

        self.player.vel = Mock()
        self.player.vel.y = 5   # falling downward

        self.player.mask = Mock()
        self.player.image = Mock()
        self.player.image.get_height.return_value = 20
        self.player.grounded = False

        # create fake platform
        self.instance = Mock()
        self.instance.pos = [0,10]
        self.instance.mask = Mock()

    def test_player_becomes_grounded_on_collision(self):

        # Simulate collision
        self.player.mask.overlap.return_value = (0, 0)
        self.instance.mask.overlap.return_value = (0, 5)

        solid_mask(self.instance, self.player)

        self.assertTrue(self.player.grounded)
        self.assertEqual(self.player.vel.y, 0)