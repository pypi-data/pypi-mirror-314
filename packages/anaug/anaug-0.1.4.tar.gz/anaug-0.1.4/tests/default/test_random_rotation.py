import unittest
import numpy as np
import cv2
from src.anaug.default import random_rotation

class TestRandomRotation(unittest.TestCase):
    def setUp(self):
        # Create a test grayscale image (128x128) and an RGB image
        self.image_grayscale = np.random.rand(128, 128).astype(np.float32)
        self.image_rgb = np.random.rand(128, 128, 3).astype(np.float32)

    def test_output_shape(self):
        """Check if the output shape matches the input shape for grayscale image."""
        rotated_image = random_rotation(self.image_grayscale, angle_range=(-30, 30))
        self.assertEqual(self.image_grayscale.shape, rotated_image.shape)

    def test_output_shape_rgb(self):
        """Check if the output shape matches the input shape for RGB image."""
        rotated_image = random_rotation(self.image_rgb, angle_range=(-30, 30))
        self.assertEqual(self.image_rgb.shape, rotated_image.shape)

    def test_angle_range_effect(self):
        """Test if different angle ranges produce different results."""
        rotated_image_low = random_rotation(self.image_grayscale, angle_range=(-15, 15))
        rotated_image_high = random_rotation(self.image_grayscale, angle_range=(-90, 90))
        self.assertFalse(np.array_equal(rotated_image_low, rotated_image_high), 
                         "Rotated images for different ranges should not be identical.")

    def test_rotation_at_zero(self):
        """Test rotation with a fixed angle of 0 degrees."""
        rotated_image = random_rotation(self.image_grayscale, angle_range=(0, 0))
        self.assertTrue(np.allclose(rotated_image, self.image_grayscale), 
                        "Rotation at 0 degrees should result in the same image.")

    def test_rotation_full_circle(self):
        """Test rotation with a full circle (360 degrees)."""
        rotated_image = random_rotation(self.image_grayscale, angle_range=(360, 360))
        self.assertTrue(np.allclose(rotated_image, self.image_grayscale), 
                        "Rotation at 360 degrees should result in the same image.")

    def test_invalid_angle_range(self):
        """Test if the function raises a ValueError for invalid angle_range."""
        with self.assertRaises(ValueError):
            random_rotation(self.image_grayscale, angle_range=("invalid", 30))

    def test_center_rotation(self):
        """Test if rotation around a custom center works correctly."""
        center = (64, 64)  # Center of the image
        rotated_image = random_rotation(self.image_grayscale, angle_range=(-45, 45), center=center)
        self.assertEqual(rotated_image.shape, self.image_grayscale.shape)

    def test_border_mode_constant(self):
        """Test rotation with a constant border mode."""
        rotated_image = random_rotation(self.image_grayscale, angle_range=(-30, 30), border_mode=cv2.BORDER_CONSTANT)
        self.assertEqual(rotated_image.shape, self.image_grayscale.shape)

    def test_border_mode_reflect(self):
        """Test rotation with a reflect border mode."""
        rotated_image = random_rotation(self.image_grayscale, angle_range=(-30, 30), border_mode=cv2.BORDER_REFLECT)
        self.assertEqual(rotated_image.shape, self.image_grayscale.shape)

    def test_non_square_image(self):
        """Test rotation for a non-square image."""
        non_square_image = np.random.rand(128, 256).astype(np.float32)
        rotated_image = random_rotation(non_square_image, angle_range=(-45, 45))
        self.assertEqual(non_square_image.shape, rotated_image.shape)

    def test_empty_image(self):
        """Test if the function handles empty images correctly."""
        empty_image = np.array([])
        with self.assertRaises(ValueError):
            random_rotation(empty_image, angle_range=(-30, 30))

if __name__ == "__main__":
    unittest.main()
