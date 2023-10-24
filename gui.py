import tkinter as tk



# Create the main window
root = tk.Tk()
root.title("Simple GUI")

# Create a label widget
label = tk.Label(root, text="Hello, this is a simple GUI!")
label.pack(padx=20, pady=20)  # Add padding around the label

# Function to be executed when the button is clicked
def on_button_click():
    print("Button clicked!")

# Create a button widget
button = tk.Button(root, text="Click me!", command=on_button_click)
button.pack(padx=20, pady=10)  # Add padding around the button

# Run the main event loop
root.mainloop()
