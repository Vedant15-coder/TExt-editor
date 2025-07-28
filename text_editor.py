import tkinter as tk
from tkinter import filedialog, messagebox, Menu, scrolledtext
import google.generativeai as genai
import speech_recognition as sr

# ---- CONFIGURE GEMINI ----
genai.configure(api_key="AIzaSyB44yyxyf8atB3Tefp7C2eMczhokKPVGc8")  # Replace with your actual API Key
model = genai.GenerativeModel("gemini-1.5-flash")

# ---- Main App Window ----
root = tk.Tk()
root.title("AI Text Editor")
root.geometry("1000x700")
root.minsize(600, 400)

# ---- Global Variables ----
current_file = None
char_count_var = tk.StringVar()
char_count_var.set("Characters: 0")

# ---- Text Area with Scrollbars ----
text_frame = tk.Frame(root)
text_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

text_area = scrolledtext.ScrolledText(
    text_frame, 
    wrap=tk.WORD, 
    font=("Arial", 12),
    undo=True,
    bg="#f8f9fa",
    fg="#212529",
    insertbackground="#007bff",
    selectbackground="#007bff",
    selectforeground="white"
)
text_area.pack(expand=True, fill=tk.BOTH)

# ---- Functions ----
def save_file():
    global current_file
    if current_file:
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(text_area.get("1.0", tk.END))
        messagebox.showinfo("Saved", f"File saved: {current_file}")
        update_title()
    else:
        save_as_file()

def save_as_file():
    global current_file
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if filepath:
        current_file = filepath
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text_area.get("1.0", tk.END))
        messagebox.showinfo("Saved", "File saved successfully.")
        update_title()

def open_file():
    global current_file
    filepath = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if filepath:
        current_file = filepath
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, content)
        update_title()
        update_char_count()

def new_file():
    global current_file
    if messagebox.askokcancel("New File", "Create a new file? Unsaved changes will be lost."):
        current_file = None
        text_area.delete("1.0", tk.END)
        update_title()
        update_char_count()

def generate_text():
    prompt = text_area.get("1.0", tk.END).strip()
    if not prompt:
        return
    response = model.generate_content(prompt)
    text_area.insert(tk.END, "\n\n[Generated Text]\n" + response.text)
    update_char_count()

def summarize_text():
    prompt = text_area.get("1.0", tk.END).strip()
    if not prompt:
        return
    response = model.generate_content(f"Summarize this:\n{prompt}")
    text_area.insert(tk.END, "\n\n[Summary]\n" + response.text)
    update_char_count()

def correct_grammar():
    prompt = text_area.get("1.0", tk.END).strip()
    if not prompt:
        return
    response = model.generate_content(f"Correct the grammar of the following:\n{prompt}")
    text_area.insert(tk.END, "\n\n[Corrected Grammar]\n" + response.text)
    update_char_count()

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Recording", "Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        text_area.insert(tk.END, f"\n[Voice Input]: {text}\n")
        update_char_count()
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand audio.")
    except sr.RequestError:
        messagebox.showerror("Error", "Could not connect to speech recognition service.")

# ---- UI Helper Functions ----
def update_title():
    if current_file:
        filename = current_file.split("/")[-1]
        root.title(f"AI Text Editor - {filename}")
    else:
        root.title("AI Text Editor - Untitled")

def update_char_count(event=None):
    content = text_area.get("1.0", tk.END)
    char_count = len(content) - 1  # Subtract 1 for the extra newline
    char_count_var.set(f"Characters: {char_count}")

def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.quit()

def show_about():
    messagebox.showinfo("About", "AI Text Editor v1.0\nPowered by Google Gemini AI\nBuilt with Python & Tkinter")

# ---- Menu Bar ----
menubar = Menu(root)
root.config(menu=menubar)

# File Menu
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_separator()
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Save As", command=save_as_file, accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app, accelerator="Ctrl+Q")

# Edit Menu
edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=lambda: text_area.edit_undo(), accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=lambda: text_area.edit_redo(), accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=lambda: text_area.event_generate("<<Cut>>"), accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=lambda: text_area.event_generate("<<Copy>>"), accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=lambda: text_area.event_generate("<<Paste>>"), accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=lambda: text_area.tag_add("sel", "1.0", "end"), accelerator="Ctrl+A")

# AI Menu
ai_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="AI", menu=ai_menu)
ai_menu.add_command(label="Generate Text", command=generate_text, accelerator="F1")
ai_menu.add_command(label="Summarize Text", command=summarize_text, accelerator="F2")
ai_menu.add_command(label="Correct Grammar", command=correct_grammar, accelerator="F3")
ai_menu.add_command(label="Voice Input", command=voice_input, accelerator="F4")

# Help Menu
help_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

# ---- Toolbar ----
toolbar = tk.Frame(root, bg="#e9ecef", height=40)
toolbar.pack(fill=tk.X, padx=5, pady=(5, 0))

# File buttons
tk.Button(toolbar, text="📄 New", command=new_file, relief=tk.FLAT, bg="#e9ecef").pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="📂 Open", command=open_file, relief=tk.FLAT, bg="#e9ecef").pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="💾 Save", command=save_file, relief=tk.FLAT, bg="#e9ecef").pack(side=tk.LEFT, padx=2)

# Separator
tk.Frame(toolbar, width=2, bg="#6c757d").pack(side=tk.LEFT, fill=tk.Y, padx=10)

# AI buttons
tk.Button(toolbar, text="✨ Generate", command=generate_text, relief=tk.FLAT, bg="#e9ecef").pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="📃 Summarize", command=summarize_text, relief=tk.FLAT, bg="#e9ecef").pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="✅ Grammar", command=correct_grammar, relief=tk.FLAT, bg="#e9ecef").pack(side=tk.LEFT, padx=2)
tk.Button(toolbar, text="🎤 Voice", command=voice_input, relief=tk.FLAT, bg="#e9ecef").pack(side=tk.LEFT, padx=2)

# ---- Status Bar ----
status_bar = tk.Frame(root, bg="#f8f9fa", height=25)
status_bar.pack(fill=tk.X, side=tk.BOTTOM)

tk.Label(status_bar, textvariable=char_count_var, bg="#f8f9fa", anchor=tk.W).pack(side=tk.LEFT, padx=10)
tk.Label(status_bar, text="Ready", bg="#f8f9fa", anchor=tk.E).pack(side=tk.RIGHT, padx=10)

# ---- Keyboard Shortcuts ----
root.bind('<Control-n>', lambda e: new_file())
root.bind('<Control-o>', lambda e: open_file())
root.bind('<Control-s>', lambda e: save_file())
root.bind('<Control-Shift-S>', lambda e: save_as_file())
root.bind('<Control-q>', lambda e: exit_app())
root.bind('<F1>', lambda e: generate_text())
root.bind('<F2>', lambda e: summarize_text())
root.bind('<F3>', lambda e: correct_grammar())
root.bind('<F4>', lambda e: voice_input())

# ---- Text Area Event Bindings ----
text_area.bind('<KeyRelease>', update_char_count)
text_area.bind('<Button-1>', update_char_count)

# ---- Initialize UI ----
update_title()
update_char_count()

# ---- Run App ----
root.mainloop()
