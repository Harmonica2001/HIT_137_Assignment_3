
# ===== Assignment_3_GUI_updated.py =====


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from functools import wraps
from PIL import Image, ImageTk
from model_loader import model_inference, modelrunner
import webbrowser


# Logging function calls using a decorator so each time a function is triggered,
# its name appears in the console for easier debugging and tracing.
def log_action(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] {func.__name__} called")
        return func(self, *args, **kwargs)
    return wrapper


# Validating input before running a model, making sure that the text box
# contains some content so empty submissions do not break the workflow.
def validate_input(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        text = self.input_entry.get("1.0", "end-1c").strip()
        if not text:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", "Invalid input: please enter some text first.")
            return
        return func(self, *args, **kwargs)
    return wrapper


# Creating the main application window by extending tkinter’s Tk class
# and organizing the interface into menus, input areas, and output sections.
class AIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter AI GUI")
        self.geometry("900x700")

        # Storing application state, including selected model, its parameters,
        # and a reference to the currently displayed image.
        self.model_name = ""
        self.model_parameters = None
        self._img_ref = None

        # Building the menu bar and attaching File, Models, and Help menus.
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        models_menu = tk.Menu(menubar, tearoff=0)
        models_menu.add_command(label="Text-to-Image", command=self.open_text_to_image_page)
        models_menu.add_command(label="Text Summarization", command=self.open_text_summarization_page)
        menubar.add_cascade(label="Models", menu=models_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About / Team", command=self.open_help_page)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Setting up model selection area with a dropdown and a load button.
        model_frame = ttk.LabelFrame(self, text="Model Selection")
        model_frame.pack(fill="x", padx=10, pady=6)

        ttk.Label(model_frame, text="Select Model:").pack(side="left", padx=5, pady=5)

        self.model_choice = tk.StringVar(value="Text-to-Image")
        self.model_dropdown = ttk.Combobox(
            model_frame,
            textvariable=self.model_choice,
            values=["Text-to-Image", "Text Summarization"],
            state="readonly",
            width=28
        )
        self.model_dropdown.pack(side="left", padx=5, pady=5)

        ttk.Button(model_frame, text="Load Model", command=self.inference_runner)\
            .pack(side="left", padx=6, pady=5)

        # Creating an input section for entering text or browsing files.
        input_frame = ttk.LabelFrame(
            self,
            text="User Input Section: Type text to summarize or a description for image generation."
        )
        input_frame.pack(fill="x", padx=10, pady=6)

        self.browse_btn = ttk.Button(input_frame, text="Browse", command=self.browse_file)
        self.browse_btn.pack(side="left", padx=6, pady=6)

        self.input_entry = tk.Text(input_frame, height=5)
        self.input_entry.pack(fill="x", padx=10, pady=6)

        btns = ttk.Frame(input_frame)
        btns.pack(fill="x", pady=(0, 6))
        ttk.Button(btns, text="Run Model", command=self.run_model).pack(side="left", padx=6)
        ttk.Button(btns, text="Clear", command=self.clear_input).pack(side="left", padx=6)

        # Creating the output section for displaying summaries or generated images.
        output_frame = ttk.LabelFrame(self, text="Model Output Section")
        output_frame.pack(fill="both", padx=10, pady=6, expand=True)

        ttk.Label(output_frame, text="Output Display:").pack(anchor="w", padx=8, pady=(6, 0))
        self.output_box = tk.Text(output_frame, wrap="word", height=10)
        self.output_box.pack(fill="both", expand=True, padx=10, pady=6)

        # Adding a dedicated image holder to reliably display generated images.
        self.image_holder = ttk.Label(output_frame)
        self.image_holder.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Creating a combined frame for model information and OOP explanations.
        info_frame = ttk.LabelFrame(self, text="Model Information & Explanation")
        info_frame.pack(fill="both", padx=10, pady=6, expand=True)

        # Displaying information about the currently selected model.
        left = ttk.Frame(info_frame)
        left.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        ttk.Label(left, text="Selected Model Info:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.model_info_box = tk.Text(left, wrap="word", height=10)
        self.model_info_box.pack(fill="both", expand=True, padx=4, pady=6)

        # Explaining OOP concepts with a dedicated text box.
        right = ttk.Frame(info_frame)
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        ttk.Label(right, text="OOP Concepts Explanation:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.explain_box = tk.Text(right, wrap="word", height=100)
        self.explain_box.pack(fill="both", expand=True, padx=4, pady=6)
        self._show_oop_explanations()

        # Preloading information for the Text-to-Image model by default.
        self._update_selected_model_info("Text-to-Image")

    # Updating the information panel on the left with details about the selected model.
    def _update_selected_model_info(self, model_key: str):
        self.model_info_box.delete("1.0", "end")
        if model_key == "Text-to-Image":
            self.model_info_box.insert("end",
                "Model: black-forest-labs/FLUX.1-dev\n"
                "Category: Image Generation\n"
                "Provider: nebius (cloud inference)\n"
            )
        else:
            self.model_info_box.insert("end",
                "Model: google/pegasus-large\n"
                "Category: Text Summarization\n"
                "Provider: hf-inference (Hugging Face)\n"
            )

    # Displaying explanations of object-oriented programming concepts
    # in the right-hand panel to help connect code with theory.
    def _show_oop_explanations(self):
        self.explain_box.delete("1.0", "end")
        self.explain_box.insert("end",
            "Inheritance:\n"
            "AIApp extends tk.Tk to create the main window.\n"
            "Backend handlers extend ModelHandler and LoggerMixin.\n\n"
            "Encapsulation:\n"
            "API keys and model parameters remain hidden inside classes.\n\n"
            "Polymorphism:\n"
            "run_inference behaves differently depending on text or image handlers.\n\n"
            "Decorators:\n"
            "@log_action logs actions, @validate_input checks user input.\n\n"
            "Method overriding:\n"
            "The __init__ method is redefined to build a custom interface.\n"
        )

    # Opening a detailed information window about the text-to-image model.
    def open_text_to_image_page(self):
        win = tk.Toplevel(self)
        win.title("Text-to-Image Model Info")
        win.geometry("680x620")
        tk.Label(win, text="Text-to-Image • black-forest-labs/FLUX.1-dev",
                 font=("Arial", 12, "bold")).pack(pady=(10, 6))

        frame = ttk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=8)
        sb = ttk.Scrollbar(frame)
        txt = tk.Text(frame, wrap="word", yscrollcommand=sb.set)
        # Configuring the scrollbar to control the text widget’s vertical view
        sb.config(command=txt.yview)
        # Packing the scrollbar on the right side and stretching it vertically
        sb.pack(side="right", fill="y")

        txt.pack(side="left", fill="both", expand=True)

        txt.insert("end",
            "FLUX.1-dev is a text-to-image AI model created by Black Forest Labs. "
            "It generates images from descriptive prompts by running on Nebius cloud servers.\n\n"
            "Models involved:\n"
            "black-forest-labs/FLUX.1-dev – the main text-to-image model used here.\n\n"
            "Process:\n"
            "1. A description is typed into the input box.\n"
            "2. The Nebius Inference API receives the text.\n"
            "3. FLUX.1-dev generates an image.\n"
            "4. The application displays the image in the output section.\n\n"
            "Packages involved:\n"
            "tkinter for GUI\n"
            "Pillow for image handling\n"
            "requests for API communication\n"
            "os for managing keys\n\n"
            "Usefulness:\n"
            "Enabling quick image generation without requiring local GPUs, "
            "making it suitable for demos and creative experiments.\n"
        )
        txt.configure(state="disabled")

    # Opening a detailed information window about the text summarization model.
    def open_text_summarization_page(self):
        win = tk.Toplevel(self)
        win.title("Text Summarization Model Info")
        win.geometry("680x620")
        tk.Label(win, text="Text Summarization • google/pegasus-large",
                 font=("Arial", 12, "bold")).pack(pady=(10, 6))

        frame = ttk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=8)
        sb = ttk.Scrollbar(frame)
        txt = tk.Text(frame, wrap="word", yscrollcommand=sb.set)
        sb.config(command=txt.yview)
        sb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)

        txt.insert("end",
            "google/pegasus-large is an abstractive summarization model from Google Research. "
            "It produces fluent summaries instead of simply copying sentences.\n\n"
            "Models involved:\n"
            "google/pegasus-large – the summarization model used in this application.\n\n"
            "Process:\n"
            "1. Text is entered into the input box.\n"
            "2. The Hugging Face API receives the content.\n"
            "3. Pegasus analyzes the input and generates a concise summary.\n"
            "4. The summary is shown in the output area.\n\n"
            "Packages involved:\n"
            "tkinter for input and display\n"
            "requests for API communication\n"
            "json for parsing responses\n"
            "os for handling API tokens\n\n"
            "Usefulness:\n"
            "Providing quick summaries of long text passages, helping reduce reading time "
            "while retaining key ideas.\n"
        )
        txt.configure(state="disabled")

    # Opening a window that displays team information and GitHub link.
    def open_help_page(self):
        win = tk.Toplevel(self)
        win.title("About / Team")
        win.geometry("500x400")
        tk.Label(win, text="Team / About", font=("Arial", 12, "bold")).pack(pady=(10, 6))

        box = tk.Text(win, wrap="word", height=20, width=60, cursor="arrow")
        box.pack(fill="both", expand=True, padx=10, pady=10)

        about_text = (
            "HIT137 – Software Now\n"
            "Group DAN/EXT 04\n\n"
            "Team Members:\n"
            " - Syed Haroon Ahmad (s393516)\n"
            " - Md Adnan Abir (s382198)\n"
            " - Simbarashe Mutyambizi (s385833)\n"
            " - Najmus Sakeeb (s393942)\n\n"
            "GitHub Repository:\n"
            "https://github.com/Harmonica2001/HIT_137_Assignment_3\n"
        )
        box.insert("1.0", about_text)

        url = "https://github.com/Harmonica2001/HIT_137_Assignment_3"
        start = box.search(url, "1.0", "end")
        if start:
            end = f"{start}+{len(url)}c"
            box.tag_add("link", start, end)
            box.tag_config("link", foreground="blue", underline=True)

            def open_link(_event=None):
                webbrowser.open(url)

            box.tag_bind("link", "<Button-1>", open_link)

        box.config(state="disabled")

    # Loading text from a chosen file and inserting it into the input box.
    def browse_file(self):
        path = filedialog.askopenfilename(title="Select text file")
        if path:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    data = f.read()
                self.input_entry.delete("1.0", "end")
                self.input_entry.insert("end", data)
            except Exception as e:
                self.output_box.delete("1.0", "end")
                self.output_box.insert("end", f"Failed to read file: {e}")

    # Clearing the input box, output text, and any displayed image.
    def clear_input(self):
        self.input_entry.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.image_holder.configure(image="")
        self._img_ref = None

    # Loading the selected model and updating the information panel accordingly.
    @log_action
    def inference_runner(self):
        p1 = model_inference(self.model_choice)
        self.model_parameters, self.model_name = p1.run_inferences()
        print(f"[INFO] Loaded: {self.model_name}")
        self._update_selected_model_info(self.model_name)

    # Running the loaded model with the provided input and displaying the result.
    @validate_input
    @log_action
    def run_model(self):
        if not self.model_name:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", "Please load and select a model first.")
            return

        user_text = self.input_entry.get("1.0", "end-1c")

        try:
            runner = modelrunner(self.model_parameters, self.model_name, user_text)
            result = runner.run_model_result()
        except Exception as e:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", f"Error while running model: {e}")
            return

        if self.model_name == "Text-to-Image":
            self.update_idletasks()
            w = max(256, self.image_holder.winfo_width())
            h = max(256, self.image_holder.winfo_height())
            img = result.resize((w, h), Image.Resampling.LANCZOS)
            self._img_ref = ImageTk.PhotoImage(img)
            self.image_holder.configure(image=self._img_ref)
            self.output_box.delete("1.0", "end")
        else:
            self.image_holder.configure(image="")
            self._img_ref = None
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", result)


# Running the application by creating an instance of AIApp
# and keeping the window open with the Tkinter event loop
if __name__ == "__main__":
    app = AIApp()
    app.mainloop()
