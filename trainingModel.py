from sklearn.model_selection import train_test_split



class trainModel:
    def __init__(self):
        # logger
        # file for logs
        pass

# load the data
# preprocess the data
# separate target variable
# impute missing values
# check further which columns do not contribute to predictions
# if the standard deviation for a column is zero, it means that the column has constant values
# and they are giving the same output both for good and bad sensors
# prepare the list of such columns to drop
# CUSTOMIZED MACHINE LEARNING APPROACH
# cluster the data
# create new columns for cluster label
# for each cluster run a loop
    # drop cluster column
    # split the data
    # train appropriate model for each cluster
    # save the model