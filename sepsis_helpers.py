import numpy as np
from math import ceil

class DeteriorationIndex():
    """ Helper class to caclulate deterioration index for a patient, across timesteps

    Input a patient sequence
        
    """
    def __init__(self, patient_row):
        """
        :param patient_row: The prepared row with patient features at each time step
        """
        self.patient = patient_row
        self.weights = {
            "hr": 0.053,
            "resp": 0.022,
            "o2sat": 0.057,
            "temp": 0.144,
            "map": 0.018,
            "wbc": 0.076,
            "platelets": 0.141,
            "creatinine": 0.060,
            "glucose": 0.049,
            "lactate": 0.009,
        }

    @staticmethod
    def severity_score_calc(severity_t, severity_t_1):
        score = 0
        if(severity_t == "severe"):
            score += 2
            # capture extra points if this is an escalation 
            if(severity_t_1 == "moderate" or severity_t_1 == "normal"):
                score += 1
        elif(severity_t == "moderate"):
            score += 1
            # capture extra points if this is an escalation 
            if(severity_t_1 == "severe"):
                score -= 1
        elif(severity_t == "normal"):
            score = 0
            # capture extra points if this is an escalation 
            if(severity_t_1 == "moderate" or severity_t_1 == "severe"):
                score -= 12
        return score

    @staticmethod
    def hr_status(heart_rate):
        if(heart_rate > 120 or heart_rate < 60):
            # severe
            return "severe"
        elif(heart_rate > 100 and heart_rate <=120):
            # moderate
            return "moderate"
        elif(heart_rate >= 60 and heart_rate <=100):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def resp_status(resp):
        if(resp > 25 or resp < 10):
            # severe
            return "severe"
        elif((resp in range (21, 25)) or (resp in range (10, 12))):
            # moderate
            return "moderate"
        elif(resp >= 12 and resp <=20):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def o2sat_status(o2sat):
        if(o2sat < 90):
            # severe
            return "severe"
        elif(o2sat in range (90, 94)):
            # moderate
            return "moderate"
        elif(o2sat >= 95):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def temp_status(temp):
        if(temp > 39 or temp < 35):
            # severe
            return "severe"
        elif((temp >= 35 and temp <= 35.9) or (temp >= 38 and temp <= 39)):
            # moderate
            return "moderate"
        elif((temp >= 36 and temp <= 37.9)):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def map_status(map):
        if(map > 130 or map < 60):
            # severe
            return "severe"
        elif((map in range (60, 70)) or (map in range (105, 130))):
            # moderate
            return "moderate"
        elif(map in range (70, 105)):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def platelets_status(platelets):
        if(platelets < 50):
            # severe
            return "severe"
        elif(platelets in range (50, 100)):
            # moderate
            return "moderate"
        elif(platelets > 100):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def wbc_status(wbc):
        if(wbc > 12 or wbc < 3):
            # severe
            return "severe"
        elif((wbc in range (3, 4)) or (wbc in range (10, 12))):
            # moderate
            return "moderate"
        elif(wbc in range (4, 10)):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def creatinine_status(creatinine):
        creatinine = round(creatinine, 1)
        if(creatinine > 2):
            # severe
            return "severe"
        elif(creatinine >=1.2 and creatinine <=2):
            # moderate
            return "moderate"
        elif(creatinine >=0.6 and creatinine <1.2):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def glucose_status(glucose):
        if(glucose > 200 or glucose < 60):
            # severe
            return "severe"
        elif(glucose in range (140, 200)):
            # moderate
            return "moderate"
        elif(glucose in range (60, 140)):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def lactate_status(lactate):
        # check ranges for tachycardia
        if(lactate > 4):
            # severe
            return "severe"
        elif(lactate in range (2, 4)):
            # moderate
            return "moderate"
        elif(lactate < 2):
            # normal - check if this improved from previous ts
            return "normal"
    
    def feature_score(self, feature_column, current_ts, status_function):
        """ Calculates the heart rate deterioration score for time step current_ts """
        #hr_score = self.calculate_score_for_feature('hr', current_ts, DeteriorationIndex.tachycardia_status)
        #hr_score = status_function(100)
        score = 0
        feature_t = self.patient.iloc[current_ts][feature_column]
        feature_t_1 = self.patient.iloc[current_ts - 1][feature_column]
        
        # check ranges for tachycardia
        status_t = status_function(feature_t)
        status_t_1 = status_function(feature_t_1)

        # calculate score
        score = self.severity_score_calc(status_t, status_t_1)
        return score
    
    def patient_full_deterioration_index(self):

        # create blank array
        patient_scores = np.zeros(len(self.patient))
        
        #iterate time steps
        for time_step in range(0, len(self.patient)):

            ts_score = 0
            ts_score += self.feature_score('hr', time_step, DeteriorationIndex.hr_status) * self.weights['hr']
            ts_score += self.feature_score('resp', time_step, DeteriorationIndex.resp_status) * self.weights['resp']
            ts_score += self.feature_score('o2sat', time_step, DeteriorationIndex.o2sat_status) * self.weights['o2sat']
            ts_score += self.feature_score('temp', time_step, DeteriorationIndex.temp_status) * self.weights['temp']
            ts_score += self.feature_score('map', time_step, DeteriorationIndex.map_status) * self.weights['map']
            ts_score += self.feature_score('wbc', time_step, DeteriorationIndex.wbc_status) * self.weights['wbc']
            ts_score += self.feature_score('platelets', time_step, DeteriorationIndex.platelets_status) * self.weights['platelets']
            ts_score += self.feature_score('creatinine', time_step, DeteriorationIndex.creatinine_status) * self.weights['creatinine']
            ts_score += self.feature_score('glucose', time_step, DeteriorationIndex.glucose_status) * self.weights['glucose']
            ts_score += self.feature_score('lactate', time_step, DeteriorationIndex.lactate_status) * self.weights['lactate']
            patient_scores[time_step] = ts_score
        
        
        return patient_scores