import tkinter as tk
from tkinter import ttk, filedialog
from functools import wraps
from model_loader import model_inference, modelrunner
from PIL import Image, ImageTk


# ---------------------- DECORATORS ----------------------
# theses are examples of decorators for log_action and validate_input 
def log_action(func):
    """Decorator for logging actions."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] Running {func.__name__} with args={args} kwargs={kwargs}")
        return func(self, *args, **kwargs)
    return wrapper


def validate_input(func):
    """Decorator to validate that input is non-empty string."""
    @wraps(func)
    def wrapper(self, input_data, *args, **kwargs):
        if not isinstance(input_data, str) or not input_data.strip():
            return "Invalid input: Please provide a non-empty string."
        return func(self, input_data, *args, **kwargs)
    return wrapper
    

# ---------------------- GUI ----------------------
class AIApp(tk.Tk): # AI app is inheriting from Tk class
    def __init__(self): # this method overrides the __init__ method from tkinter
        super().__init__() 
        self.title("Tkinter AI GUI")
        self.geometry("900x700")

        # Encapsulation: private attributes the loaded model and notes are private to the class
        self._loaded_model = None
        self._notes = "" 

        # ---------------- Menu ----------------
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        # Models menu (with dropdown options opening new pages)
        models_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Models", menu=models_menu)
        models_menu.add_command(label="Text-to-Image", command=self.open_text_to_image_page)
        models_menu.add_command(label="Text Summarization", command=self.open_text_summarization_page)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About / Team", command=self.open_help_page)

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

        ttk.Button(model_frame, text="Load Model", command=self.inference_runner).pack(side="left", padx=5, pady=5)

        # ---------------- Input Section ----------------
        input_frame = ttk.LabelFrame(
            self,
            text="User Input Section: Enter a brief description of the image you want to create if you've chosen the Text to Image model. If you want to summarize text, you can type it in or upload a text file."
        )
        input_frame.pack(fill="x", padx=10, pady=5)

        self.browse_btn = ttk.Button(input_frame, text="Browse", command=self.browse_file)
        self.browse_btn.pack(side="left", padx=5)

        self.input_entry = tk.Text(input_frame, height=5, width=60)
        self.input_entry.pack(padx=10, pady=10, fill="x")

        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Run Model", command=self.run_model).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_input).pack(side="left", padx=5)

        # ---------------- Output Section ----------------
        output_frame = ttk.LabelFrame(self, text="Model Output Section", height=10)
        output_frame.pack(fill="both", padx=10, pady=5, expand=True)

        ttk.Label(output_frame, text="Output Display:").pack(anchor="w", padx=5, pady=5)
        self.output_box = tk.Text(output_frame, wrap="word", height=10)
        self.output_box.pack(fill="both", expand=True, padx=10, pady=5)

        info_explain_frame = ttk.LabelFrame(self, text="Model Information & Explanation")
        info_explain_frame.pack(fill="both", padx=10, pady=5, expand=True)

        # Left: Model Info
        model_info_frame = ttk.Frame(info_explain_frame)
        model_info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ttk.Label(model_info_frame, text="Selected Model Info:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.model_info_box = tk.Text(model_info_frame, wrap="word", height=10)
        self.model_info_box.pack(fill="both", expand=True, padx=5, pady=5)

        # Right: OOP Explanations
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

    # ---------------- Menu Command Methods ----------------
    def open_text_to_image_page(self):
        win = tk.Toplevel(self)
        win.title("Text-to-Image Model Info")
        win.geometry("500x400")
        tk.Label(win, text="Text-to-Image Model Information", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Text(win, wrap="word", height=20, width=60).pack(padx=10, pady=10, fill="both", expand=True)

    def open_text_summarization_page(self):
        win = tk.Toplevel(self)
        win.title("Text Summarization Model Info")
        win.geometry("500x400")
        tk.Label(win, text="Text Summarization Model Information", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Text(win, wrap="word", height=20, width=60).pack(padx=10, pady=10, fill="both", expand=True)

    def open_help_page(self):
        win = tk.Toplevel(self)
        win.title("About / Team")
        win.geometry("500x400")
        tk.Label(win, text="Team Members Information", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Text(win, wrap="word", height=20, width=60).pack(padx=10, pady=10, fill="both", expand=True)

    # ---------------- Model Methods ----------------
    def inference_runner(self):
        p1 = model_inference(self.model_choice)
        self.model_parameters, self.model_name = p1.run_inferences()
        print(self.model_name)
        if self.model_name == "Text-to-Image":
            self.model_info_box.delete("1.0", tk.END)
            self.explain_box.delete("1.0", tk.END)
            self.explain_box.insert(
                tk.END,
                "Inheritance: Used in Text model and Image model Handlers, inheriting from Model Handler class\n"
                "Encapsulation: Implemented on the inference api key with PROTECTED status\n"
                "Polymorphism: Utilized on the run inference function\n"
                "Decorators: Utilized on the log action and ensure input functions\n"
                "Method overriding:??"
            )
            self.model_info_box.insert(tk.END, "Model: black-forest-labs/FLUX.1-dev\nCategory: Image Generation\nDescription: Generates images from text prompts.\n")
        else:
            self.model_info_box.delete("1.0", tk.END)
            self.explain_box.delete("1.0", tk.END)
            self.explain_box.insert(
                tk.END,
                "Inheritance: Used in Text model and Image model Handlers, inheriting from Model Handler class\n"
                "Encapsulation: Implemented on the inference api key with PROTECTED status\n"
                "Polymorphism: Utilized on the run inference function\n"
                "Decorators: Utilized on the log action and ensure input functions\n"
                "Method overriding:??"
            )
            self.model_info_box.insert(tk.END, "Model: pegasus-Large\nCategory: Text Summarization\nDescription: Summarizes long texts into concise sentences.\n")
# this is an example of polymorphism, the function call is the same but the output hanlding is polymorphic
# the output handling is different based on the model type


    @validate_input # the validate_input decorator is used to make sure a model name was chosen
    @log_action # this logs that a model was loaded
    def run_model(self): 
        if self.model_name == "Text-to-Image":
            self.modela = modelrunner(self.model_parameters, self.model_name, str(self.input_entry.get("1.0", "end-1c")))
            self.result = self.modela.run_model_result()
            self.char_width = self.output_box.cget('width')
            self.char_height = self.output_box.cget('height')

            self.pixel_width = self.output_box.winfo_width()
            self.pixel_height = self.output_box.winfo_height()

            self.result = self.result.resize((self.pixel_width, self.pixel_height), Image.Resampling.LANCZOS)
            self.result = ImageTk.PhotoImage(self.result)
            self.output_box.delete("1.0", tk.END)
            self.output_label_image = tk.Label(self.output_box, image=self.result)
            self.output_label_image.pack(fill="both", expand=True)

        else:
            self.modela = modelrunner(self.model_parameters, self.model_name, self.input_entry.get("1.0", "end-1c"))
            self.result = self.modela.run_model_result()
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, self.result)

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select File")
        if file_path:
            with open(file_path) as file:
                self.input_entry.delete("1.0", tk.END)
                self.input_entry.insert(tk.END, file.read())

    def clear_input(self):
        if self.model_name == "Text-to-Image":
            self.output_label_image.config(image="")
            self.input_entry.delete("1.0", tk.END)
            self.output_box.delete("1.0", tk.END)
            self.output_box.config(width=self.pixel_width, height=self.pixel_height)
        else:
            self.input_entry.delete("1.0", tk.END)
            self.output_box.delete("1.0", tk.END)