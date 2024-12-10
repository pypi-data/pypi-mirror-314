# Author: Hauxu Yu

# A module for utility functions

import numpy as np
import pandas as pd
import os
from tqdm import tqdm
from pyteomics import mass
from pyteomics.mass.mass import isotopologues, calculate_mass
from datetime import datetime
import re


def generate_sample_table(path=None, output=True):
    """
    Generate a sample table from the mzML or mzXML files in the specified path.
    The stucture of the path should be:
    path
    ├── data
    │   ├── sample1.mzml
    │   ├── sample2.mzml
    │   └── ...
    └── ...

    Parameters
    ----------
    path : str
        Path to the main directory that contains a subdirectory 'data' with mzML or mzXML files.
    output : bool
        If True, output the sample table to a csv file.

    Return
    ------
    sample_table : pandas DataFrame
        A DataFrame with two columns: 'Sample' and 'Groups'.

    Output
    ------
    sample_table.csv : csv file
        A csv file with two columns: 'Sample' and 'Groups' in the specified path.
    """

    # if path is not specified, use the current working directory
    if path is None:
        path = os.getcwd()
    
    path_data = os.path.join(path, 'data')

    if os.path.exists(path_data):
        file_names = [os.path.splitext(f)[0] for f in os.listdir(path_data) if f.lower().endswith('.mzml') or f.lower().endswith('.mzxml')]
        file_names = [f for f in file_names if not f.startswith(".")]   # for Mac OS
        file_names = sorted(file_names)
        sample_table = pd.DataFrame({'Sample': file_names, "is_qc": [None]*len(file_names), "is_blank": [None]*len(file_names)})
    else:
        raise FileNotFoundError(f"The path {path_data} does not exist.")
    
    if output:
        sample_table.to_csv(os.path.join(path, 'sample_table.csv'), index=False)
        return None
    else:
        return sample_table


def get_timestamps(path=None, output=True):
    """
    Get timestamps for individual files and sort the files by time.
    The stucture of the path should be:
    path
    ├── data
    │   ├── sample1.mzml
    │   ├── sample2.mzml
    │   └── ...
    └── ...

    Parameters
    ----------
    path : str
        Path to the main directory that contains a subdirectory 'data' with mzML or mzXML files.
    output : bool
        If True, output the timestamps to a txt file with two columns: 'file_name' and 'aquisition_time'.

    Return
    ------
    file_times : list
        A list of tuples with two elements: 'file_name' and 'aquisition_time'.

    Output
    ------
    timestamps.txt : txt file
        A txt file with two columns: 'file_name' and 'aquisition_time' in the specified path.
    """

    # if path is not specified, use the current working directory
    if path is None:
        path = os.getcwd()
    
    path_data = os.path.join(path, 'data')

    if os.path.exists(path_data):
        file_names = [f for f in os.listdir(path_data) if f.lower().endswith('.mzml') or f.lower().endswith('.mzxml')]
        file_names = [f for f in file_names if not f.startswith(".")]  # for Mac OS
        file_names = sorted(file_names)

    times = []
    print("Getting timestamps for individual files...")
    for f in tqdm(file_names):
        tmp = os.path.join(path_data, f)
        times.append(get_start_time(tmp))
    
    file_names = [f.split(".")[0] for f in file_names]
    
    # sort the files by time
    file_times = list(zip(file_names, times))
    file_times = sorted(file_times, key=lambda x: x[1])

    # output to a txt file using pandas

    df = pd.DataFrame(file_times, columns=["file_name", "aquisition_time"])
    if output:
        output_path = os.path.join(path, "timestamps.txt")
        df.to_csv(output_path, sep="\t", index=False)
    else:
        return df


# Note: this function is not used in the current version of the package
def cal_ion_mass(formula, adduct, charge):
    """
    A function to calculate the ion mass of a given formula, adduct and charge.

    Parameters
    ----------
    formula: str
        The chemical formula of the ion.
    adduct: str
        Adduct of the ion.
    charge: int
        Charge of the ion. 
        Use signs for specifying ion modes: +1 for positive mode and -1 for negative mode.

    Returns
    -------
    ion_mass: float
        The ion mass of the given formula, adduct and charge.
    """

    # if there is a D in the formula, and not followed by a lowercase letter, replace it with H[2]
    if 'D' in formula and not formula[formula.find('D') + 1].islower():
        formula = formula.replace('D', 'H[2]')

    # calculate the ion mass
    final_formula = formula + adduct
    ion_mass = (mass.calculate_mass(formula=final_formula) - charge * _ELECTRON_MASS) / abs(charge)
    return ion_mass

_ELECTRON_MASS = 0.00054858


# Note: this function is not used in the current version of the package
def calculate_isotope_distribution(formula, mass_resolution=10000, intensity_threshold=0.001):

    mass = []
    abundance = []

    for i in isotopologues(formula, report_abundance=True, overall_threshold=intensity_threshold):
        mass.append(calculate_mass(i[0]))
        abundance.append(i[1])
    mass = np.array(mass)
    abundance = np.array(abundance)
    order = np.argsort(mass)
    mass = mass[order]
    abundance = abundance[order]

    mass_diffrence = mass[0] / mass_resolution
    # merge mass with difference lower than mass_diffrence
    groups = []
    group = [0]
    for i in range(1, len(mass)):
        if mass[i] - mass[i-1] < mass_diffrence:
            group.append(i)
        else:
            groups.append(group)
            group = [i]
    groups.append(group)

    mass = [np.mean(mass[i]) for i in groups]
    abundance = [np.sum(abundance[i]) for i in groups]
    abundance = np.array(abundance) / np.max(abundance)

    return mass, abundance
    
def get_start_time(file_name):
    """
    Function to get the start time of the raw data.

    Parameters
    ----------
    file_name : str
        Absolute path of the raw data.
    """

    if os.path.exists(str(file_name)):
        with open(file_name, "rb") as f:
            for l in f:
                l = str(l)
                if "startTimeStamp" in str(l):
                    t = l.split("startTimeStamp")[1].split('"')[1]
                    return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")


def extract_signals_from_string(ms2):
    """
    Extract signals from MS2 spectrum in string format.

    Parameters
    ----------
    ms2 : str
        MS2 spectrum in string format. Format: "mz1;intensity1|mz2;intensity2|..."
        example: "100.0;1000.0|200.0;2000.0|300.0;3000.0|"
    
    returns
    ----------
    peaks : numpy.array
        Peaks in numpy array format.
    """
    
    # Use findall function to extract all numbers matching the pattern
    numbers = re.findall(r'\d+\.\d+', ms2)
    
    # Convert the extracted numbers from strings to floats
    numbers = [float(num) for num in numbers]
    
    numbers = np.array(numbers).reshape(-1, 2)

    return numbers


def convert_signals_to_string(signals):
    """
    Convert peaks to string format.

    Parameters
    ----------
    signals : numpy.array
        MS2 signals organized as [[mz1, intensity1], [mz2, intensity2], ...]

    Returns
    -------
    string : str
        Converted signals in string format. Format: "mz1;intensity1|mz2;intensity2|..."
    """

    if signals is None:
        return None
    
    string = ""
    for i in range(len(signals)):
        string += str(np.round(signals[i, 0], decimals=4)) + ";" + str(np.round(signals[i, 1], decimals=4)) + "|"
    string = string[:-1]
    
    return string