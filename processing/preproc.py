import os
import cv2
from datetime import datetime
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
    _, thresh = cv2.threshold(greyscale_img, 127, 255, cv2.THRESH_BINARY)
    # thresh_adp = cv2.adaptiveThreshold(
    # greyscale_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    # )

    cv2.imwrite(f"{out_path}/grayscale_{in_file_name}", greyscale_img)
    cv2.imwrite(f"{out_path}/thresh_{in_file_name}", thresh)


def increase_contrast(in_file_name, out_path, alpha=1.2, beta=0):
    # Load the image
    image = cv2.imread(f"input/{in_file_name}")
    contrasted_img = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    cv2.imwrite(f"{out_path}/contrast_{in_file_name}", contrasted_img)


def sharpen_image(in_file_name, out_path):
    image = cv2.imread(f"input/{in_file_name}")

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    sharpened_image = cv2.filter2D(image, -1, kernel)

    cv2.imwrite(f"{out_path}/sharpened_{in_file_name}", sharpened_image)


def denoise_image(in_file_name, out_path, ksize=5):
    image = cv2.imread(f"input/{in_file_name}")

    denoised_image = cv2.GaussianBlur(image, (ksize, ksize), 0)

    cv2.imwrite(f"{out_path}/denoised_{in_file_name}", denoised_image)


def process_images(out_path):
    input_file_names = [name for name in os.listdir("input")]

    for file_name in input_file_names:
        greyscale(in_file_name=file_name, out_path=out_path)
        increase_contrast(in_file_name=file_name, out_path=out_path)
        sharpen_image(in_file_name=file_name, out_path=out_path)
        denoise_image(in_file_name=file_name, out_path=out_path)


if __name__ == "__main__":
    path = create_output_folder()
    print(f"Created: {path}")
    # greyscale(in_file_name="test_input.jpg", out_path=path)
    process_images(out_path=path)
