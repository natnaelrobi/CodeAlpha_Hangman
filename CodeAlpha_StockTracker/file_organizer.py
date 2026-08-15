import os
import shutil
from pathlib import Path

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".json"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"]
}


class FileOrganizer:
    # Lambda function to determine file category based on extension
    get_category = lambda self, ext: next(
        (cat for cat, exts in FILE_CATEGORIES.items() if ext.lower() in exts),
        "Others"
    )

    def __init__(self, target_directory):
        self.target_path = Path(target_directory).resolve()
        self.moved_counts = {}
        self.total_files = 0

    def validate_directory(self):
        if not self.target_path.exists():
            raise FileNotFoundError(f"Directory '{self.target_path}' does not exist.")
        if not self.target_path.is_dir():
            raise NotADirectoryError(f"Path '{self.target_path}' is not a valid directory.")

    def organize(self):
        self.validate_directory()
        print(f"\nScanning and organizing: {self.target_path}\n" + "-" * 50)

        # For loop to iterate through all items in the directory
        for item in self.target_path.iterdir():
            try:
                # Conditional checks for valid files and exclusion rules
                if item.is_file() and item.name != "portfolio_report.csv":
                    extension = item.suffix
                    if not extension:
                        continue

                    # Invoking the lambda function method to categorize
                    category = self.get_category(extension)
                    dest_folder = self.target_path / category
                    dest_folder.mkdir(exist_ok=True)

                    dest_path = dest_folder / item.name
                    counter = 1

                    # While loop to handle naming collisions safely
                    while dest_path.exists():
                        dest_path = dest_folder / f"{item.stem}_{counter}{extension}"
                        counter += 1

                    shutil.move(str(item), str(dest_path))
                    self.moved_counts[category] = self.moved_counts.get(category, 0) + 1
                    self.total_files += 1
                    print(f"Moved: {item.name} ➡️ {category}/")

            except PermissionError:
                print(f"❌ Permission denied: Cannot move '{item.name}'.")
            except Exception as e:
                print(f"❌ Error processing '{item.name}': {e}")

        self.print_summary()

    def print_summary(self):
        print("\n" + "=" * 50)
        print(f"✨ Organization Complete! Total files moved: {self.total_files}")
        for category, count in self.moved_counts.items():
            print(f"   - {category}: {count} file(s)")
        print("=" * 50)


def main():
    print("=" * 50)
    print("      CODEALPHA PYTHON INTERNSHIP        ")
    print("      TASK 3: AUTOMATED FILE ORGANIZER   ")
    print("=" * 50)

    # While loop for robust user input error recovery
    while True:
        target = input("Enter target directory path (leave blank for current dir): ").strip()
        if not target:
            target = "."

        try:
            organizer = FileOrganizer(target)
            organizer.organize()
            break
        except (FileNotFoundError, NotADirectoryError) as e:
            print(f"❌ {e}\nPlease enter a valid path.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()