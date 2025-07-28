import tkinter as tk
from tkinter import filedialog, messagebox
import google.generativeai as genai
import speech_recognition as sr

# ---- CONFIGURE GEMINI ----
genai.configure(api_key="AIzaSyB44yyxyf8atB3Tefp7C2eMczhokKPVGc8")  # Replace with your actual API Key
model = genai.GenerativeModel("gemini-1.5-flash")

# ---- Main App Window ----
root = tk.Tk()
root.title("AI Text Editor")
root.geometry("800x600")

text_area = tk.Text(root, wrap=tk.WORD, font=("Arial", 14))
text_area.pack(expand=True, fill=tk.BOTH)

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

# ---- Buttons ----
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="💾 Save", command=save_file).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="📂 Open", command=open_file).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="✨ Generate", command=generate_text).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="📃 Summarize", command=summarize_text).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="✅ Grammar Fix", command=correct_grammar).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="🎤 Voice Input", command=voice_input).pack(side=tk.LEFT, padx=5)

# ---- Run App ----
root.mainloop()
