import numpy as np
from typing import Optional


def noise(
    image: np.ndarray,
    noise_type: str = 'gaussian',
    noise_intensity: float = 0.05,
    scale: Optional[float] = None
) -> np.ndarray:
    """
    Adds noise to the image to simulate different scanning conditions.

    Parameters
    ----------
    image : np.ndarray
        Input image as a 2D (grayscale) or 3D (multi-channel/color) NumPy array.
        For floating-point images, pixel values should be in [0, 1].
        For integer images (e.g., uint8), pixel values should be in [0, 255].
    noise_type : str, optional
        Type of noise to add. Supported types:
        - 'gaussian': Adds Gaussian noise.
        - 'salt_and_pepper': Adds salt-and-pepper noise.
        - 'poisson': Adds Poisson noise.
        Default is 'gaussian'.
    noise_intensity : float, optional
        Intensity of the noise.
        - For 'gaussian', it represents the standard deviation (must be non-negative).
        - For 'salt_and_pepper', it represents the proportion of affected pixels (0 <= noise_intensity <= 1).
        - For 'poisson', it represents the scaling factor (must be non-negative).
        Default is 0.05.
    scale : float, optional
        Scaling factor for Poisson noise. Relevant only if `noise_type` is 'poisson'.
        Must be positive. If not provided, defaults to 1.0.

    Returns
    -------
    np.ndarray
        Image with added noise, maintaining the original shape and data type.

    Raises
    ------
    TypeError
        If the input image is not a NumPy array or if parameters are of incorrect types.
    ValueError
        If the noise type is unsupported, if noise intensity is invalid, or if required parameters are missing.

    Examples
    --------
    >>> import numpy as np
    >>> from anaug.default.noise import noise
    >>> # Grayscale image example with Gaussian noise
    >>> gray_image = np.random.rand(128, 128).astype(np.float32)
    >>> noisy_image = noise(gray_image, noise_type='gaussian', noise_intensity=0.1)

    >>> # Color image example with salt-and-pepper noise
    >>> color_image = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)
    >>> noisy_color = noise(color_image, noise_type='salt_and_pepper', noise_intensity=0.05)

    >>> # Poisson noise with custom scale
    >>> poisson_noisy = noise(gray_image, noise_type='poisson', noise_intensity=5.0, scale=10.0)
    """
    # Validate input type
    if not isinstance(image, np.ndarray):
        raise TypeError(f"Input image must be a NumPy array, but got {type(image).__name__}.")

    # Validate image dimensions
    if image.ndim not in [2, 3]:
        raise ValueError(f"Input image must be 2D or 3D, but got {image.ndim}D.")

    # Validate supported data types
    supported_dtypes = {np.uint8, np.float32, np.float64}
    if image.dtype.type not in supported_dtypes:
        raise ValueError(f"Unsupported image data type: {image.dtype.type}. Supported types are: {supported_dtypes}.")

    # Validate noise_type
    supported_noise_types = {'gaussian', 'salt_and_pepper', 'poisson'}
    if not isinstance(noise_type, str):
        raise TypeError(f"'noise_type' must be a string, but got {type(noise_type).__name__}.")
    if noise_type not in supported_noise_types:
        raise ValueError(f"Unsupported noise type '{noise_type}'. Supported types are: {supported_noise_types}.")

    # Validate noise_intensity
    if not isinstance(noise_intensity, (int, float)):
        raise TypeError(f"'noise_intensity' must be a float, but got {type(noise_intensity).__name__}.")

    # Adjust validation to allow noise_intensity=0.0
    if noise_type == 'gaussian':
        if noise_intensity < 0:
            raise ValueError(f"For 'gaussian' noise, 'noise_intensity' must be non-negative, but got {noise_intensity}.")
    elif noise_type == 'salt_and_pepper':
        if not (0 <= noise_intensity <= 1):
            raise ValueError(f"For 'salt_and_pepper' noise, 'noise_intensity' must be between 0 and 1, but got {noise_intensity}.")
    elif noise_type == 'poisson':
        if noise_intensity < 0:
            raise ValueError(f"For 'poisson' noise, 'noise_intensity' (scale) must be non-negative, but got {noise_intensity}.")

    # Determine the valid range based on data type
    dtype = image.dtype.type
    if dtype == np.uint8:
        min_val, max_val = 0, 255
    elif dtype in {np.float32, np.float64}:
        min_val, max_val = 0.0, 1.0
    else:
        # This block should be unreachable due to earlier dtype validation
        raise ValueError(f"Unsupported image data type: {dtype}.")

    # If noise_intensity is zero, return the original image
    if noise_intensity == 0.0:
        return image.copy()

    # Gaussian Noise
    if noise_type == 'gaussian':
        mean = 0
        std = noise_intensity
        gauss = np.random.normal(mean, std, image.shape).astype(dtype)
        noisy_image = image + gauss
        noisy_image = np.clip(noisy_image, min_val, max_val)
        return noisy_image

    # Salt-and-Pepper Noise
    elif noise_type == 'salt_and_pepper':
        noisy_image = image.copy()
        total_pixels = image.size
        num_salt = int(np.ceil(noise_intensity * total_pixels * 0.5))
        num_pepper = int(np.ceil(noise_intensity * total_pixels * 0.5))

        # Generate flat indices
        noisy_image_flat = noisy_image.flatten()
        coords_salt = np.random.choice(total_pixels, num_salt, replace=False)
        coords_pepper = np.random.choice(total_pixels, num_pepper, replace=False)

        # Apply salt noise
        noisy_image_flat[coords_salt] = max_val

        # Apply pepper noise
        noisy_image_flat[coords_pepper] = min_val

        # Reshape back to original shape
        noisy_image = noisy_image_flat.reshape(image.shape)

        return noisy_image

    # Poisson Noise
    elif noise_type == 'poisson':
        if scale is None:
            scale = 1.0
        elif not isinstance(scale, (int, float)):
            raise TypeError(f"'scale' must be a float, but got {type(scale).__name__}.")
        if scale <= 0 and noise_intensity != 0.0:
            raise ValueError(f"'scale' must be positive, but got {scale}.")

        if dtype in {np.float32, np.float64}:
            scaled_image = image * noise_intensity * scale
            # Ensure no negative values
            if np.any(scaled_image < 0):
                raise ValueError("Scaled image contains negative values, which are not allowed for Poisson noise.")

            noisy_image = np.random.poisson(scaled_image).astype(float) / (noise_intensity * scale)
        elif dtype == np.uint8:
            # For uint8 images, ensure scaling to avoid overflow
            scaled_image = image.astype(np.float64) * noise_intensity * scale
            noisy_image = np.random.poisson(scaled_image).astype(float) / (noise_intensity * scale)

        # Clip to valid range
        noisy_image = np.clip(noisy_image, min_val, max_val)

        # Preserve original dtype
        if dtype == np.uint8:
            # Round before casting to avoid truncation
            noisy_image = np.round(noisy_image).astype(dtype)
        else:
            noisy_image = noisy_image.astype(dtype)

        return noisy_image

    else:
        # This else block is theoretically unreachable due to earlier validation
        raise ValueError(f"Unsupported noise type '{noise_type}'.")
