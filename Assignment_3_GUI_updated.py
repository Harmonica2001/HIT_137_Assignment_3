# ===== File: Assignment_3_GUI_updated.py =====
import tkinter as tk
from tkinter import ttk, filedialog
from functools import wraps
from PIL import Image, ImageTk
from model_loader import model_inference, modelrunner


# ---------------- Decorators ----------------
def log_action(func):
    """Decorator for logging actions."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] {func.__name__} called")
        return func(self, *args, **kwargs)
    return wrapper


def validate_input(func):
    """Prevent running the model with empty input."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        text = self.input_entry.get("1.0", "end-1c").strip()
        if not text:
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", "Invalid input: please enter some text first.")
            return
        return func(self, *args, **kwargs)
    return wrapper


# ---------------- GUI App ----------------
class AIApp(tk.Tk):  # Inheritance: AIApp subclasses tk.Tk
    def __init__(self):  # Method overriding of Tk.__init__
        super().__init__()
        self.title("Tkinter AI GUI")
        self.geometry("900x700")

        # App state
        self.model_name = ""
        self.model_parameters = None
        self._img_ref = None  # keep image reference for Tk

        # ---- Menubar ----
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

        # ---- Model Selection ----
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

        # ---- Input Section ----
        input_frame = ttk.LabelFrame(
            self,
            text="User Input Section: Enter text for summarization or a description for image generation."
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

        # ---- Output Section ----
        output_frame = ttk.LabelFrame(self, text="Model Output Section")
        output_frame.pack(fill="both", padx=10, pady=6, expand=True)

        ttk.Label(output_frame, text="Output Display:").pack(anchor="w", padx=8, pady=(6, 0))
        self.output_box = tk.Text(output_frame, wrap="word", height=10)
        self.output_box.pack(fill="both", expand=True, padx=10, pady=6)

        # dedicated image holder (more reliable than Text embedding)
        self.image_holder = ttk.Label(output_frame)
        self.image_holder.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # ---- Info + OOP ----
        info_frame = ttk.LabelFrame(self, text="Model Information & Explanation")
        info_frame.pack(fill="both", padx=10, pady=6, expand=True)

        # Left: Selected Model Info (⚠️ keep simple like your original)
        left = ttk.Frame(info_frame)
        left.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        ttk.Label(left, text="Selected Model Info:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.model_info_box = tk.Text(left, wrap="word", height=10)
        self.model_info_box.pack(fill="both", expand=True, padx=4, pady=6)

        # Right: OOP Explanations
        right = ttk.Frame(info_frame)
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        ttk.Label(right, text="OOP Concepts Explanation:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.explain_box = tk.Text(right, wrap="word", height=100)
        self.explain_box.pack(fill="both", expand=True, padx=4, pady=6)
        self._show_oop_explanations()

        # Prime the Selected Model Info with a short summary (same style you used)
        self._update_selected_model_info("Text-to-Image")

    # -------- keep the Selected Model Info short (as you had it) --------
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

    # -------- OOP text (right panel) --------
    def _show_oop_explanations(self):
        self.explain_box.delete("1.0", "end")
        self.explain_box.insert("end",
            "Inheritance:\n"
            "• AIApp subclasses tk.Tk.\n"
            "• Backend handlers inherit from ModelHandler and a Logger mixin (multiple inheritance).\n\n"
            "Encapsulation:\n"
            "• Private attributes (API keys, parameters) are not exposed outside their classes.\n\n"
            "Polymorphism:\n"
            "• run_inference(model_details, input_text) is implemented differently for text vs image.\n\n"
            "Decorators:\n"
            "• @log_action logs GUI/backend actions.\n"
            "• @validate_input prevents running with empty input.\n\n"
            "Method overriding:\n"
            "• AIApp.__init__ overrides Tk initialization to build menus, frames, and widgets.\n"
        )

    # --------------- Menu windows --------------------
    def open_text_to_image_page(self):
        """Models > Text-to-Image — human bullets about the model and key packages."""
        win = tk.Toplevel(self)
        win.title("Text-to-Image Model Info")
        win.geometry("680x560")

        tk.Label(win, text="Text-to-Image • black-forest-labs/FLUX.1-dev",
                 font=("Arial", 12, "bold")).pack(pady=(10, 6))

        frame = ttk.Frame(win); frame.pack(fill="both", expand=True, padx=10, pady=8)
        sb = ttk.Scrollbar(frame)
        txt = tk.Text(frame, wrap="word", yscrollcommand=sb.set)
        sb.config(command=txt.yview); sb.pack(side="right", fill="y"); txt.pack(side="left", fill="both", expand=True)

        txt.insert("end",
            "• What it is:\n"
            "  FLUX.1-dev is a lightweight text-to-image model from Black Forest Labs. It turns short natural-language "
            "  prompts into pictures. We use a cloud inference endpoint so no local GPU is required.\n\n"
            "• How we use it here:\n"
            "  Your prompt from the input box is sent to a Nebius Inference endpoint. The endpoint returns an image, "
            "  which we render in the preview area and resize to fit the window.\n\n"
            "• Strengths:\n"
            "  Quick to try, free-tier friendly, ideal for demos and coursework. No heavy downloads; you can swap to a "
            "  different model easily if needed.\n\n"
            "• Limitations:\n"
            "  Quality depends on the prompt; complex scenes may take several attempts. Requires internet and a valid "
            "  API key for the cloud service.\n\n"
            "• Important packages used in this app:\n"
            "  – tkinter: builds the GUI (windows, menus, buttons, text fields).\n"
            "  – Pillow (PIL): opens the returned image, resizes it, and shows it in the preview label.\n"
            "  – requests / HTTP client (inside model_loader): sends the prompt to Nebius and reads back image bytes.\n"
            "  – io / base64 (as needed in model_loader): safely handle binary image responses.\n"
            "  – os / environment variables: read API keys without committing secrets to GitHub.\n"
            "  – (service) Nebius Inference API: hosts FLUX.1-dev and returns generated images over HTTP.\n\n"
            "• Typical I/O:\n"
            "  Input: a short description, e.g., “a small red coffee mug on a wooden desk, soft light”.\n"
            "  Output: a PNG/JPEG image matching the prompt, displayed in the GUI.\n"
        )
        txt.configure(state="disabled")

    def open_text_summarization_page(self):
        """Models > Text Summarization — human bullets about the model and key packages."""
        win = tk.Toplevel(self)
        win.title("Text Summarization Model Info")
        win.geometry("680x560")

        tk.Label(win, text="Text Summarization • google/pegasus-large",
                 font=("Arial", 12, "bold")).pack(pady=(10, 6))

        frame = ttk.Frame(win); frame.pack(fill="both", expand=True, padx=10, pady=8)
        sb = ttk.Scrollbar(frame)
        txt = tk.Text(frame, wrap="word", yscrollcommand=sb.set)
        sb.config(command=txt.yview); sb.pack(side="right", fill="y"); txt.pack(side="left", fill="both", expand=True)

        txt.insert("end",
            "• What it is:\n"
            "  google/pegasus-large is an abstractive summarization model from Google Research. It rewrites long text "
            "  into a short, fluent summary rather than copying sentences.\n\n"
            "• How we use it here:\n"
            "  The text from the input box is sent to the Hugging Face Inference API. The model returns a concise "
            "  summary, which we show in the Output Display area.\n\n"
            "• Strengths:\n"
            "  Great for condensing articles, reports, and study notes into readable key points.\n\n"
            "• Limitations:\n"
            "  Very long inputs may need trimming; factual quality depends on the source text. Requires internet and, "
            "  if needed, an HF API token.\n\n"
            "• Important packages used in this app:\n"
            "  – tkinter: provides the text input and the output display.\n"
            "  – requests / HTTP client (inside model_loader): calls the Hugging Face Inference endpoint.\n"
            "  – json: parses the response to extract the summary text.\n"
            "  – os / environment variables: store tokens/keys safely for API access.\n"
            "  – (service) Hugging Face Inference API: hosts google/pegasus-large and returns summaries over HTTP.\n\n"
            "• Typical I/O:\n"
            "  Input: 2–8 paragraphs of text you want condensed.\n"
            "  Output: a brief, coherent summary (a few sentences) shown in the Output box.\n"
        )
        txt.configure(state="disabled")

    def open_help_page(self):
        win = tk.Toplevel(self)
        win.title("About / Team")
        win.geometry("480x360")
        tk.Label(win, text="Team / About", font=("Arial", 12, "bold")).pack(pady=(10, 6))
        box = tk.Text(win, wrap="word")
        box.pack(fill="both", expand=True, padx=10, pady=10)
        box.insert("end",
            "Add your team members here with student IDs and roles (GUI, backend, testing, docs). "
            "Mention the GitHub repository URL and how contributions were divided.\n"
        )
        box.configure(state="disabled")

    # -------- Buttons --------
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

    def clear_input(self):
        self.input_entry.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.image_holder.configure(image="")
        self._img_ref = None

    # -------- Load + Run --------
    @log_action
    def inference_runner(self):
        """Load the model (parameters + name) and refresh the short Selected Model Info."""
        p1 = model_inference(self.model_choice)
        self.model_parameters, self.model_name = p1.run_inferences()
        print(f"[INFO] Loaded: {self.model_name}")
        self._update_selected_model_info(self.model_name)

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
            # result is a PIL.Image
            self.update_idletasks()
            w = max(256, self.image_holder.winfo_width())
            h = max(256, self.image_holder.winfo_height())
            img = result.resize((w, h), Image.Resampling.LANCZOS)
            self._img_ref = ImageTk.PhotoImage(img)
            self.image_holder.configure(image=self._img_ref)
            self.output_box.delete("1.0", "end")
        else:
            # result is a summary string
            self.image_holder.configure(image="")
            self._img_ref = None
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", result)


# main.py runs AIApp
