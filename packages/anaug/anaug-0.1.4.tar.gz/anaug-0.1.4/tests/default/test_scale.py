import unittest
import numpy as np
from src.anaug.default import scale

class TestScale(unittest.TestCase):
    """Test cases for the scale augmentation function"""

    def setUp(self):
        """Set up test image for use in multiple tests"""
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    
    def test_upscale(self):
        """Test scaling up an image and verify the new dimensions"""
        scale_factor = 2.0
        result = scale(self.test_image, scale_factor)
        self.assertEqual(result.shape, (200, 200, 3))

    def test_downscale(self):
        """Test scaling down an image and verify the new dimensions"""
        scale_factor = 0.5
        result = scale(self.test_image, scale_factor)
        self.assertEqual(result.shape, (50, 50, 3))

    def test_scale_unchanged(self):
        """Test scaling with a factor of 1.0, ensuring no dimension change"""
        scale_factor = 1.0
        result = scale(self.test_image, scale_factor)
        self.assertEqual(result.shape, self.test_image.shape)
        
    def test_scale_grayscale(self):
        """Test scaling a grayscale image to verify behavior with single-channel images"""
        gray_image = np.zeros((100, 100), dtype=np.uint8)
        scale_factor = 1.5
        result = scale(gray_image, scale_factor)
        self.assertEqual(result.shape, (150, 150))

    def test_type_preservation(self):
        """Test that the output image maintains the same dtype as the input"""
        scale_factor = 1.5
        result = scale(self.test_image, scale_factor)
        self.assertEqual(result.dtype, self.test_image.dtype)
    
    def test_very_small_image(self):
        """Test scaling a very small image (1x1 pixel) to verify correct handling"""
        small_image = np.zeros((1, 1, 3), dtype=np.uint8)
        scale_factor = 2.0
        result = scale(small_image, scale_factor)
        self.assertEqual(result.shape, (2, 2, 3))

    def test_invalid_scale_factor(self):
        """Test scaling with an invalid scale factor (e.g., negative or zero)"""
        with self.assertRaises(ValueError):
            scale(self.test_image, -1.0)

    def test_non_integer_dimensions(self):
        """Test scaling with a factor that results in non-integer dimensions"""
        scale_factor = 1.333
        result = scale(self.test_image, scale_factor)
        self.assertEqual(result.shape, (133, 133, 3))

    def test_empty_image(self):
        """Test scaling an empty image (0x0 size) to ensure expected behavior"""
        empty_image = np.zeros((0, 0, 3), dtype=np.uint8)
        scale_factor = 2.0
        with self.assertRaises(ValueError):
            scale(empty_image, scale_factor)

    def test_high_scale_factor(self):
        """Test scaling with a very large factor to verify dimension limits"""
        scale_factor = 2000.0
        with self.assertRaises(ValueError):
            scale(self.test_image, scale_factor)

if __name__ == '__main__':
    unittest.main()
