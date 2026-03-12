import os
import csv

OUTPUT_FOLDER = "outputs"


def export_txt(content):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    path = os.path.join(OUTPUT_FOLDER, "digital_notes.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path


def export_csv(tasks):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    path = os.path.join(OUTPUT_FOLDER, "tasks.csv")

    with open(path, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Task", "Status"])

        for task in tasks:
            writer.writerow([task, "Pending"])

    return path