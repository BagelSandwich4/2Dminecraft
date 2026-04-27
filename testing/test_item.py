import unittest
from unittest.mock import patch, Mock
import pygame
from item import Item

class TestItem(unittest.TestCase):
    '''
    Unit tests for the Item class. 

    
    Verifies Item behavior related to player interaction, specifically ensuring 
    that an item becomes invisible after being successfully picked up. External 
    Pygame functionality such as image loading, surface transformation, and mask 
    creation is mocked so tests can run without accessing the filesystem or requiring a display.

    This test verifies the item state rather than simulating a behavior.

    '''

    def setUp(self):
        '''
        
        Initialize Pygame for Item unit tests.

        Pygame is initialized once per test to ensure that mocked image loading and
        surface-related operations can be performed. No inputs/outputs.

        '''
        pygame.init()

    @patch("pygame.transform.flip")
    @patch("pygame.mask.from_surface")
    @patch("pygame.transform.scale")
    @patch("pygame.image.load")
    def test_item_becomes_invisible_after_pickup(self, mock_load, mock_scale, mock_mask, mock_flip):
        '''
        Verify that an Item becomes invisible after being successfully picked up.

        This test simulates a collision between the item and a player and mocks a
        successful pickup by the hotbar. It asserts that the item's visible state is
        set to False after the pickup occurs.

        '''
        # Create fake image surface
        fake_surface = Mock()
        fake_surface.convert_alpha.return_value = fake_surface

        mock_load.return_value = fake_surface
        mock_scale.return_value = fake_surface
        mock_flip.return_value = fake_surface
        mock_mask.return_value = Mock()

        # Create item
        item = Item(
            image="fake.png",
            position=(0, 0),
            size=(1, 1)
        )

        # Make item visible (required for pickup)
        item.visible = True

        # Mock player
        player = Mock()
        player.pos = Mock()
        player.pos.x = 0
        player.pos.y = 0
        player.mask = Mock()

        # Force overlap to happen
        item.mask.overlap = Mock(return_value=(0, 0))

        # Mock hotbar
        hotbar = Mock()
        hotbar.pick_up_item.return_value = True

        # Run method
        item.pick_up(hotbar, player)

        # Assertions
        self.assertFalse(item.visible)
        hotbar.pick_up_item.assert_called_once()