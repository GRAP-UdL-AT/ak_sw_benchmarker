"""
Project: ak_sw_benchmarker Azure Kinect Size Estimation https://github.com/juancarlosmiranda/ak_size_weight_sim/

* PAgFRUIT http://www.pagfruit.udl.cat/en/
* GRAP http://www.grap.udl.cat/

Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda/
Date: February 2022
Description:
    From dataframe, this calculates metrics for: axis_01=caliber, axis_02=height, mass
    axis_01 = is the major axis
    axis_02 = is the minor axis

    By rule, in the paper is expressed using this rule, the measure taken in laboratory is axis_01

    https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
    30/01/2023, changes in variables names: caliber, height, mass
Use:

"""
import math
from reports_management.metrics_calculations import MetricsCalculations
from sklearn.metrics import r2_score
from reports_management.comparative_measures_reports_selector import ComparativeMeasuresReportSelector
# todo: pasar test_frame_comparative_mass a clase
# todo: pasar test_folder_comparative_mass a clase



class ComparativeMeasuresReport:
    comparative_df = None
    report_selector = None
    depth_metrics = MetricsCalculations('mm.')
    axis_01_metrics = MetricsCalculations('mm.')
    axis_02_metrics = MetricsCalculations('mm.')
    weight_metrics = MetricsCalculations('gr.')

    def __init__(self, input_dataset_df, report_selector):
        self.comparative_df = input_dataset_df
        self.report_selector = report_selector
        self.calculate_metrics()

    def __del__(self):
        print('------------------------------->')

    def calculate_depth_metrics(self):
        # ---------------
        # depth
        # ---------------
        total_objects = self.comparative_df.shape[0]
        self.comparative_df['depth_abs_dif'] = abs(self.comparative_df['pred.depth_mm'] - self.comparative_df[
            'lab.depth_mm'])
        self.comparative_df['depth_mape_abs_dif'] = abs(
            (self.comparative_df['lab.depth_mm'] - self.comparative_df['pred.depth_mm']) / self.comparative_df[
                'lab.depth_mm'])
        self.comparative_df['depth_sqr_dif'] = pow(
            (self.comparative_df['pred.depth_mm'] - self.comparative_df['lab.depth_mm']), 2)
        mean_lab_depth = self.comparative_df[
            'lab.depth_mm'].mean()  # todo: check this decimals could be cause of errors!!
        self.comparative_df['depth_sqr_mean_dif'] = pow((self.comparative_df['lab.depth_mm'] - mean_lab_depth), 2)
        total_sqr_dif_depth = self.comparative_df['depth_sqr_dif'].sum()
        total_abs_dif_depth = self.comparative_df['depth_abs_dif'].sum()
        total_mape_abs_dif_depth = self.comparative_df['depth_mape_abs_dif'].sum()
        total_r1 = total_sqr_dif_depth
        total_r2 = self.comparative_df['depth_sqr_mean_dif'].sum()

        self.depth_metrics.total_objects = self.comparative_df['pred.depth_mm'].count()
        self.depth_metrics.sum_predict_objects = self.comparative_df['pred.depth_mm'].sum()
        self.depth_metrics.mean_predict_objects = self.comparative_df['pred.depth_mm'].mean()
        self.depth_metrics.sum_measured_objects = self.comparative_df['lab.depth_mm'].sum()
        self.depth_metrics.mean_measured_objects = self.comparative_df['lab.depth_mm'].mean()
        self.depth_metrics.MSE = total_sqr_dif_depth / total_objects
        self.depth_metrics.MAE = total_abs_dif_depth / total_objects
        self.depth_metrics.RMSE = math.sqrt(total_sqr_dif_depth / total_objects)
        self.depth_metrics.MAPE = total_mape_abs_dif_depth / total_objects

        y_true = self.comparative_df['lab.depth_mm']
        y_pred = self.comparative_df['pred.depth_mm']

        self.depth_metrics.R2 = r2_score(y_true, y_pred)  # real


    def calculate_axis_01_metrics(self):
        # ---------------
        # caliber
        # ---------------
        total_objects = self.comparative_df.shape[0]
        self.comparative_df['axis_01_abs_dif'] = abs(self.comparative_df['pred.axis_01_mm'] - self.comparative_df['lab.axis_01_mm'])
        self.comparative_df['axis_01_mape_abs_dif'] = abs((self.comparative_df['lab.axis_01_mm'] - self.comparative_df['pred.axis_01_mm']) / self.comparative_df['lab.axis_01_mm'])
        self.comparative_df['axis_01_sqr_dif'] = pow((self.comparative_df['pred.axis_01_mm'] - self.comparative_df['lab.axis_01_mm']), 2)

        mean_lab_axis_01 = self.comparative_df['lab.axis_01_mm'].mean()  # todo: check this decimals could be cause of errors!!
        self.comparative_df['axis_01_sqr_mean_dif'] = pow((self.comparative_df['lab.axis_01_mm'] - mean_lab_axis_01), 2)

        total_sqr_dif_axis_01 = self.comparative_df['axis_01_sqr_dif'].sum()
        total_abs_dif_axis_01 = self.comparative_df['axis_01_abs_dif'].sum()
        total_mape_abs_dif_axis_01 = self.comparative_df['axis_01_mape_abs_dif'].sum()
        SSE_axis_01 = total_sqr_dif_axis_01
        SST_axis_01 = self.comparative_df['axis_01_sqr_mean_dif'].sum()

        self.axis_01_metrics.total_objects = self.comparative_df['pred.axis_01_mm'].count()
        self.axis_01_metrics.sum_predict_objects = self.comparative_df['pred.axis_01_mm'].sum()
        self.axis_01_metrics.mean_predict_objects = self.comparative_df['pred.axis_01_mm'].mean()
        self.axis_01_metrics.sum_measured_objects = self.comparative_df['lab.axis_01_mm'].sum()
        self.axis_01_metrics.mean_measured_objects = self.comparative_df['lab.axis_01_mm'].mean()
        self.axis_01_metrics.MSE = total_sqr_dif_axis_01 / total_objects
        self.axis_01_metrics.MAE = total_abs_dif_axis_01 / total_objects
        self.axis_01_metrics.RMSE = math.sqrt(total_sqr_dif_axis_01 / total_objects)
        self.axis_01_metrics.MAPE = total_mape_abs_dif_axis_01 / total_objects

        # todo 23/02/2022, there is a bug with apple 136, this column is calculated as zero 'caliber_sqr_mean_dif'
        y_true = self.comparative_df['lab.axis_01_mm']
        y_pred = self.comparative_df['pred.axis_01_mm']

        R2_2 = 1 - (SSE_axis_01 / SST_axis_01)
        #self.caliber_metrics.R2 = r2_score(y_pred, y_true)
        self.axis_01_metrics.R2 = r2_score(y_true, y_pred)  # real
        #self.caliber_metrics.R2 = r2_score(y_pred, y_true)  # not real

        print('R2_2 ->', R2_2)
        print('SSE_axis_01 ->', SSE_axis_01)
        print('SST_axis_01 ->', SST_axis_01)
        print('self.axis_01_metrics.R2 ->', self.axis_01_metrics.R2)
        print('real -> r2_score(y_true, y_pred)', r2_score(y_true, y_pred))
        print('r2_score(y_pred, y_true)', r2_score(y_pred, y_true))


    def calculate_axis_02_metrics(self):
        # ---------------
        # height
        # ---------------
        total_objects = self.comparative_df.shape[0]
        self.comparative_df['axis_02_abs_dif'] = abs(self.comparative_df['pred.axis_02_mm'] - self.comparative_df['lab.axis_02_mm'])
        self.comparative_df['axis_02_mape_abs_dif'] = abs((self.comparative_df['lab.axis_02_mm'] - self.comparative_df['pred.axis_02_mm']) / self.comparative_df['lab.axis_02_mm'])
        self.comparative_df['axis_02_sqr_dif'] = pow((self.comparative_df['pred.axis_02_mm'] - self.comparative_df['lab.axis_02_mm']), 2)

        mean_lab_axis_02 = self.comparative_df['lab.axis_02_mm'].mean()  # todo: check this decimals could be cause of errors!!
        self.comparative_df['axis_02_sqr_mean_dif'] = pow((self.comparative_df['lab.axis_02_mm'] - mean_lab_axis_02), 2)
        total_sqr_dif_axis_02 = self.comparative_df['axis_02_sqr_dif'].sum()
        total_abs_dif_axis_02 = self.comparative_df['axis_02_abs_dif'].sum()
        total_mape_abs_dif_axis_02 = self.comparative_df['axis_02_mape_abs_dif'].sum()

        SSE_axis_02 = total_sqr_dif_axis_02
        SST_axis_02 = self.comparative_df['axis_02_sqr_mean_dif'].sum()

        self.axis_02_metrics.total_objects = self.comparative_df['pred.axis_02_mm'].count()
        self.axis_02_metrics.sum_predict_objects = self.comparative_df['pred.axis_02_mm'].sum()
        self.axis_02_metrics.mean_predict_objects = self.comparative_df['pred.axis_02_mm'].mean()
        self.axis_02_metrics.sum_measured_objects = self.comparative_df['lab.axis_02_mm'].sum()
        self.axis_02_metrics.mean_measured_objects = self.comparative_df['lab.axis_02_mm'].mean()
        self.axis_02_metrics.MSE = total_sqr_dif_axis_02 / total_objects
        self.axis_02_metrics.MAE = total_abs_dif_axis_02 / total_objects
        self.axis_02_metrics.RMSE = math.sqrt(total_sqr_dif_axis_02 / total_objects)
        self.axis_02_metrics.MAPE = total_mape_abs_dif_axis_02 / total_objects

        #self.height_metrics.R2 = 1 - (SSE_height / SST_height)

        # TODO: 03/08/2022
        y_true = self.comparative_df['lab.axis_02_mm']
        y_pred = self.comparative_df['pred.axis_02_mm']

        self.axis_02_metrics.R2 = r2_score(y_true, y_pred)  # real
        #R2_2 = 1 - (SSE_height / SST_height)

        #print('R2_2 ->', R2_2)
        print('SSE_axis_02 ->', SSE_axis_02)
        print('SST_axis_02 ->', SST_axis_02)
        print('self.axis_02_metrics.R2 ->', self.axis_02_metrics.R2)
        print('r2_score(y_true, y_pred)', r2_score(y_true, y_pred))
        print('r2_score(y_pred, y_true)', r2_score(y_pred, y_true))



    def calculate_weight_metrics(self):
        # ---------------
        # WEIGHT
        # ---------------
        total_objects = self.comparative_df.shape[0]
        self.comparative_df['weight_abs_dif'] = abs(self.comparative_df['pred.weight_gr'] - self.comparative_df['lab.weight_gr'])  # TODO: MAE
        self.comparative_df['weight_mape_abs_dif'] = abs((self.comparative_df['lab.weight_gr'] - self.comparative_df['pred.weight_gr']) / self.comparative_df['lab.weight_gr']) #todo: ok
        self.comparative_df['weight_sqr_dif'] = pow((self.comparative_df['lab.weight_gr'] - self.comparative_df['pred.weight_gr']), 2)  # todo: good

        mean_lab_weight = self.comparative_df['lab.weight_gr'].mean()
        self.comparative_df['weight_sqr_mean_dif'] = pow((self.comparative_df['lab.weight_gr'] - mean_lab_weight), 2)  # TODO: SST

        total_sqr_dif_weight = self.comparative_df['weight_sqr_dif'].sum()
        total_abs_dif_weight = self.comparative_df['weight_abs_dif'].sum()  # TODO: MAE

        total_mape_abs_dif_weight = self.comparative_df['weight_mape_abs_dif'].sum()
        #SSE_mass = total_sqr_dif_weight  # it was used for R2
        #SST_mass = self.comparative_df['mass_sqr_mean_dif'].sum()  # it was used for R2

        self.weight_metrics.total_objects = self.comparative_df['pred.weight_gr'].count()
        self.weight_metrics.sum_predict_objects = self.comparative_df['pred.weight_gr'].sum()
        self.weight_metrics.mean_predict_objects = self.comparative_df['pred.weight_gr'].mean()
        self.weight_metrics.sum_measured_objects = self.comparative_df['lab.weight_gr'].sum()
        self.weight_metrics.mean_measured_objects = self.comparative_df['lab.weight_gr'].mean()

        self.weight_metrics.MSE = total_sqr_dif_weight / total_objects
        self.weight_metrics.MAE = total_abs_dif_weight / total_objects  # TODO: MAE
        self.weight_metrics.RMSE = math.sqrt(total_sqr_dif_weight / total_objects)
        self.weight_metrics.MAPE = total_mape_abs_dif_weight / total_objects

        # TODO: 03/08/2022
        y_true = self.comparative_df['lab.weight_gr']
        y_pred = self.comparative_df['pred.weight_gr']

        #R2_2 = 1 - (SSE_mass / SST_mass)  # TODO: CORRECT THIS
        self.weight_metrics.R2 = r2_score(y_true, y_pred)    # real # 1 - (total_r1 / total_r2) # TODO: CORRECT THIS
        #print('R2_1 -->', self.mass_metrics.R2)
        #print('R2_2 -->', R2_2)


    def calculate_metrics(self):
        if self.report_selector == ComparativeMeasuresReportSelector.WEIGHT:
            #self.calculate_depth_metrics() # todo: check this it is not generalizable
            self.calculate_axis_01_metrics()
            self.calculate_axis_02_metrics()
            self.calculate_weight_metrics()
        elif self.report_selector == ComparativeMeasuresReportSelector.DEPTH:
            self.calculate_depth_metrics()
        elif self.report_selector == ComparativeMeasuresReportSelector.A1: # TODO: CHANGE TO A1 and A2
            self.calculate_axis_01_metrics()
        elif self.report_selector == ComparativeMeasuresReportSelector.A2:
            self.calculate_axis_02_metrics()

    def get_depth_metrics(self):
        return self.depth_metrics

    def get_axis_01_metrics(self):
        return self.axis_01_metrics

    def get_axis_02_metrics(self):
        return self.axis_02_metrics

    def get_weight_metrics(self):
        return self.weight_metrics

    def get_comparative_df(self):
        """
        Returns comparative Pandas dataframe to make plots
        :return:
        """
        return self.comparative_df

    def print_metrics(self):

        if self.report_selector == ComparativeMeasuresReportSelector.WEIGHT:
            print('--- AXIS_01 CALIBER MEASURES ---')
            self.axis_01_metrics.print_metrics()
            print('--- AXIS_02 HEIGHT MEASURES ---')
            self.axis_02_metrics.print_metrics()
            total_lab_yield = self.weight_metrics.sum_measured_objects
            total_frame_yield = self.weight_metrics.sum_predict_objects
            print('--- WEIGHT MEASURES ---')
            self.weight_metrics.print_metrics()
            print(f'total_objects-> {self.weight_metrics.total_objects}')
            print(f'total_lab_yield-> {total_lab_yield} gr, {total_lab_yield / 1000} kg')
            print(f'total_frame_yield-> {total_frame_yield} gr, {total_frame_yield / 1000} kg')
            print(
                f'mean_lab_weight-> {self.weight_metrics.mean_measured_objects} gr, {self.weight_metrics.mean_measured_objects / 1000} kg')
        elif self.report_selector == ComparativeMeasuresReportSelector.DEPTH:
            print('--- DEPTH MEASURES ---')
            self.depth_metrics.print_metrics()
        elif self.report_selector == ComparativeMeasuresReportSelector.A1:
            print('--- AXIS_01 CALIBER MEASURES ---')
            self.axis_01_metrics.print_metrics()
        elif self.report_selector == ComparativeMeasuresReportSelector.A2:
            print('--- AXIS_02 HEIGHT MEASURES ---')
            self.axis_02_metrics.print_metrics()

    def print_depth_metrics(self):
        print('--- DEPTH MEASURES ---')
        self.depth_metrics.print_metrics('mm.')

    def print_axis_01_metrics(self):
        print('--- AXIS_01 CALIBER MEASURES ---')
        self.axis_01_metrics.print_metrics('mm.')

    def print_axis_02_metrics(self):
        print('--- AXIS_02 HEIGHT MEASURES ---')
        self.axis_02_metrics.print_metrics('mm.')

    def print_weight_metrics(self):
        print('--- MASS MEASURES ---')
        self.weight_metrics.print_metrics('gr.')

    def print_total_yield(self):
        total_lab_yield = self.weight_metrics.sum_measured_objects
        total_frame_yield = self.weight_metrics.sum_predict_objects
        print(f'total_objects-> {self.weight_metrics.total_objects}')
        print(f'total_lab_yield-> {total_lab_yield} gr, {total_lab_yield / 1000} kg')
        print(f'total_frame_yield-> {total_frame_yield} gr, {total_frame_yield / 1000} kg')
        print(
            f'mean_lab_weight-> {self.weight_metrics.mean_measured_objects} gr, {self.weight_metrics.mean_measured_objects / 1000} kg')

    def export_data_csv(self, path_output_comparative):
        self.comparative_df.to_csv(path_output_comparative, float_format='%.3f', sep=';')   # 03/10/2022 modified decimals from .2f to .3f
