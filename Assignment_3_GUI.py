import tkinter as tk
from tkinter import ttk


class AIApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Model Integration GUI")
        self.geometry("800x600")

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
        label = ttk.Label(self.input_tab, text="Select input type (Text, Image, Audio):")
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

    def build_model_info_tab(self):
        label = ttk.Label(self.model_info_tab, text="Model Information:")
        label.pack(pady=10)

        self.model_info_box = tk.Text(self.model_info_tab, wrap="word", height=20)
        self.model_info_box.pack(expand=True, fill="both", padx=10, pady=10)

    def run_inference(self):
        # Placeholder function
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, f"Running {self.model_choice.get()} on input: {self.input_entry.get()}")


if __name__ == "__main__":
    app = AIApp()
    app.mainloop()
