import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_core.prompts import PromptTemplate
from flask import request, Flask, jsonify
import json



# Load the .env.dev file
load_dotenv('server/.env.dev')

# Access the environment variable
key = os.getenv('GOOGLE_API_KEY')

def load_llm():
    llm = GoogleGenerativeAI(
        model="gemini-pro", google_api_key=key,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
    return llm


# Example prompt
def template(question):
    data = {}

    prompt = f"Create a daily fitness routine for someone who wants to lose 5 kg in {question} days."

    prompt = PromptTemplate.from_template(prompt)

    try:
        chain = prompt | load_llm()
        chain = chain.invoke({"question":question})
        data['response'] = chain
        json_response = json.dumps(data, indent=4)
    except Exception as e:
        data['response'] = e

    return json_response
if __name__ == "__main__":
    question = 30
    print(template(question))








