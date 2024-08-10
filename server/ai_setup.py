import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import getpass


# Load the .env.dev file
load_dotenv('server/.env.dev')

# Access the environment variable
key = os.getenv('GOOGLE_API_KEY')
hf_api_token=os.getenv('HUGGINGFACEHUB_API_TOKEN')


# If the Hugging Face token is not set, prompt the user to input it
if not hf_api_token:
    hf_api_token = getpass.getpass("Enter your Hugging Face token: ")
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_api_token


def load_llm():
    llm = GoogleGenerativeAI(
        model="gemini-pro", google_api_key=key,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
    return llm

def load_llm_from_hf():
    # Initialize the LLM using the Hugging Face Endpoint
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-Nemo-Instruct-2407",
        task="text-generation",
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
        api_key=hf_api_token  # Pass the API token here
    )

    chat_model = ChatHuggingFace(llm=llm)
    
    return chat_model



def respond(survey):
    response_schemas = [
        ResponseSchema(
            name="Goal",
            description=f"The gym goal is '{survey['What is the gym goal']}'. Generate a schedule that aligns with this goal while considering the user's class schedule."
        ),
        ResponseSchema(
            name="FreeTime",
            description=f"The user has '{survey['How much free time you have']}' each week. Consider this when generating the exercise schedule."
        ),
        ResponseSchema(
            name="ClassSchedule",
            description=f"The user's weekly class schedule is '{survey['What is your weekly schedule looks like']}'. Ensure the exercise schedule does not conflict with this."
        ),
       
    ]
    
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    
    prompt = PromptTemplate(
        template="Generate a workout schedule for the next 7 days considering the user's goals, free time, class schedule, weight, and height.\n{format_instructions}\n{user_data}",
        input_variables=["user_data"],
        partial_variables={"format_instructions": format_instructions},
    )
    
    llm = load_llm()
    chain = prompt | llm | output_parser

    # Prepare user data to be passed into the chain
    user_data = {
        "gym_goal": survey['What is the gym goal'],
        "free_time": survey['How much free time you have'],
        "class_schedule": survey['What is your weekly schedule looks like'],
        
    }

    try:
        response = chain.invoke({"user_data": user_data})
    except Exception as e:
        print(f"Error: {str(e)}")
        # Handle missing keys or unexpected format here
        response = {"error": "The LLM response was incomplete. Please check the input data and try again."}
    
    return response



if __name__ == "__main__":
    question = 30
    survey = {
    "What is the gym goal": "Lose weight",
    "How much free time you have": "10 hours per week",
    "What is your weekly schedule looks like": {
        "Monday": "9:00 AM - 10:30 AM (Math), 2:00 PM - 3:30 PM (History)",
        "Tuesday": "10:00 AM - 11:30 AM (Physics), 1:00 PM - 2:30 PM (Chemistry)",
        "Wednesday": "9:00 AM - 10:30 AM (Math), 2:00 PM - 3:30 PM (History)",
        "Thursday": "10:00 AM - 11:30 AM (Physics), 1:00 PM - 2:30 PM (Chemistry)",
        "Friday": "9:00 AM - 10:30 AM (English), 2:00 PM - 3:30 PM (Biology)",
    },
    "What is your current weight?": "70 kg",
    "What is your height?": "170 cm",
    "What is your preferred workout environment?": "Gym",
    "Are there any specific exercises or activities you enjoy?": "Running, Swimming, Yoga",
    "Do you have any injuries or physical limitations?": "Knee pain when running, lower back issues",
    "What is your current fitness level?": "Intermediate",
    "What is your desired intensity level for workouts?": "Medium"
}

    
    print(respond(survey))








