import numpy as np

class DeteriorationIndex():
    """ Helper class to caclulate deterioration index for a patient, at a timestep

    Input a patient sequence
        
    """
    def __init__(self, patient_row):
        """
        :param patient_row: The prepared row with patient features at each time step
        """
        self.patient = patient_row

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
                score -= 1

    @staticmethod
    def tachycardia_status(heart_rate):
        # check ranges for tachycardia
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
    def tachypnea_bradypnea_status(resp):
        # check ranges for tachycardia
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
        # check ranges for tachycardia
        if(o2sat < 90):
            # severe
            return "severe"
        elif(resp in range (90, 94)):
            # moderate
            return "moderate"
        elif(resp >= 95):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def temp_status(temp):
        # check ranges for tachycardia
        if(temp > 39 or temp < 35):
            # severe
            return "severe"
        elif((temp in range (35, 35.9)) or (temp in range (38, 39))):
            # moderate
            return "moderate"
        elif(temp in range (36, 37.9)):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def map_status(map):
        # check ranges for tachycardia
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
        # check ranges for tachycardia
        if(platelets < 50000):
            # severe
            return "severe"
        elif(platelets in range (50000, 100000)):
            # moderate
            return "moderate"
        elif(platelets > 100000):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def wbc_status(wbc):
        # check ranges for tachycardia
        if(wbc > 12000 or wbc < 3000):
            # severe
            return "severe"
        elif((wbc in range (3000, 4000)) or (wbc in range (10000, 12000))):
            # moderate
            return "moderate"
        elif(wbc in range (4000, 10000)):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def creatinine_status(creatinine):
        # check ranges for tachycardia
        if(creatinine > 2):
            # severe
            return "severe"
        elif(creatinine in range (1.2, 2)):
            # moderate
            return "moderate"
        elif(creatinine in range (0.6, 1.2)):
            # normal - check if this improved from previous ts
            return "normal"
    @staticmethod
    def glucose_status(glucose):
        # check ranges for tachycardia
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

    def hr_score(self, current_ts):
        """ Calculates the heart rate deterioration score for time step current_ts """
        hr_score = 0
        hr_t = self.patient.iloc[current_ts]['hr']
        hr_t_1 = self.patient.iloc[current_ts - 1]['hr']
        
        # check ranges for tachycardia
        tachycardia_status_t = self.tachycardia_status(hr_t)
        tachycardia_status_t_1 = self.tachycardia_status(hr_t_1)

        # calculate score
        hr_score = self.severity_score_calc(tachycardia_status_t, tachycardia_status_t_1)
        
        return hr_score

    def resp_score(self, current_ts):
        """ Calculates the respiratory deterioration score for time step current_ts """
        resp_score = 0
        resp_t = self.patient.iloc[current_ts]['resp']
        resp_t_1 = self.patient.iloc[current_ts - 1]['resp']
        
        # check ranges for tachycardia
        tachypnea_bradypnea_status_t = self.tachypnea_bradypnea_status(resp_t)
        tachypnea_bradypnea_status_t_1 = self.tachypnea_bradypnea_status(resp_t_1)

        # calculate score
        resp_score = self.severity_score_calc(tachypnea_bradypnea_status_t, tachypnea_bradypnea_status_t_1)
        
        return resp_score