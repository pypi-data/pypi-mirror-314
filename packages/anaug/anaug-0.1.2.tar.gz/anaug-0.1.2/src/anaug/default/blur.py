"""
Image Blurring Module

This module provides functions to apply various blur effects to images, including Gaussian blur, uniform blur, median blur, and motion blur. These functions can handle both 2D (grayscale) and 3D (color) images, making them versatile for different image processing tasks.

Functions:
- motion_blur: Applies motion blur to an image.
- blur: General blur function supporting multiple types of blur.

Usage Examples:
------------
>>> import numpy as np
>>> from your_module_path import blur
>>> # Create a sample image
>>> image = np.random.rand(128, 128, 3)
>>> # Apply Gaussian blur
>>> blurred_image = blur(image, blur_type='gaussian', blur_radius=2)
>>> # Apply motion blur
>>> motion_blurred = blur(image, blur_type='motion', blur_radius=5, length=10, angle=45)
"""

from scipy.ndimage import gaussian_filter, uniform_filter, median_filter
import numpy as np
import cv2

def motion_blur(image, length=5, angle=0):
    """
    Applies motion blur to an image.

    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - length (int): Length of the motion blur effect.
    - angle (float): Angle of motion blur in degrees.

    Returns:
    - np.array: Motion-blurred image.
    """
    # Create an empty kernel
    kernel = np.zeros((length, length))
    center = length // 2

    # Set a line along the motion direction
    kernel[center, :] = 1  # Horizontal line in the kernel
    kernel /= kernel.sum()  # Normalize the kernel to maintain brightness

    # Rotate the kernel to the specified angle
    M = cv2.getRotationMatrix2D((center, center), angle, 1)
    kernel = cv2.warpAffine(kernel, M, (length, length))

    # Apply the motion blur kernel to the image
    return cv2.filter2D(image, -1, kernel)

def blur(image, blur_type='gaussian', blur_radius=1, **kwargs):
    """
    Applies blur to a given image.

    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - blur_type (str): Type of blur to apply ('gaussian', 'uniform', 'median', 'motion').
    - blur_radius (float): Standard deviation for Gaussian kernel or size for uniform/median filter. Higher values increase blur.
    - **kwargs: Additional parameters for specific blur types (e.g., length, angle for motion blur).

    Returns:
    - np.array: Blurred image with the same shape as input.
    """
    if blur_type == 'gaussian':
        return gaussian_filter(image, sigma=blur_radius)
    elif blur_type == 'uniform':
        return uniform_filter(image, size=int(blur_radius))
    elif blur_type == 'median':
        return median_filter(image, size=int(blur_radius))
    elif blur_type == 'motion':
        length = kwargs.get('length', 5)
        angle = kwargs.get('angle', 0)
        return motion_blur(image, length=length, angle=angle)
    else:
        raise ValueError("Unsupported blur type. Use 'gaussian', 'uniform', 'median', or 'motion'.")
