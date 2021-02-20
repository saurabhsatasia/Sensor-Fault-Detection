from sklearn.model_selection import train_test_split
from data_ingestion import data_loader
from data_preprocessing import preprocessing
from data_preprocessing import clustering
from best_model_finder import tuner
from file_operations import file_methods
from application_logging import logger


class trainModel:
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open("Training_Logs/ModelTraininLog.txt", 'a+')

    def trainingModel(self):
        # Logging the start of Training
        self.log_writer.log(self.file_object, "Start of Training")
        try:
            # Get data from source
            data_getter = data_loader.Data_Getter(self.file_object, self.log_writer)
            data = data_getter.get_data()
            """Data Preprocessing"""
            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            data = preprocessor.remove_columns(data, ['Wafer'])

            # separate independent features(predictors) and dependent/target feature
            X,Y = preprocessor.separate_label_feature(data, label_column_name='Output')

            # check if missing values are present in the dataset
            is_null_present = preprocessor.is_null_present(X)

            # if missing values are there, replace them appropriately
            if is_null_present:
                X=preprocessor.impute_missing_values(data=X)

            # check further which columns do not contribute to predictions
            # if standard deviation for a column is zero, it means that the column has constant values
            # and they are giving the same output for both good and bad sensors
            # prepare the list of such columns to drop
            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(X)

            #drop the columns obtained above
            X = preprocessor.remove_columns(X, cols_to_drop)

            """Apply the KMeans Clustering approach"""
            kmeans=clustering.KMeansClustering(self.file_object, self.log_writer)
            number_of_clusters=kmeans.elbow_plot(X)

            # Divide the data into clusters
            X = kmeans.create_clusters(X, number_of_clusters)

            # create a new column in the dataset consisting of the corresponding cluster assignments
            X['Labels'] = Y

            # getting the inique clusters from our dataset
            list_of_clusters = X['Cluster'].unique()

            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""
            for i in list_of_clusters:
                cluster_data = X[X['Cluster']==i] # filter the data for one cluster

                # Prepare the feature and Label columns:
                cluster_features = cluster_data.drop(['Labels', 'Cluster'], axis=1)
                cluster_label = cluster_data['Labels']

                # Splitting the data into training and test set for each cluster
                X_train, X_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1/3, random_state=355)
                model_finder = tuner.Model_Finder(self.file_object, self.log_writer)

                # getting the best model for each of the clusters
                best_model_name, best_model = model_finder.get_best_model(train_x=X_train, train_y=y_train,test_x=X_test, test_y=y_test)

                # saving the best model to the directory
                file_op = file_methods.File_Operation(self.file_object, self.log_writer)
                save_model = file_op.save_model(best_model, best_model_name+str(i))

            # logging the Successfull Training
            self.log_writer.log(self.file_object, "Successfull End of Training")
            self.file_object.close()
        except Exception:
            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')
            self.file_object.close()
            raise Exception
