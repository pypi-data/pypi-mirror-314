#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from kpi_monitor.data_analysis import run_aggregation_and_plot  # This function returns the Figure object

def run_analysis():
    # Clear the plot frame before adding a new plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Get user inputs from the form
    recipient = [recipient for recipient, var in recipient_var.items() if var.get()]
    product = [product for product, var in product_var.items() if var.get()]
    func = func_var.get()
    period = period_var.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    # Validate inputs (you can expand this)
    if not recipient or not product or not start_date or not end_date:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    try:
        # Call your analysis function and get the figure
        fig = run_aggregation_and_plot(recipient, product, func, period, start_date, end_date)

        # Embed the plot in the plot_frame
        canvas = FigureCanvasTkAgg(fig, plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add a toolbar for interactivity
        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        #messagebox.showinfo("Success", "Analysis completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("FCR Data Analysis Dashboard")
root.geometry("1900x950")  # Adjusted size for the new layout

# Frame for form (left side)
form_frame = tk.Frame(root, width=400)
form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Frame for plot (right side)
plot_frame = tk.Frame(root, width=1000, height=800)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
plot_frame.pack_propagate(False)  # Prevent resizing when adding plots

# Default values
default_func = "sum"
default_period = "D"
default_start_date = "2024-08-01"
default_end_date = "2024-11-01"

# Options for Recipients and Products
recipient_options = ["flower", "volue", "energinet", "bixia", "jamtkraft"]
product_options = ["fcr-n", "fcr-d-up", "fcr-d-down"]

# Create dictionaries to store checkboxes for Recipients and Products
recipient_var = {recipient: tk.BooleanVar() for recipient in recipient_options}
product_var = {product: tk.BooleanVar() for product in product_options}

# Titles font
fonts = ("Arial", 13, "bold")

# Add widgets to the form_frame
tk.Label(form_frame, text="Recipient(s):", font=fonts).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)

# Display recipients in two columns
for idx, recipient in enumerate(recipient_options[:len(recipient_options)//2]):
    tk.Checkbutton(form_frame, text=recipient, variable=recipient_var[recipient]).grid(row=idx+1, column=0, sticky="w", padx=5)

for idx, recipient in enumerate(recipient_options[len(recipient_options)//2:]):
    tk.Checkbutton(form_frame, text=recipient, variable=recipient_var[recipient]).grid(row=idx+1, column=1, sticky="w", padx=5)

tk.Label(form_frame, text="Product(s):", font=fonts).grid(row=len(recipient_options)//2 + 2, column=0, columnspan=2, sticky="w", padx=5, pady=5)

# Display products
for idx, product in enumerate(product_options):
    tk.Checkbutton(form_frame, text=product, variable=product_var[product]).grid(row=idx + len(recipient_options)//2 + 3, column=0, sticky="w", padx=5)

# Add a line break before next section
tk.Label(form_frame, text="Function:", font=fonts).grid(row=idx + len(product_options) + 6, column=0, sticky="w", padx=5, pady=10)
func_var = tk.StringVar(value=default_func)
tk.OptionMenu(form_frame, func_var, "sum", "mean", "both").grid(row=idx + len(product_options) + 6, column=1, sticky="w", padx=5)

tk.Label(form_frame, text="Agg. Period:", font=fonts).grid(row=idx + len(product_options) + 7, column=0, sticky="w", padx=5, pady=10)
period_var = tk.StringVar(value=default_period)
tk.OptionMenu(form_frame, period_var, "h", "D", "W", "ME", "Y").grid(row=idx + len(product_options) + 7, column=1, sticky="w", padx=5)

tk.Label(form_frame, text="Start Date:", font=fonts).grid(row=idx + len(product_options) + 8, column=0, sticky="w", padx=5)
start_date_entry = tk.Entry(form_frame, width=30)
start_date_entry.grid(row=idx + len(product_options) + 8, column=1, sticky="w", padx=5)
start_date_entry.insert(0, default_start_date)  # Set default value

tk.Label(form_frame, text="End Date:", font=fonts).grid(row=idx + len(product_options) + 9, column=0, sticky="w", padx=5)
end_date_entry = tk.Entry(form_frame, width=30)
end_date_entry.grid(row=idx + len(product_options) + 9, column=1, sticky="w", padx=5)
end_date_entry.insert(0, default_end_date)  # Set default value

run_button = tk.Button(form_frame, text="Run Analysis", command=run_analysis)
run_button.grid(row=idx + len(product_options) + 10, column=0, columnspan=2, pady=10)

# Run the main event loop
root.mainloop()

def main():
    # Your original Tkinter dashboard code here
    root = tk.Tk()
    # rest of the dashboard code...

if __name__ == "__main__":
    main()