import cv2
import matplotlib.pyplot as plt
from anaug.default import scale, flip, noise, random_rotation, random_crop, intensity, elastic_deformation, occlusion, blur

# Load the image
image_path = "images/mri.jpg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if image is None:
    raise FileNotFoundError(f"The image at path '{image_path}' could not be loaded. Ensure the path is correct.")

image = image / 255.0  # Normalize the image to [0, 1]

# Define augmentation parameters
params = {
    'blur': {'blur_radius': 2},
    'elastic_deformation': {'alpha': 30, 'sigma': 4},
    'flip': {'flip_horizontal': True, 'flip_vertical': False},
    'intensity': {'brightness_factor': 1.2, 'contrast_factor': 1.3},
    'noise': {'noise_type': 'gaussian', 'noise_intensity': 0.1},
    'occlusion': {'mask_shape': 'rectangle', 'mask_size_range': (0.1, 0.2)},
    'random_rotation': {'angle_range': (-15, 15)},
    'random_crop': {'crop_size': (0.8, 0.8), 'scaling_factor': 1.0},
    'scale': {'scale_factor': 0.8}
}

# Apply augmentations (manually applying each augmentation)
try:
    augmented_image = blur(image, **params['blur'])
    augmented_image = elastic_deformation(image, **params['elastic_deformation'])
    augmented_image = flip(augmented_image, **params['flip'])
    augmented_image = intensity(augmented_image, **params['intensity'])
    augmented_image = noise(augmented_image, **params['noise'])
    augmented_image = occlusion(augmented_image, **params['occlusion'])
    augmented_image = random_rotation(augmented_image, **params['random_rotation'])
    augmented_image = random_crop(augmented_image, **params['random_crop'])
    augmented_image = scale(augmented_image, **params['scale'])
except Exception as e:
    raise RuntimeError(f"An error occurred while applying augmentations: {e}")

# Display original and augmented images
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(image, cmap="gray")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("Augmented Image")
plt.imshow(augmented_image, cmap="gray")
plt.axis("off")

plt.tight_layout()
plt.show()
