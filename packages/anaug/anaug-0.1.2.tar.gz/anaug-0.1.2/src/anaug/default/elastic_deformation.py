import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
from typing import Optional, Union


def elastic_deformation(
    image: Union[np.ndarray, np.generic],
    alpha: float = 34.0,
    sigma: float = 4.0,
    random_state: Optional[Union[int, np.random.RandomState]] = None
) -> np.ndarray:
    """
    Apply elastic deformation to an image using displacement fields.

    Parameters
    ----------
    image : np.ndarray
        Input image as a 2D (grayscale) or 3D (color) NumPy array.
    alpha : float, optional
        Scale factor that controls the intensity of the deformation. Must be positive.
        Default is 34.0.
    sigma : float, optional
        Standard deviation of the Gaussian kernel that controls the smoothness of the deformation.
        Must be positive. Default is 4.0.
    random_state : int or np.random.RandomState, optional
        Seed or RandomState instance for reproducibility. If None, a random seed is used.
        Default is None.

    Returns
    -------
    np.ndarray
        Deformed image with the same shape and dtype as the input.

    Raises
    ------
    TypeError
        If `image` is not a NumPy array or if `random_state` is not of the correct type.
    ValueError
        If `alpha` or `sigma` are non-positive, or if `image` has unsupported dimensions.

    Examples
    --------
    >>> import cv2
    >>> import matplotlib.pyplot as plt
    >>> from elastic_deformation import elastic_deformation  # Replace with actual module path
    >>> image = cv2.imread('path_to_image.jpg', cv2.IMREAD_GRAYSCALE)
    >>> deformed_image = elastic_deformation(image, alpha=34, sigma=4, random_state=42)
    >>> plt.imshow(deformed_image, cmap='gray')
    >>> plt.show()
    """
    # ---------------------
    # Type Validation
    # ---------------------
    if not isinstance(image, np.ndarray):
        raise TypeError(f"Expected 'image' to be a NumPy array, but got {type(image).__name__}.")

    if image.ndim not in [2, 3]:
        raise ValueError(f"Input image must be 2D or 3D, but got {image.ndim}D.")

    if not isinstance(alpha, (int, float)) or alpha <= 0:
        raise ValueError(f"'alpha' must be a positive float, but got {alpha}.")

    if not isinstance(sigma, (int, float)) or sigma <= 0:
        raise ValueError(f"'sigma' must be a positive float, but got {sigma}.")

    if random_state is None:
        rng = np.random.RandomState()
    elif isinstance(random_state, int):
        rng = np.random.RandomState(random_state)
    elif isinstance(random_state, np.random.RandomState):
        rng = random_state
    else:
        raise TypeError(f"'random_state' must be None, int, or np.random.RandomState, but got {type(random_state).__name__}.")

    shape = image.shape
    ndim = image.ndim

    # ---------------------
    # Generate Displacement Fields
    # ---------------------
    displacement_fields = []
    for axis in range(ndim):
        # Generate random displacement field with the same shape as the image
        random_field = rng.rand(*shape) * 2 - 1  # Values in [-1, 1]
        displacement = gaussian_filter(random_field, sigma=sigma, mode='constant', cval=0) * alpha
        displacement_fields.append(displacement)

    # ---------------------
    # Create Meshgrid for Coordinates
    # ---------------------
    if ndim == 2:
        # For 2D images, axes are (y, x)
        y, x = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), indexing='ij')
        indices = (y + displacement_fields[0], x + displacement_fields[1])
    elif ndim == 3:
        # For 3D images, axes are (z, y, x)
        z, y, x = np.meshgrid(
            np.arange(shape[0]),
            np.arange(shape[1]),
            np.arange(shape[2]),
            indexing='ij'
        )
        indices = (
            z + displacement_fields[0],
            y + displacement_fields[1],
            x + displacement_fields[2]
        )

    # ---------------------
    # Apply Elastic Deformation
    # ---------------------
    deformed_image = map_coordinates(
        image,
        indices,
        order=1,
        mode='reflect'
    ).reshape(shape)

    return deformed_image