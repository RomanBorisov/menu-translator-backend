from django.shortcuts import render
import os
import base64
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from openai import OpenAI

class ProcessImageView(APIView):
    """
    API endpoint that accepts an image and sends it to OpenAI for processing.
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        api_key = settings.OPENAI_API_KEY

        if not api_key:
            raise ValueError("OpenAI API key is not set. Please check your environment variables.")

        self.client = OpenAI(api_key=api_key)
        
        self.prompt_template = """Analyze this restaurant menu image and return a JSON with the following structure:
        {  
        "categories": [  
            {  
            "name": "string",  
            "items": [  
                {  
                "name": "string",  
                "price": "string",  
                "description": "string",  
                "ingredients": ["string"],  
                "allergens": ["string"],  
                "history": "string"  
                }  
            ]  
            }  
        ]  
        }  
    
        Follow the rules:  
        - Don't be lazy and return all menu items in JSON  
        - If menu has sections on the photo – they should become categories in JSON. Otherwise use one category named "Menu".  
        - Name and price must be taken from the menu. If there are no prices, put N/A in the field.  
        - For description, ingredients and allergens you must act like a chef and describe me the dish yourself.  
        - For history, provide 3–5 interesting sentences about the dish's origin, cultural significance, and historical facts.  
        - (!) ONLY JSON IS ALLOWED as an answer. No explanation, semicolons, other text and any other symbols are allowed!"""
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests to process images."""

        if 'image' not in request.FILES:
            return Response(
                {"error": "No image file provided. Please upload an image."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            image_file = request.FILES['image']
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            response = self.client.chat.completions.create,
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert chef and food historian who analyzes restaurant menus and returns well-structured JSON data only."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.prompt_template},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            
            ai_response = {
                "result": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
            return Response(ai_response, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Error processing image: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
