# Sensor-Fault-Detection
## Classification Problem Statement:
* To build a classification methodology to predict the quality of wafer sensors based on the given training data.
### Data Description:
* The client will send data in multiple sets of files in batches at a given location. Data will contain Wafer names and 590 columns of different sensor values for each wafer. The last column will have the "Good/Bad" value for each wafer.
* "Good/Bad" column will have two unique values +1 and -1.  
    >* "+1" represents Bad wafer.<br>
    >* "-1" represents Good Wafer. 
* Apart from training files, we also require a "schema" (source of truth) file from the client, which contains all the relevant information about the training files such as:
    * Name of the files, Length of Date value in FileName, Length of Time value in FileName, Number of Columns, Name of the Columns, and their datatype.
    


 
