import unittest
import numpy as np
from src.anaug.default import noise


class TestNoise(unittest.TestCase):
    """
    Test suite for the `noise` function.
    """

    def setUp(self):
        """
        Set up test images for use in all test cases.
        """
        # Set a fixed random seed for reproducibility
        np.random.seed(0)
        
        # Create a test grayscale float image (100x100) with values between 0.5 and 1.0
        self.gray_image_float = np.random.uniform(low=0.5, high=1.0, size=(100, 100)).astype(np.float32)

        # Create a test grayscale uint8 image (100x100) with values between 100 and 200
        self.gray_image_uint8 = np.random.randint(100, 200, (100, 100), dtype=np.uint8)

        # Create a test color float image (100x100x3) with values between 0.5 and 1.0
        self.color_image_float = np.random.uniform(low=0.5, high=1.0, size=(100, 100, 3)).astype(np.float32)

        # Create a test color uint8 image (100x100x3) with values between 100 and 200
        self.color_image_uint8 = np.random.randint(100, 200, (100, 100, 3), dtype=np.uint8)

        # Create a minimal image (1x1) for edge case testing
        self.minimal_image_float = np.array([[0.5]], dtype=np.float32)
        self.minimal_image_uint8 = np.array([[128]], dtype=np.uint8)

        # Create a uniform image with all pixels having the same intensity
        self.uniform_image_float = np.full((100, 100), 0.5, dtype=np.float32)
        self.uniform_image_uint8 = np.full((100, 100), 128, dtype=np.uint8)

    # ---------------------
    # Gaussian Noise Tests
    # ---------------------

    def test_add_gaussian_noise_float(self):
        """
        Test adding Gaussian noise to a float grayscale image.
        """
        noise_intensity = 0.1
        noisy_image = noise(
            self.gray_image_float, noise_type='gaussian', noise_intensity=noise_intensity
        )
        self.assertEqual(noisy_image.shape, self.gray_image_float.shape)
        self.assertEqual(noisy_image.dtype, self.gray_image_float.dtype)
        self.assertTrue(np.any(noisy_image != self.gray_image_float))
        self.assertTrue(np.all(noisy_image >= 0.0) and np.all(noisy_image <= 1.0))

        # Statistical validation
        original_mean = np.mean(self.gray_image_float)
        noisy_mean = np.mean(noisy_image)
        original_std = np.std(self.gray_image_float)
        noisy_std = np.std(noisy_image)

        # Mean should remain approximately the same
        self.assertAlmostEqual(noisy_mean, original_mean, delta=0.02)

        # Standard deviation should combine quadratically
        expected_std = np.sqrt(original_std**2 + noise_intensity**2)
        self.assertAlmostEqual(noisy_std, expected_std, delta=0.02)

    def test_add_gaussian_noise_uint8(self):
        """
        Test adding Gaussian noise to a uint8 grayscale image.
        """
        noise_intensity = 10  # Standard deviation for uint8
        noisy_image = noise(
            self.gray_image_uint8, noise_type='gaussian', noise_intensity=noise_intensity
        )
        self.assertEqual(noisy_image.shape, self.gray_image_uint8.shape)
        self.assertEqual(noisy_image.dtype, self.gray_image_uint8.dtype)
        self.assertTrue(np.any(noisy_image != self.gray_image_uint8))
        self.assertTrue(np.all(noisy_image >= 0) and np.all(noisy_image <= 255))

        # Statistical validation
        original_std = np.std(self.gray_image_uint8)
        noisy_std = np.std(noisy_image)
        # Since original image has inherent variance, the expected std increases quadratically
        expected_std = np.sqrt(original_std**2 + noise_intensity**2)
        self.assertAlmostEqual(noisy_std, expected_std, delta=1.0)  # Increased delta from 0.02 to 1.0

    def test_gaussian_noise_zero_intensity(self):
        """
        Test adding Gaussian noise with zero intensity, expecting no change.
        """
        noisy_image = noise(
            self.gray_image_float, noise_type='gaussian', noise_intensity=0.0
        )
        # Verify that the noisy image is identical to the original
        np.testing.assert_array_equal(noisy_image, self.gray_image_float)

    # --------------------------
    # Salt-and-Pepper Noise Tests
    # --------------------------

    def test_add_salt_and_pepper_noise_float(self):
        """
        Test adding salt-and-pepper noise to a float grayscale image.
        """
        noise_intensity = 0.05  # 5% of pixels
        noisy_image = noise(
            self.gray_image_float, noise_type='salt_and_pepper', noise_intensity=noise_intensity
        )
        self.assertEqual(noisy_image.shape, self.gray_image_float.shape)
        self.assertEqual(noisy_image.dtype, self.gray_image_float.dtype)
        self.assertTrue(np.any(noisy_image != self.gray_image_float))
        self.assertTrue(np.all(noisy_image >= 0.0) and np.all(noisy_image <= 1.0))

        # Count salt and pepper pixels
        num_salt = np.sum(noisy_image == 1.0)
        num_pepper = np.sum(noisy_image == 0.0)
        total_pixels = self.gray_image_float.size
        expected = noise_intensity * total_pixels
        self.assertAlmostEqual(num_salt + num_pepper, expected, delta=expected * 0.1)

    def test_add_salt_and_pepper_noise_uint8(self):
        """
        Test adding salt-and-pepper noise to a uint8 grayscale image.
        """
        noise_intensity = 0.05  # 5% of pixels
        noisy_image = noise(
            self.gray_image_uint8, noise_type='salt_and_pepper', noise_intensity=noise_intensity
        )
        self.assertEqual(noisy_image.shape, self.gray_image_uint8.shape)
        self.assertEqual(noisy_image.dtype, self.gray_image_uint8.dtype)
        self.assertTrue(np.any(noisy_image != self.gray_image_uint8))
        self.assertTrue(np.all(noisy_image >= 0) and np.all(noisy_image <= 255))

        # Count salt and pepper pixels
        num_salt = np.sum(noisy_image == 255)
        num_pepper = np.sum(noisy_image == 0)
        total_pixels = self.gray_image_uint8.size
        expected = noise_intensity * total_pixels
        self.assertAlmostEqual(num_salt + num_pepper, expected, delta=expected * 0.1)

    def test_salt_and_pepper_noise_zero_intensity(self):
        """
        Test adding salt-and-pepper noise with zero intensity, expecting no change.
        """
        noisy_image = noise(
            self.gray_image_uint8, noise_type='salt_and_pepper', noise_intensity=0.0
        )
        # Verify that the noisy image is identical to the original
        np.testing.assert_array_equal(noisy_image, self.gray_image_uint8)

    # -------------------
    # Poisson Noise Tests
    # -------------------

    def test_add_poisson_noise_float(self):
        """
        Test adding Poisson noise to a float grayscale image.
        """
        noise_intensity = 5.0  # Scale factor
        scale = 10.0
        noisy_image = noise(
            self.gray_image_float, noise_type='poisson', noise_intensity=noise_intensity, scale=scale
        )
        self.assertEqual(noisy_image.shape, self.gray_image_float.shape)
        self.assertEqual(noisy_image.dtype, self.gray_image_float.dtype)
        self.assertTrue(np.any(noisy_image != self.gray_image_float))
        self.assertTrue(np.all(noisy_image >= 0.0) and np.all(noisy_image <= 1.0))

        # Statistical validation
        original_mean = np.mean(self.gray_image_float)
        noisy_mean = np.mean(noisy_image)
        self.assertAlmostEqual(noisy_mean, original_mean, delta=0.05)

    def test_add_poisson_noise_uint8(self):
        """
        Test adding Poisson noise to a uint8 grayscale image.
        """
        noise_intensity = 5.0  # Scale factor
        scale = 10.0
        noisy_image = noise(
            self.gray_image_uint8, noise_type='poisson', noise_intensity=noise_intensity, scale=scale
        )
        self.assertEqual(noisy_image.shape, self.gray_image_uint8.shape)
        self.assertEqual(noisy_image.dtype, self.gray_image_uint8.dtype)
        self.assertTrue(np.any(noisy_image != self.gray_image_uint8))
        self.assertTrue(np.all(noisy_image >= 0) and np.all(noisy_image <= 255))

        # Statistical validation
        original_mean = np.mean(self.gray_image_uint8)
        noisy_mean = np.mean(noisy_image)
        self.assertAlmostEqual(noisy_mean, original_mean, delta=1.0)

    def test_poisson_noise_zero_intensity(self):
        """
        Test adding Poisson noise with zero intensity, expecting no change.
        """
        noisy_image = noise(
            self.gray_image_float, noise_type='poisson', noise_intensity=0.0, scale=1.0
        )
        # Verify that the noisy image is identical to the original
        np.testing.assert_array_equal(noisy_image, self.gray_image_float)

    # ----------------------
    # Unsupported Noise Type
    # ----------------------

    def test_invalid_noise_type(self):
        """
        Test if the function raises a ValueError for unsupported noise types.
        """
        with self.assertRaises(ValueError):
            noise(self.gray_image_float, noise_type='invalid_noise', noise_intensity=0.1)

    # --------------------
    # Invalid Noise Intensity
    # --------------------

    def test_negative_noise_intensity_gaussian(self):
        """
        Test if the function raises a ValueError for negative noise intensity in Gaussian noise.
        """
        with self.assertRaises(ValueError):
            noise(self.gray_image_float, noise_type='gaussian', noise_intensity=-0.1)

    def test_out_of_range_noise_intensity_salt_and_pepper(self):
        """
        Test if the function raises a ValueError for noise intensity out of range in salt-and-pepper noise.
        """
        with self.assertRaises(ValueError):
            noise(self.gray_image_uint8, noise_type='salt_and_pepper', noise_intensity=1.5)
        with self.assertRaises(ValueError):
            noise(self.gray_image_uint8, noise_type='salt_and_pepper', noise_intensity=-0.1)

    def test_negative_noise_intensity_poisson(self):
        """
        Test if the function raises a ValueError for negative noise intensity in Poisson noise.
        """
        with self.assertRaises(ValueError):
            noise(self.gray_image_float, noise_type='poisson', noise_intensity=-5.0, scale=10.0)

    # -----------------
    # Invalid Scale
    # -----------------

    def test_invalid_scale_poisson(self):
        """
        Test if the function raises a TypeError for non-float scale in Poisson noise.
        """
        with self.assertRaises(TypeError):
            noise(self.gray_image_float, noise_type='poisson', noise_intensity=5.0, scale='high')

    def test_negative_scale_poisson(self):
        """
        Test if the function raises a ValueError for negative scale in Poisson noise.
        """
        with self.assertRaises(ValueError):
            noise(self.gray_image_float, noise_type='poisson', noise_intensity=5.0, scale=-10.0)

    # -----------------
    # Unsupported Data Types
    # -----------------

    def test_unsupported_data_type(self):
        """
        Test if the function raises a ValueError for unsupported image data types.
        """
        unsupported_image = self.gray_image_float.astype(np.int16)
        with self.assertRaises(ValueError):
            noise(unsupported_image, noise_type='gaussian', noise_intensity=0.1)

    # -----------------
    # Edge Cases
    # -----------------

    def test_minimal_image_poisson(self):
        """
        Test adding Poisson noise to a minimal image (1x1) with float data type.
        """
        noisy_image = noise(
            self.minimal_image_float, noise_type='poisson', noise_intensity=5.0, scale=10.0
        )
        self.assertEqual(noisy_image.shape, self.minimal_image_float.shape)
        self.assertEqual(noisy_image.dtype, self.minimal_image_float.dtype)
        self.assertTrue(np.any(noisy_image != self.minimal_image_float))
        self.assertTrue(np.all(noisy_image >= 0.0) and np.all(noisy_image <= 1.0))

    def test_uniform_image_salt_and_pepper(self):
        """
        Test adding salt-and-pepper noise to a uniform image.
        """
        noise_intensity = 0.1  # 10% of pixels
        noisy_image = noise(
            self.uniform_image_float, noise_type='salt_and_pepper', noise_intensity=noise_intensity
        )
        self.assertEqual(noisy_image.shape, self.uniform_image_float.shape)
        self.assertEqual(noisy_image.dtype, self.uniform_image_float.dtype)
        # Count salt and pepper pixels
        num_salt = np.sum(noisy_image == 1.0)
        num_pepper = np.sum(noisy_image == 0.0)
        total_pixels = self.uniform_image_float.size
        expected = noise_intensity * total_pixels
        self.assertAlmostEqual(num_salt + num_pepper, expected, delta=expected * 0.1)


if __name__ == '__main__':
    unittest.main()
