import numpy as np
from model import PTSD_model
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import TextElement,BarChartModule, ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement

class text1(TextElement):
	def __init__(self,text):
		self.out = text
	def render(self, model):
		return str(self.out)



t1 = text1("Bar Chart of people looking for treatment and people who have received care")

bar1 = BarChartModule(fields = [{"Label":"People looking for treatment","Color":"Purple"},{"Label":"People who have received care","Color":"Green"}])

t2 =  text1("First Graph. All values are a percentage of the total number of people(agents).")
chart1 = ChartModule(series=[{"Label":"Percentage of people who achieved remission","Color":"Green"},
							{"Label":"Percentage of people who have dropped out of treatment","Color":"Black"},
							{"Label":"Percentage of people who lost their housing","Color":"Red"}])

t3 = text1("Bar chart of people's current PTSD severity")
bar2 = BarChartModule(fields = [{"Label":"People in remission","Color":"Green"},{"Label":"People with mild PTSD","Color":"Yellow"},
								{"Label":"People with moderate PTSD","Color":"Orange"},
								{"Label":"People with severe PTSD","Color":"Red"}])

chart2 = ChartModule(series = [{"Label":"Percentage of people who are employable","Color":"Green"},
								{"Label":"Percentage of people who are not employable","Color":"Red"}])

t4 = text1("Second graph. All values are a percentage of the total number of people(agents).")

model_params={
	"patient_N": UserSettableParameter("number","Number of People with PTSD",value = 10000),
	"psycho_N": UserSettableParameter("number","Number of Therapists trained to treat PTSD",value =400),
	"session_cost": UserSettableParameter("number","How much will a patient pay for a each session", value = 100),
	"expenses": UserSettableParameter("number","What is the cost of living and renting in the area",value = 750)
}


server = ModularServer(
	PTSD_model,
	[t1,bar1,t2,chart1,t3,bar2,t4,chart2], # visualized elements that are rendered
	"PTSD Treatment Model", # name
	model_params, # inputed parameters
)


