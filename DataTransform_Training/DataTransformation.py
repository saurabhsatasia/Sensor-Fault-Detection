from datetime import datetime
from os import listdir
import pandas as pd
from application_logging.logger import App_Logger

class dataTransform:
    def __init__(self):
        self.goodDataPath = 'Training_Raw_files_validated/Good_Raw'
        self.logger = App_Logger()

    def replaceMissingWithNull(self):
        log_file = open("Training_Logs/dataTransformLog.txt", 'a+')
        try:
            onlyfiles=[f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                csv = pd.read_csv(self.goodDataPath+"/"+file)
                csv.fillna('NULL', inplace=True)
                csv['Wafer'] = csv['Wafer'].str[6:]
                csv.to_csv(self.goodDataPath+"/"+file, index=None, header=True)
                self.logger.log(log_file, f"{file}: File Transformed successfully!!")
        except Exception as e:
            self.logger.log(log_file, f"Data Transformation Failed because:: {e}")
            log_file.close()
        log_file.close()