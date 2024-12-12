# AN-Augment
[![package-publish](https://github.com/lunovian/an-augment/actions/workflows/python-publish.yml/badge.svg)](https://github.com/lunovian/an-augment/actions/workflows/python-publish.yml)
[![pages-publish](https://github.com/lunovian/an-augment/actions/workflows/pages-publish.yml/badge.svg)](https://github.com/lunovian/an-augment/actions/workflows/pages-publish.yml)

**AN-Augment** (**Advanced and Novel Augmentation**) is a Python library offering advanced and innovative data augmentation techniques for diverse domains, from medical imaging to environmental data. It enhances dataset diversity, improving model robustness and performance across applications.

## Augmentations

**AN-Augment** provides a wide range of built-in augmentations to enhance your datasets across multiple domains:

### **Core Features:**

- **Fine-Grained Control**: Adjustable parameters for precise transformation intensity and probability.
- **Batch Processing & Randomization**: Apply augmentations to image/data batches with flexible randomization settings.
- **Visualization Tools**: Easily visualize original and augmented data side-by-side for quick quality checks.

### **Multi-Domain Augmentations:**

- **Medical Imaging**:
  - [ ] **Augment Metadata for Labels and Masks**: Streamline label and mask processing during augmentation.
  - [ ] **Add GAN-Based Synthetic Image Generation**: Generate synthetic medical images to enrich datasets.
  - [ ] **Random Block Masks for Occlusion Simulation**: Simulate occlusions for robustness testing.
  - [ ] **3D Elastic Transformations for Volumetric Data**: Apply elastic deformations for 3D medical volumes.
  - [ ] **Fourier Transform Filters for Frequency-Based Augmentation**: Enhance feature learning with frequency-domain transformations.
  - [ ] **Contrast-Enhanced Region Augmentation**: Improve model sensitivity to contrast-specific areas.
  - [ ] **Simulated Lesions/Anomalies Augmentation**: Add realistic lesions to improve rare anomaly detection.

- **Mechanical Simulations**:
  - **Add Stress-Based Transformations**: Simulate structural stress conditions for robustness.
  - **Dynamic Scaling and Rotation**: Introduce scaling and rotational effects to mechanical structures.
  - **Apply Structural Noise Augmentation**: Add noise specific to mechanical patterns to enrich datasets.
  - **Load Simulation Augmentation**: Simulate load-based distortions and deformations.

- **Environmental Data**:
  - **Simulate Cloud Occlusions**: Apply cloud-like occlusions for satellite and environmental imagery.
  - **Add Noise for Sensor Simulation**: Introduce sensor-based noise patterns for realism.
  - **Spatial Scaling and Shifting**: Apply shifts and scaling to spatial data.
  - **Enhance Terrain Patterns**: Augment terrain-based features with synthetic distortions.

- **Water Systems**:
  - **Wave Simulation Augmentation**: Generate wave-like distortions for water bodies.
  - **Flow Distortion Augmentation**: Simulate flow patterns in water datasets.
  - **Add Scaling Factors for Dynamic Modeling**: Apply scaling for dynamic hydrodynamic modeling.
  - **Turbulence Simulation**: Introduce turbulence effects for water-based data.

## Installation

To install **AN-Augment**, use pip:

```bash
pip install an-augment
```

Alternatively, you can install the latest development version from the repository:

```bash
git clone https://github.com/lunovian/an-augment.git
cd an-augment
pip install -r requirements.txt
```

## Usage

Here’s a quick example of how to use **AN-Augment** for medical imaging augmentations:

```python
import cv2
import matplotlib.pyplot as plt
from an_augment.default import scale, flip, noise, random_rotation, random_crop, intensity, elastic_deformation, occlusion, blur

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

```

Here is an example of the original image and the augmented result:

| Original Image                     | Augmented Image                     |
|------------------------------------|-------------------------------------|
| ![Original Image](images/original_image.png)  | ![Augmented Image](images/augmented_image.png) |

For other domains (e.g., mechanical or environmental), the process is similar—just import the relevant augmentation module (e.g., `MechanicalAugmentation`, `EnvironmentalAugmentation`, etc.).

## Contributing

We welcome contributions! Fork the repository, make your changes, and submit a pull request. You can contribute new augmentation types or improve existing ones.

## License

**AN-Augment** is licensed under the Apache-2.0 License.
