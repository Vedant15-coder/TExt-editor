import tkinter as tk
from tkinter import filedialog, messagebox
import google.generativeai as genai
import speech_recognition as sr

# ---- CONFIGURE GEMINI ----
genai.configure(api_key="AIzaSyB44yyxyf8atB3Tefp7C2eMczhokKPVGc8")
model = genai.GenerativeModel("gemini-1.5-flash")

# ---- Main Root Window ----
root = tk.Tk()
root.title("AI Text Editor")
root.geometry("800x600")

# ---- Welcome Frame ----
welcome_frame = tk.Frame(root, bg="white")
welcome_frame.place(relwidth=1, relheight=1)

welcome_label = tk.Label(
    welcome_frame,
    text="Welcome back Vedant,\nHow can I help you today?",
    font=("Helvetica", 20, "bold"),
    bg="white",
    fg="#333"
)
welcome_label.pack(pady=80)

def animate_button(step=0):
    if step <= 10:
        get_started_btn.place(relx=0.5, rely=0.5 + (10 - step) * 0.01, anchor="center")
        root.after(20, lambda: animate_button(step + 1))

def launch_text_editor():
    welcome_frame.destroy()

    global text_area

    text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 14))
    text_area.pack(expand=True, fill=tk.BOTH)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="💾 Save", command=save_file).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="📂 Open", command=open_file).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="✨ Generate", command=generate_text).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="📃 Summarize", command=summarize_text).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="✅ Grammar Fix", command=correct_grammar).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="🎤 Voice Input", command=voice_input).pack(side=tk.LEFT, padx=5)

get_started_btn = tk.Button(
    welcome_frame,
    text="🚀 Get Started",
    font=("Arial", 16),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    command=launch_text_editor
)
animate_button()

# ---- Functions ----
def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt")
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text_area.get("1.0", tk.END))
        messagebox.showinfo("Saved", "File saved successfully.")

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, content)

def generate_text():
    prompt = text_area.get("1.0", tk.END).strip()
    if not prompt:
        return
    response = model.generate_content(prompt)
    text_area.insert(tk.END, "\n\n[Generated Text]\n" + response.text)

def summarize_text():
    prompt = text_area.get("1.0", tk.END).strip()
    if not prompt:
        return
    response = model.generate_content(f"Summarize this:\n{prompt}")
    text_area.insert(tk.END, "\n\n[Summary]\n" + response.text)

def correct_grammar():
    prompt = text_area.get("1.0", tk.END).strip()
    if not prompt:
        return
    response = model.generate_content(f"Correct the grammar of the following:\n{prompt}")
    text_area.insert(tk.END, "\n\n[Corrected Grammar]\n" + response.text)

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Recording", "Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        text_area.insert(tk.END, f"\n[Voice Input]: {text}\n")
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand audio.")
    except sr.RequestError:
        messagebox.showerror("Error", "Could not connect to speech recognition service.")

# ---- Start GUI ----
root.mainloop()
