import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def make_to_gbr(data, save = False):
    subset = data[data["iso_d"] == "GBR"]
    if save:
        subset.to_csv("../data/to_gbr.csv")
    return subset

def make_from_gbr(data, save = False):
    subset = data[data["iso_o"] == "GBR"]
    if save:
        subset.to_csv("../data/from_gbr.csv")
    return subset

def get_colony_isos(data):
    family = data[data["family"] == "GBR"]
    f1 = family["sever"] >= 1947
    f2 = family["indepdate"] >= 1947
    f3 = f1 | f2
    subset = family[f3]
    isos = subset.iso_o.unique()
    return isos


# Make csv of extended trading networks.
# This is used to find the primary trading partners of a country
# in a specified year.
def make_extended_trading(data, save = False):
    isos = get_colony_isos(data)
    
    f1 = data.iso_d.isin(isos)
    f2 = data.iso_o.isin(isos)
    f3 = f1 | f2

    subset = data[f3]

    if save:
        subset.to_csv("../data/extended_trading.csv")
    return subset
    
# Make csv of the primary colonies that will be used in the visualization.
# This is the main dataset for the project.
def make_primary_colonies(data, save = False):
    family = data[data["family"] == "GBR"]
    isos = get_colony_isos(data)
    np.append(isos, "GBR")

    f1 = family.iso_d.isin(isos)
    f2 = family.iso_o.isin(isos)
    f3 = f1 & f2

    subset = family[f3]

    if save:
        subset.to_csv("../data/primary_colonies.csv")
    return subset

def make_filtered(data, save = False):
    pass

def filter_from_to(data, origin, dest, save = False):
    f1 = data["iso_o"] == origin
    f2 = data["iso_d"] == dest
    f3 = f1 & f2
    subset = data[f3]
    if save:
        subset.to_csv("../data/gha_to_gbr.csv")
    return subset


def get_stats(data):
    print("Mean: ", np.mean(data["flow"]))
    print("Variance: ", np.var(data["flow"]))

def get_flow_hist(data):
    a = data[data["flow"] > 0]
    hist, bins = np.histogram(a["flow"], bins = [0, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0])
    print(hist/np.sum(hist))
    print(bins)

if __name__ == "__main__":
    data = pd.read_stata("../data/col_regfile09.dta")
    #gha_to_gbr = filter_from_to(data, "GHA", "GBR")
    #gbr_to_gha = filter_from_to(data, "GBR", "GHA")
    #a = range(len(gha_to_gbr))
    #plt.plot(a, gha_to_gbr["flow"], a, gbr_to_gha["flow"])
    #plt.show()
    make_primary_colonies(data, True)
    make_extended_trading(data, True)
