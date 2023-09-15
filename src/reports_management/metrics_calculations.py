"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_weight_sim/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    This class contains results of metrics calculations. It is used to print data ant for storage results
Use:
"""


class MetricsCalculations:
    total_objects = 0
    sum_predict_objects = 0.0
    mean_predict_objects = 0.0
    sum_measured_objects = 0.0
    mean_measured_objects = 0.0
    MSE = 0.0
    MAE = 0.0
    RMSE = 0.0
    MAPE = 0.0
    R2 = 0.0
    unit_of_measurement = None

    def __init__(self, unit_of_measurement):
        self.unit_of_measurement = unit_of_measurement

    def print_metrics(self):
        print(f'total_objects-> {self.total_objects}')
        print(f'sum predicted ={self.sum_predict_objects}')
        print(f'mean predicted ={self.mean_predict_objects}')
        print(f'sum measured ={self.sum_measured_objects}')
        print(f'mean measured ={self.mean_measured_objects}')
        print(f'MSE = {self.MSE}')
        print(f'MAE = {self.MAE} {self.unit_of_measurement}')
        print(f'RMSE = {self.RMSE}')
        print(f'MAPE = {self.MAPE}')
        print(f'R2={self.R2}')

    def print_metrics_02(self):
        string_to_go = f'total_objects-> {self.total_objects},\n sum predicted ={self.sum_predict_objects},\n mean predicted ={self.mean_predict_objects},\n sum measured ={self.sum_measured_objects},\n mean measured ={self.mean_measured_objects},\n MSE = {self.MSE},\n MAE = {self.MAE} {self.unit_of_measurement},\n RMSE = {self.RMSE},\n MAPE = {self.MAPE},\n R2={self.R2}'

        return string_to_go

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (str(self.total_objects),
                                                           str(self.sum_predict_objects),
                                                           str(self.mean_predict_objects),
                                                           str(self.sum_measured_objects),
                                                           str(self.mean_measured_objects),
                                                           str(self.MSE),
                                                           str(self.MAE),
                                                           str(self.RMSE),
                                                           str(self.MAPE),
                                                           str(self.R2)
                                                           )
"""
Project: Size Estimation
Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
Date: February 2022
Description:
    This class contains results of metrics calculations. It is used to print data and for storage results
Use:
"""

"""
class MetricsCalculations:
    total_objects = 0
    sum_predict_objects = 0.0
    mean_predict_objects = 0.0
    sum_measured_objects = 0.0
    mean_measured_objects = 0.0
    MSE = 0.0
    MAE = 0.0
    RMSE = 0.0
    MAPE = 0.0
    R2 = 0.0
    unit_of_measurement = None

    def __init__(self, unit_of_measurement):
        self.unit_of_measurement = unit_of_measurement

    def print_metrics(self):
        print(f'total_objects-> {self.total_objects}')
        print(f'sum predicted ={self.sum_predict_objects}')
        print(f'mean predicted ={self.mean_predict_objects}')
        print(f'sum measured ={self.sum_measured_objects}')
        print(f'mean measured ={self.mean_measured_objects}')
        print(f'MSE = {self.MSE}')
        print(f'MAE = {self.MAE} {self.unit_of_measurement}')
        print(f'RMSE = {self.RMSE}')
        print(f'MAPE = {self.MAPE}')
        print(f'R2={self.R2}')

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (str(self.total_objects),
                                                           str(self.sum_predict_objects),
                                                           str(self.mean_predict_objects),
                                                           str(self.sum_measured_objects),
                                                           str(self.mean_measured_objects),
                                                           str(self.MSE),
                                                           str(self.MAE),
                                                           str(self.RMSE),
                                                           str(self.MAPE),
                                                           str(self.R2)
                                                           )
"""