# custom_plotter.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def make_plot(file_path, ax, color, linestyle, text_fontsize):
    # Determine the file extension
    if file_path.endswith('.xlsx'):
        engine = 'openpyxl'
    elif file_path.endswith('.xls'):
        engine = 'xlrd'
    else:
        raise ValueError("Unsupported file type")

    workbook = pd.ExcelFile(file_path, engine=engine)
    sheet_names = workbook.sheet_names

    toughness = np.array([])
    tensile = np.array([])
    elong = np.array([])
    youngs = np.array([])

    for i, sheet_name in enumerate(sheet_names):
        if i == 0 or i == 1:
            continue
        data = pd.read_excel(workbook, sheet_name=sheet_name, header=1, skiprows=[0, 2])
        data.columns = ['Strain', 'Standard force']

        try:
            elongation = data['Strain'][2:].astype(float)  # Convert percentage to a decimal
            stress = data['Standard force'][2:].astype(float)  # Stress is the force per unit area
        except:
            elongation = data['Dehnung'][2:].astype(float)  # Convert percentage to a decimal
            stress = data['Standardkraft'][2:].astype(float)  # Stress is the force per unit area

        ax.plot(elongation, stress, linestyle=linestyle, color=color)

def plot_custom_files(files, axis_label_fontsize, tick_label_fontsize, text_fontsize, x_label, y_label):
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = plt.cm.tab20(np.linspace(0, 1, len(files)))
    linestyles = [":", "--", "-", "-."] * (len(files) // 4 + 1)

    legend_elements = []
    texts = []

    for file, color, linestyle in zip(files, colors, linestyles):
        make_plot(file, ax, color, linestyle, text_fontsize)
        legend_elements.append(Line2D([0], [0], color=color, lw=2, linestyle=linestyle, label=os.path.splitext(os.path.basename(file))[0]))

    ax.set_xlabel(x_label, fontsize=axis_label_fontsize)
    ax.set_ylabel(y_label, fontsize=axis_label_fontsize)
    ax.tick_params(axis='both', which='major', labelsize=tick_label_fontsize)
    ax.grid(True, which='both', axis='both', color='gray', linestyle=':', linewidth=0.5)
    plt.legend(handles=legend_elements, loc='lower right', fontsize=text_fontsize)

    plt.tight_layout()
    return fig, ax

