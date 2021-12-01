import numpy as np
import scipy
from scipy import stats


# We begin by defining a very basic random variable

sk = np.arange(1,4)
s_pk = (.332,.302,.366)
severity_rv = stats.rv_discrete(name = 'severity_rv',values = (sk,s_pk))

dk = np.arange(2)
d_pk = (0.9928,0.0072)
dropout_rv = stats.rv_discrete(name = 'dropout_rv',values=(dk,d_pk))

improvement_rv = stats.rv_discrete(name = 'imrpovement_rv', values = (dk, (0.695,0.305)))

ck = np.arange(1,4)
change_rv = stats.rv_discrete(name = 'change_rv',values = (ck,(0.75,0.20,.05)))


# functions utilised to help collect data
def num_dropout(model):
    total = 0
    return total

def num_remission(model):
    return len([1 for a in model.schedule.agents if a.remission == True])


# functions utilised to update agent parameters
def therapy_session(weeks,severity):
    drop_out = dropout_rv.rvs(size=1)[0]
    if drop_out == 1:
        return 2
    if severity == 1 and weeks == 12:
        return 1
    if severity == 2 and weeks == 14:
        return 1
    if severity == 3 and weeks == 16:
        return 1
    return 0

def employable(severity):
    if severity == 2:
        return np.random.choice(np.arange(0,2), p=[0.6,0.4])
    if severity == 3:
        return np.random.choice(np.arange(0,2),p=[0.8,0.2])
    return 1

def severity_change():
    improvement = improvement_rv.rvs(size=1)[0]
    if improvement == 0:
        return 0
    return change_rv.rvs(size=1)[0]



from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class PTSD_patient(Agent):
    def __init__(self,unique_id,model):
        super().__init__(unique_id,model) 
        self.starting_severity = severity_rv.rvs(size =1)[0]
        self.current_severity = self.starting_severity
        self.employable = bool(employable(self.current_severity))
        self.savings = np.random.choice(np.arange(10000,100000))
        self.livingexpenses = model.cost_of_living 
        self.looking_for_treatment = True
        self.weeks_in_treatment = 0
        self.current_treatment_duration = 0
        self.drop_out = False
        self.completed_treatments = 0
        self.remission = False
        self.homeless = False
        self.received_care = False

        
    def step(self):
        # if the person is not currently employable and not homeless then they will
        # pay their living expenses using their savings
        if self.employable == False and self.homeless == False:
            self.savings -= self.livingexpenses
            if self.savings < 0:
                self.homeless = True

        # if the patient has droped out or has completed 4 treatments or is in remission then he will do nothing.
        if self.drop_out == True or self.completed_treatments == 4 or self.remission == True:
            return
        # check if the person is looking for treatment
        if self.looking_for_treatment == True:
            # if they are looking for treatment check if
            # there is a therapy slot available
            if self.model.num_open_slot_therapist > 0:
                # if there is availability then the patient
                # take the slot
                # update parameters
                self.looking_for_treatment = False
                self.model.num_open_slot_therapist -= 1
                # treatment will begin the following week
            # if no slot is available then the patient will
            # check again next week
            else:
                return
        # if the patient is in therapy then the week will be spent in
        # therapy
        else:
            # If the person is not currently employable then they pay for the session using their savings
            # if they cannot afford it then they will drop out and we update parameters
            if self.savings < self.model.session_cost and self.employable == False:
                self.drop_out = True
                self.model.num_open_slot_therapist += 1
                return
            # update total number of weeks in treatment
            # and current treatment duration of the agent
            # if person is not employable then they incur treatment cost
            self.weeks_in_treatment += 1
            self.current_treatment_duration += 1
            self.received_care = self.weeks_in_treatment != 0
            if self.employable == False:
                self.savings -= self.model.session_cost

            # call therapy function to handle updating status
            a = therapy_session(self.current_treatment_duration,self.current_severity)
            
            # if a value of 2 is returned then that means the patient has dropped out
            # of treatment
            if a == 2:
                self.drop_out = True
                self.model.num_open_slot_therapist += 1
                return
            # if a value of 1 is returned then that means the person has completed one treatment course
            if a == 1:
                self.completed_treatments += 1
                # we call the severity_change function to check if and by how much the patient has improved with the given treatment
                change = severity_change()
                # if they have improved then we will update their parameters appropriately
                if change > 0:
                    # Their current severity is chnaged to reflect their improvement
                    self.current_severity = max(self.current_severity - change,0)
                    
                    # if their current severity is 0 then they are considered in remission
                    # and thus no longer need treatment and are employable
                    if self.current_severity == 0:
                        self.remission = True
                        self.model.num_open_slot_therapist +=1
                        self.employable = True
                        return
                    # We will re-evaluate if they are employable given their new severity    
                    self.employable = bool(employable(self.current_severity))
                # if they have completed the maximum number of available treatment courses then
                # they can no longer be in treatment and we update the number of therapy slots that are open 
                if self.completed_treatments == 4:
                    self.model.num_open_slot_therapist += 1
                    return
                # In all other cases we will reset their current treatment duration as they will be starting a new treatment course.    
                self.current_treatment_duration = 0

            # if a value of 0 is returned then the person has not yet completed their current treatment course    
            if a == 0:
                return
                    
                        
class PTSD_model(Model):
    
    def __init__(self,patient_N,psycho_N,session_cost,expenses):
        self.num_patients = patient_N
        self.num_open_slot_therapist = psycho_N*21
        self.schedule = RandomActivation(self)
        self.session_cost = session_cost
        self.week = 0
        self.running = True
        self.cost_of_living = expenses
        # Create agents
        for i in range(self.num_patients):
            patient = PTSD_patient(i,self)
            self.schedule.add(patient)
            
        self.datacollector = DataCollector(
            model_reporters = {"Open Therapy Slots":lambda m: m.num_open_slot_therapist,
                               "People with PTSD": lambda m: m.num_patients,
                               "Number of people who achieved remission":lambda m: len([1 for a in m.schedule.agents if a.remission == True]),
                               "People looking for treatment": lambda m: len([1 for a in m.schedule.agents if a.looking_for_treatment == True]),
                               "People who have received care": lambda m: len([1 for a in m.schedule.agents if a.received_care== True]),
                               "People in remission": lambda m: len([1 for a in m.schedule.agents if a.remission == True]),
                               "People with mild PTSD": lambda m: len([1 for a in m.schedule.agents if a.current_severity == 1]),
                               "People with moderate PTSD": lambda m: len([1 for a in m.schedule.agents if a.current_severity == 2]),
                               "People with severe PTSD": lambda m: len([1 for a in m.schedule.agents if a.current_severity == 3]),
                               "Percentage of people who achieved remission": lambda m: round(((len([1 for a in m.schedule.agents if a.remission == True])/m.num_patients)*100),2),
                               "Percentage of people who have dropped out of treatment": lambda m: round(((len([1 for a in m.schedule.agents if a.drop_out == True])/m.num_patients)*100),2),
                               "Percentage of people who lost their housing": lambda m: round(((len([1 for a in m.schedule.agents if a.homeless == True])/m.num_patients)*100),2),
                               "Percentage of people who are employable": lambda m: round(((len([1 for a in m.schedule.agents if a.employable == True])/m.num_patients)*100),2),
                               "Percentage of people who are not employable": lambda m: round(((len([1 for a in m.schedule.agents if a.employable == False])/m.num_patients)*100),2)
                               }
            )
        self.datacollector.collect(self)
    def step(self):
        """
        Advance the model by one step
        """
        
        self.schedule.step()
        self.week += 1
        self.datacollector.collect(self)
        if self.week == 104:
            self.running = False

