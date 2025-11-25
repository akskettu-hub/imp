import os
from datetime import datetime
import re


def create_input_folder(dir: str):
    if os.path.exists(dir):
        print(f"Directory '{dir}' already exists")
        return

    try:
        os.makedirs(dir)
        print(f"Created directory: {dir}")

    except OSError as e:
        print(f"Error creating directory '{dir}': {e}")


def create_output_folder():
    base_dir = "postp_output"
    os.makedirs(base_dir, exist_ok=True)
    date = datetime.now().strftime("%d%m%Y")

    existing_folders = [
        name
        for name in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, name))
        and name.startswith(f"postp_output_{date}_")
    ]

    next_index = len(existing_folders)

    folder_name = f"postp_output_{date}_{next_index:02d}"
    folder_path = os.path.join(base_dir, folder_name)

    os.makedirs(folder_path)
    print(f"Created output directory: {folder_path}")
    return folder_path


def process_txt(in_path="postp_input", out_path="postp_output"):
    input_file_names = [name for name in os.listdir(in_path)]

    for file_name in input_file_names:
        with open(f"{in_path}/{file_name}", "r", encoding="utf-8") as f:
            text = f.read().replace("\n", " ").replace("\r", "")
            text = re.sub(r"\s+", " ", text).strip()

        with open(f"{out_path}/{file_name}", "w", encoding="utf-8") as f:
            f.write(text)

    print(f"Processed {len(input_file_names)} files")


def remove_linebrakes(in_path=None):
    out_path = create_output_folder()

    if in_path is not None:
        process_txt(in_path=in_path, out_path=out_path)

    else:
        process_txt(out_path=out_path)


if __name__ == "__main__":
    path = create_output_folder()
    print(f"Created: {path}")
    process_txt(out_path=path)
