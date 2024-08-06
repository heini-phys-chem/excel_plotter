# main.py
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import Scale, Entry
import pandas as pd
import matplotlib.pyplot as plt
from excel_processor import process_excel
from plotter import plot_data
from subplots_plotter import plot_subplots  # Import the new function
from custom_plotter import plot_custom_files
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExcelFileAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel File Analyzer")
        self.results = []
        self.df_results = None
        self.custom_files = []

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)  # New tab for subplots
        self.notebook.add(self.tab1, text="Analyze")
        self.notebook.add(self.tab2, text="Plot")
        self.notebook.add(self.tab3, text="Custom Plot")
        self.notebook.add(self.tab4, text="Subplots")  # Add the new tab

        self.create_analyze_tab()
        self.create_plot_tab()
        self.create_custom_plot_tab()
        self.create_subplots_tab()  # Create the new tab

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.close_button = ttk.Button(self.root, text="Close", command=self.on_closing)
        self.close_button.pack(pady=10)

    def create_analyze_tab(self):
        frame = ttk.Frame(self.tab1, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        label = ttk.Label(frame, text="Excel File Analyzer", font=("Arial", 14))
        label.pack(pady=10)

        self.process_button = ttk.Button(frame, text="Select Files and Analyze", command=self.process_files)
        self.process_button.pack(pady=20)

        self.save_button = ttk.Button(frame, text="Save Results as CSV", command=self.save_results, state=tk.DISABLED)
        self.save_button.pack(pady=20)

    def create_plot_tab(self):
        self.plot_frame = ttk.Frame(self.tab2, padding="10")
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        self.plot_button = ttk.Button(self.plot_frame, text="Plot Data", command=self.plot_data, state=tk.DISABLED)
        self.plot_button.pack(pady=20)

        self.save_plot_button = ttk.Button(self.plot_frame, text="Save Plot", command=self.save_plot, state=tk.DISABLED)
        self.save_plot_button.pack(pady=20)

        self.update_plot_button = ttk.Button(self.plot_frame, text="Update Plot", command=self.update_plot, state=tk.DISABLED)
        self.update_plot_button.pack(pady=20)

        self.axis_label_fontsize_slider = Scale(self.plot_frame, from_=8, to_=32, orient=tk.HORIZONTAL, label="Axis Label Font Size")
        self.axis_label_fontsize_slider.set(12)
        self.axis_label_fontsize_slider.pack(pady=10)

        self.tick_label_fontsize_slider = Scale(self.plot_frame, from_=8, to_=32, orient=tk.HORIZONTAL, label="Tick Label Font Size")
        self.tick_label_fontsize_slider.set(10)
        self.tick_label_fontsize_slider.pack(pady=10)

        self.text_fontsize_slider = Scale(self.plot_frame, from_=8, to_=32, orient=tk.HORIZONTAL, label="Text Font Size")
        self.text_fontsize_slider.set(10)
        self.text_fontsize_slider.pack(pady=10)

        self.x_label_entry = Entry(self.plot_frame, width=20)
        self.x_label_entry.insert(0, "Toughness")
        self.x_label_entry.pack(pady=10)
        self.y_label_entry = Entry(self.plot_frame, width=20)
        self.y_label_entry.insert(0, "Tensile Strength [MPa]")
        self.y_label_entry.pack(pady=10)

        self.canvas = None

    def create_custom_plot_tab(self):
        self.custom_plot_frame = ttk.Frame(self.tab3, padding="10")
        self.custom_plot_frame.pack(fill=tk.BOTH, expand=True)

        self.custom_plot_button = ttk.Button(self.custom_plot_frame, text="Select Files and Plot", command=self.plot_custom_data)
        self.custom_plot_button.pack(pady=20)

        self.save_custom_plot_button = ttk.Button(self.custom_plot_frame, text="Save Custom Plot", command=self.save_custom_plot, state=tk.DISABLED)
        self.save_custom_plot_button.pack(pady=20)

        self.custom_update_plot_button = ttk.Button(self.custom_plot_frame, text="Update Custom Plot", command=self.update_custom_plot, state=tk.DISABLED)
        self.custom_update_plot_button.pack(pady=20)

        self.custom_axis_label_fontsize_slider = Scale(self.custom_plot_frame, from_=8, to_=32, orient=tk.HORIZONTAL, label="Axis Label Font Size")
        self.custom_axis_label_fontsize_slider.set(12)
        self.custom_axis_label_fontsize_slider.pack(pady=10)

        self.custom_tick_label_fontsize_slider = Scale(self.custom_plot_frame, from_=8, to_=32, orient=tk.HORIZONTAL, label="Tick Label Font Size")
        self.custom_tick_label_fontsize_slider.set(10)
        self.custom_tick_label_fontsize_slider.pack(pady=10)

        self.custom_text_fontsize_slider = Scale(self.custom_plot_frame, from_=8, to_=32, orient=tk.HORIZONTAL, label="Text Font Size")
        self.custom_text_fontsize_slider.set(10)
        self.custom_text_fontsize_slider.pack(pady=10)

        self.custom_x_label_entry = Entry(self.custom_plot_frame, width=20)
        self.custom_x_label_entry.insert(0, "Elongation [%]")
        self.custom_x_label_entry.pack(pady=10)
        self.custom_y_label_entry = Entry(self.custom_plot_frame, width=20)
        self.custom_y_label_entry.insert(0, "Tensile Strength [MPa]")
        self.custom_y_label_entry.pack(pady=10)

        self.custom_canvas = None

    def create_subplots_tab(self):  # New method to create the subplots tab
        self.subplots_frame = ttk.Frame(self.tab4, padding="10")
        self.subplots_frame.pack(fill=tk.BOTH, expand=True)

        self.subplots_button = ttk.Button(self.subplots_frame, text="Plot Subplots", command=self.plot_subplots, state=tk.DISABLED)
        self.subplots_button.pack(pady=20)

        self.save_subplots_button = ttk.Button(self.subplots_frame, text="Save Subplots", command=self.save_subplots, state=tk.DISABLED)
        self.save_subplots_button.pack(pady=20)

        self.subplots_axis_label_fontsize_slider = Scale(self.subplots_frame, from_=8, to_=32, orient=tk.HORIZONTAL, label="Axis Label Font Size")
        self.subplots_axis_label_fontsize_slider.set(12)
        self.subplots_axis_label_fontsize_slider.pack(pady=10)

        self.subplots_tick_label_fontsize_slider = Scale(self.subplots_frame, from_=8, to_=32, orient=tk.HORIZONTAL, label="Tick Label Font Size")
        self.subplots_tick_label_fontsize_slider.set(10)
        self.subplots_tick_label_fontsize_slider.pack(pady=10)

        self.subplots_text_fontsize_slider = Scale(self.subplots_frame, from_=8, to_=32, orient=tk.HORIZONTAL, label="Text Font Size")
        self.subplots_text_fontsize_slider.set(10)
        self.subplots_text_fontsize_slider.pack(pady=10)

        self.subplots_canvas = None

    def process_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Excel Files",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if not file_paths:
            return

        self.results = []
        self.custom_files = file_paths

        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            file_name_no_ext = os.path.splitext(file_name)[0]
            try:
                result = process_excel(file_path)
                result["File Name"] = file_name_no_ext
                self.results.append(result)
            except ValueError as e:
                messagebox.showerror("Error", f"Error processing {file_name}: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred with {file_name}: {e}")

        if self.results:
            df_results = pd.DataFrame(self.results)
            cols = df_results.columns.tolist()
            cols.insert(0, cols.pop(cols.index("File Name")))
            self.df_results = df_results[cols]
            messagebox.showinfo("Success", "Files processed successfully. You can now save the results.")
            self.save_button.config(state=tk.NORMAL)
            self.plot_button.config(state=tk.NORMAL)
            self.update_plot_button.config(state=tk.NORMAL)
            self.subplots_button.config(state=tk.NORMAL)  # Enable the subplots button
            self.custom_update_plot_button.config(state=tk.NORMAL)

    def save_results(self):
        save_path = filedialog.asksaveasfilename(
            title="Save Results As",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if save_path:
            self.df_results.to_csv(save_path, index=False)
            messagebox.showinfo("Success", f"Analysis results saved to {save_path}")

    def plot_data(self):
        if self.df_results is None:
            messagebox.showerror("Error", "No data available for plotting.")
            return

        if self.canvas is not None:
            self.canvas.get_tk_widget().pack_forget()

        axis_label_fontsize = self.axis_label_fontsize_slider.get()
        tick_label_fontsize = self.tick_label_fontsize_slider.get()
        text_fontsize = self.text_fontsize_slider.get()
        x_label = self.x_label_entry.get()
        y_label = self.y_label_entry.get()

        self.canvas = plot_data(self.df_results, self.plot_frame, axis_label_fontsize, tick_label_fontsize, text_fontsize, x_label, y_label)
        self.save_plot_button.config(state=tk.NORMAL)

    def update_plot(self):
        self.plot_data()

    def save_plot(self):
        save_path = filedialog.asksaveasfilename(
            title="Save Plot As",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if save_path and self.canvas:
            self.canvas.figure.savefig(save_path, dpi=300)
            messagebox.showinfo("Success", f"Plot saved to {save_path}")

    def plot_custom_data(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Excel Files",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if not file_paths:
            return

        self.custom_files = file_paths

        if self.custom_canvas is not None:
            self.custom_canvas.get_tk_widget().pack_forget()

        axis_label_fontsize = self.custom_axis_label_fontsize_slider.get()
        tick_label_fontsize = self.custom_tick_label_fontsize_slider.get()
        text_fontsize = self.custom_text_fontsize_slider.get()
        x_label = self.custom_x_label_entry.get()
        y_label = self.custom_y_label_entry.get()

        fig, ax = plot_custom_files(file_paths, axis_label_fontsize, tick_label_fontsize, text_fontsize, x_label, y_label)
        self.custom_canvas = FigureCanvasTkAgg(fig, master=self.custom_plot_frame)
        self.custom_canvas.draw()
        self.custom_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.save_custom_plot_button.config(state=tk.NORMAL)
        self.custom_update_plot_button.config(state=tk.NORMAL)

    def update_custom_plot(self):
        if not self.custom_files:
            messagebox.showerror("Error", "No files available for plotting.")
            return

        if self.custom_canvas is not None:
            self.custom_canvas.get_tk_widget().pack_forget()

        axis_label_fontsize = self.custom_axis_label_fontsize_slider.get()
        tick_label_fontsize = self.custom_tick_label_fontsize_slider.get()
        text_fontsize = self.custom_text_fontsize_slider.get()
        x_label = self.custom_x_label_entry.get()
        y_label = self.custom_y_label_entry.get()

        fig, ax = plot_custom_files(self.custom_files, axis_label_fontsize, tick_label_fontsize, text_fontsize, x_label, y_label)
        self.custom_canvas = FigureCanvasTkAgg(fig, master=self.custom_plot_frame)
        self.custom_canvas.draw()
        self.custom_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_subplots(self):  # New method to plot subplots
        if self.df_results is None:
            messagebox.showerror("Error", "No data available for plotting.")
            return

        if self.subplots_canvas is not None:
            self.subplots_canvas.get_tk_widget().pack_forget()

        axis_label_fontsize = self.subplots_axis_label_fontsize_slider.get()
        tick_label_fontsize = self.subplots_tick_label_fontsize_slider.get()
        text_fontsize = self.subplots_text_fontsize_slider.get()

        self.subplots_canvas = plot_subplots(self.df_results, self.subplots_frame, axis_label_fontsize, tick_label_fontsize, text_fontsize)
        self.save_subplots_button.config(state=tk.NORMAL)

    def save_subplots(self):
        save_path = filedialog.asksaveasfilename(
            title="Save Subplots As",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if save_path and self.subplots_canvas:
            self.subplots_canvas.figure.savefig(save_path, dpi=300)
            messagebox.showinfo("Success", f"Subplots saved to {save_path}")

    def save_custom_plot(self):  # Added missing method
        save_path = filedialog.asksaveasfilename(
            title="Save Custom Plot As",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if save_path and self.custom_canvas:
            self.custom_canvas.figure.savefig(save_path, dpi=300)
            messagebox.showinfo("Success", f"Custom plot saved to {save_path}")

    def on_closing(self):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
            plt.close('all')
        if self.custom_canvas:
            self.custom_canvas.get_tk_widget().pack_forget()
            plt.close('all')
        if self.subplots_canvas:
            self.subplots_canvas.get_tk_widget().pack_forget()
            plt.close('all')
        self.root.destroy()
        sys.exit()

def create_gui():
    root = tk.Tk()
    root.geometry("800x600")
    app = ExcelFileAnalyzerApp(root)
    root.mainloop()

if __name__ == '__main__':
    create_gui()

