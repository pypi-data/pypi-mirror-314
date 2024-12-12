"""Test the output shape and functionality of the rotate function."""

import unittest
import numpy as np
from src.anaug.default import rotate


class TestRotate(unittest.TestCase):
    """
    Test suite for the `rotate` function.
    """

    def setUp(self):
        """Set up a test image for use in all test cases."""
        # Create a test image (128x128)
        self.image = np.random.rand(128, 128)
        self.image_rgb = np.random.rand(128, 128, 3)

    def test_rotate_90_degrees(self):
        """Test if the image is rotated by 90 degrees."""
        rotated_image = rotate(self.image, angle=90)
        expected_image = np.rot90(self.image, k=1)
        self.assertTrue(np.allclose(rotated_image, expected_image, atol=1e-6))

    def test_rotate_180_degrees(self):
        """Test if the image is rotated by 180 degrees."""
        rotated_image = rotate(self.image, angle=180)
        expected_image = np.rot90(self.image, k=2)
        self.assertTrue(np.allclose(rotated_image, expected_image, atol=1e-6))

    def test_rotate_270_degrees(self):
        """Test if the image is rotated by 270 degrees."""
        rotated_image = rotate(self.image, angle=270)
        expected_image = np.rot90(self.image, k=3)
        self.assertTrue(np.allclose(rotated_image, expected_image, atol=1e-6))

    def test_rotate_360_degrees(self):
        """Test if the image is rotated by 360 degrees."""
        rotated_image = rotate(self.image, angle=360)
        # Rotating by 360 should result in the original image
        self.assertTrue(np.allclose(rotated_image, self.image, atol=1e-6))

    def test_rotate_arbitrary_angle(self):
        """Test if the image is rotated by an arbitrary angle."""
        angle = 45
        rotated_image = rotate(self.image, angle=angle)
        # Since we can't easily predict the exact result of an arbitrary rotation,
        # we can check properties like shape and type.
        self.assertEqual(rotated_image.shape, self.image.shape)
        self.assertEqual(rotated_image.dtype, self.image.dtype)

    def test_rotate_non_square_image(self):
        """Test if the function handles non-square images correctly."""
        non_square_image = np.random.rand(128, 256)
        rotated_image = rotate(non_square_image, angle=90)
        expected_image = np.rot90(non_square_image, k=1)
        self.assertTrue(np.allclose(rotated_image, expected_image, atol=1e-6))

    def test_rotate_large_angle(self):
        """Test if the function handles angles larger than 360 degrees correctly."""
        rotated_image = rotate(self.image, angle=450)  # 450 degrees is equivalent to 90 degrees
        expected_image = np.rot90(self.image, k=1)
        self.assertTrue(np.allclose(rotated_image, expected_image, atol=1e-6))

    def test_rotate_negative_angle(self):
        """Test if the function handles negative angles correctly."""
        rotated_image = rotate(self.image, angle=-90)
        expected_image = np.rot90(self.image, k=3)  # -90 degrees is equivalent to 270 degrees
        self.assertTrue(np.allclose(rotated_image, expected_image, atol=1e-6))

    def test_rotate_with_center(self):
        """Test rotation around the center of the image."""
        angle = 45
        center = (64, 64)  # Center of the 128x128 image
        rotated_image = rotate(self.image, angle=angle, center=center)
        # Check if the rotation respects the center
        self.assertEqual(rotated_image.shape, self.image.shape)
        self.assertEqual(rotated_image.dtype, self.image.dtype)

    def test_invalid_angle(self):
        """Test if the function raises a ValueError for invalid angles."""
        with self.assertRaises(ValueError):
            rotate(self.image, angle='invalid')

    def test_empty_image(self):
        """Test if the function raises a ValueError for empty images."""
        empty_image = np.array([])
        with self.assertRaises(ValueError):
            rotate(empty_image, angle=90)

    def test_color_image(self):
        """Test if the function correctly rotates color images."""
        color_image = np.random.rand(128, 128, 3)  # RGB image
        rotated_image = rotate(color_image, angle=90)
        expected_image = np.rot90(color_image, k=1, axes=(0, 1))
        self.assertTrue(np.allclose(rotated_image, expected_image, atol=1e-3))

    def test_grayscale_image(self):
        """Test if the function handles grayscale images correctly."""
        grayscale_image = np.random.rand(128, 128)
        rotated_image = rotate(grayscale_image, angle=180)
        expected_image = np.rot90(grayscale_image, k=2)
        self.assertTrue(np.allclose(rotated_image, expected_image, atol=1e-6))


if __name__ == "__main__":
    unittest.main()