import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

class Preprocessor:
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def remove_columns(self, data, columns):
        self.logger_object.log(self.file_object, "Entered the remove_columns method of the Preprocessor class")
        self.data = data
        self.columns = columns
        try:
            self.useful_data = self.data.drop(labels=self.columns, axis=1)
            self.logger_object.log(self.file_object, "Column removal Successful.Exited the remove_columns method of the Preprocessor class")
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occured in remove_columns method of the Preprocessor class. Exception message: {str(e)}')
            self.logger_object.log(self.file_object, f'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            raise Exception()

    def separate_label_feature(self, data, label_column_name):
        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X = data.drop(labels=label_column_name,
                               axis=1)  # drop the columns specified and separate the feature columns
            self.Y = data[label_column_name]  # Filter the Label columns
            self.logger_object.log(self.file_object, 'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X, self.Y
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occured in separate_label_feature method of the Preprocessor class. Exception message: {str(e)} ')
            self.logger_object.log(self.file_object, 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()

    def is_null_present(self,data):
        try:
            self.null_counts = data.isna().sum()
            for i in self.null_counts:
                if i > 0:
                    self.null_present = True
                    break
            if self.null_present:
                df_with_null = pd.DataFrame()
                df_with_null['columns'] = data.columns
                df_with_null['missing_values_count'] = np.asarray(data.isna().sum())
                df_with_null.to_csv('preprocessing_data/null_values.csv')
            self.logger_object.log(self.file_object,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present

        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occured in is_null_present method of the Preprocessor class. Exception message: {str(e)} ')
            self.logger_object.log(self.file_object, 'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
        raise Exception()

    def impute_missing_values(self, data):
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data = data
        try:
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            self.new_array = imputer.fit_transform(self.data)  # impute the missing values

            # convert the nd-array returned in the step above to a Dataframe
            self.new_data = pd.DataFrame(data=self.new_array, columns=self.data.columns)
            self.logger_object.log(self.file_object, 'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.new_data
        except Exception as e:
            self.logger_object.log(self.file_object, f'Exception occured in impute_missing_values method of the Preprocessor class. Exception message: {str(e)} ')
            self.logger_object.log(self.file_object, 'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

