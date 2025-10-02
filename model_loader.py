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


# ------------------------
# Base class + Polymorphism
# ------------------------
class ModelHandler:
    """Base model handler"""
    def __init__(self):
    #api key variable using protect encapsulation
        self._api_key_value="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"
    def run_inference(self,model_details,input_data):
        raise NotImplementedError("Subclasses must override this method")


# ------------------------
# Multiple Inheritance
# ------------------------
class LoggerMixin:
    """Provides logging functionality"""

    def log(self, msg):
        print(f"[LoggerMixin] {msg}")


# ------------------------
# Polymorphic subclasses
# ------------------------
class TextModelHandler(ModelHandler, LoggerMixin):
    """Handler for text models"""
    
    @log_action
    @ensure_input   # multiple decorators
    
    def run_inference(self,model_details,input_data):
        '''
        Parameters:
        The function receives the model parameters from model inference class which are required to run inference
        Then the next parameter is input_data which is the input received from the input_entry text widget
        
        Results:
        The model will return a summary of the text, focusing on important keywords and points of the text

        '''
        self.log("TextModelHandler is generating text...")
        # Model inference
        self.text_client = InferenceClient(
            provider=model_details["provider"],
            api_key=ModelHandler()._api_key_value,
        )
        
        self.text_result = self.text_client.summarization(input_data, model=model_details["model"])
        return self.text_result["summary_text"]


class ImageModelHandler(ModelHandler, LoggerMixin):
    '''
        Parameters:
        The function receives the model parameters from model inference class which are required to run inference
        Then the next parameter is input_data which is the input received from the input_entry text widget
        
        Results:
        The model will return an image of the user's input
    '''
    
    @log_action
    @ensure_input   # multiple decorators
    def run_inference(self,model_details,input_data):
      
        self.log("ImageModelHandler is classifying image...")
        # Model inferencing
        self.client = InferenceClient(
        provider=model_details["provider"],
        api_key=ModelHandler()._api_key_value)
    
   
        self.image = self.client.text_to_image(input_data,model=model_details["model"])
        return self.image
class modelrunner:
     '''
     Parameters:
     The function receives the model parameters from model inference class which are required to run inference
     Then the next parameter is input_data which is the input received from the input_entry text widget
    
     Results:
     Returns the result from the selected model type, either Text or Image
     ''' 
     def __init__(self,model_parameters,model_name,input_data):
         
         self.input_data=input_data
         print(self.input_data)
         self.model_name=model_name
         print(self.model_name)
         #go through this
         self.model_details=model_parameters
         self.handlers = {
            "Text Summarization": TextModelHandler(),
            "Text-to-Image": ImageModelHandler()
         }
        
     
     def run_model_result(self):
         self.handler = self.handlers.get(self.model_name)
         if self.handler:
            self.result = self.handler.run_inference(self.model_details,self.input_data)
            
            return self.result
         else:
            self.result = "Please select a model."        
     
class model_inference:
    '''
        Parameters:
        model name used to select the appropriate parameters for the selected model from the user
        Results:
        Returns the model parameters and the model name
    '''
    def __init__(self,model_choice):
         self.model_choice=model_choice
              
    def run_inferences(self):
                # Get selected model + input
                self.model_name =self.model_choice.get()
                # Display output
                if self.model_name=="Text-to-Image":
                    #load model parameters
                    self.image_model_details={"provider":"nebius","model":"black-forest-labs/FLUX.1-dev"}
                    return (self.image_model_details,self.model_name)
                else:
                    self.text_model_details={"provider":"hf-inference","model":"google/pegasus-large"}  
                    return (self.text_model_details,self.model_name)

                    

