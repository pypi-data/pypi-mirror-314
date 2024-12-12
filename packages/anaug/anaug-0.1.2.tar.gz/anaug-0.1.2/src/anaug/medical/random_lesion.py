import numpy as np
from scipy.ndimage import gaussian_filter
from typing import Tuple, Optional

def generate_perlin_noise(shape: Tuple[int, int], scale: float = 10.0, seed: Optional[int] = None) -> np.ndarray:
    """
    Generates a 2D Perlin noise array.

    Parameters:
    - shape (tuple): Shape of the noise array (height, width).
    - scale (float): Scale of the noise features.
    - seed (int, optional): Seed for random number generator.

    Returns:
    - np.ndarray: 2D array of Perlin noise in range [0, 1].
    """
    if seed is not None:
        np.random.seed(seed)
    height, width = shape
    d = (height // int(scale), width // int(scale))
    gradients = np.random.rand(d[0]+1, d[1]+1, 2) * 2 - 1
    gradients /= np.linalg.norm(gradients, axis=2, keepdims=True) + 1e-10

    def perlin(x, y):
        x0 = x.astype(int)
        y0 = y.astype(int)
        x_frac = x - x0
        y_frac = y - y0

        g00 = gradients[x0, y0]
        g10 = gradients[x0 + 1, y0]
        g01 = gradients[x0, y0 + 1]
        g11 = gradients[x0 + 1, y0 + 1]

        dot00 = g00[:, :, 0] * x_frac + g00[:, :, 1] * y_frac
        dot10 = g10[:, :, 0] * (x_frac - 1) + g10[:, :, 1] * y_frac
        dot01 = g01[:, :, 0] * x_frac + g01[:, :, 1] * (y_frac - 1)
        dot11 = g11[:, :, 0] * (x_frac - 1) + g11[:, :, 1] * (y_frac - 1)

        u = fade(x_frac)
        v = fade(y_frac)

        nx0 = lerp(dot00, dot10, u)
        nx1 = lerp(dot01, dot11, u)

        n = lerp(nx0, nx1, v)
        return n

    def fade(t):
        return 6 * t**5 - 15 * t**4 + 10 * t**3

    def lerp(a, b, t):
        return a + t * (b - a)

    # Create 2D grid for x and y
    x = np.linspace(0, d[0], height, endpoint=False)
    y = np.linspace(0, d[1], width, endpoint=False)
    x, y = np.meshgrid(x, y, indexing='ij')

    noise = perlin(x, y)
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    return noise

def random_lesion(
    image: np.ndarray,
    intensity_range: Tuple[float, float] = (0.2, 0.8),
    size_range: Tuple[int, int] = (10, 50),
    shape: str = 'circle',
    location: Optional[Tuple[int, int]] = None,
    texture_strength: float = 0.5,
    num_lesions: int = 1,
    blending_mode: str = 'additive',
    seed: Optional[int] = None  # Added seed parameter
) -> np.ndarray:
    """
    Generates one or multiple random lesions with specified properties and adds them to the image.

    Parameters:
    - image (np.ndarray): Input image as a 2D numpy array with values in [0, 1].
    - intensity_range (tuple): Min and max intensity for the lesion.
    - size_range (tuple): Min and max size of the lesion (radius for circles or largest dimension for other shapes).
    - shape (str): Shape of the lesion ('circle', 'ellipse', 'irregular').
    - location (tuple, optional): Center of the lesion as (x, y). If None, random locations are chosen.
    - texture_strength (float): Strength of texture variation (0 for smooth, 1 for highly textured).
    - num_lesions (int): Number of lesions to generate.
    - blending_mode (str): Blending mode ('additive', 'overlay').
    - seed (int, optional): Seed for random number generator.

    Returns:
    - np.ndarray: Image with the generated lesion(s).
    """
    if seed is not None:
        np.random.seed(seed)

    # Validate inputs
    if not isinstance(image, np.ndarray) or image.ndim != 2:
        raise ValueError("Input image must be a 2D numpy array.")
    if not (0 <= intensity_range[0] < intensity_range[1] <= 1):
        raise ValueError("intensity_range must have values within [0, 1] and be in increasing order.")
    if not (0 < size_range[0] < size_range[1]):
        raise ValueError("size_range must have positive values in increasing order.")
    if shape not in ['circle', 'ellipse', 'irregular']:
        raise ValueError("shape must be one of 'circle', 'ellipse', or 'irregular'.")
    if not (0 <= texture_strength <= 1):
        raise ValueError("texture_strength must be between 0 and 1.")
    if not isinstance(num_lesions, int) or num_lesions < 1:
        raise ValueError("num_lesions must be a positive integer.")
    if blending_mode not in ['additive', 'overlay']:
        raise ValueError("blending_mode must be either 'additive' or 'overlay'.")

    augmented_image = image.copy()

    for _ in range(num_lesions):
        # Generate lesion properties
        intensity = np.random.uniform(*intensity_range)
        size = np.random.randint(*size_range)

        # Choose location
        if location is None:
            center_x = np.random.randint(size, image.shape[1] - size)
            center_y = np.random.randint(size, image.shape[0] - size)
        else:
            center_x, center_y = location
            if not (0 <= center_x < image.shape[1] and 0 <= center_y < image.shape[0]):
                raise ValueError("Location must be within the bounds of the image.")
            # Ensure lesion fits within the image
            if not (size <= center_x < image.shape[1] - size and size <= center_y < image.shape[0] - size):
                raise ValueError("Lesion size with given location exceeds image boundaries.")

        # Create lesion mask
        x, y = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        if shape == 'circle':
            distance_sq = (x - center_x) ** 2 + (y - center_y) ** 2
            mask = distance_sq <= size ** 2
            lesion = np.zeros_like(image)
            lesion[mask] = intensity
        elif shape == 'ellipse':
            axis_x = size * np.random.uniform(0.5, 1.5)
            axis_y = size
            distance = (((x - center_x) / axis_x) ** 2 + ((y - center_y) / axis_y) ** 2)
            mask = distance <= 1
            lesion = np.zeros_like(image)
            lesion[mask] = intensity
        elif shape == 'irregular':
            # Generate Perlin noise for more realistic textures
            noise = generate_perlin_noise(image.shape, scale=size / 5, seed=seed)
            lesion = noise * intensity
            # Create mask based on noise threshold
            threshold = 0.5
            mask = noise > threshold
            lesion = np.zeros_like(image)
            lesion[mask] = intensity

        # Add texture
        if shape != 'irregular':
            texture = np.random.normal(0, 1, image.shape)
            texture = gaussian_filter(texture, sigma=size * 0.5 * (1 - texture_strength))
            texture = (texture - texture.min()) / (texture.max() - texture.min())
            texture = texture * texture_strength
            lesion[mask] += texture[mask] * intensity  # Apply texture only within the mask
            lesion = np.clip(lesion, 0, 1)

        # Blend lesion with image
        if blending_mode == 'additive':
            augmented_image = np.clip(augmented_image + lesion, 0, 1)
        elif blending_mode == 'overlay':
            mask = lesion > 0
            augmented_image[mask] = augmented_image[mask] * (1 - intensity) + intensity
            augmented_image = np.clip(augmented_image, 0, 1)

    return augmented_image
