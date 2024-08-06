# subplots_plotter.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def plot_subplots(df_results, plot_frame, axis_label_fontsize, tick_label_fontsize, text_fontsize):
    if df_results is None:
        raise ValueError("No data available for plotting.")

    file_names = df_results['File Name']
    mean_tensile_strength = df_results['Mean Tensile Strength']
    std_tensile_strength = df_results['Std Tensile Strength']
    mean_elongation = df_results['Mean Elongation']
    std_elongation = df_results['Std Elongation']
    mean_youngs_modulus = df_results['Mean Young\'s Modulus']
    std_youngs_modulus = df_results['Std Young\'s Modulus']
    mean_toughness = df_results['Mean Toughness']
    std_toughness = df_results['Std Toughness']

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    bar_width = 0.4

    # Tensile Strength
    axs[0, 0].bar(file_names, mean_tensile_strength, yerr=std_tensile_strength, capsize=5, color='blue', alpha=0.7)
    axs[0, 0].set_title("Tensile Strength", fontsize=axis_label_fontsize)
    axs[0, 0].set_xlabel("File Name", fontsize=axis_label_fontsize)
    axs[0, 0].set_ylabel("Tensile Strength [MPa]", fontsize=axis_label_fontsize)
    axs[0, 0].tick_params(axis='both', which='major', labelsize=tick_label_fontsize)
    axs[0, 0].grid(True)
    axs[0, 0].tick_params(axis='x', rotation=45)

    # Elongation
    axs[0, 1].bar(file_names, mean_elongation, yerr=std_elongation, capsize=5, color='green', alpha=0.7)
    axs[0, 1].set_title("Elongation", fontsize=axis_label_fontsize)
    axs[0, 1].set_xlabel("File Name", fontsize=axis_label_fontsize)
    axs[0, 1].set_ylabel("Elongation [%]", fontsize=axis_label_fontsize)
    axs[0, 1].tick_params(axis='both', which='major', labelsize=tick_label_fontsize)
    axs[0, 1].grid(True)
    axs[0, 1].tick_params(axis='x', rotation=45)

    # Young's Modulus
    axs[1, 0].bar(file_names, mean_youngs_modulus, yerr=std_youngs_modulus, capsize=5, color='red', alpha=0.7)
    axs[1, 0].set_title("Young's Modulus", fontsize=axis_label_fontsize)
    axs[1, 0].set_xlabel("File Name", fontsize=axis_label_fontsize)
    axs[1, 0].set_ylabel("Young's Modulus [MPa]", fontsize=axis_label_fontsize)
    axs[1, 0].tick_params(axis='both', which='major', labelsize=tick_label_fontsize)
    axs[1, 0].grid(True)
    axs[1, 0].tick_params(axis='x', rotation=45)

    # Toughness
    axs[1, 1].bar(file_names, mean_toughness, yerr=std_toughness, capsize=5, color='purple', alpha=0.7)
    axs[1, 1].set_title("Toughness", fontsize=axis_label_fontsize)
    axs[1, 1].set_xlabel("File Name", fontsize=axis_label_fontsize)
    axs[1, 1].set_ylabel("Toughness", fontsize=axis_label_fontsize)
    axs[1, 1].tick_params(axis='both', which='major', labelsize=tick_label_fontsize)
    axs[1, 1].grid(True)
    axs[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    return canvas

