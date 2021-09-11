import os
import csv
import pandas as pd
import numpy as np
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
#Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

# show an "Open" dialog box and return the path to the selected file
filename = askopenfilename() 

# reading csv file using file chooser dialogue
file_path, base_file_name = os.path.split(filename)
file_name, file_extension = os.path.splitext(base_file_name)
df = pd.read_csv(filename, index_col='#symbol')

#Data filtering based on Absolute logFC >= 1 and adjusted p value < 0.005
filtered = df.loc[(abs(df["logFC"]) >= 1) & (df["adj.p"] < 0.005)]

#Separating up and down regulated genes
upregulated = filtered.loc[filtered["logFC"] > 0]
downregulated = filtered.loc[filtered["logFC"] < 0]
up = pd.DataFrame(upregulated.index.values, columns = ['Up'])
down = pd.DataFrame(downregulated.index.values, columns = ['Down'])

#Combining both Up and down regulated genes into a DataFrame
AllGenes = pd.concat([up,down])
AllGenes["Up"] = AllGenes["Up"].sort_values(ascending = True).values
AllGenes["Down"] = AllGenes["Down"].sort_values(ascending = True).values

#Remove Unnecessary column and rows with nan values
AllGenes = AllGenes.reset_index()
AllGenes = AllGenes.drop(columns = ["index"])
if down.size < up.size :
    AllGenes.dropna(subset = ["Up"], inplace = True)
else :
    AllGenes.dropna(subset = ["Down"], inplace = True)

#Writing to a csv file
AllGenes.to_csv(file_name + "Filtered" + file_extension)