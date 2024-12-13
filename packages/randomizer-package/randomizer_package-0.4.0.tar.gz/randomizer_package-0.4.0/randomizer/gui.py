# Notes:
    # Button 1 kay Enter Button
    # Button 2 kay Settings Button
    # Button 3 kay Shuffle Button
        # Note: Please Make this a drop down
        # Add options (Single Output, Multiple Output, Group Output)
    # Button 4 kay Clear Button

from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage, Menu, Toplevel, Label, Entry, BooleanVar
from randomizer.controller import enterBtn, clearBtn, settingsBtn, preferences
from randomizer.model import GroupRandomizer, Preferences, ShuffleRandomizer

# Please change the asset path accordingly
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Desktop\Programming Files\randomizer_nblancs\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def main():
    global selected_shuffle_option
    selected_shuffle_option = "Single Output"

    window = Tk()
    window.geometry("720x760")
    window.configure(bg = "#FFFFFF")
    window.title("Randomizer")

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 760,
        width = 720,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_4.png"))

    # Clear Button
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: clearBtn(entry_2, entry_1),  # Clears entry_1 and entry_2
        relief="flat"
    )
    button_1.place(
        x=270.0,
        y=681.0,
        width=180.0,
        height=50.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        360.0,
        205.0,
        image=image_image_1
    )

    # Text Area 1
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        360.0,
        205.0,
        image=entry_image_1
    )
    entry_1 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=165.0,
        y=135.0,
        width=390.0,
        height=138.0
    )

    # Text Area 2
    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        360.0,
        594.0,
        image=entry_image_2
    )
    entry_2 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=165.0,
        y=524.0,
        width=390.0,
        height=138.0
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        360.0,
        37.0,
        image=image_image_2
    )

    canvas.create_text(
        330.0,
        92.0,
        anchor="nw",
        text="INPUT ",
        fill="#000000",
        font=("Inter", 20 * -1)
    )

    canvas.create_text(
        262.0,
        17.0,
        anchor="nw",
        text="RANDOMIZER",
        fill="#000000",
        font=("Inter", 24 * -1)
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        443.0,
        33.0,
        image=image_image_3
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))

    # Settings Button
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: settingsBtn(window), # Please Edit the method in controller.py
        relief="flat"
    )
    button_2.place(
        x=459.0,
        y=310.0,
        width=32.0,
        height=32.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))

    # Function to update the shuffle option text
    def update_shuffle_option(option):
        global selected_shuffle_option
        selected_shuffle_option = option
        canvas.itemconfig(textSelectedOption, text=f"Shuffle Option: {option}")
        if option == "Group Output":
            open_group_window()

    # Shuffle Button
    def open_shuffle_menu(event):
        shuffle_menu = Menu(window, tearoff=0)
        shuffle_menu.add_command(label="Single Output", command=lambda: update_shuffle_option("Single Output"))
        shuffle_menu.add_command(label="Multiple Output", command=lambda: update_shuffle_option("Multiple Output"))
        shuffle_menu.add_command(label="Group Output", command=lambda: update_shuffle_option("Group Output"))
        shuffle_menu.add_command(label="Single Picker", command=lambda: update_shuffle_option("Single Picker"))
        shuffle_menu.post(event.x_root, event.y_root)

    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    button_3.place(
        x=270.0,
        y=300.0,
        width=180.0,
        height=50.0
    )

    # Bind the button click to show the dropdown menu
    button_3.bind("<Button-1>", open_shuffle_menu)

    canvas.create_text(
        323.0,
        485.0,
        anchor="nw",
        text="RESULT",
        fill="#000000",
        font=("Inter", 20 * -1)
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        360.0,
        594.0,
        image=image_image_4
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_1.png"))

    # Enter Button
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: open_group_window() if selected_shuffle_option == "Group Output" else enterBtn(entry_1, entry_2, selected_shuffle_option, preferences.allow_duplicates), # Open group window if Group Output is selected
        relief="flat"
    )
    button_4.place(
        x=270.0,
        y=393.0,
        width=180.0,
        height=50.0
    )

    # Label text for shuffle
    textSelectedOption = canvas.create_text(
        270.0,
        360.0,
        anchor="nw",
        text="Shuffle Option: Single Output",  # Default value
        fill="#000000",
        font=("Inter", 14 * -1)
    )

    def open_group_window():
        group_window = Toplevel(window)
        group_window.title("Group Output Settings")
        group_window.geometry("300x200")
        group_window.configure(bg="#FFFFFF")

        window_width = window.winfo_width()
        window_height = window.winfo_height()
        group_window_width = 300
        group_window_height = 200
        position_right = int(window.winfo_x() + (window_width / 2) - (group_window_width / 2))
        position_down = int(window.winfo_y() + (window_height / 2) - (window_height / 2))
        group_window.geometry(f"{group_window_width}x{group_window_height}+{position_right}+{position_down}")

        Label(group_window, text="Number of Groups:", bg="#FFFFFF").pack(pady=5)
        group_count_entry = Entry(group_window)
        group_count_entry.pack(pady=5)

        Label(group_window, text="Elements per Group:", bg="#FFFFFF").pack(pady=5)
        group_size_entry = Entry(group_window)
        group_size_entry.pack(pady=5)

        def apply_group_constraints():
            group_size = int(group_size_entry.get())
            number_of_groups = int(group_count_entry.get())
            enterBtn(entry_1, entry_2, "Group Output", preferences.allow_duplicates, group_size, number_of_groups)
            group_window.destroy()

        Button(group_window, text="Enter", command=apply_group_constraints).pack(pady=10)

    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main()