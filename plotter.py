# plotter.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from adjustText import adjust_text
import pandas as pd
import tkinter as tk

def plot_data(df_results, plot_frame, axis_label_fontsize, tick_label_fontsize, text_fontsize, x_label, y_label):
    if df_results is None:
        raise ValueError("No data available for plotting.")

    cmap = plt.cm.viridis
    norm = plt.Normalize(df_results['Mean Young\'s Modulus'].min(), df_results['Mean Young\'s Modulus'].max())

    fig, ax = plt.subplots(figsize=(10, 6))

    # Extract means and standard deviations
    mean_toughness = df_results['Mean Toughness']
    std_toughness = df_results['Std Toughness']
    mean_tensile_strength = df_results['Mean Tensile Strength']
    std_tensile_strength = df_results['Std Tensile Strength']
    mean_youngs_modulus = df_results['Mean Young\'s Modulus']

    # Plot the points with error bars
    for i, (x, y, xerr, yerr) in enumerate(zip(mean_toughness, mean_tensile_strength, std_toughness, std_tensile_strength)):
        ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', ecolor='k', elinewidth=1, capsize=3, alpha=0.4)

    # Scatter plot with colors
    scatter = ax.scatter(mean_toughness, mean_tensile_strength, c=mean_youngs_modulus, cmap=cmap, s=100, alpha=0.6)

    texts = []

    for i, row in df_results.iterrows():
        color = cmap(norm(row['Mean Young\'s Modulus']))
        text = ax.text(row['Mean Toughness'], row['Mean Tensile Strength'], row['File Name'], color=color, fontsize=text_fontsize)
        texts.append(text)

    adjust_text(
        texts,
        expand_points=(1.2, 1.2),
        lim=100,
        arrowprops=dict(arrowstyle='->', color='red', alpha=0.9, linewidth=1, linestyle=":")
    )

    plt.colorbar(scatter, ax=ax, label="Young's Modulus [MPa]")
    ax.set_xlabel(x_label, fontsize=axis_label_fontsize)
    ax.set_ylabel(y_label, fontsize=axis_label_fontsize)
    ax.tick_params(axis='both', which='major', labelsize=tick_label_fontsize)
    ax.grid(True, which='both', axis='both', color='gray', linestyle='--', linewidth=0.5)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    return canvas

