import numpy as np
import cv2

def random_rotation(image, angle_range=(-30, 30), center=None, scale=1.0, border_mode=cv2.BORDER_REFLECT):
    """
    Applies a random rotation to the image within the specified angle range.
    
    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - angle_range (tuple): Range of angles to randomly rotate the image, e.g., (-30, 30).
    - center (tuple or None): The point around which to rotate the image. If None, the image center is used.
    - scale (float): Scaling factor applied during the rotation. Default is 1.0 (no scaling).
    - border_mode (int): Pixel extrapolation method for areas outside the image. Default is cv2.BORDER_REFLECT.

    Returns:
    - np.array: Rotated image with the same shape as input.

    Raises:
    - TypeError: If the input image is not a numpy array.
    - ValueError: If angle_range is not a tuple of two numeric values.
    """
    # Validate input type
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a numpy array.")

    # Validate angle_range
    if not (isinstance(angle_range, tuple) and len(angle_range) == 2 and 
            all(isinstance(a, (int, float)) for a in angle_range)):
        raise ValueError("angle_range must be a tuple of two numeric values.")

    # Randomly select an angle within the specified range
    angle = np.random.uniform(angle_range[0], angle_range[1])

    # Get the image dimensions and calculate the center
    h, w = image.shape[:2]
    if center is None:
        center = (w / 2, h / 2)

    # Compute the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=scale)

    # Apply rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h), borderMode=border_mode)
    return rotated_image