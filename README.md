
# Description #

This is a simple agent based model of the treatment of PTSD.

# Running the model #
To run the model:
1) run the command `mesa runserver` in the directory of the model.
2) Open https://127.0.0.1:8521/ in your browser
3) Set your desired parameters and hit the Reset button then Run.


# Assumptions made for the model #

These are the assumptions of our model:


First, and probably most importantly, we will not consider the risk for revictimization and retraumatization. Additionally, PTSD can be totally debilitating but we will assume that every person in our model has the capacity to adhere to treatment if they choose to. We will not consider comorbidities or anything that may interrupt the person's treatment such as inability to pay or incarceration. This does not mean that we will not consider patients ceasing treatment of their own volition.

	Suicide: We will not factor in the risk of suicide as there doesn't seem to be any reliable data.

	Assumptions of severity:

							We will be using the data from above that states
							36.6% are classified as serious, 30.2% are classified as mild and 33.2% are moderate. 

	Assumption of providers: 
							Our model will assume that each provider can see patients 4 days a week for 8 hours per day. There will two distinct types of providers.

							Therapist: We will assume that each session with a therapist spans one hour and a half. Therefore, each therapist can see 21 patients every week. We will also assume that each therapist has qualification in trauma therapy of each kind. There will be no variation among therapists and as such we will only be tracking the number of slots available. After speaking with a longtime professional, I was informed that at maxiumum, a therapist would see have about 30 patients that they see at varying frequency. From our conversation, I have decided that to stick with 21 patients per week.s 


							Psychiatrist: We will assume that each session with a psychiatrist spans one hour. Therefore, each psychiatrist can see 32 patients every every weel. Again we will not differientiate among psychiatrist and as such we will only keep track of the number of slots available.

	Assumption of qualified Therapists: 
										Our model will assume that each therapist can see patients 4 days a week for 8 hours per day. Each session will span one and a half hours and each person will need weekly sessions. Therefore, each therapist can see 21 patients every week and has 21 slots available. We will also assume that each therapist has qualification in trauma therapy of each kind. There will be no variation among therapists. Therefore, we will intialize an empty array with 21*N slots such that N is the number of therapists in our model. 


	Assumption of treatment: 	
								We will not consider the possibility of worsening symptoms, instead we will lump in the probability of worsening symptoms with the probability of no changes.
								If a person improves then we will assume that 75% drop one severity scale, 20% drop two severity scales and 5% drop three severity scales.

	Assumption of dropping out:
								The likelihood of dropping out each week will be estimated at 1.915%. If a person drops out then we will assume they no longer will seek treatment.


	Assumptions of employability:
		We will not track employment but rather if the person is able to maintain employment or not

		1) For those who have mild PTSD, we will assume that they all can hold a job.
		2) For those with moderate PTSD, we will assume that 60% of them cannot hold a job and 40% can hold a job.
		3) For those with severe PTSD, we will assume that 80% are not employable/cannot hold a job
			==> Given a sample of 100 people, this would mean that we expect 49 of them to be unable to hold a job, which is lower than the statistic above that says 2/3 of people with PTSD are unemployed. Of course these two things do not equate as we are not talking about actual employment in our model.