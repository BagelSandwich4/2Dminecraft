import unittest
from unittest.mock import patch, Mock
from player import Player
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from collections import defaultdict


class TestPlayer(unittest.TestCase):

    # replace real functions (temporarily) in order to run a simulation
    @patch("pygame.mask.from_surface")
    @patch("pygame.transform.scale")
    @patch("pygame.image.load")
    def setUp(self, mock_load, mock_scale, mock_mask):
        """
        Class that resets player before each test run.
        Each test restarts with the player at position (10,10).
        Each test also creates a fake/"mock" object for each run in order to guage
        correct and incorrect behaviors; does the image turn?
        """
        fake_surface = Mock()
        fake_mask = Mock()

        mock_load.return_value.convert_alpha.return_value = fake_surface
        mock_scale.return_value = fake_surface
        mock_mask.return_value = fake_mask

        self.player = Player((10, 10))

    # replaces pygame.key.get_pressed with a mock. allows control over what key gets pressed in a test
    # Ex: make get_pressed() return whatever key presses you want and test how your code reacts
    @patch("pygame.key.get_pressed")
    def test_change_image_left(self, mock_get_pressed):

        # Arrange
        fake_keys = defaultdict(bool)
        fake_keys[K_LEFT] = True
        mock_get_pressed.return_value = fake_keys

        # Act
        self.player.change_image()

        # Assert
        self.assertEqual(self.player.image, self.player.imageleft)

    @patch("pygame.key.get_pressed")
    def test_change_image_right(self, mock_get_pressed):

        # Arrange
        fake_keys = defaultdict(bool)
        fake_keys[K_RIGHT] = True
        mock_get_pressed.return_value = fake_keys

        # Act
        self.player.change_image()

        # Assert
        self.assertEqual(self.player.image, self.player.imageright)


if __name__ == "__main__":
    unittest.main()
