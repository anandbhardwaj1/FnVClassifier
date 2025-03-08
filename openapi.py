#
import requests
import base64
import re

from flask import jsonify
from config import LLM_API_URL, LLM_API_KEY 


def extract_response(response):
    try:
        response_json = response.json()  # Convert response object to JSON (dict)
        return response_json["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        print(f"Error extracting content from response: {str(e)}")
        print(f"Response structure: {response.json()}")
        raise Exception(f"Invalid response structure: {str(e)}")
    except Exception as e:
        print(f"Unexpected error extracting response: {str(e)}")
        raise


def parse_text_to_dict(text):
    headings = ["Item", "Percentage", "Judgement", "Insights", "ShelfLife"]
    parsed_data = {}

    for heading in headings:
        match = re.search(rf"{heading}:\s*(.*?)(?=\n[A-Z]|$)", text, re.DOTALL)
        if match:
            items = [line.strip('- ').strip() for line in match.group(1).strip().split("\n") if line.strip()]
            parsed_data[heading] = items if len(items) > 1 else items[0]  # Store list if multiple items exist

    return parsed_data


def call_llm(base64_image):
    try:
        global response
        url = LLM_API_URL
        headers = {
            "Content-Type": "application/json",
            "Authorization": LLM_API_KEY
        }
        data = {
            "model": "bedrock-claude-3-5-sonnet",
            "messages": [
                {
                    "role": "user",
                    # "content": "what llm are you"
                    "content": [
                        {"type": "text", "text": """You are a warehouse Fruits, Vegetables & Flowers quality checker. We provide you with a snapshot of entire lot of items. Firstly identify the vegetable/fruit. Consider these criterions for the acceptance or rejection of fruit/ vegetable identified:
                            1. Cauliflower: accept if Firm & milky white with tight bounded curd. Reject if - Loose curd, infested, under/over weight, rottened, visibility of foreign matter, Worm infestation, Major yellow, purple curd.
                             2. Banana: reject if Black and damaged, fungal infested, bruise marks on skin, sunburn and chilling injury (low temperature), cuts, natural cracks, ruptured skin, Soft fruit not allowed.
                             3. Orange: reject if Brown spots, sunburn, cut/crack, shriveling and superficial healed  on skin, blemishes and discoloration, freezing damage, chilling injury, and insect damage, over ripen having loose jacket.
                             4. Grapes: accept if Fresh and green stalk,sweet in taste, Crispy in texture. Reject if - Brown berry, ripe , fungal & rotten , dry stalk , loose berry.  Estimate the percentage of bad items, be accurate & give few insights on the quality. Write your response in short bullet points, start with one word classifcation for the quality of entire lot mentioning 'Quality', then percentage of bad item mentioning 'Percentage' only with value
                             5. Tomato: accept if Turning Color (Not fully red), Clean, Fresh, Semi ripe, Uniform sizes. Reject if - Borer holes, Over ripe, Ruptured skin, Shriveled, Viral spots (Jaundice), Pinkish fruits, Blossom end rot, Blight issue.

                             Based on these criterions, identify the percentage of bad items (please be more aggresive with rejection criterions). Based on the parameters provided for the mentioned items, write a judgement for each parameter. Your response should be strcitly in format: 1. Item Detected (mention 'Item: ') 2. Bad quality percentage (mention 'Percentage: ') 3. Your judgement for the paramters for quality check (mention 'Judgement: ') 4. Provide the helpful insghts on how the lot can be used further (mention 'Insights: '). 4. Also estimate the life of the current state of the lot. Just menton the estimated shelf life number (mention 'ShelfLife: ')"""
                         },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"  # Adjust to "high" for detailed analysis
                            }
                        }
                    ]
                }
            ]
        }
        
        # API request with timeout
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        # Check if response is successful
        if response.status_code != 200:
            print(f"API Error: Status code {response.status_code}")
            print(f"Error details: {response.text}")
            return {"error": f"API Error {response.status_code}: Failed to process image"}
            
        # Extract and parse the response
        try:
            response_content = extract_response(response)
            print("response", response_content)
            parsed_dict = parse_text_to_dict(response_content)
            
            # Check if parsing was successful
            if not parsed_dict or len(parsed_dict) == 0:
                return {"error": "Failed to parse LLM response", "raw_response": response_content}
                
            return parsed_dict
            
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            print(f"Raw response: {response.text}")
            return {"error": f"Failed to process LLM response: {str(e)}"}
            
    except requests.exceptions.Timeout:
        print("Request timed out")
        return {"error": "Request to LLM API timed out"}
        
    except requests.exceptions.ConnectionError:
        print("Connection error")
        return {"error": "Connection error. Please check your internet connection."}
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": f"An unexpected error occurred: {str(e)}"}