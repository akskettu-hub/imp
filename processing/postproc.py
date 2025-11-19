import os
from datetime import datetime
import re


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
    return folder_path


def process_txt(out_path):
    input_file_names = [name for name in os.listdir("postp_input")]

    for file_name in input_file_names:
        with open(f"postp_input/{file_name}", "r", encoding="utf-8") as f:
            text = f.read().replace("\n", " ").replace("\r", "")
            text = re.sub(r"\s+", " ", text).strip()

        with open(f"{out_path}/{file_name}", "w", encoding="utf-8") as f:
            f.write(text)


if __name__ == "__main__":
    path = create_output_folder()
    print(f"Created: {path}")
    process_txt(out_path=path)
