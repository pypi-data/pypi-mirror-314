import cv2

def scale(image, scale_factor, max_dimension=10000):
    """
    Scale an image by a given factor.

    Args:
        image (numpy.ndarray): Input image to be scaled.
        scale_factor (float): Factor to scale the image. Must be > 0.
        max_dimension (int): Maximum allowable dimension for the scaled image. Default is 10000.

    Returns:
        numpy.ndarray: Scaled image with adjusted dimensions.

    Raises:
        ValueError: If scale_factor is <= 0, input image is empty, or resulting dimensions exceed the allowable limit.
    """
    if scale_factor <= 0:
        raise ValueError("Scale factor must be greater than zero.")
    
    if image is None or image.size == 0:
        raise ValueError("Input image is empty and cannot be scaled.")

    # Compute new dimensions
    height, width = image.shape[:2]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    if new_width == 0 or new_height == 0:
        raise ValueError("Scaled dimensions are invalid (resulting in zero size).")
    
    if new_width > max_dimension or new_height > max_dimension:
        raise ValueError(f"Scaled dimensions ({new_width}x{new_height}) exceed the allowable limit of {max_dimension} pixels.")

    # Resize using OpenCV
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
