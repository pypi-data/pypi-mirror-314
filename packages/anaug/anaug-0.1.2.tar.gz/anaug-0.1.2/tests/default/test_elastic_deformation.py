# tests/default/test_elastic_deformation.py

import unittest
import numpy as np
from src.anaug.default import elastic_deformation


class TestElasticDeformation(unittest.TestCase):
    """
    Test suite for the `elastic_deformation` function.
    """

    def setUp(self):
        """Set up test images for use in all test cases."""
        # Create a test grayscale image (128x128)
        self.gray_image = np.random.rand(128, 128).astype(np.float32)

        # Create a test color image (128x128x3)
        self.color_image = np.random.rand(128, 128, 3).astype(np.float32)

        # Create a test 3D image (64x64x64)
        self.three_d_image = np.random.rand(64, 64, 64).astype(np.float32)

    def test_output_shape_2d(self):
        """Test if the output shape matches the input shape for 2D images."""
        deformed = elastic_deformation(self.gray_image, alpha=34, sigma=4, random_state=42)
        self.assertEqual(self.gray_image.shape, deformed.shape)

    def test_output_shape_3d(self):
        """Test if the output shape matches the input shape for 3D images."""
        deformed = elastic_deformation(self.three_d_image, alpha=34, sigma=4, random_state=42)
        self.assertEqual(self.three_d_image.shape, deformed.shape)

    def test_deformation_effect_2d(self):
        """Test if elastic deformation alters the 2D image."""
        deformed = elastic_deformation(self.gray_image, alpha=34, sigma=4, random_state=42)
        self.assertFalse(np.array_equal(self.gray_image, deformed))
        # Check statistical differences
        self.assertAlmostEqual(self.gray_image.mean(), deformed.mean(), delta=0.1)
        self.assertAlmostEqual(self.gray_image.std(), deformed.std(), delta=0.1)

    def test_deformation_effect_3d(self):
        """Test if elastic deformation alters the 3D image."""
        # Reduce alpha to prevent excessive deformation
        deformed = elastic_deformation(self.three_d_image, alpha=10, sigma=4, random_state=42)
        self.assertFalse(np.array_equal(self.three_d_image, deformed))
        # Check statistical differences with a reasonable delta
        self.assertAlmostEqual(self.three_d_image.mean(), deformed.mean(), delta=0.1)
        self.assertAlmostEqual(self.three_d_image.std(), deformed.std(), delta=0.2)  # Increased delta

    def test_invalid_alpha(self):
        """Test if elastic deformation handles invalid alpha values correctly."""
        with self.assertRaises(ValueError):
            elastic_deformation(self.gray_image, alpha=-10, sigma=4)
        with self.assertRaises(ValueError):
            elastic_deformation(self.gray_image, alpha=0, sigma=4)

    def test_invalid_sigma(self):
        """Test if elastic deformation handles invalid sigma values correctly."""
        with self.assertRaises(ValueError):
            elastic_deformation(self.gray_image, alpha=34, sigma=-4)
        with self.assertRaises(ValueError):
            elastic_deformation(self.gray_image, alpha=34, sigma=0)

    def test_invalid_image_dimensions(self):
        """Test if elastic deformation handles invalid image dimensions correctly."""
        # 1D image
        one_d_image = np.random.rand(128).astype(np.float32)
        with self.assertRaises(ValueError):
            elastic_deformation(one_d_image, alpha=34, sigma=4)

        # 4D image
        four_d_image = np.random.rand(64, 64, 64, 3).astype(np.float32)
        with self.assertRaises(ValueError):
            elastic_deformation(four_d_image, alpha=34, sigma=4)

    def test_non_numpy_input(self):
        """Test if elastic deformation handles non-NumPy array inputs correctly."""
        non_numpy_input = [[1, 2], [3, 4]]
        with self.assertRaises(TypeError):
            elastic_deformation(non_numpy_input, alpha=34, sigma=4)

    def test_random_state_reproducibility(self):
        """Test if elastic deformation produces the same output with the same random state."""
        deformed1 = elastic_deformation(self.gray_image, alpha=34, sigma=4, random_state=42)
        deformed2 = elastic_deformation(self.gray_image, alpha=34, sigma=4, random_state=42)
        self.assertTrue(np.array_equal(deformed1, deformed2))

    def test_random_state_variability(self):
        """Test if elastic deformation produces different outputs with different random states."""
        deformed1 = elastic_deformation(self.gray_image, alpha=34, sigma=4, random_state=42)
        deformed2 = elastic_deformation(self.gray_image, alpha=34, sigma=4, random_state=43)
        self.assertFalse(np.array_equal(deformed1, deformed2))

    def test_dtype_preservation(self):
        """Test if elastic deformation preserves the dtype of the input image."""
        deformed_gray = elastic_deformation(self.gray_image, alpha=34, sigma=4, random_state=42)
        deformed_color = elastic_deformation(self.color_image, alpha=34, sigma=4, random_state=42)
        deformed_3d = elastic_deformation(self.three_d_image, alpha=10, sigma=4, random_state=42)
        self.assertEqual(self.gray_image.dtype, deformed_gray.dtype)
        self.assertEqual(self.color_image.dtype, deformed_color.dtype)
        self.assertEqual(self.three_d_image.dtype, deformed_3d.dtype)


if __name__ == "__main__":
    unittest.main()