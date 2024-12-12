import cv2
import numpy as np

def rotate(image, angle, mode='nearest', center=None):
    """
    Rotate the image by the specified angle around a given center.
    
    Parameters:
    - image (np.ndarray): Input image as a 2D (grayscale) or 3D (multi-channel) numpy array.
    - angle (float): Angle by which to rotate the image (in degrees).
    - mode (str): Points outside the boundaries of the input are filled according to the given mode
                  ('constant', 'nearest', 'mirror', or 'wrap').
    - center (tuple or None): The point around which to rotate the image. If None, the image center is used.
    
    Returns:
    - np.ndarray: Rotated image.
    
    Raises:
    - TypeError: If the input image is not a numpy array.
    - ValueError: If the angle is not numeric, the mode is invalid, or center is improperly defined.
    """
    # Validate input type
    if not isinstance(image, np.ndarray):
        raise TypeError("Input image must be a numpy array.")
    
    # Validate angle
    if not isinstance(angle, (int, float)):
        raise ValueError("Angle must be a numeric value.")
    
    # Validate image dimensions
    if image.ndim < 2 or image.ndim > 3:
        raise ValueError("Input image must be a 2D (grayscale) or 3D (multi-channel) array.")
    
    # Validate mode
    valid_modes = ['constant', 'nearest', 'mirror', 'wrap']
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode '{mode}'. Supported modes are: {valid_modes}")

    # Handle rotations that are multiples of 90 degrees
    if angle % 90 == 0:
        k = int(angle / 90) % 4
        return np.rot90(image, k=k, axes=(0, 1))

    # Define center
    h, w = image.shape[:2]
    if center is None:
        center = (w / 2, h / 2)

    # Map mode to OpenCV border modes
    cv2_border_modes = {
        'constant': cv2.BORDER_CONSTANT,
        'nearest': cv2.BORDER_REPLICATE,
        'mirror': cv2.BORDER_REFLECT,
        'wrap': cv2.BORDER_WRAP
    }
    border_mode = cv2_border_modes[mode]

    # Compute the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)

    # Apply the rotation
    if image.ndim == 3:  # Multi-channel image
        rotated_channels = [cv2.warpAffine(image[..., i], rotation_matrix, (w, h), borderMode=border_mode)
                            for i in range(image.shape[2])]
        rotated_image = np.stack(rotated_channels, axis=-1)
    else:  # Grayscale image
        rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h), borderMode=border_mode)

    return rotated_image