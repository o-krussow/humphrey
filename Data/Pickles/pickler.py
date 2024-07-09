import pickle
from os import listdir
from os.path import isfile, join

csvs = {}

csvpath = "../csvs/"
        
#Get a list of csv files, path is not included
csvfilelist = [csvpath+f for f in listdir(csvpath) if isfile(join(csvpath, f))] 

for csv in csvfilelist:
    with open(csv, "r") as f:
        file_contents = f.read()

    #split file by newline
    split_file = file_contents.split("\n")
    tmp_list = []
    #iterate thru each line in file. Then add a tuple to tmp_list, after splitting the line around ","
    for line in split_file:
        #(date, price)
        try:
            tmp_list.append((line.split(",")[0], float(line.split(",")[1])))
        except ValueError:
            continue
        except IndexError:
            continue

    if csv.replace(csvpath, "") == "fixedcsv":
        continue
    #store list of tuples to self.csvs for future reference.
    csvs[csv.replace(csvpath, "").replace(".csv", "")] = tmp_list


# open a file, where you ant to store the data
file = open('pickled_csvs', 'wb')

# dump information to that file
pickle.dump(csvs, file)

# close the file
file.close()
