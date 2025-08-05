# excel_processor.py
import pandas as pd
import numpy as np
from scipy.integrate import simpson
from scipy.stats import linregress

def process_excel(file_path):
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

    for i, sheet_name in enumerate(sheet_names):
        if sheet_name == "Parameters" or sheet_name == "Results" or sheet_name == "Statistics":
            continue
        data = pd.read_excel(workbook, sheet_name=sheet_name, header=1, skiprows=[0, 2])
        data.columns = ['Strain', 'Standard force']

        try:
            elongation = data['Strain'][2:].astype(float)  # Convert percentage to a decimal
            stress = data['Standard force'][2:].astype(float)  # Stress is the force per unit area
        except:
            elongation = data['Dehnung'][2:].astype(float)  # Convert percentage to a decimal
            stress = data['Standardkraft'][2:].astype(float)  # Stress is the force per unit area

        # Calculate the area under the curve using Simpson's rule for the stress-strain curve
        area = simpson(x=elongation, y=stress)

        tensile = np.append(tensile, np.max(stress.values))
        elong = np.append(elong, elongation.values[-1])
        toughness = np.append(toughness, area)

    statistics_df = pd.read_excel(workbook, sheet_name='Statistics')
    # Extract the second value (Young's modulus) and the third value (standard deviation) from the 'Et' column
    try:
        youngs_modulus = statistics_df['Et'].iloc[1]  # Second row (index 1)
        std_dev = statistics_df['Et'].iloc[2]         # Third row (index 2)
    except:
        youngs_modulus = statistics_df['EH'].iloc[1]  # Second row (index 1)
        std_dev = statistics_df['EH'].iloc[2]         # Third row (index 2)

    results = {
        "Mean Tensile Strength": np.mean(tensile),
        "Std Tensile Strength": np.std(tensile),
        "Mean Young's Modulus": youngs_modulus,
        "Std Young's Modulus": std_dev,
        "Mean Toughness": np.mean(toughness),
        "Std Toughness": np.std(toughness),
        "Mean Elongation": np.mean(elong),
        "Std Elongation": np.std(elong),
    }
    return results
