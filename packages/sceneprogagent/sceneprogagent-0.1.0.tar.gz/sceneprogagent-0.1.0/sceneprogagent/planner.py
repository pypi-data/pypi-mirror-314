from sceneprogllm import LLM

class Planner:
    def __init__(self, name, planning_examples=None, tool_description=None):
        self.name = name

        if not planning_examples:
            planning_examples = """
Input: Cook pasta
Output:
    {{
    '1': 'Invoke the BoilWater tool to boil water',
    '2': 'Invoke the AddPasta tool to add pasta to boiling water',
    '3': 'Invoke the Timer tool to set a timer for 8-12 minutes',
    '4': 'Invoke the DrainPasta tool to drain the pasta once cooked',
    'start': 1,
    }}

Input: Book a flight ticket from New York to Los Angeles for December 25th
Output:
    {{
    '1': 'Invoke the SearchFlights tool to search for flights from New York to Los Angeles on December 25th',
    '2': 'Invoke the ComparePrices tool to compare flight prices',
    '3': 'Invoke the BookFlight tool to book the selected flight',
    'start': 1,
    }}

Input: Write a blog post about sustainable living
Output:
    {{
    '1': 'Invoke the ResearchTopic tool to gather information about sustainable living',
    '2': 'Invoke the GenerateOutline tool to create an outline for the blog post',
    '3': 'Invoke the WriteDraft tool to write a draft of the blog post',
    '4': 'Invoke the Proofread tool to proofread and edit the blog post',
    'start': 1,
    }}

Input: Organize a meeting with the team next Monday at 10 AM
Output:
    {{
    '1': 'Invoke the CheckAvailability tool to check the team’s availability for next Monday at 10 AM',
    '2': 'Invoke the BookMeetingRoom tool to reserve a meeting room',
    '3': 'Invoke the SendInvites tool to send calendar invitations to the team',
    'start': 1,
    }}

Input: Plan a weekend trip to the mountains
Output:
    {{
    '1': 'Invoke the SearchDestinations tool to find mountain destinations',
    '2': 'Invoke the CheckWeather tool to check the weekend weather forecast',
    '3': 'Invoke the BookAccommodation tool to book a cabin or hotel',
    '4': 'Invoke the CreatePackingList tool to generate a packing list for the trip',
    'start': 1,
    }}

Input: Create a presentation about artificial intelligence
Output:
    {{
    '1': 'Invoke the ResearchTopic tool to gather information about artificial intelligence',
    '2': 'Invoke the CreateSlideOutline tool to draft the structure of the presentation',
    '3': 'Invoke the DesignSlides tool to design slides for the presentation',
    '4': 'Invoke the ReviewPresentation tool to review and refine the slides',
    'start': 1,
    }}

Input: Make a smoothie
Output:
    {{
    '1': 'Invoke the GatherIngredients tool to list required ingredients (e.g., fruits, milk, yogurt)',
    '2': 'Invoke the BlendIngredients tool to blend the ingredients',
    '3': 'Invoke the Serve tool to pour the smoothie into a glass',
    'start': 1,
    }}

Input: Schedule a doctor’s appointment
Output:
    {{
    '1': 'Invoke the FindDoctors tool to search for available doctors',
    '2': 'Invoke the CheckAvailability tool to check appointment slots',
    '3': 'Invoke the BookAppointment tool to confirm the appointment',
    'start': 1,
    }}
"""

        self.description = f"""
Given the user query, your task is to generate a plan, primarily in plane english, whose successful execution will lead to the resolution of the query. 
You must generate the plan as a list of steps (a python dictionary with numbers '1', '2', '3' being keys and steps being respective values). At each step, you may use a maximum of one tool from the tools available to you.
Each step should be a simple instruction that can be executed, a call to action. In addition to the steps, you must also include a key 'start' which indicates the starting step of the plan. Example, if we want to start the plan from step 2, the 'start' key should have the value 2.
The tools available to you are:
{tool_description}
Here are a few examples of how your response should look like:
{planning_examples}
"""
        self.llm = LLM(name=name, system_desc=self.description, response_format="json")

    def run(self, query):
        response = self.llm.run(query)
        plan = []
        for key, value in response.items():
            if key == "start":
                plan_idx = int(value)
                continue
            plan.append(value)
        return plan, plan_idx
    
    def __call__(self, query):
        plan, plan_idx = self.run(query)
        prompt = f"""
The plan you generated for the query: {query} is as follows:
{plan}
with the starting step being: {plan_idx}
Check if the plan is correct, complete and only uses the tools available to you. If you need to make any changes, do so now. If you cannot generate a plan, simply return a single item 'CANNOT PLAN'.
"""
        plan, plan_idx = self.run(prompt)
        return plan, plan_idx
    
    def refine_plan(self, query, plan, plan_idx, result):
        prompt = f"""
For the query: {query}, you had generated the following plan:
{plan}
However, while executing step {plan[plan_idx-1]}, we encountered an error: {result}.
Modify the plan accordingly to address the error. Also, update the starting step of the plan so that the steps before the error are not repeated.
"""
        plan, plan_idx = self(prompt)
        return plan, plan_idx