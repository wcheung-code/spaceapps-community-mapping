# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 09:40:56 2024

@author: Rabin
"""
import os
import pandas as pd
from time import strptime
from tkinter import filedialog

# Display the dialog for browsing files.
file_name = filedialog.askopenfilename()
# Print the selected file path.
print(file_name)

#%%
raw_df = pd.read_csv(file_name)
#extract data 
population=raw_df[raw_df['Component']=='Population']
immigrants=raw_df[raw_df['Component']=='Immigrants']
emigrants=raw_df[raw_df['Component']=='Emigrants']

#save output files.
population.to_csv(os.path.join(os.path.dirname(file_name), 'irish_population.csv'))
immigrants.to_csv(os.path.join(os.path.dirname(file_name), 'immigrants.csv'))
emigrants.to_csv(os.path.join(os.path.dirname(file_name), 'emigrants.csv'))
