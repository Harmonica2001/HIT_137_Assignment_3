import tkinter as tk
from tkinter import ttk


# ------------------------
# Multiple Decorators
# ------------------------
def log_action(func):
    """Decorator to log the action being performed"""
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] Running {func.__name__} with args={args}")
        return func(self, *args, **kwargs)
    return wrapper


def ensure_input(func):
    """Decorator to ensure that input data is not empty"""
    def wrapper(self, input_data):
        if not input_data:
            return "Error: No input provided!"
        return func(self, input_data)
    return wrapper


# ------------------------
# Base class + Polymorphism
# ------------------------
class ModelHandler:
    """Base model handler"""

    def run_inference(self, input_data):
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
    def run_inference(self, input_data):
        self.log("TextModelHandler is generating text...")
        # Fake model output for now
        return f"Generated text from input: {input_data}"


class ImageModelHandler(ModelHandler, LoggerMixin):
    """Handler for image models"""

    @log_action
    @ensure_input   # multiple decorators
    def run_inference(self, input_data):
        self.log("ImageModelHandler is classifying image...")
        # Fake model output for now
        return f"Classified image '{input_data}' as: Cat"


# ------------------------
# Main Tkinter Application
# ------------------------
class AIApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Model Integration GUI")
        self.geometry("800x600")

        # Model handlers for polymorphism
        self.handlers = {
            "Text Generator (GPT-2)": TextModelHandler(),
            "Image Classifier (ViT)": ImageModelHandler()
        }

        # Create Notebook (tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Create tabs
        self.input_tab = ttk.Frame(notebook)
        self.model_tab = ttk.Frame(notebook)
        self.output_tab = ttk.Frame(notebook)
        self.explanation_tab = ttk.Frame(notebook)
        self.model_info_tab = ttk.Frame(notebook)

        # Add tabs to notebook
        notebook.add(self.input_tab, text="Input Selection")
        notebook.add(self.model_tab, text="Model Selection")
        notebook.add(self.output_tab, text="Output")
        notebook.add(self.explanation_tab, text="Explanations")
        notebook.add(self.model_info_tab, text="Model Info")

        # Build content in each tab
        self.build_input_tab()
        self.build_model_tab()
        self.build_output_tab()
        self.build_explanation_tab()
        self.build_model_info_tab()

    def build_input_tab(self):
        label = ttk.Label(self.input_tab, text="Select input type (Text or Image):")
        label.pack(pady=10)

        self.input_type = tk.StringVar()
        dropdown = ttk.Combobox(self.input_tab, textvariable=self.input_type,
                                values=["Text", "Image"], state="readonly")
        dropdown.pack(pady=10)

        self.input_entry = ttk.Entry(self.input_tab, width=50)
        self.input_entry.pack(pady=10)

    def build_model_tab(self):
        label = ttk.Label(self.model_tab, text="Select AI model:")
        label.pack(pady=10)

        self.model_choice = tk.StringVar()
        dropdown = ttk.Combobox(self.model_tab, textvariable=self.model_choice,
                                values=["Text Generator (GPT-2)", "Image Classifier (ViT)"],
                                state="readonly")
        dropdown.pack(pady=10)

        run_button = ttk.Button(self.model_tab, text="Run Inference", command=self.run_inference)
        run_button.pack(pady=20)

    def build_output_tab(self):
        label = ttk.Label(self.output_tab, text="Model Output:")
        label.pack(pady=10)

        self.output_box = tk.Text(self.output_tab, wrap="word", height=20)
        self.output_box.pack(expand=True, fill="both", padx=10, pady=10)

    def build_explanation_tab(self):
        label = ttk.Label(self.explanation_tab, text="OOP Concepts Explanation:")
        label.pack(pady=10)

        self.explain_box = tk.Text(self.explanation_tab, wrap="word", height=20)
        self.explain_box.pack(expand=True, fill="both", padx=10, pady=10)

        # Pre-fill explanations
        explanation_text = (
            "Encapsulation: Each tab UI is built inside its own method.\n"
            "Inheritance: AIApp inherits from tk.Tk.\n"
            "Method Overriding: __init__ overrides tk.Tk constructor.\n"
            "Polymorphism: ModelHandler subclasses (TextModelHandler, ImageModelHandler)\n"
            "   provide different run_inference implementations.\n"
            "Multiple Inheritance: TextModelHandler and ImageModelHandler inherit from both\n"
            "   ModelHandler and LoggerMixin.\n"
            "Multiple Decorators: log_action and ensure_input wrap run_inference methods.\n"
        )
        self.explain_box.insert(tk.END, explanation_text)

    def build_model_info_tab(self):
        label = ttk.Label(self.model_info_tab, text="Model Information:")
        label.pack(pady=10)

        self.model_info_box = tk.Text(self.model_info_tab, wrap="word", height=20)
        self.model_info_box.pack(expand=True, fill="both", padx=10, pady=10)

        info_text = (
            "Text Generator (GPT-2): A small transformer model for text generation.\n"
            "Image Classifier (ViT): Vision Transformer model for classifying images.\n"
        )
        self.model_info_box.insert(tk.END, info_text)

    def run_inference(self):
        # Get selected model + input
        model_name = self.model_choice.get()
        input_data = self.input_entry.get()

        handler = self.handlers.get(model_name)

        if handler:
            result = handler.run_inference(input_data)
        else:
            result = "Please select a model."

        # Display output
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, result)


if __name__ == "__main__":
    app = AIApp()
    app.mainloop()
