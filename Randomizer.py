import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import urllib.request
import zipfile
import shutil

# URL and filename for the Celeste graphics dump
graphics_dump_url = "https://www.dropbox.com/scl/fi/tvr8hafluov3no8tmmpzm/Celeste-Graphics-Dump-v1400.zip?rlkey=oeb5tlngtftl9p4wb39rrnpg4&st=r2ku2zbd&dl=1"
graphics_dump_filename = "Celeste Graphics Dump v1400.zip"

def download_graphics_dump(download_path):
    dump_path = os.path.join(download_path, graphics_dump_filename)
    urllib.request.urlretrieve(graphics_dump_url, dump_path)
    return dump_path

def unzip_graphics_dump(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)  # Remove the zip file after extraction

def create_everest_yaml(mod_folder_path):
    yaml_content = """- Name: Celeste Randomized Textures
  Version: 1.0.0
  Dependencies:
    - Name: Everest
      Version: 1.4961.0
"""
    with open(os.path.join(mod_folder_path, "everest.yaml"), "w") as file:
        file.write(yaml_content)

def package_mod(mod_folder_path):
    shutil.make_archive(mod_folder_path, 'zip', mod_folder_path)
    shutil.rmtree(mod_folder_path)  # Clean up the mod folder after zipping

def swap_file_names_in_directory(directory_path, num_times, progress_var, progress_bar):
    for _ in range(num_times):
        total_files = sum([len(files) for _, _, files in os.walk(directory_path)])
        processed_files = 0
        
        for root, _, files in os.walk(directory_path):
            if files:
                shuffled_names = files[:]
                random.shuffle(shuffled_names)

                # Temporarily rename files to avoid conflicts
                temp_names = {}
                for original, shuffled in zip(files, shuffled_names):
                    temp_names[original] = f"{shuffled}.temp"
                    os.rename(os.path.join(root, original), os.path.join(root, temp_names[original]))
                
                # Rename to final shuffled names
                for original, shuffled in zip(files, shuffled_names):
                    os.rename(os.path.join(root, temp_names[original]), os.path.join(root, shuffled))
                    
                # Update progress
                processed_files += len(files)
                progress_var.set(processed_files / total_files * 100)
                progress_bar.update()

    messagebox.showinfo("Complete", "Textures have been randomized and the mod has been created successfully!")

def start_randomization():
    mod_directory_path = path_entry.get()
    num_times = times_entry.get()

    if not os.path.isdir(mod_directory_path):
        messagebox.showerror("Error", "Please select a valid directory.")
        return
    
    if not num_times.isdigit() or not (1 <= int(num_times) <= 4):
        messagebox.showerror("Error", "Please enter a number between 1 and 4.")
        return
    
    num_times = int(num_times)
    progress_var.set(0)
    progress_bar.update()

    # Step 1: Download the graphics dump
    dump_zip_path = download_graphics_dump(mod_directory_path)

    # Step 2: Unzip the graphics dump
    dump_folder_path = os.path.join(mod_directory_path, "celeste_graphics")
    unzip_graphics_dump(dump_zip_path, dump_folder_path)

    # Step 3: Randomize the file names
    swap_file_names_in_directory(dump_folder_path, num_times, progress_var, progress_bar)

    # Step 4: Create the mod folder structure
    mod_folder_path = os.path.join(mod_directory_path, "Celeste_Randomized_Textures")
    os.makedirs(mod_folder_path, exist_ok=True)
    create_everest_yaml(mod_folder_path)

    # Step 5: Move the randomized textures to the mod folder
    for item in os.listdir(dump_folder_path):
        source = os.path.join(dump_folder_path, item)
        destination = os.path.join(mod_folder_path, item)
        if os.path.isdir(source):
            shutil.move(source, destination)
        else:
            shutil.move(source, destination)

    # Step 6: Delete the celeste_graphics folder
    shutil.rmtree(dump_folder_path)

    # Step 7: Package everything into a zip file
    package_mod(mod_folder_path)

# Set up the GUI
root = tk.Tk()
root.title("Celeste Texture Randomizer")

# Celeste-themed colors
bg_color = "#1d1f33"
fg_color = "#c2c9ff"
button_color = "#3a3d5f"
highlight_color = "#ff99ff"

# Set background color
root.configure(bg=bg_color)

# Directory Selection
frame1 = tk.Frame(root, bg=bg_color)
frame1.pack(pady=10)
tk.Label(frame1, text="Select Mod Output Directory:", fg=fg_color, bg=bg_color, font=("Fixedsys", 12)).grid(row=0, column=0, padx=5, pady=5)
path_entry = tk.Entry(frame1, width=50, bg=button_color, fg=fg_color, insertbackground=fg_color, font=("Fixedsys", 12))
path_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame1, text="Browse", command=lambda: path_entry.insert(0, filedialog.askdirectory()), bg=highlight_color, fg=fg_color, font=("Fixedsys", 12)).grid(row=0, column=2, padx=5, pady=5)

# Number of Times to Randomize
frame2 = tk.Frame(root, bg=bg_color)
frame2.pack(pady=10)
tk.Label(frame2, text="Number of Times to Randomize (1-4):", fg=fg_color, bg=bg_color, font=("Fixedsys", 12)).grid(row=1, column=0, padx=5, pady=5)
times_entry = tk.Entry(frame2, width=10, bg=button_color, fg=fg_color, insertbackground=fg_color, font=("Fixedsys", 12))
times_entry.grid(row=1, column=1, padx=5, pady=5)
times_entry.insert(0, "1")  # Default to 1 time

# Progress Bar
frame3 = tk.Frame(root, bg=bg_color)
frame3.pack(pady=10, fill="x")
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame3, variable=progress_var, maximum=100, style="TProgressbar")
progress_bar.pack(fill="x", padx=10)

# Go Button
frame4 = tk.Frame(root, bg=bg_color)
frame4.pack(pady=10)
tk.Button(frame4, text="Go", command=start_randomization, bg=highlight_color, fg=fg_color, font=("Fixedsys", 12)).pack()

# Customize the progress bar style for the Celeste theme
style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar", troughcolor=button_color, background=highlight_color, thickness=15)

root.mainloop()
