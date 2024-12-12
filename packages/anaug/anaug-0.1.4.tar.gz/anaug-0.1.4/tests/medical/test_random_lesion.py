import unittest
import numpy as np
from src.anaug.medical.random_lesion import random_lesion


class TestRandomLesion(unittest.TestCase):
    """Unit tests for the random lesion generation function."""

    def setUp(self):
        """Set up a sample image and fix the random seed for reproducibility."""
        self.image = np.zeros((256, 256), dtype=np.float32)
        # Note: Avoid setting a global seed here to allow individual tests to control seeding.

    def _count_lesion_pixels(self, original_image, lesion_image, threshold=0.1):
        """Helper method to count the number of lesion pixels above a threshold."""
        lesion_diff = lesion_image - original_image
        return np.sum(lesion_diff > threshold)

    def test_output_shape(self):
        """Test if the output image has the same shape as the input."""
        lesion_image = random_lesion(self.image)
        self.assertEqual(lesion_image.shape, self.image.shape, "Output shape mismatch.")

    def test_output_dtype(self):
        """Test if the output image has the correct data type."""
        lesion_image = random_lesion(self.image)
        self.assertEqual(lesion_image.dtype, self.image.dtype, "Output dtype mismatch.")

    def test_intensity_range(self):
        """Test if the added lesion has intensity within the specified range."""
        intensity_range = (0.3, 0.7)
        lesion_image = random_lesion(self.image, intensity_range=intensity_range, seed=42)
        lesion_diff = lesion_image - self.image

        # Create a mask of pixels affected by the lesion
        lesion_mask = lesion_diff > 0

        # Check that all lesion pixels are within the intensity range
        self.assertTrue(np.all(lesion_diff[lesion_mask] >= intensity_range[0]),
                        f"Some lesion pixels have intensity below {intensity_range[0]}.")
        self.assertTrue(np.all(lesion_diff[lesion_mask] <= intensity_range[1]),
                        f"Some lesion pixels have intensity above {intensity_range[1]}.")

    def test_size_range(self):
        """Test if the lesion size is within the specified range."""
        size_range = (20, 50)
        lesion_image = random_lesion(self.image, size_range=size_range, seed=42)
        lesion_area = self._count_lesion_pixels(self.image, lesion_image, threshold=0.1)
        expected_min_area = 250  # Approximate minimum area
        expected_max_area = 10000  # Approximate maximum area
        self.assertTrue(expected_min_area < lesion_area < expected_max_area,
                        f"Lesion area {lesion_area} is outside the expected range.")

    def test_texture_strength(self):
        """Test the effect of the texture_strength parameter."""
        # Generate two lesions with different texture strengths
        lesion_smooth = random_lesion(self.image, texture_strength=0.1, seed=1)
        lesion_textured = random_lesion(self.image, texture_strength=0.9, seed=1)

        # Calculate standard deviations of lesion intensities
        lesion_diff_smooth = lesion_smooth - self.image
        lesion_diff_textured = lesion_textured - self.image
        std_smooth = np.std(lesion_diff_smooth[lesion_diff_smooth > 0])
        std_textured = np.std(lesion_diff_textured[lesion_diff_textured > 0])

        self.assertGreater(std_textured, std_smooth * 1.2,
                           "Texture strength did not increase lesion variability as expected.")

    def test_clipping(self):
        """Test if the function clips the output values within [0, 1]."""
        lesion_image = random_lesion(self.image, intensity_range=(0.5, 0.9), seed=42)
        self.assertTrue(np.all(lesion_image >= 0),
                        "Lesion image contains values below 0.")
        self.assertTrue(np.all(lesion_image <= 1),
                        "Lesion image contains values above 1.")

    def test_shapes(self):
        """Test for different lesion shapes."""
        shapes = ['circle', 'ellipse', 'irregular']
        for shape in shapes:
            with self.subTest(shape=shape):
                lesion_image = random_lesion(self.image, shape=shape, seed=42)
                self.assertEqual(lesion_image.shape, self.image.shape,
                                 f"Output shape mismatch for shape '{shape}'.")
                # Check that at least some pixels have been modified
                self.assertTrue(np.max(lesion_image) > 0,
                                f"No lesion detected for shape '{shape}'.")

    def test_invalid_inputs(self):
        """Test if invalid inputs raise appropriate errors."""
        test_cases = [
            {"image": np.ones((256, 256, 3)), "params": {"intensity_range": (0.2, 0.8)}, "error": ValueError},
            {"image": self.image, "params": {"intensity_range": (1.5, 2)}, "error": ValueError},
            {"image": self.image, "params": {"size_range": (-10, 50)}, "error": ValueError},
            {"image": self.image, "params": {"shape": 'invalid_shape'}, "error": ValueError},
            {"image": self.image, "params": {"texture_strength": -0.1}, "error": ValueError},
            {"image": self.image, "params": {"texture_strength": 1.5}, "error": ValueError},
            {"image": self.image, "params": {"num_lesions": 0}, "error": ValueError},
            {"image": self.image, "params": {"blending_mode": 'unsupported_mode'}, "error": ValueError},
        ]

        for case in test_cases:
            with self.subTest(params=case["params"]):
                with self.assertRaises(case["error"]):
                    random_lesion(case["image"], **case["params"])

    def test_specific_location(self):
        """Test if the lesion is placed at a specific location."""
        location = (128, 128)
        size_range = (19, 21)
        lesion_image = random_lesion(self.image, location=location, size_range=size_range, seed=42)

        # Verify the lesion is centered around the specified location
        lesion_diff = lesion_image - self.image
        coords = np.argwhere(lesion_diff > 0)
        if coords.size == 0:
            self.fail("No lesion detected at the specified location.")
        center_of_mass = coords.mean(axis=0)
        distance = np.linalg.norm(center_of_mass - np.array(location))
        self.assertLess(distance, 10, f"Lesion center is too far from the specified location: {distance} pixels.")

    def test_multiple_lesions(self):
        """Test generating multiple lesions."""
        num_lesions = 5
        lesion_image = random_lesion(self.image, num_lesions=num_lesions, seed=42)
        lesion_area = self._count_lesion_pixels(self.image, lesion_image, threshold=0.1)
        expected_min_area = num_lesions * 200  # Approximate minimum area per lesion
        expected_max_area = num_lesions * 10000  # Approximate maximum area per lesion

        self.assertTrue(expected_min_area < lesion_area < expected_max_area,
                        f"Total lesion area {lesion_area} is outside the expected range for {num_lesions} lesions.")

    def test_blending_modes(self):
        """Test different blending modes."""
        blending_modes = ['additive', 'overlay']
        for mode in blending_modes:
            with self.subTest(blending_mode=mode):
                lesion_image = random_lesion(self.image, blending_mode=mode, seed=42)
                self.assertEqual(lesion_image.shape, self.image.shape,
                                 f"Output shape mismatch for blending mode '{mode}'.")
                self.assertTrue(np.max(lesion_image) > 0,
                                f"No lesion detected for blending mode '{mode}'.")

    def test_non_zero_input_image(self):
        """Test how lesions are added to a non-zero input image."""
        input_image = np.full((256, 256), 0.5, dtype=np.float32)
        lesion_image = random_lesion(input_image, intensity_range=(0.2, 0.4), seed=42)
        self.assertTrue(np.all(lesion_image >= 0.5),
                        "Lesion addition resulted in values below the original image intensity.")
        self.assertTrue(np.all(lesion_image <= 0.9),
                        "Lesion addition resulted in values above the expected maximum intensity.")

    def test_seed_consistency(self):
        """Test if setting a seed produces consistent lesions."""
        seed = 123
        lesion1 = random_lesion(self.image, seed=seed)
        lesion2 = random_lesion(self.image, seed=seed)
        np.testing.assert_array_almost_equal(lesion1, lesion2, decimal=5,
                                             err_msg="Lesions with the same seed are not identical.")

    def test_lesion_overlap(self):
        """Test if multiple lesions do not unintentionally overlap excessively."""
        num_lesions = 10
        lesion_image = random_lesion(self.image, num_lesions=num_lesions, seed=42)
        lesion_area = self._count_lesion_pixels(self.image, lesion_image, threshold=0.1)
        expected_min_total_area = num_lesions * 200  # Approximate minimum area
        # Allow some overlap, so max area can be up to the image size
        expected_max_total_area = self.image.size

        self.assertTrue(expected_min_total_area < lesion_area < expected_max_total_area,
                        "Lesion overlap may be excessive or lesions are not being added correctly.")

    def test_large_image_performance(self):
        """Test function performance on a large image."""
        large_image = np.zeros((1024, 1024), dtype=np.float32)
        try:
            lesion_image = random_lesion(large_image, num_lesions=20, size_range=(30, 60), seed=42)
            self.assertEqual(lesion_image.shape, large_image.shape,
                             "Output shape mismatch for large image.")
            self.assertTrue(np.max(lesion_image) > 0, "No lesion detected on large image.")
        except Exception as e:
            self.fail(f"Function failed on large image with exception: {e}")


if __name__ == '__main__':
    unittest.main()
