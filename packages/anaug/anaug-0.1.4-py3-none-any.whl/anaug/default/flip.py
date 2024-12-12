import numpy as np
from typing import Union, List


def flip(
    image: np.ndarray,
    axes: Union[str, List[str]] = 'horizontal'
) -> np.ndarray:
    """
    Flips the image horizontally, vertically, or along specified axes.

    Parameters
    ----------
    image : np.ndarray
        Input image as a 2D (grayscale) or 3D (multi-channel) NumPy array.
    axes : Union[str, List[str]], optional
        Specifies the axes to flip the image along.
        - 'horizontal': Flip left-right.
        - 'vertical': Flip up-down.
        - 'both': Flip both horizontally and vertically.
        - List[str]: Specify a list of axes to flip, e.g., ['horizontal', 'vertical'].
        Default is 'horizontal'.

    Returns
    -------
    np.ndarray
        Flipped image based on specified axes.

    Raises
    ------
    TypeError
        If the input image is not a NumPy array or if axes are not specified correctly.
    ValueError
        If the input image has invalid dimensions or if invalid axes are specified.

    Examples
    --------
    >>> import numpy as np
    >>> from anaug.default.flip import flip
    >>> image = np.array([[1, 2], [3, 4]])
    >>> flip(image, axes='horizontal')
    array([[2, 1],
           [4, 3]])
    
    >>> flip(image, axes='vertical')
    array([[3, 4],
           [1, 2]])
    
    >>> flip(image, axes='both')
    array([[4, 3],
           [2, 1]])
    
    >>> flip(image, axes=['horizontal', 'vertical'])
    array([[4, 3],
           [2, 1]])
    """
    # Validate input type
    if not isinstance(image, np.ndarray):
        raise TypeError(f"Input image must be a NumPy array, but got {type(image).__name__}.")

    # Validate image dimensions
    if image.ndim not in [2, 3]:
        raise ValueError(f"Input image must be 2D or 3D, but got {image.ndim}D.")

    # Normalize axes to a list
    if isinstance(axes, str):
        axes = [axes]
    elif isinstance(axes, list):
        if not all(isinstance(axis, str) for axis in axes):
            raise TypeError("All elements in the axes list must be strings.")
    else:
        raise TypeError(f"'axes' must be a string or a list of strings, but got {type(axes).__name__}.")

    # Define valid axes
    valid_axes = {'horizontal', 'vertical'}
    for axis in axes:
        if axis not in valid_axes:
            raise ValueError(f"Invalid axis '{axis}'. Valid axes are 'horizontal' and 'vertical'.")

    # Apply flips based on specified axes
    flipped_image = image.copy()
    for axis in axes:
        if axis == 'horizontal':
            flipped_image = np.fliplr(flipped_image)
        elif axis == 'vertical':
            flipped_image = np.flipud(flipped_image)

    return flipped_image