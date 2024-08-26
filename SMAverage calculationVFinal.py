import tkinter as tk
from tkinter import messagebox, Canvas
import re

def calculate_average_views(view_counts):
    if not view_counts:
        return "0"  # Return just the number, no label
    
    average_views = sum(view_counts) / len(view_counts)
    return f"{average_views:,.0f}"

def calculate_sum_views(view_counts):
    return f"{sum(view_counts):,}"

def parse_views(data):
    view_counts = []
    for match in re.finditer(r'(\d+\.?\d*)[KM]', data):
        number = float(match.group(1))
        if 'K' in match.group(0):
            view_counts.append(int(number * 1_000))
        elif 'M' in match.group(0):
            view_counts.append(int(number * 1_000_000))
    return view_counts

def on_calculate():
    data = text_entry.get("1.0", tk.END)
    try:
        view_counts = parse_views(data)
        average_result = calculate_average_views(view_counts)
        sum_result = calculate_sum_views(view_counts)
        view_counts_str = ', '.join([f'{count:,}' for count in view_counts])
        result = f"Data Calculated:\n{view_counts_str}"
        
        # Show result in the output text widget
        output_text.config(state=tk.NORMAL)  # Allow editing the Text widget
        output_text.delete("1.0", tk.END)  # Clear the previous content
        output_text.insert(tk.END, result)  # Insert the new result
        output_text.config(state=tk.DISABLED)  # Make the Text widget read-only
        
        # Show average in the average views text box
        average_text.config(state=tk.NORMAL)  # Allow editing the Text widget
        average_text.delete("1.0", tk.END)  # Clear previous average result
        average_text.insert(tk.END, f"Average of views: {average_result}")  # Insert new average result
        average_text.config(state=tk.DISABLED)  # Make the Text widget read-only

        # Show sum in the sum views text box
        sum_text.config(state=tk.NORMAL)  # Allow editing the Text widget
        sum_text.delete("1.0", tk.END)  # Clear previous sum result
        sum_text.insert(tk.END, f"Sum of views: {sum_result}")  # Insert new sum result
        sum_text.config(state=tk.DISABLED)  # Make the Text widget read-only

        # Copy the numeric average views to clipboard
        root.clipboard_clear()  # Clear the clipboard
        root.clipboard_append(average_result)  # Append the numeric average views to the clipboard
        root.update()  # Update the clipboard

    except ValueError:
        messagebox.showerror("Error", "Please enter valid view counts data.")

def on_new_data():
    text_entry.delete("1.0", tk.END)  # Clear the text entry widget
    output_text.config(state=tk.NORMAL)  # Allow editing the Text widget
    output_text.delete("1.0", tk.END)  # Clear the output text widget
    output_text.config(state=tk.DISABLED)  # Make the Text widget read-only
    average_text.config(state=tk.NORMAL)  # Allow editing the Text widget
    average_text.delete("1.0", tk.END)  # Clear the average text widget
    average_text.config(state=tk.DISABLED)  # Make the Text widget read-only
    sum_text.config(state=tk.NORMAL)  # Allow editing the Text widget
    sum_text.delete("1.0", tk.END)  # Clear the sum text widget
    sum_text.config(state=tk.DISABLED)  # Make the Text widget read-only

def on_exit():
    root.destroy()  # Close the application

def create_gradient(canvas, width, height, color1, color2):
    '''Create a vertical gradient from color1 to color2 on the canvas'''
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    
    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height
    
    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr:04x}{ng:04x}{nb:04x}'
        canvas.create_line(0, i, width, i, fill=color)

# Setting up the GUI
root = tk.Tk()
root.title("Views Calculator")
root.geometry("600x600")

# Create a canvas for the gradient background
canvas = Canvas(root, width=600, height=600)
canvas.pack(fill='both', expand=True)

# Create the gradient (from dark blue to purple)
create_gradient(canvas, 600, 600, '#2C3E50', '#8E44AD')

# Create a frame to hold all the widgets (without specifying bg color)
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Styles
title_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")
output_font = ("Helvetica", 11)
text_font = ("Helvetica", 11)
note_font = ("Helvetica", 10, "italic")

label = tk.Label(frame, text="Enter your data:", font=title_font, fg="#ECF0F1", bg="#2C3E50")
label.pack(pady=10)

text_entry = tk.Text(frame, width=60, height=8, font=text_font, bd=2, relief="groove")
text_entry.pack(pady=10)

# Frame for buttons
button_frame = tk.Frame(frame)
button_frame.pack(pady=10)

calculate_button = tk.Button(button_frame, text="Calculate", font=button_font, bg="#3498DB", fg="white", bd=3, relief="raised", command=on_calculate)
calculate_button.pack(side=tk.LEFT, padx=10)

new_data_button = tk.Button(button_frame, text="New Data", font=button_font, bg="#1ABC9C", fg="white", bd=3, relief="raised", command=on_new_data)
new_data_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame, text="Exit", font=button_font, bg="#E74C3C", fg="white", bd=3, relief="raised", command=on_exit)
exit_button.pack(side=tk.LEFT, padx=10)

output_text = tk.Text(frame, width=60, height=8, font=output_font, bd=2, relief="groove", wrap=tk.WORD, bg="#ECF0F1", fg="#2C3E50")
output_text.pack(pady=10)
output_text.config(state=tk.DISABLED)  # Make the Text widget initially read-only

average_label = tk.Label(frame, text="Average of views:", font=label_font, fg="#ECF0F1", bg="#2C3E50")
average_label.pack(pady=5)

average_text = tk.Text(frame, width=60, height=2, font=text_font, bd=2, relief="groove", bg="#ECF0F1", fg="#2C3E50")
average_text.pack(pady=5)
average_text.config(state=tk.DISABLED)  # Make the Text widget initially read-only

sum_label = tk.Label(frame, text="Sum of views:", font=label_font, fg="#ECF0F1", bg="#2C3E50")
sum_label.pack(pady=5)

sum_text = tk.Text(frame, width=60, height=2, font=text_font, bd=2, relief="groove", bg="#ECF0F1", fg="#2C3E50")
sum_text.pack(pady=5)
sum_text.config(state=tk.DISABLED)  # Make the Text widget initially read-only

# Add attribution note
attribution_label = tk.Label(frame, text="Created by ENG Mohamad Adnan Jamal", font=note_font, fg="#ECF0F1", bg="#2C3E50")
attribution_label.pack(pady=20)

root.mainloop()
