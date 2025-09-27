'''
This file performs all the backend operations in relation to the project
'''

import os
from huggingface_hub import InferenceClient
from PIL import Image,ImageTk

def log_action(func):
    """Decorator to log the action being performed"""
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] Running {func.__name__} with args={args}")
        return func(self, *args, **kwargs)
    return wrapper


def ensure_input(func):
    """Decorator to ensure that input data is not empty"""
    def wrapper(self,model_details,input_data):
        if not input_data:
            return "Error: No input provided!"
        return func(self,model_details,input_data)
    return wrapper

class ModelHandler:
    """Base model handler"""
    def __init__(self):
        # Encapsulation is used here to make sure that the api keys are not
        # accessed/modified outside this class.
        # --------------  YOUR API KEYS  --------------
        self._hf_api_key   = "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"
        self._nebius_api_key = (
            "eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ."
            "eyJzdWIiOiJnaXRodWJ8MjI5MDkzMzM5Iiwic2NvcGUiOiJvcGVuaWQgb2ZmbGluZV9hY2Nlc3MiLCJpc3MiOiJhcGlfa2V5X2lzc3VlciIsImF1ZCI6WyJodHRwczovL25lYml1cy1pbmZlcmVuY2UuZXUuYXV0aDAuY29tL2FwaS92Mi8iXSwiZXhwIjoxOTE2NjMwMzkwLCJ1dWlkIjoiMDE5OTg5OWMtZmE3Ny03NmFjLTg3NWQtZmZkOTcwM2JlZmU2IiwibmFtZSI6IkFJIEluZmVyZW5jZSIsImV4cGlyZXNfYXQiOiIyMDMwLTA5LTI2VDA1OjE5OjUwKzAwMDAifQ."
            "w3fFOwTOO_oc02IECxf1qD5b_Dj8LiBS0cZwSGEc0IU"
        )
        # ----------------------------------------------
    def run_inference(self,model_details,input_data):
        raise NotImplementedError("Subclasses must override this method")

class LoggerMixin:
    """Provides logging functionality"""

    def log(self, msg):
        print(f"[LoggerMixin] {msg}")


# Polymorphism: this is used here to define the same method 'run_interfence '
# in different classes with different implementations
# Multiple Inheritance: both the TextModelHandler and ImageModelHandler
# classes inherit from the ModelHandler class and LoggerMixin class.
class TextModelHandler(ModelHandler, LoggerMixin):
    """Handler for text models"""
    
    @log_action
    @ensure_input   # multiple decorators
    def run_inference(self,model_details,input_data):
        '''
        The model will return a summary of the text,
        focusing on important keywords and points of the text
        '''
        self.log("TextModelHandler is generating text...")
        # Model inference
        self.text_client = InferenceClient(
            provider=model_details["provider"],
            api_key=self._hf_api_key,     # <--- Hugging Face key used here
        )
        self.text_result = self.text_client.summarization(
            input_data,
            model=model_details["model"]
        )
        return self.text_result["summary_text"]


class ImageModelHandler(ModelHandler, LoggerMixin):
    '''
        The model will return an image of the user's input
    '''
    @log_action
    @ensure_input   # multiple decorators
    def run_inference(self,model_details,input_data):
        self.log("ImageModelHandler is classifying image...")
        # Model inferencing
        self.client = InferenceClient(
            provider=model_details["provider"],
            api_key=self._nebius_api_key,  # <--- Nebius key used here
        )
        self.image = self.client.text_to_image(
            input_data,
            model=model_details["model"]
        )
        return self.image


class modelrunner:
     '''
     Returns the result from the selected model type, either Text or Image
     ''' 
     def __init__(self,model_parameters,model_name,input_data):
         self.input_data=input_data
         print(self.input_data)
         self.model_name=model_name
         print(self.model_name)
         self.model_details=model_parameters
         self.handlers = {
            "Text Summarization": TextModelHandler(),
            "Text-to-Image": ImageModelHandler()
         }
        
     def run_model_result(self):
         self.handler = self.handlers.get(self.model_name)
         if self.handler:
            self.result = self.handler.run_inference(
                self.model_details,self.input_data
            )
            return self.result
         else:
            self.result = "Please select a model."        


class model_inference:
    '''
        Returns the model parameters and the model name
    '''
    def __init__(self,model_choice):
         self.model_choice=model_choice
              
    def run_inferences(self):
        self.model_name = self.model_choice.get()
        if self.model_name=="Text-to-Image":
            self.image_model_details={"provider":"nebius",
                                      "model":"black-forest-labs/FLUX.1-dev"}
            return (self.image_model_details,self.model_name)
        else:
            self.text_model_details={"provider":"hf-inference",
                                     "model":"google/pegasus-large"}  
            return (self.text_model_details,self.model_name)
