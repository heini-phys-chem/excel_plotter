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
    youngs = np.array([])

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

        # Calculate Young's modulus
        young = (stress[500] - stress[400]) / ((elongation[500] - elongation[400]) * 0.01)

        strain = elongation[300:1500]
        stress_2 = stress[300:1500]
        strain *= 0.01
        # Perform linear regression on the data
        slope, intercept, r_value, p_value, std_err = linregress(strain, stress_2)

        # Calculate Young's modulus (slope of the linear fit)
        youngs_modulus = slope

        youngs = np.append(youngs, young)
        tensile = np.append(tensile, np.max(stress.values))
        elong = np.append(elong, elongation.values[-1])
        toughness = np.append(toughness, area)

    results = {
        "Mean Tensile Strength": np.mean(tensile),
        "Std Tensile Strength": np.std(tensile),
        "Mean Young's Modulus": np.mean(youngs),
        "Std Young's Modulus": np.std(youngs),
        "Mean Toughness": np.mean(toughness),
        "Std Toughness": np.std(toughness),
        "Mean Elongation": np.mean(elong),
        "Std Elongation": np.std(elong),
    }
    return results

