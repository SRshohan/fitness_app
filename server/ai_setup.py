import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_core.prompts import PromptTemplate
from flask import request, Flask, jsonify
import json
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate



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

def respond():
    response_schemas = [
        ResponseSchema(name="schedule", description="Generate list of times that person needs to exercise."),
        ResponseSchema(name="")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = PromptTemplate(
        template="Generate a schedule based on the user's data.\n{format_instructions}\n{user_data}",
        input_variables=["user_data"],
        partial_variables={"format_instructions": format_instructions},
    )
    llm = load_llm()
    chain = prompt | llm | output_parser
    response = chain.invoke({"user_data": "Sample user data"})
    return response

if __name__ == "__main__":
    question = 30
    print(respond())








