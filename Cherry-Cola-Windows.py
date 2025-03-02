import pygame
import tkinter as tk
from tkinter import PhotoImage

# Button mappings for Xbox, PlayStation, PS3, Nintendo, and Steam controllers
XBOX_BUTTON_NAMES = {
    0: "A", 1: "B", 2: "X", 3: "Y", 4: "LB", 5: "RB",
    6: "Back", 7: "Start", 8: "Left Stick", 9: "Right Stick",
    10: "Xbox Button", 11: "Share Button", 12: "Left Trigger", 13: "Right Trigger"
}

PS_BUTTON_NAMES = {
    0: "Cross", 1: "Circle", 2: "Square", 3: "Triangle", 4: "L1", 5: "R1",
    6: "Share", 7: "Options", 8: "Left Stick", 9: "Right Stick",
    10: "PS Button", 11: "Touchpad", 12: "Left Trigger", 13: "Right Trigger"
}

PS3_BUTTON_NAMES = {
    0: "X", 1: "O", 2: "Square", 3: "Triangle", 4: "L1", 5: "R1",
    6: "Select", 7: "Start", 8: "Left Stick", 9: "Right Stick",
    10: "PS Button", 11: "Home", 12: "Left Trigger", 13: "Right Trigger"
}

NINTENDO_BUTTON_NAMES = {
    0: "A", 1: "B", 2: "X", 3: "Y", 4: "L", 5: "R",
    6: "ZL", 7: "ZR", 8: "Left Stick", 9: "Right Stick",
    10: "Minus", 11: "Plus", 12: "Home", 13: "Capture"
}

STEAM_BUTTON_NAMES = {
    0: "A", 1: "B", 2: "X", 3: "Y", 4: "L1", 5: "R1",
    6: "Back", 7: "Start", 8: "Left Stick", 9: "Right Stick",
    10: "Steam", 11: "Left Trigger", 12: "Right Trigger", 13: "Left Pad", 14: "Right Pad"
}

# Initialize Pygame and joystick module
pygame.init()
pygame.joystick.init()

# Create Tkinter window with rounded corners
root = tk.Tk()
root.title("🍒🥤 Cherry Cola")  # Set emoji in the window title
root.geometry("800x600")
root.resizable(True, True)  # Make window resizable

# Set an image file as the icon
try:
    icon_image = PhotoImage(file="cherry_cola_icon.png")  # Use a PNG image for the icon
    root.iconphoto(False, icon_image)
except Exception as e:
    print(f"Error loading image for icon: {e}")
    # Optionally set a fallback icon or message here

# Modern Theme
light_mode = {"bg": "white", "fg": "black", "canvas": "#f7f7f7", "stick": "black", "button_bg": "#4CAF50"}
dark_mode = {"bg": "#1e1e1e", "fg": "white", "canvas": "#333333", "stick": "#00ffcc", "button_bg": "#444444"}
current_mode = light_mode  # Start in Light Mode

# Status label to display the latest input
status_label = tk.Label(root, text="Waiting for controller...", font=("Helvetica", 14), fg=current_mode["fg"], bg=current_mode["bg"])
status_label.pack(pady=20)

# Canvas for virtual controller visualization
canvas = tk.Canvas(root, width=700, height=400, bg=current_mode["canvas"], highlightthickness=0, bd=0)
canvas.pack(pady=20)

# Create base circles for joystick area
canvas.create_oval(100, 50, 200, 150, outline="gray", width=2)  # Left Stick Base
canvas.create_oval(400, 50, 500, 150, outline="gray", width=2)  # Right Stick Base

# Create joystick circles (small, smooth sticks)
joystick1 = canvas.create_oval(140, 90, 160, 110, fill=current_mode["stick"], outline="")
joystick2 = canvas.create_oval(440, 90, 460, 110, fill=current_mode["stick"], outline="")

# Create virtual buttons for the controller, including triggers
button_rects = {}
button_coords = [
    (50, 200, "A"), (150, 200, "B"), (250, 200, "X"), (350, 200, "Y"),
    (50, 300, "LB"), (150, 300, "RB"), (250, 300, "Back"), (350, 300, "Start"),
    (50, 400, "Left Trigger"), (150, 400, "Right Trigger")
]
for x, y, name in button_coords:
    button_rects[name] = canvas.create_rectangle(x, y, x + 50, y + 50, fill="gray", outline="black")
    canvas.create_text(x + 25, y + 25, text=name, fill="white", font=("Helvetica", 12))

# Variables for smooth movement
joystick_pos = {"left_x": 0, "left_y": 0, "right_x": 0, "right_y": 0}
button_states = {name: False for name in XBOX_BUTTON_NAMES}

def update_joystick(axis, value):
    """Smooth joystick movement by interpolating positions."""
    if axis == 0:  # Left Stick (Horizontal)
        joystick_pos["left_x"] = value
    elif axis == 1:  # Left Stick (Vertical)
        joystick_pos["left_y"] = value
    elif axis == 2:  # Right Stick (Horizontal)
        joystick_pos["right_x"] = value
    elif axis == 3:  # Right Stick (Vertical)
        joystick_pos["right_y"] = value

def smooth_update():
    """Smoothly update joystick positions on the canvas."""
    # Get current target positions
    left_x = 150 + joystick_pos["left_x"] * 40
    left_y = 100 + joystick_pos["left_y"] * 40
    right_x = 450 + joystick_pos["right_x"] * 40
    right_y = 100 + joystick_pos["right_y"] * 40

    # Move joystick circles smoothly
    canvas.coords(joystick1, left_x - 10, left_y - 10, left_x + 10, left_y + 10)
    canvas.coords(joystick2, right_x - 10, right_y - 10, right_x + 10, right_y + 10)

    root.after(16, smooth_update)  # Run at ~60 FPS

def toggle_dark_mode():
    """Switch between dark and light mode."""
    global current_mode
    current_mode = dark_mode if current_mode == light_mode else light_mode
    
    root.configure(bg=current_mode["bg"])
    status_label.config(bg=current_mode["bg"], fg=current_mode["fg"])
    canvas.config(bg=current_mode["canvas"])
    toggle_button.config(bg=current_mode["button_bg"], fg=current_mode["fg"], activebackground=current_mode["canvas"])
    canvas.itemconfig(joystick1, fill=current_mode["stick"])
    canvas.itemconfig(joystick2, fill=current_mode["stick"])

# Modern Button Style (rounded)
toggle_button = tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode, font=("Helvetica", 12, "bold"), 
                          bg=current_mode["button_bg"], fg=current_mode["fg"], relief="flat", padx=20, pady=10, 
                          borderwidth=2, highlightthickness=0)
toggle_button.pack(pady=10)

# Function to check for controller and update status
def check_controller():
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        controller_name = joystick.get_name()
        status_label.config(text=f"Controller Connected: {controller_name}")
        
        # Check if it is a PlayStation, PS3, Steam, or Nintendo controller
        if "PlayStation" in controller_name:
            return joystick, PS_BUTTON_NAMES if "PS3" not in controller_name else PS3_BUTTON_NAMES
        elif "Nintendo" in controller_name or "Pro Controller" in controller_name or "Joy-Con" in controller_name:
            return joystick, NINTENDO_BUTTON_NAMES
        elif "Steam Controller" in controller_name:
            return joystick, STEAM_BUTTON_NAMES
        else:
            return joystick, XBOX_BUTTON_NAMES
    else:
        status_label.config(text="Controller disconnected.")
        return None, None

# Detect connected controllers
joystick, button_names = check_controller()

# Update the button appearance based on pressed state
def update_button_state(button, pressed, pressure=None):
    """Update button state, change color to green if pressed or based on pressure for triggers."""
    if button == "Left Trigger" or button == "Right Trigger":
        # For triggers, we can change color based on the pressure (axis value)
        if pressure > 0.1:
            color = "green"  # Trigger is pressed
        else:
            color = "gray"  # Trigger is not pressed
    else:
        # For regular buttons, just turn green when pressed
        color = "green" if pressed else "gray"
    
    canvas.itemconfig(button_rects[button], fill=color)

# Update loop
def update():
    global button_names
    if joystick:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                # Handle button presses properly
                button_name = button_names.get(event.button, f"Unknown Button {event.button}")
                update_button_state(button_name, True)  # Change color to green
                status_label.config(text=f"Pressed: {button_name}")

            if event.type == pygame.JOYBUTTONUP:
                # Handle button releases properly
                button_name = button_names.get(event.button, f"Unknown Button {event.button}")
                update_button_state(button_name, False)  # Change color back to gray
                status_label.config(text=f"Released: {button_name}")

            if event.type == pygame.JOYAXISMOTION:
                # Handle joystick axes motion properly (joysticks are axes, not buttons)
                if event.axis == 0:  # Left Stick (Horizontal)
                    update_joystick(event.axis, event.value)
                elif event.axis == 1:  # Left Stick (Vertical)
                    update_joystick(event.axis, event.value)
                elif event.axis == 2:  # Right Stick (Horizontal)
                    update_joystick(event.axis, event.value)
                elif event.axis == 3:  # Right Stick (Vertical)
                    update_joystick(event.axis, event.value)

                # Handle triggers (emulated as buttons)
                if event.axis == 2:  # Left Trigger (Axis 2)
                    update_button_state("Left Trigger", True, event.value)
                if event.axis == 5:  # Right Trigger (Axis 5)
                    update_button_state("Right Trigger", True, event.value)

            if event.type == pygame.JOYHATMOTION:
                status_label.config(text=f"D-Pad moved: {event.value}")

    root.after(50, update)  # Run update every 50ms

# Start smooth update loop
smooth_update()
update()
root.mainloop()
pygame.quit()
