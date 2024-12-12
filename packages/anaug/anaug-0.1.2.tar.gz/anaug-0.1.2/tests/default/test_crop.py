import unittest
import numpy as np
from src.anaug.default import crop


class TestCropFunction(unittest.TestCase):
    
    def setUp(self):
        # Create a synthetic grayscale image (100x100)
        self.gray_image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        
        # Create a synthetic color image (100x100x3)
        self.color_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    
    def test_basic_cropping_grayscale(self):
        top, left, height, width = 10, 10, 50, 50
        cropped = crop(self.gray_image, top, left, height, width)
        expected = self.gray_image[top:top+height, left:left+width]
        np.testing.assert_array_equal(cropped, expected)
    
    def test_basic_cropping_color(self):
        top, left, height, width = 20, 20, 60, 60
        cropped = crop(self.color_image, top, left, height, width)
        expected = self.color_image[top:top+height, left:left+width, :]
        np.testing.assert_array_equal(cropped, expected)
    
    def test_crop_with_negative_coordinates(self):
        top, left, height, width = -10, 20, 50, 50
        with self.assertRaises(ValueError):
            crop(self.gray_image, top, left, height, width)
    
    def test_crop_with_zero_height(self):
        top, left, height, width = 10, 10, 0, 50
        with self.assertRaises(ValueError):
            crop(self.gray_image, top, left, height, width)
    
    def test_crop_with_non_integer_parameters(self):
        top, left, height, width = 10.5, '20', 50, 50
        with self.assertRaises(TypeError):
            crop(self.gray_image, top, left, height, width)
    
    def test_crop_exceeds_boundaries_without_adjustment(self):
        top, left, height, width = 80, 80, 30, 30  # Exceeds 100x100
        with self.assertRaises(ValueError):
            crop(self.gray_image, top, left, height, width)
    
    def test_crop_exceeds_boundaries_with_adjustment(self):
        top, left, height, width = 80, 80, 30, 30  # Exceeds 100x100
        cropped = crop(
            self.gray_image,
            top,
            left,
            height,
            width,
            adjust_if_exceeds=True,
            pad_value=(255,)
        )
        expected_cropped = self.gray_image[80:100, 80:100]
        expected_padded = np.pad(
            expected_cropped,
            pad_width=((0, 10), (0, 10)),
            mode='constant',
            constant_values=255
        )
        np.testing.assert_array_equal(cropped, expected_padded)
    
    def test_crop_with_pad_value_multi_channel(self):
        top, left, height, width = 90, 90, 20, 20  # Exceeds 100x100 for 3 channels
        cropped = crop(
            self.color_image,
            top,
            left,
            height,
            width,
            adjust_if_exceeds=True,
            pad_value=(0, 128, 255)
        )
        # Expected cropped part
        expected_cropped = self.color_image[90:100, 90:100, :]
        # Expected padding: pad_bottom=20-10=10, pad_right=20-10=10
        pad_bottom, pad_right = 10, 10
        padded_channels = []
        for c, pad_val in enumerate((0, 128, 255)):
            channel = expected_cropped[:, :, c]
            padded_channel = np.pad(
                channel,
                pad_width=((0, pad_bottom), (0, pad_right)),
                mode='constant',
                constant_values=pad_val
            )
            padded_channels.append(padded_channel)
        expected_padded = np.stack(padded_channels, axis=2)
        np.testing.assert_array_equal(cropped, expected_padded)
    
    def test_crop_with_partial_padding_color(self):
        top, left, height, width = 95, 95, 10, 10  # Exceeds by 5 pixels each side
        cropped = crop(
            self.color_image,
            top,
            left,
            height,
            width,
            adjust_if_exceeds=True,
            pad_value=(255, 0, 0)  # Red padding
        )
        # Expected cropped part
        expected_cropped = self.color_image[95:100, 95:100, :]
        # Expected padding: pad_bottom=10-5=5, pad_right=10-5=5
        pad_bottom, pad_right = 5, 5
        padded_channels = []
        for c, pad_val in enumerate((255, 0, 0)):
            channel = expected_cropped[:, :, c]
            padded_channel = np.pad(
                channel,
                pad_width=((0, pad_bottom), (0, pad_right)),
                mode='constant',
                constant_values=pad_val
            )
            padded_channels.append(padded_channel)
        expected_padded = np.stack(padded_channels, axis=2)
        np.testing.assert_array_equal(cropped, expected_padded)
    
    def test_crop_with_pad_value_multi_channel_invalid_length(self):
        # pad_value length does not match number of channels
        top, left, height, width = 90, 90, 20, 20
        with self.assertRaises(ValueError):
            crop(
                self.color_image,
                top,
                left,
                height,
                width,
                adjust_if_exceeds=True,
                pad_value=(0, 128)  # Only 2 values instead of 3
            )
    
    def test_crop_no_blur_radius_one_grayscale(self):
        top, left, height, width = 10, 10, 50, 50
        cropped = crop(
            self.gray_image,
            top,
            left,
            height,
            width,
            adjust_if_exceeds=True,
            pad_value=(0,)
        )
        expected = self.gray_image[top:top+height, left:left+width]
        np.testing.assert_array_equal(cropped, expected)
    
    def test_crop_no_blur_radius_one_color(self):
        top, left, height, width = 10, 10, 50, 50
        cropped = crop(
            self.color_image,
            top,
            left,
            height,
            width,
            adjust_if_exceeds=True,
            pad_value=(0, 0, 0)
        )
        expected = self.color_image[top:top+height, left:left+width, :]
        np.testing.assert_array_equal(cropped, expected)
    
    def test_crop_entire_image(self):
        top, left, height, width = 0, 0, 100, 100
        cropped = crop(
            self.gray_image,
            top,
            left,
            height,
            width
        )
        np.testing.assert_array_equal(cropped, self.gray_image)
    
    def test_crop_with_partial_padding_grayscale(self):
        top, left, height, width = 95, 95, 10, 10  # Exceeds by 5 pixels each side
        cropped = crop(
            self.gray_image,
            top,
            left,
            height,
            width,
            adjust_if_exceeds=True,
            pad_value=(128,)
        )
        expected_cropped = self.gray_image[95:100, 95:100]
        expected_padded = np.pad(
            expected_cropped,
            pad_width=((0, 5), (0, 5)),
            mode='constant',
            constant_values=128
        )
        np.testing.assert_array_equal(cropped, expected_padded)

    def test_crop_with_non_standard_dimensions(self):
        # Create an image with shape (100, 100, 4) - RGBA
        rgba_image = np.random.randint(0, 256, (100, 100, 4), dtype=np.uint8)
        top, left, height, width = 10, 10, 80, 80
        cropped = crop(
            rgba_image,
            top,
            left,
            height,
            width
        )
        expected = rgba_image[top:top+height, left:left+width, :]
        np.testing.assert_array_equal(cropped, expected)

if __name__ == '__main__':
    unittest.main()