# controller.py
from randomizer.model import ShuffleRandomizer, GroupRandomizer, Preferences
from tkinter import Text, Toplevel, Label, Entry, Button, Checkbutton, BooleanVar

# Initialize preferences
preferences = Preferences()

def enterBtn(entry_1: Text, entry_2: Text, shuffle_option: str, allow_duplicates: bool = True, group_size: int = None, number_of_groups: int = None):
    # Get input from entry_1
    input_text = entry_1.get("1.0", "end-1c").strip()
    if not input_text:
        entry_2.delete("1.0", "end")
        entry_2.insert("1.0", "Error: Input is empty.")
        return

    # Split input by commas and remove any extra whitespace
    inputs = [item.strip() for item in input_text.split(",") if item.strip()]
    
    if shuffle_option == "Multiple Output":
        randomizer = GroupRandomizer(allow_duplicates=allow_duplicates)
        randomizer.add_inputs(inputs)
        randomizer.set_group_size(2)
        results = randomizer.generate_groups()
        results = [", ".join(map(str, group)) for group in results]
        entry_2.delete("1.0", "end")
        entry_2.insert("1.0", "\n".join(results))
    elif shuffle_option == "Group Output":
        randomizer = GroupRandomizer(allow_duplicates=allow_duplicates)
        randomizer.add_inputs(inputs)
        if group_size:
            randomizer.set_group_size(group_size)
        if number_of_groups:
            randomizer.set_number_of_groups(number_of_groups)
        results = randomizer.generate_groups()
        results = [", ".join(map(str, group)) for group in results]
        entry_2.delete("1.0", "end")
        entry_2.insert("1.0", "\n".join(results))
    elif shuffle_option == "Single Picker":
        randomizer = ShuffleRandomizer(allow_duplicates=allow_duplicates)
        randomizer.add_inputs(inputs)
        try:
            result = randomizer.pick_single_item()
            entry_2.delete("1.0", "end")
            entry_2.insert("1.0", str(result))
        except IndexError:
            entry_2.delete("1.0", "end")
            entry_2.insert("1.0", "Error: No items to pick from.")
    else:
        randomizer = ShuffleRandomizer(allow_duplicates=allow_duplicates)
        randomizer.add_inputs(inputs)
        results = randomizer.shuffle_items()
        entry_2.delete("1.0", "end")
        entry_2.insert("1.0", ", ".join(map(str, results)))

def settingsBtn(main_window):
    settings_window = Toplevel(main_window)
    settings_window.title("Settings")
    settings_window.geometry("300x150")
    settings_window.configure(bg="#FFFFFF")

    # Center the settings window
    window_width = main_window.winfo_width()
    window_height = main_window.winfo_height()
    settings_window_width = 300
    settings_window_height = 150
    position_right = int(main_window.winfo_x() + (window_width / 2) - (settings_window_width / 2))
    position_down = int(main_window.winfo_y() + (window_height / 2) - (settings_window_height / 2))
    settings_window.geometry(f"{settings_window_width}x{settings_window_height}+{position_right}+{position_down}")

    # Checkbox for "Do Not Allow Duplicates"
    allow_duplicates_var = BooleanVar(value=not preferences.allow_duplicates)

    def on_checkbox_toggled():
        preferences.allow_duplicates = not allow_duplicates_var.get()

    checkbox = Checkbutton(settings_window, text="Do Not Allow Duplicates", bg="#FFFFFF",
                           variable=allow_duplicates_var, command=on_checkbox_toggled)
    checkbox.pack(pady=10)

    def go_back():
        settings_window.destroy()

    back_button = Button(settings_window, text="Back", command=go_back)
    back_button.pack(pady=10)

def clear_text_area(entry: Text, entry1: Text):
    entry.delete('1.0', 'end')
    entry1.delete('1.0', 'end')

def clearBtn(entry: Text, entry1: Text):
    clear_text_area(entry, entry1)
