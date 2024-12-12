import numpy as np


def intensity(
    image: np.ndarray,
    brightness_factor: float = 1.0,
    contrast_factor: float = 1.0
) -> np.ndarray:
    """
    Adjusts brightness and contrast of a given image.

    Parameters
    ----------
    image : np.ndarray
        Input image as a 2D (grayscale) or 3D (multi-channel/color) NumPy array.
    brightness_factor : float, optional
        Factor to adjust brightness. Values > 1 increase brightness, values < 1 decrease brightness.
        Must be positive. Default is 1.0 (no change).
    contrast_factor : float, optional
        Factor to adjust contrast. Values > 1 increase contrast, values < 1 decrease contrast.
        Must be positive. Default is 1.0 (no change).

    Returns
    -------
    np.ndarray
        Image with adjusted brightness and contrast, maintaining the original shape and data type.

    Raises
    ------
    TypeError
        If the input image is not a NumPy array.
    ValueError
        If the image has unsupported dimensions or if factors are non-positive.

    Examples
    --------
    >>> import numpy as np
    >>> from anaug.default.intensity import intensity
    >>> # Grayscale image example
    >>> gray_image = np.array([[100, 150], [200, 250]], dtype=np.uint8)
    >>> adjusted_image = intensity(gray_image, brightness_factor=1.2, contrast_factor=1.5)
    >>> print(adjusted_image)
    [[...]]
    
    >>> # Color image example
    >>> color_image = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)
    >>> adjusted_color = intensity(color_image, brightness_factor=0.8, contrast_factor=1.3)
    >>> print(adjusted_color.shape)
    (128, 128, 3)
    """
    # Validate input type
    if not isinstance(image, np.ndarray):
        raise TypeError(f"Input image must be a NumPy array, but got {type(image).__name__}.")

    # Validate image dimensions
    if image.ndim not in [2, 3]:
        raise ValueError(f"Input image must be 2D or 3D, but got {image.ndim}D.")

    # Validate brightness_factor and contrast_factor
    if not isinstance(brightness_factor, (int, float)):
        raise TypeError(f"'brightness_factor' must be a float, but got {type(brightness_factor).__name__}.")
    if not isinstance(contrast_factor, (int, float)):
        raise TypeError(f"'contrast_factor' must be a float, but got {type(contrast_factor).__name__}.")

    if brightness_factor <= 0:
        raise ValueError(f"'brightness_factor' must be positive, but got {brightness_factor}.")
    if contrast_factor <= 0:
        raise ValueError(f"'contrast_factor' must be positive, but got {contrast_factor}.")

    # Determine the data type and appropriate clipping range
    dtype = image.dtype
    if np.issubdtype(dtype, np.integer):
        info = np.iinfo(dtype)
    elif np.issubdtype(dtype, np.floating):
        info = np.finfo(dtype)
    else:
        raise ValueError(f"Unsupported image data type: {dtype}.")

    # Convert image to float for processing
    image_float = image.astype(float)

    # Adjust brightness
    image_bright = image_float * brightness_factor

    # Adjust contrast
    mean_intensity = np.mean(image_bright)
    image_contrast = contrast_factor * (image_bright - mean_intensity) + mean_intensity

    # Clip values to the valid range based on original data type
    image_clipped = np.clip(image_contrast, info.min, info.max)

    # Convert back to original data type
    adjusted_image = image_clipped.astype(dtype)

    return adjusted_image