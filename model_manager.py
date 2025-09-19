

class ModelManager:
    def __init__(self):
        self.loaded_model = None    
    def load_model(self, model_choice):
        """Load model info based on selection."""
        if model_choice == "Text-to-Image":
            self.loaded_model = model_choice
            return "Model: black-forest-labs/FLUX.1-dev (Text-to-Image)\nCategory: Image generation\nFree on Hugging Face."
        elif model_choice == "Text Generation":
            self.loaded_model = model_choice
            return "Model: pegasus-Large (Text Summarization)\nCategory: NLP\nFree on Hugging Face."
        else:
            return "Please select a in order to run it model."

    def run_model(self, input_data):
        """Run selected model on user input."""
        if not self.loaded_model:
            return "Please load a model first."
        if self.loaded_model == "Text-to-Image":
            return f"Generated image from: {input_data}"
        elif self.loaded_model == "Text Summarization":
            return f"Generated text continuation for: {input_data}"
