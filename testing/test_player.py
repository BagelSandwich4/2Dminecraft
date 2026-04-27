import unittest
from unittest.mock import patch, Mock
from controller import Controller
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from collections import defaultdict


class TestController(unittest.TestCase):
    """   
    Unit tests for the Controller class, using mocked Pygame functions to verify
    input handling and image changes without loading external assets.

    Inputs:
        mocked state or interactions you provide

    Outputs:
        changes in object state or return values you assert on
    """

    # replace real functions (temporarily) in order to run a simulation
    @patch("pygame.mask.from_surface")
    @patch("pygame.transform.scale")
    @patch("pygame.image.load")
    def setUp(self, mock_load, mock_scale, mock_mask):
        """   
        Set up a fresh Controller instance before each test.

        This method mocks Pygame functions that depend on external resources
        (image loading, surface scaling, and mask creation) to prevent filesystem
        access and graphical dependencies during testing. A new Controller is then
        initialized with a consistent starting state to ensure tests are isolated
        and repeatable.
        """
        fake_surface = Mock()
        fake_mask = Mock()

        mock_load.return_value.convert_alpha.return_value = fake_surface
        mock_scale.return_value = fake_surface
        mock_mask.return_value = fake_mask

        self.controller = Controller((10, 10))

    # replaces pygame.key.get_pressed with a mock. allows control over what key gets pressed in a test
    # Ex: make get_pressed() return whatever key presses you want and test how your code reacts
    @patch("pygame.key.get_pressed")
    def test_change_image_left(self, mock_get_pressed):
        '''  
        Verify that the Controller updates the active image to the left-facing image
        when the 'a' key is pressed.
        '''

        # Arrange
        fake_keys = defaultdict(bool)
        fake_keys[K_LEFT] = True
        mock_get_pressed.return_value = fake_keys

        # Act
        self.controller.change_image()

        # Assert
        self.assertEqual(self.controller.image, self.controller.imageleft)

    @patch("pygame.key.get_pressed")
    def test_change_image_right(self, mock_get_pressed):
        '''
        Verify that the Controller updates the active image to the right-facing image
        when the 'd' key is pressed.
        '''

        # Arrange
        fake_keys = defaultdict(bool)
        fake_keys[K_RIGHT] = True
        mock_get_pressed.return_value = fake_keys

        # Act
        self.controller.change_image()

        # Assert
        self.assertEqual(self.controller.image, self.controller.imageright)


if __name__ == "__main__":
    unittest.main()
