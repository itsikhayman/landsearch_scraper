import os

class Step4:
    def prompt_to_open_file(self, file_path):
        open_file = input(f"Do you want to open the file now? (yes/no): ").strip().lower()
        if open_file == 'yes':
            os.system(f'start excel.exe "{file_path}"')
