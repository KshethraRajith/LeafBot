
import base64
from openai import OpenAI

class PlantAI:
    @staticmethod
    def convert_image_to_base64(image_path): 
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        return base64_image

    def get_image_details(image_path):
            
        print(f"Image path: {image_path}")
        # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
        # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
        client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key="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",
        )

        print(f"Image to base64")
        base64_image = PlantAI.convert_image_to_base64(image_path)

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "get details of the plant"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/png;base64," + base64_image
                            }
                        }
                    ]
                }
            ],
            model="gpt-4o-mini",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
        return response.choices[0].message.content
