import tkinter as tk
from tkinter import filedialog
import re
import os

def select_file():
    root = tk.Tk()
    root.withdraw()
    try:
        filename = filedialog.askopenfilename()
        if not filename:
            print("No file selected. Exiting.")
            exit()pip freeze > requirements.txt
        return filename
    except Exception as e:
        print(f"Error in file selection: {e}")
        exit()

def clean_line(line):
    # Updated regex pattern to match the email and password, stopping at a space or second colon
    match = re.match(r'(\S+@\S+?):(\S+?)(?=\s|:|$)', line)
    if match:
        email, password = match.groups()
        return f'{email}:{password}\n'
    return None

def process_chunks(file_object, chunk_size=1000):
    while True:
        lines = [line for line in file_object]
        if not lines:
            break
        for line in lines:
            cleaned_line = clean_line(line)
            if cleaned_line:
                yield cleaned_line

def process_and_save_file(original_filename, chunk_size=1000):
    new_filename = f"{os.path.splitext(original_filename)[0]}_cleaned.txt"

    try:
        with open(original_filename, 'r') as infile, open(new_filename, 'w') as outfile:
            chunk_generator = process_chunks(infile, chunk_size)
            for cleaned_line in chunk_generator:
                outfile.write(cleaned_line)
        return new_filename
    except Exception as e:
        print(f"Error processing the file: {e}")
        exit()

def main():
    print("Starting file processing...")
    filename = select_file()
    new_filename = process_and_save_file(filename)
    print(f"Finished processing. The cleaned file is saved as '{new_filename}'.")

if __name__ == "__main__":
    main()
