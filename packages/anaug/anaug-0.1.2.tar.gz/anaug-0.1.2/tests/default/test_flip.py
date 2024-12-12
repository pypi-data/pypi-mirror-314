import unittest
import numpy as np
from src.anaug.default import flip


class TestFlip(unittest.TestCase):
    """
    Test suite for the `flip` function.
    """

    def setUp(self):
        """Set up test images for use in all test cases."""
        # Create a test grayscale image (128x128)
        self.gray_image = np.random.rand(128, 128)

        # Create a test color image (128x128x3)
        self.color_image = np.random.rand(128, 128, 3)

        # Create a minimal image (1x1)
        self.minimal_image = np.array([[1]])

        # Create images with single rows and columns
        self.single_row_image = np.array([[1, 2, 3, 4, 5]])
        self.single_column_image = np.array([[1], [2], [3], [4], [5]])

    def test_horizontal_flip_grayscale(self):
        """Test if the grayscale image is flipped horizontally."""
        flipped = flip(self.gray_image, axes='horizontal')
        expected = np.fliplr(self.gray_image)
        np.testing.assert_array_equal(flipped, expected)

    def test_vertical_flip_grayscale(self):
        """Test if the grayscale image is flipped vertically."""
        flipped = flip(self.gray_image, axes='vertical')
        expected = np.flipud(self.gray_image)
        np.testing.assert_array_equal(flipped, expected)

    def test_both_flips_grayscale(self):
        """Test if the grayscale image is flipped both horizontally and vertically."""
        flipped = flip(self.gray_image, axes=['horizontal', 'vertical'])
        expected = np.flipud(np.fliplr(self.gray_image))
        np.testing.assert_array_equal(flipped, expected)

    def test_flip_no_flipping_grayscale(self):
        """Test if the grayscale image remains unchanged when no axes are specified."""
        flipped = flip(self.gray_image, axes=[])
        expected = self.gray_image.copy()
        np.testing.assert_array_equal(flipped, expected)

    def test_flip_empty_axes_list_grayscale(self):
        """Test if the grayscale image remains unchanged when an empty list is provided for axes."""
        flipped = flip(self.gray_image, axes=[])
        expected = self.gray_image.copy()
        np.testing.assert_array_equal(flipped, expected)

    def test_invalid_axes_grayscale(self):
        """Test if the function raises an error for invalid axes in grayscale images."""
        with self.assertRaises(ValueError):
            flip(self.gray_image, axes='diagonal')

        with self.assertRaises(ValueError):
            flip(self.gray_image, axes=['horizontal', 'diagonal'])

        with self.assertRaises(TypeError):
            flip(self.gray_image, axes=123)

    def test_horizontal_flip_color(self):
        """Test if the color image is flipped horizontally."""
        flipped = flip(self.color_image, axes='horizontal')
        expected = np.fliplr(self.color_image)
        np.testing.assert_array_equal(flipped, expected)

    def test_vertical_flip_color(self):
        """Test if the color image is flipped vertically."""
        flipped = flip(self.color_image, axes='vertical')
        expected = np.flipud(self.color_image)
        np.testing.assert_array_equal(flipped, expected)

    def test_both_flips_color(self):
        """Test if the color image is flipped both horizontally and vertically."""
        flipped = flip(self.color_image, axes=['horizontal', 'vertical'])
        expected = np.flipud(np.fliplr(self.color_image))
        np.testing.assert_array_equal(flipped, expected)

    def test_flip_empty_axes_list_color(self):
        """Test if the color image remains unchanged when an empty list is provided for axes."""
        flipped = flip(self.color_image, axes=[])
        expected = self.color_image.copy()
        np.testing.assert_array_equal(flipped, expected)

    def test_flip_no_flipping_color(self):
        """Test if the color image remains unchanged when no axes are specified."""
        flipped = flip(self.color_image, axes=[])
        expected = self.color_image.copy()
        np.testing.assert_array_equal(flipped, expected)

    def test_horizontal_flip_minimal(self):
        """Test horizontal flip on a minimal image (1x1)."""
        flipped = flip(self.minimal_image, axes='horizontal')
        expected = np.fliplr(self.minimal_image)
        np.testing.assert_array_equal(flipped, expected)

    def test_vertical_flip_minimal(self):
        """Test vertical flip on a minimal image (1x1)."""
        flipped = flip(self.minimal_image, axes='vertical')
        expected = np.flipud(self.minimal_image)
        np.testing.assert_array_equal(flipped, expected)

    def test_both_flips_minimal(self):
        """Test flipping both horizontally and vertically on a minimal image (1x1)."""
        flipped = flip(self.minimal_image, axes=['horizontal', 'vertical'])
        expected = np.flipud(np.fliplr(self.minimal_image))
        np.testing.assert_array_equal(flipped, expected)

    def test_flip_single_row(self):
        """Test flipping a single-row image horizontally and vertically."""
        # Horizontal flip should reverse the row
        flipped_h = flip(self.single_row_image, axes='horizontal')
        expected_h = np.fliplr(self.single_row_image)
        np.testing.assert_array_equal(flipped_h, expected_h)

        # Vertical flip should have no effect since there's only one row
        flipped_v = flip(self.single_row_image, axes='vertical')
        expected_v = np.flipud(self.single_row_image)
        np.testing.assert_array_equal(flipped_v, expected_v)

    def test_flip_single_column(self):
        """Test flipping a single-column image horizontally and vertically."""
        # Horizontal flip should have no effect since there's only one column
        flipped_h = flip(self.single_column_image, axes='horizontal')
        expected_h = np.fliplr(self.single_column_image)
        np.testing.assert_array_equal(flipped_h, expected_h)

        # Vertical flip should reverse the column
        flipped_v = flip(self.single_column_image, axes='vertical')
        expected_v = np.flipud(self.single_column_image)
        np.testing.assert_array_equal(flipped_v, expected_v)

    def test_flip_invalid_input_type(self):
        """Test if the function raises a TypeError for non-NumPy array inputs."""
        with self.assertRaises(TypeError):
            flip([[1, 2], [3, 4]], axes='horizontal')

    def test_flip_invalid_image_dimensions(self):
        """Test if the function raises a ValueError for images with invalid dimensions."""
        # 1D array
        one_d_image = np.array([1, 2, 3, 4])
        with self.assertRaises(ValueError):
            flip(one_d_image, axes='horizontal')

        # 4D array
        four_d_image = np.random.rand(64, 64, 64, 3)
        with self.assertRaises(ValueError):
            flip(four_d_image, axes='horizontal')

    def test_flip_data_type_preservation_grayscale(self):
        """Test if the data type is preserved after flipping a grayscale image."""
        image = self.gray_image.astype(np.float32)
        flipped = flip(image, axes='horizontal')
        self.assertEqual(flipped.dtype, image.dtype)

    def test_flip_data_type_preservation_color(self):
        """Test if the data type is preserved after flipping a color image."""
        image = self.color_image.astype(np.float64)
        flipped = flip(image, axes='vertical')
        self.assertEqual(flipped.dtype, image.dtype)

    def test_flip_invalid_axes_type(self):
        """Test if the function raises a TypeError when axes list contains non-string elements."""
        with self.assertRaises(TypeError):
            flip(self.gray_image, axes=['horizontal', 123])

    def test_flip_multiple_axes_invalid_combination(self):
        """Test if the function raises a ValueError for invalid combinations of axes."""
        with self.assertRaises(ValueError):
            flip(self.color_image, axes=['horizontal', 'vertical', 'diagonal'])


if __name__ == "__main__":
    unittest.main()