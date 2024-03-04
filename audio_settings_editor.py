import os
import random
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, Toplevel
from excel_export import export_to_excel

class AudioSettingsEditor:
    def __init__(self):
        self.file_path = ""
        self.track_paths = {
            1: "C:/Users/Admin/Desktop/LSPU_Target_Curve/EQ/PM/SD30s.wav",
            2: "C:/Users/Admin/Desktop/LSPU_Target_Curve/EQ/PM/SO30s.wav",
            3: "C:/Users/Admin/Desktop/LSPU_Target_Curve/EQ/PM/IV30s.wav",
            4: "C:/Users/Admin/Desktop/LSPU_Target_Curve/EQ/PM/PY30s.wav",
            5: "C:/Users/Admin/Desktop/LSPU_Target_Curve/EQ/PM/DP30s.wav"
        }

        self.create_initial_screen()

    def create_initial_screen(self):
        self.root = tk.Tk()  # Create the root window
        self.root.withdraw()  # Hide the initial screen
        self.file_path = filedialog.askopenfilename(initialdir="/", title="Select Preference.txt",
                                                    filetypes=[("Text files", "*.txt")])
        if self.file_path:
            self.randomize_filter_values()
            self.open_trial_screen(1)

    # Inside the AudioSettingsEditor class

    def open_trial_screen(self, trial_num):
        trial_screen: Toplevel = tk.Toplevel(self.root)
        trial_screen.title(f"Trial {trial_num} of 5")

        label_title = tk.Label(trial_screen, text="Listening Test Software", font=("Arial", 24, "bold"))
        label_title.pack(pady=20)

        label_subtitle = tk.Label(trial_screen,
                                  text="Adjust the headphone's sound until it matches your preference",
                                  font=("Arial", 16))
        label_subtitle.pack(pady=10)

        frame_buttons = tk.Frame(trial_screen)
        frame_buttons.pack(pady=50)

        eq_buttons = [("Tonality", 1), ("Bass", 3), ("Treble", 4), ("Intensity", 5)]
        for label_text, filter_num in eq_buttons:
            label = tk.Label(frame_buttons, text=label_text, font=("Arial", 16))
            label.grid(row=filter_num - 1, column=0, padx=5, pady=5)
            if label_text == "Tonality":
                up_button = tk.Button(frame_buttons, text="▲", font=("Arial", 16),
                                      command=lambda filter_num=filter_num: self.update_tonality_value(True))
                down_button = tk.Button(frame_buttons, text="▼", font=("Arial", 16),
                                        command=lambda filter_num=filter_num: self.update_tonality_value(False))
            else:
                up_button = tk.Button(frame_buttons, text="▲", font=("Arial", 16),
                                      command=lambda filter_num=filter_num: self.update_filter_value(filter_num, True))
                down_button = tk.Button(frame_buttons, text="▼", font=("Arial", 16),
                                        command=lambda filter_num=filter_num: self.update_filter_value(filter_num,
                                                                                                       False))
            up_button.grid(row=filter_num - 1, column=1, padx=5, pady=5)
            down_button.grid(row=filter_num - 1, column=2, padx=5, pady=5)

        play_button = tk.Button(trial_screen, text="Play Audio", font=("Arial", 16),
                                command=lambda trial_num=trial_num: self.play_audio(trial_num))
        play_button.pack(pady=20)

        next_button = tk.Button(trial_screen, text="Next", font=("Arial", 16),
                                command=lambda: self.save_preference(trial_num))
        next_button.pack(pady=20)

        # Add an exit button to close the trial screen
        exit_button = tk.Button(trial_screen, text="Exit", font=("Arial", 16), command=lambda: sys.exit(0))
        exit_button.pack(pady=20)

        self.pages = {}
        self.pages[trial_num] = trial_screen
        try:
            trial_screen.mainloop()  # Ensure the trial screen is displayed
        except KeyboardInterrupt:
            print("Program is being closed...")
            self.root.destroy()

    def create_ending_screen(self):
        ending_screen = tk.Toplevel()
        ending_screen.title("End of Trials")

        label_title = tk.Label(ending_screen, text="Thank you for participating", font=("Arial", 24, "bold"))
        label_title.pack(pady=20)

        # Destroy the root window when ending screen is displayed
        self.root.destroy()

        ending_screen.mainloop()

    def randomize_filter_values(self):
        filter1_value = round(random.uniform(-5, 5) / 0.25) * 0.25
        if filter1_value > 0:
            filter2_value = -filter1_value
        else:
            filter2_value = -filter1_value
        self.set_filter_value(1, filter1_value)
        self.set_filter_value(2, filter2_value)
        for i in range(3, 6):
            filter_value = round(random.uniform(-5, 5) / 0.25) * 0.25
            self.set_filter_value(i, filter_value)

    def set_filter_value(self, filter_num, value):
        if not self.file_path:
            print("Error: Preference.txt not uploaded.")
            return

        lines = self.read_file(self.file_path)
        for i, line in enumerate(lines):
            if f"Filter {filter_num}" in line:
                parts = line.split(" ")
                for j, part in enumerate(parts):
                    if part == "Gain":
                        parts[j + 1] = "{:.2f}".format(value)
                lines[i] = " ".join(parts)

        self.update_file(self.file_path, lines)
        self.print_preference()

    def update_filter_value(self, filter_num, up):
        if not self.file_path:
            print("Error: Preference.txt not uploaded.")
            return

        lines = self.read_file(self.file_path)
        for i, line in enumerate(lines):
            if f"Filter {filter_num}" in line:
                parts = line.split(" ")
                for j, part in enumerate(parts):
                    if part == "Gain":
                        current_db = float(parts[j + 1])
                        parts[j + 1] = "{:.2f}".format(current_db + 0.25 if up else current_db - 0.25)
                lines[i] = " ".join(parts)

        self.update_file(self.file_path, lines)
        self.print_preference()

    def update_tonality_value(self, up):
        if not self.file_path:
            print("Error: Preference.txt not uploaded.")
            return

        lines = self.read_file(self.file_path)
        for i, line in enumerate(lines):
            if "Filter 1" in line:
                parts = line.split(" ")
                for j, part in enumerate(parts):
                    if part == "Gain":
                        current_db = float(parts[j + 1])
                        parts[j + 1] = "{:.2f}".format(current_db - 0.25 if up else current_db + 0.25)
                lines[i] = " ".join(parts)
            elif "Filter 2" in line:
                parts = line.split(" ")
                for j, part in enumerate(parts):
                    if part == "Gain":
                        current_db = float(parts[j + 1])
                        parts[j + 1] = "{:.2f}".format(current_db + 0.25 if up else current_db - 0.25)
                lines[i] = " ".join(parts)

        self.update_file(self.file_path, lines)
        self.print_preference()

    def read_file(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
        return lines

    def update_file(self, file_path, lines):
        with open(file_path, "w") as file:
            file.writelines(lines)

    def play_audio(self, trial_num):
        track_path = self.track_paths.get(trial_num)
        if track_path:
            os.system("start /min wmplayer.exe /play /close \"{}\"".format(track_path))
        else:
            print(f"Track path not found for trial {trial_num}.")

    def save_preference(self, trial_num):
        # Read Preference.txt
        lines = self.read_file(self.file_path)

        # Save a copy of Preference.txt
        preference_dir = "data"
        if not os.path.exists(preference_dir):
            os.makedirs(preference_dir)
        shutil.copy(self.file_path, os.path.join(preference_dir, f"PF{trial_num}.txt"))

        # Export lines to Excel
        excel_file = os.path.join("data", f"PF{trial_num}.xlsx")
        export_to_excel(excel_file, lines)

        # Close the current trial screen
        self.pages[trial_num].destroy()

        # Open the next trial screen if it's not the last one
        next_trial = trial_num + 1
        if next_trial <= 5:
            self.randomize_filter_values()
            self.open_trial_screen(next_trial)
        # Open the ending screen if it's the last trial
        if trial_num == 5:
            self.create_ending_screen()


    def print_preference(self):
        if self.file_path:
            print("Preference.txt contents:")
            with open(self.file_path, "r") as file:
                for line in file:
                    print(line.strip())
        else:
            print("Error: Preference.txt not uploaded.")

    def export_to_excel(self, excel_file):
        # Read the contents of Preference.txt
        lines = self.read_file(self.file_path)

        # Initialize variables for storing filter values
        tonality_value = 0
        bass_value = 0
        treble_value = 0
        intensity_value = 0

        # Extract filter values from Preference.txt
        for line in lines:
            if "Filter 2" in line:
                filter2_gain = float(line.split("Gain")[1].strip().split(" ")[0])
                tonality_value = filter2_gain * 2
            elif "Filter 3" in line:
                bass_value = float(line.split("Gain")[1].strip().split(" ")[0])
            elif "Filter 4" in line:
                treble_value = float(line.split("Gain")[1].strip().split(" ")[0])
            elif "Filter 5" in line:
                intensity_value = float(line.split("Gain")[1].strip().split(" ")[0])

        # Write data to Excel file
        self.ws.append(["Preference Adjustments", "Value (dB)"])
        self.ws.append(["Tonality", tonality_value])
        self.ws.append(["Bass", bass_value])
        self.ws.append(["Treble", treble_value])
        self.ws.append(["Intensity", intensity_value])

        # Save Excel file
        self.wb.save(excel_file)

    # Create an instance of AudioSettingsEditor to start the application


app = AudioSettingsEditor()