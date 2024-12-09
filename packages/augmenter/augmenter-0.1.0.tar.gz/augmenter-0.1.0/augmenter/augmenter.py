import os
import cv2
import albumentations as A
import random
from pathlib import Path


class Augmenter:
    def __init__(self):
        # Define available transformations
        self.transforms = {
            "flip": A.HorizontalFlip(p=1),
            "rotate": A.Rotate(limit=45, p=1),
            "blur": A.GaussianBlur(blur_limit=(3, 7), p=1),
            "brightness_contrast": A.RandomBrightnessContrast(p=1),
            "grayscale": A.ToGray(p=1),
            "noise": A.GaussNoise(var_limit=(10.0, 50.0), p=1),
            "sharpen": A.Sharpen(alpha=(0.2, 0.5), p=1),
            "crop": A.RandomResizedCrop(height=200, width=200, scale=(0.8, 1.0), p=1),
            # Add more augmentations as needed
        }

    def apply(self, image_dir, augmentations, save_path, mixing=False, variations_per_image=1):
        """
        Apply augmentations to all images in a directory, including subdirectories.

        Args:
            image_dir (str): Path to the root directory containing images.
            augmentations (list): List of augmentations to apply.
            save_path (str): Directory to save augmented images (with preserved structure).
            mixing (bool): If True, apply random combinations of augmentations to each image.
            variations_per_image (int): Number of augmented variations to create per image (only when mixing=True).

        Returns:
            int: Count of augmented images created.
        """
        if not os.path.exists(image_dir):
            raise ValueError(f"Image directory '{image_dir}' does not exist!")

        if not save_path:
            raise ValueError("Save path must be specified!")

        if mixing and variations_per_image < 1:
            raise ValueError("Variations per image must be at least 1 when mixing is enabled.")

        # Create save directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)

        augmented_count = 0

        # Walk through the directory structure
        for root, _, files in os.walk(image_dir):
            relative_path = os.path.relpath(root, image_dir)
            save_subdir = os.path.join(save_path, relative_path)
            os.makedirs(save_subdir, exist_ok=True)

            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Load the image
                image = cv2.imread(file_path)
                if image is None:
                    print(f"Skipping file '{file_name}', not a valid image.")
                    continue

                if mixing:
                    for i in range(variations_per_image):
                        num_augmentations = random.randint(1, len(augmentations))
                        selected_augmentations = random.sample(augmentations, num_augmentations)
                        augmented_image = image

                        for aug in selected_augmentations:
                            transform = self.transforms.get(aug)
                            if transform:
                                augmented_image = transform(image=augmented_image)["image"]

                        augmented_count += 1
                        base_name, ext = os.path.splitext(file_name)
                        save_file_path = os.path.join(save_subdir, f"{base_name}_mix_{i+1}{ext}")
                        cv2.imwrite(save_file_path, augmented_image)
                else:
                    # Apply each augmentation individually
                    for aug in augmentations:
                        transform = self.transforms.get(aug)
                        if not transform:
                            print(f"Skipping unknown augmentation '{aug}'.")
                            continue

                        augmented_image = transform(image=image)["image"]
                        augmented_count += 1

                        # Save augmented image
                        base_name, ext = os.path.splitext(file_name)
                        save_file_path = os.path.join(save_subdir, f"{base_name}_{aug}{ext}")
                        cv2.imwrite(save_file_path, augmented_image)

        return augmented_count
