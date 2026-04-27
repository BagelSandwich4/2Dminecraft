import unittest
from unittest.mock import patch, Mock
from health_bar import Health_Bar


class TestHealthBar(unittest.TestCase):
    '''
    Unit tests for the HealthBar class.
    
    Verifies that health-related logic behaves correctly, specifically that taking 
    damage reduces the health points as expected. Pygame image-loading and surface-scaling 
    functionality is mocked so tests can run.
    '''

    @patch("pygame.transform.scale")
    @patch("pygame.image.load")
    def test_damage_lowers_hp(self, mock_load, mock_scale):
        '''
        Verify that calling the damage method correctly decreases health points.

        This test applies a fixed amount of damage to a Health_Bar instance and
        verifies that the hp value is reduced by the expected amount.
        '''

        # Fake surface that safely supports convert_alpha
        fake_surface = Mock()
        fake_surface.convert_alpha.return_value = fake_surface
        mock_load.return_value = fake_surface
        mock_scale.return_value = fake_surface

        bar = Health_Bar((0, 0), 10)
        bar.damage(2)

        self.assertEqual(bar.hp, 8)


if __name__ == "__main__":
    unittest.main()