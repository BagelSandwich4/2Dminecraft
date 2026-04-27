import unittest
from unittest.mock import patch, Mock
from collisions import solid_mask

class Testsolid_mask(unittest.TestCase):
    """
    Unit tests for the solid_mask collision function.

    This test suite verifies that when a player collides with a solid instance
    while moving downward, the player's state is updated correctly. In particular,
    it checks that the player becomes grounded and that vertical velocity is reset.

    Mocks are used to simulate player and platform objects so collision behavior
    can be tested without relying on real game entities or Pygame surfaces.
    """

    def setUp(self):
        '''
        Create mock objects in preparation for testing.

        Inputs:
            A mock player with a position, velocity, mask, image, etc to simulate with.
            A mock platform with a position and mask to simulate with.
        
        Outputs:
            No values returned. The test state prepares the output.
        '''

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
        '''
        Assert that the player is both grounded and has zero velocity when in contact
        with the platform. 

        This function simulates a collision between the fake player and platform by 
        mocking mask overlap behavior. Once collided, the player's vertical velocity must 
        reset to zero and their grounded state must be True.
        '''

        # Simulate collision
        self.player.mask.overlap.return_value = (0, 0)
        self.instance.mask.overlap.return_value = (0, 5)

        solid_mask(self.instance, self.player)

        self.assertTrue(self.player.grounded)
        self.assertEqual(self.player.vel.y, 0)