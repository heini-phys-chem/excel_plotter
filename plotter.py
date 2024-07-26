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
    scatter = ax.scatter(df_results['Mean Toughness'], df_results['Mean Tensile Strength'], c=df_results['Mean Young\'s Modulus'], cmap=cmap, s=100, alpha=0.6)
    texts = []

    for i, row in df_results.iterrows():
        color = cmap(norm(row['Mean Young\'s Modulus']))
        text = ax.text(row['Mean Toughness'], row['Mean Tensile Strength'], row['File Name'], color=color, fontsize=text_fontsize)
        texts.append(text)

    adjust_text(
        texts,
        expand_points=(1.2, 1.2),
        lim=100,
        arrowprops=dict(arrowstyle='->', color='red', alpha=0.9, linewidth=3, linestyle=":")
    )

    plt.colorbar(scatter, label="Young's Modulus [MPa]")
    ax.set_xlabel(x_label, fontsize=axis_label_fontsize)
    ax.set_ylabel(y_label, fontsize=axis_label_fontsize)
    ax.tick_params(axis='both', which='major', labelsize=tick_label_fontsize)
    ax.grid(True, which='both', axis='both', color='gray', linestyle='--', linewidth=0.5)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    return canvas

