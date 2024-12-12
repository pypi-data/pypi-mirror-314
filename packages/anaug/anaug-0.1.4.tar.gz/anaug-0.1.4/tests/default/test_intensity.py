import unittest
import numpy as np
from src.anaug.default import intensity


class TestIntensityScaling(unittest.TestCase):
    """
    Test suite for the `intensity` function.
    """

    def setUp(self):
        """
        Set up test images for use in all test cases.
        """
        # Create a test grayscale image (128x128) with values between 0 and 1
        self.gray_image_float = np.random.rand(128, 128).astype(np.float32)

        # Create a test grayscale image (128x128) with values between 0 and 255
        self.gray_image_uint8 = np.random.randint(0, 256, (128, 128), dtype=np.uint8)

        # Create a test color image (128x128x3) with values between 0 and 1
        self.color_image_float = np.random.rand(128, 128, 3).astype(np.float32)

        # Create a test color image (128x128x3) with values between 0 and 255
        self.color_image_uint8 = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)

        # Create a minimal image (1x1)
        self.minimal_image = np.array([[128]], dtype=np.uint8)

        # Create a uniform image (all pixels have the same intensity)
        self.uniform_image_uint8 = np.full((128, 128), 128, dtype=np.uint8)
        self.uniform_image_float = np.full((128, 128, 3), 0.5, dtype=np.float32)

    def test_output_shape_grayscale_float(self):
        """
        Test if the output shape matches the input shape for 2D grayscale float images.
        """
        scaled_image = intensity(
            self.gray_image_float, brightness_factor=1.2, contrast_factor=1.2
        )
        self.assertEqual(self.gray_image_float.shape, scaled_image.shape)
        self.assertEqual(scaled_image.dtype, self.gray_image_float.dtype)

    def test_output_shape_grayscale_uint8(self):
        """
        Test if the output shape matches the input shape for 2D grayscale uint8 images.
        """
        scaled_image = intensity(
            self.gray_image_uint8, brightness_factor=1.2, contrast_factor=1.2
        )
        self.assertEqual(self.gray_image_uint8.shape, scaled_image.shape)
        self.assertEqual(scaled_image.dtype, self.gray_image_uint8.dtype)

    def test_output_shape_color_float(self):
        """
        Test if the output shape matches the input shape for 3D color float images.
        """
        scaled_image = intensity(
            self.color_image_float, brightness_factor=1.2, contrast_factor=1.2
        )
        self.assertEqual(self.color_image_float.shape, scaled_image.shape)
        self.assertEqual(scaled_image.dtype, self.color_image_float.dtype)

    def test_output_shape_color_uint8(self):
        """
        Test if the output shape matches the input shape for 3D color uint8 images.
        """
        scaled_image = intensity(
            self.color_image_uint8, brightness_factor=1.2, contrast_factor=1.2
        )
        self.assertEqual(self.color_image_uint8.shape, scaled_image.shape)
        self.assertEqual(scaled_image.dtype, self.color_image_uint8.dtype)

    def test_brightness_increase_grayscale_float(self):
        """
        Test if increasing brightness on a grayscale float image works correctly.
        """
        scaled_image = intensity(
            self.gray_image_float, brightness_factor=1.5, contrast_factor=1.0
        )
        # Since brightness_factor >1, the mean intensity should increase
        original_mean = np.mean(self.gray_image_float)
        scaled_mean = np.mean(scaled_image)
        self.assertGreater(scaled_mean, original_mean)

    def test_brightness_decrease_grayscale_uint8(self):
        """
        Test if decreasing brightness on a grayscale uint8 image works correctly.
        """
        scaled_image = intensity(
            self.gray_image_uint8, brightness_factor=0.5, contrast_factor=1.0
        )
        # Since brightness_factor <1, the mean intensity should decrease
        original_mean = np.mean(self.gray_image_uint8)
        scaled_mean = np.mean(scaled_image)
        self.assertLess(scaled_mean, original_mean)

    def test_contrast_increase_color_float(self):
        """
        Test if increasing contrast on a color float image works correctly.
        """
        scaled_image = intensity(
            self.color_image_float, brightness_factor=1.0, contrast_factor=1.5
        )
        # Contrast increase should lead to higher standard deviation
        original_std = np.std(self.color_image_float)
        scaled_std = np.std(scaled_image)
        self.assertGreater(scaled_std, original_std)

    def test_contrast_decrease_color_uint8(self):
        """
        Test if decreasing contrast on a color uint8 image works correctly.
        """
        scaled_image = intensity(
            self.color_image_uint8, brightness_factor=1.0, contrast_factor=0.5
        )
        # Contrast decrease should lead to lower standard deviation
        original_std = np.std(self.color_image_uint8)
        scaled_std = np.std(scaled_image)
        self.assertLess(scaled_std, original_std)

    def test_brightness_and_contrast_grayscale_float(self):
        """
        Test simultaneous adjustment of brightness and contrast on a grayscale float image.
        Ensures that brightness increases and contrast decreases the standard deviation.
        """
        brightness_factor = 0.8  # Decrease brightness
        contrast_factor = 0.8    # Decrease contrast
        scaled_image = intensity(
            self.gray_image_float, brightness_factor=brightness_factor, contrast_factor=contrast_factor
        )
        
        # Calculate means and standard deviations
        original_mean = np.mean(self.gray_image_float)
        scaled_mean = np.mean(scaled_image)
        original_std = np.std(self.gray_image_float)
        scaled_std = np.std(scaled_image)
        
        # Brightness Decrease: Mean should decrease
        self.assertLess(scaled_mean, original_mean)
        
        # Contrast Decrease: Standard deviation should decrease
        self.assertLess(scaled_std, original_std * brightness_factor)
        
        # Alternatively, considering the multiplicative effect:
        # std_contrast = brightness_factor * contrast_factor * original_std
        expected_std = brightness_factor * contrast_factor * original_std
        self.assertAlmostEqual(scaled_std, expected_std, delta=0.05 * original_std)

    def test_minimal_image_uint8(self):
        """
        Test intensity adjustment on a minimal image (1x1) with uint8 data type.
        """
        scaled_image = intensity(
            self.minimal_image, brightness_factor=1.5, contrast_factor=1.5
        )
        expected_value = self.minimal_image[0, 0] * 1.5  # Brightness
        expected_value = 1.5 * (expected_value - expected_value) + expected_value  # Contrast
        expected_value = np.clip(expected_value, 0, 255)
        self.assertEqual(scaled_image[0, 0], expected_value)
        self.assertEqual(scaled_image.dtype, self.minimal_image.dtype)

    def test_uniform_image_uint8_brightness(self):
        """
        Test brightness adjustment on a uniform uint8 image.
        """
        scaled_image = intensity(
            self.uniform_image_uint8, brightness_factor=1.2, contrast_factor=1.0
        )
        expected = np.clip(self.uniform_image_uint8 * 1.2, 0, 255).astype(np.uint8)
        np.testing.assert_array_equal(scaled_image, expected)

    def test_uniform_image_float_contrast(self):
        """
        Test contrast adjustment on a uniform float image.
        """
        scaled_image = intensity(
            self.uniform_image_float, brightness_factor=1.0, contrast_factor=1.5
        )
        # Since the image is uniform, contrast adjustment should have no effect
        np.testing.assert_array_equal(scaled_image, self.uniform_image_float)

    def test_invalid_image_type(self):
        """
        Test if the function raises a TypeError for non-NumPy array inputs.
        """
        with self.assertRaises(TypeError):
            intensity([[1, 2], [3, 4]], brightness_factor=1.2, contrast_factor=1.2)

    def test_invalid_image_dimensions(self):
        """
        Test if the function raises a ValueError for images with invalid dimensions.
        """
        # 1D image
        one_d_image = np.array([1, 2, 3, 4])
        with self.assertRaises(ValueError):
            intensity(one_d_image, brightness_factor=1.2, contrast_factor=1.2)

        # 4D image
        four_d_image = np.random.rand(64, 64, 64, 3).astype(np.float32)
        with self.assertRaises(ValueError):
            intensity(four_d_image, brightness_factor=1.2, contrast_factor=1.2)

    def test_invalid_brightness_factor_type(self):
        """
        Test if the function raises a TypeError for non-float brightness_factor.
        """
        with self.assertRaises(TypeError):
            intensity(self.gray_image_float, brightness_factor='high', contrast_factor=1.2)

    def test_invalid_contrast_factor_type(self):
        """
        Test if the function raises a TypeError for non-float contrast_factor.
        """
        with self.assertRaises(TypeError):
            intensity(self.gray_image_float, brightness_factor=1.2, contrast_factor='high')

    def test_negative_brightness_factor(self):
        """
        Test if the function raises a ValueError for negative brightness_factor.
        """
        with self.assertRaises(ValueError):
            intensity(self.gray_image_float, brightness_factor=-1.0, contrast_factor=1.2)

    def test_zero_contrast_factor(self):
        """
        Test if the function raises a ValueError for zero contrast_factor.
        """
        with self.assertRaises(ValueError):
            intensity(self.gray_image_float, brightness_factor=1.2, contrast_factor=0.0)


if __name__ == "__main__":
    unittest.main()