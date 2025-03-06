#
import requests
import base64


# import pandas as pd

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def extract_response(response_json):
    response_json = response.json()  # Convert response object to JSON (dict)
    return response_json["choices"][0]["message"]["content"]


# def read_context(file):
#     pd.read_excel('/Users/heril.changwal/Desktop/gen_ai_hackathon/qrg.xlsx')

def call_llm(base64_image):
    global response
    # base64_image = encode_image_to_base64(
    #     "lot-rotten-tomatoes-thrown-into-pit-spoiled-product-is-tomatoes_157650-188.jpg")
    url = "https://bedrock.llm.in-west.swig.gy/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-v-n7IXIpgsSw3zwRDS1mFA"
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

                     Based on these criterions, identify the percentage of bad items. Then also create a summary insight in bullet points on what parameters you judged the item lot on. Your response should be in format: 1. Percentage 2. Your paramters for quality check 3. Provide the helpful insghts on how the lot can be used further. 4. Also estimate the life of the current state of the lot."""
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
    response = requests.post(url, headers=headers, json=data)
    response_content = extract_response(response)
    print(response_content)
    return response_content



# response = requests.post(url, headers=headers, json=data)
# print("Response Status Code:", response.status_code)
# print("Response JSON:", response.json())  # Full error details

#      "define grade of entire lot based quality of the majority of items in the lot, with the percentage of bad items, be accurate & give few insights on the quality. Write your response in short bullet points, start with one word classifcation for the quality of entire lot mentioning 'Quality', then percentage of bad item mentioning 'Percentage' only with value and then elaborate on the insights in short starting by 'Insight'.