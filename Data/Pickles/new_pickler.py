import pickle
from os import listdir
from os.path import isfile, join, dirname
import pandas as pd
import numpy as np

csvpath = join(dirname(__file__), '../csvs/')
pickled_df = pd.DataFrame()
for f in listdir(csvpath):
    if isfile(join(csvpath, f)):
        dates = np.loadtxt(csvpath+f, skiprows=1, usecols = 0, delimiter = ',', dtype='str')
        prices = np.loadtxt(csvpath+f, skiprows=1, usecols = 1, delimiter = ',')

        df = pd.DataFrame(prices)
        df = df.set_index(dates)
        df.columns = [f.replace(".csv", "")]
        pickled_df = pd.merge(pickled_df, df, how='outer',left_index=True, right_index=True)

file = open('pickled_df', 'wb')

# dump information to that file
pickle.dump(pickled_df, file)

# close the file
file.close()