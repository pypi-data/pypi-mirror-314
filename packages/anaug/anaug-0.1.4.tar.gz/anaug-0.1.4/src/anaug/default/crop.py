import numpy as np
from typing import Tuple

def crop(
    image: np.ndarray,
    top: int,
    left: int,
    height: int,
    width: int,
    *,
    adjust_if_exceeds: bool = False,
    pad_value: Tuple[int, ...] = (0,)
) -> np.ndarray:
    """
    Crop an image to the specified size and position.

    Parameters:
    ----------
    image : np.ndarray
        Input image as a 2D (grayscale) or 3D (color) NumPy array.
    top : int
        Top pixel coordinate (row index).
    left : int
        Left pixel coordinate (column index).
    height : int
        Desired height of the cropped image.
    width : int
        Desired width of the cropped image.
    adjust_if_exceeds : bool, optional
        If set to True, adjusts the crop parameters to fit within the image boundaries
        instead of raising an error. Defaults to False.
    pad_value : Tuple[int, ...], optional
        Value to use for padding if `adjust_if_exceeds` is True and the crop exceeds image boundaries.
        The length of the tuple should match the number of channels in the image.
        Defaults to (0,).

    Returns:
    -------
    np.ndarray
        Cropped image with the same number of channels and dtype as input.

    Raises:
    ------
    TypeError
        If input parameters are not of the expected types.
    ValueError
        If crop parameters are invalid or exceed image boundaries when `adjust_if_exceeds` is False.
        If `pad_value` length does not match number of channels in image.

    Examples:
    --------
    ```python
    import cv2
    import matplotlib.pyplot as plt

    # Load a sample color image
    image = cv2.imread('path_to_image.jpg')

    # Define crop parameters
    top, left, height, width = 50, 100, 200, 300

    # Perform cropping
    cropped_image = crop(image, top, left, height, width)

    # Display the original and cropped images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Cropped Image")
    plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.tight_layout()
    plt.show()
    ```
    """
    # ---------------------
    # Type Validation
    # ---------------------
    if not isinstance(image, np.ndarray):
        raise TypeError(f"Expected 'image' to be a NumPy array, but got {type(image).__name__}.")

    if image.ndim not in [2, 3]:
        raise ValueError(f"Input image must be 2D or 3D, but got {image.ndim}D.")

    for param, name in zip([top, left, height, width], ['top', 'left', 'height', 'width']):
        if not isinstance(param, int):
            raise TypeError(f"Parameter '{name}' must be an integer, but got {type(param).__name__}.")

    if height <= 0 or width <= 0:
        raise ValueError("Parameters 'height' and 'width' must be positive integers.")

    image_height, image_width = image.shape[:2]

    # ---------------------
    # Boundary Validation
    # ---------------------
    exceeds = (
        top < 0 or left < 0 or
        top + height > image_height or
        left + width > image_width
    )

    if exceeds and not adjust_if_exceeds:
        raise ValueError(
            f"Invalid crop parameters: (top={top}, left={left}, height={height}, width={width}) "
            f"exceed image dimensions ({image_height}, {image_width})."
        )

    if not exceeds:
        # Perform Cropping
        cropped = image[top:top + height, left:left + width].copy()
        return cropped

    # If exceeds and adjust_if_exceeds == True
    # Adjust crop parameters
    new_top = max(top, 0)
    new_left = max(left, 0)
    new_bottom = min(top + height, image_height)
    new_right = min(left + width, image_width)
    cropped = image[new_top:new_bottom, new_left:new_right].copy()

    # Calculate required padding
    pad_bottom = height - (new_bottom - new_top)
    pad_right = width - (new_right - new_left)

    if pad_bottom > 0 or pad_right > 0:
        if image.ndim == 2:
            # Grayscale Image
            pad_width_tuple = ((0, pad_bottom), (0, pad_right))
            if isinstance(pad_value, tuple):
                if len(pad_value) != 1:
                    raise ValueError(
                        f"Length of 'pad_value' ({len(pad_value)}) does not match number of channels (1)."
                    )
                pad_val = pad_value[0]
            else:
                pad_val = pad_value
            cropped = np.pad(
                cropped,
                pad_width=pad_width_tuple,
                mode='constant',
                constant_values=pad_val
            )
        else:
            # Multi-channel Image
            num_channels = image.shape[2]
            if not isinstance(pad_value, tuple):
                raise TypeError(f"Parameter 'pad_value' must be a tuple for multi-channel images, got {type(pad_value).__name__}.")
            if len(pad_value) != num_channels:
                raise ValueError(
                    f"Length of 'pad_value' ({len(pad_value)}) does not match number of channels ({num_channels})."
                )
            # Pad each channel individually
            padded_channels = []
            for c in range(num_channels):
                channel = cropped[:, :, c]
                pad_val = pad_value[c]
                padded_channel = np.pad(
                    channel,
                    pad_width=((0, pad_bottom), (0, pad_right)),
                    mode='constant',
                    constant_values=pad_val
                )
                padded_channels.append(padded_channel)
            # Stack channels back
            cropped = np.stack(padded_channels, axis=2)

    return cropped.copy()