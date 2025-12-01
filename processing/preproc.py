import os
import cv2
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def create_output_folder():
    base_dir = "output"
    os.makedirs(base_dir, exist_ok=True)
    date = datetime.now().strftime("%d%m%Y")

    existing_folders = [
        name
        for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name))
        and name.startswith(f"output_{date}_")
    ]

    next_index = len(existing_folders)

    folder_name = f"output_{date}_{next_index:02d}"
    folder_path = os.path.join(base_dir, folder_name)

    os.makedirs(folder_path)
    return folder_path


def greyscale(in_file_name, out_path):
    img = cv2.imread(f"input/{in_file_name}")

    greyscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, thresh = cv2.threshold(greyscale_img, 127, 255, cv2.THRESH_BINARY)
    thresh_adp = cv2.adaptiveThreshold(
        greyscale_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    cv2.imwrite(f"{out_path}/grayscale_{in_file_name}", greyscale_img)
    cv2.imwrite(f"{out_path}/thresh_{in_file_name}", thresh_adp)


def brightness(in_file_name, out_path):
    # Load the image
    image = cv2.imread("input/{in_file_name}")

    # Plot the original image
    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(image)

    # Adjust the brightness and contrast
    # Adjusts the brightness by adding 10 to each pixel value
    brightness = 10
    # Adjusts the contrast by scaling the pixel values by 2.3
    contrast = 2.3
    image2 = cv2.addWeighted(
        image, contrast, np.zeros(image.shape, image.dtype), 0, brightness
    )

    # Save the image
    cv2.imwrite("modified_image.jpg", image2)

    # Plot the contrast image
    plt.subplot(1, 2, 2)
    plt.title("Brightness & contrast")
    plt.imshow(image2)
    plt.show()


def process_images(out_path):
    input_file_names = [name for name in os.listdir("input")]

    for file_name in input_file_names:
        greyscale(in_file_name=file_name, out_path=out_path)


if __name__ == "__main__":
    path = create_output_folder()
    print(f"Created: {path}")
    # greyscale(in_file_name="test_input.jpg", out_path=path)
    process_images(out_path=path)
