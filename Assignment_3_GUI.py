import tkinter as tk
from tkinter import ttk, filedialog
from model_manager import ModelManager
from Logger import Logger

def validate_input(func): #Decorator to validate user input selection.

    def wrapper(self, input_data):
        if not isinstance(input_data, str) or not input_data.strip():
            return "Invalid input: Please provide a non-empty string."
        return func(self, input_data)
    return wrapper

class AIApp(tk.Tk,Logger,ModelManager):
    def __init__(self):
        super().__init__()
        self.title("Tkinter AI GUI")
        self.geometry("900x700")

        # Manager for model operations
        self.model_manager = ModelManager()

        # Menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        models_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Models", menu=models_menu)
        models_menu.add_command(label="Load Model")

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")

        # ---------------- Model Selection ----------------
        model_frame = ttk.LabelFrame(self, text="Model Selection")
        model_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(model_frame, text="Select Model:").pack(side="left", padx=5, pady=5)
        self.model_choice = tk.StringVar()
        self.model_dropdown = ttk.Combobox(
            model_frame,
            textvariable=self.model_choice,
            values=["Text-to-Image", "Text Summarization"],
            state="readonly",
            width=30,
        )
        self.model_dropdown.pack(side="left", padx=5, pady=5)

        ttk.Button(model_frame, text="Load Model", command=self.load_model).pack(side="left", padx=5, pady=5)

        # ---------------- Input Section ----------------
        input_frame = ttk.LabelFrame(self, text="User Input Section")
        input_frame.pack(fill="x", padx=10, pady=5)

        self.input_type = tk.StringVar(value="Text")
        ttk.Radiobutton(input_frame, text="Text", variable=self.input_type, value="Text", command=self.toggle_input).pack(side="left", padx=5)
        ttk.Radiobutton(input_frame, text="Image", variable=self.input_type, value="Image", command=self.toggle_input).pack(side="left", padx=5)

        # Browse button (hidden until Image selected)
        self.browse_btn = ttk.Button(input_frame, text="Browse", command=self.browse_file)
        self.browse_btn.pack(side="left", padx=5)
        self.browse_btn.pack_forget()

        self.input_entry = tk.Text(input_frame, height=5, width=60)
        self.input_entry.pack(padx=10, pady=10, fill="x")

        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Run Model", command=self.run_model).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_input).pack(side="left", padx=5)

        # ---------------- Output Section ----------------
        output_frame = ttk.LabelFrame(self, text="Model Output Section")
        output_frame.pack(fill="both", padx=10, pady=5, expand=True)

        ttk.Label(output_frame, text="Output Display:").pack(anchor="w", padx=5, pady=5)
        self.output_box = tk.Text(output_frame, wrap="word", height=10)
        self.output_box.pack(fill="both", expand=True, padx=10, pady=5)

        # ---------------- Model Info & Explanations ----------------
        info_explain_frame = ttk.LabelFrame(self, text="Model Information & Explanation")
        info_explain_frame.pack(fill="both", padx=10, pady=5, expand=True)

        model_info_frame = ttk.Frame(info_explain_frame)
        model_info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ttk.Label(model_info_frame, text="Selected Model Info:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.model_info_box = tk.Text(model_info_frame, wrap="word", height=10)
        self.model_info_box.pack(fill="both", expand=True, padx=5, pady=5)

        explain_frame = ttk.Frame(info_explain_frame)
        explain_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ttk.Label(explain_frame, text="OOP Concepts Explanation:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.explain_box = tk.Text(explain_frame, wrap="word", height=10)
        self.explain_box.pack(fill="both", expand=True, padx=5, pady=5)

        # ---------------- Notes Section ----------------
        notes_frame = ttk.LabelFrame(self, text="Notes")
        notes_frame.pack(fill="x", padx=10, pady=5)

        self.notes_box = tk.Text(notes_frame, wrap="word", height=3)
        self.notes_box.pack(fill="x", padx=5, pady=5)

    # ---------------- Methods ----------------
    def toggle_input(self):
        if self.input_type.get() == "Image":
            self.browse_btn.pack(side="left", padx=5)
        else:
            self.browse_btn.pack_forget()

    def load_model(self):
        """Load the selected model and display model info."""
        selected = self.model_choice.get()
        if not selected:
            self.model_info_box.delete("1.0", tk.END)
            self.model_info_box.insert(tk.END, "Please select a model from the dropdown menu")
            return

        self.loaded_model = selected
        self.model_info_box.delete("1.0", tk.END)

        if selected == "Text-to-Image":
            self.model_info_box.insert(
                tk.END,
                "Model: black-forest-labs/FLUX.1-dev (Text-to-Image)\n"
                "Category: Image Generation\n"
                "Free on Hugging Face.\n"
                "Description: This model generates images based off text prompts.\n"
            )

        elif selected == "Text Summarization":
            # Display BOTH models’ info side by side
            self.model_info_box.insert(
                tk.END,
                "Model 2: pegasus-Large (Text Summarization)\n"
                "Category: Text Summarization\n"
                "Free on Hugging Face.\n"
                "Description: It will condense large pieces of text into concise sentences.\n"
            )
    @validate_input
    def run_model(self):
        input_data = self.input_entry.get("1.0", tk.END).strip()
        result = self.model_manager.run_model(input_data)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, result)

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select File")
        if file_path:
            self.input_entry.delete("1.0", tk.END)
            self.input_entry.insert(tk.END, file_path)

    def clear_input(self):
        self.input_entry.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)
