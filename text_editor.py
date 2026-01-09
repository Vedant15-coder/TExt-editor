import os
import tkinter as tk
from tkinter import messagebox, Scrollbar
import google.generativeai as genai
import threading
import speech_recognition as sr

# -- API KEY via environment variable

# For demo/testing; use environment for production!


# === SAVE CHAT FUNCTION (moved up to prevent NameError) ===
def save_chat():
    try:
        with open("chat_history.txt", "w", encoding="utf-8") as f:
            for msg in chat_history:
                role = msg["role"].capitalize()
                f.write(f"{role}: {msg['parts'][0]}\n\n")
        messagebox.showinfo("Saved", "Chat saved to chat_history.txt!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save chat: {e}")

def add_message(text, sender="user"):
    frame = tk.Frame(chat_frame, bg="#16213e")
    chat_canvas.update_idletasks()
    canvas_width = chat_canvas.winfo_width()
    wrap_length = max(600, canvas_width - 100)

    label = tk.Label(
        frame,
        text=text,
        padx=20, pady=15,
        bg="#DCF8C6" if sender == "user" else "#2d3748",
        fg="black" if sender == "user" else "white", 
        anchor="e" if sender == "user" else "w",
        justify="right" if sender == "user" else "left",
        wraplength=wrap_length,
        font=("Arial", 12)
    )
    label.pack(fill="both", expand=True)
    frame.pack(fill="x", pady=8, padx=30)
    chat_frame.update_idletasks()
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
    chat_canvas.yview_moveto(1)

def send_message():
    user_msg = user_entry.get()
    if not user_msg.strip(): return
    add_message(user_msg, sender="user")
    user_entry.delete(0, tk.END)
    threading.Thread(target=generate_ai_reply, args=(user_msg,)).start()

def generate_ai_reply(user_msg):
    try:
        add_message("Thinking...", sender="ai")
        chat_history.append({"role": "user", "parts": [user_msg]})
        response = model.generate_content(chat_history)
        chat_history.append({"role": "model", "parts": [response.text]})
        chat_frame.winfo_children()[-1].destroy()
        add_message(response.text, sender="ai")
    except Exception as e:
        chat_frame.winfo_children()[-1].destroy()
        add_message(f"Error: {e}", sender="ai")

def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

def toggle_fullscreen(event):
    current_state = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not current_state)

def update_chat_layout():
    chat_canvas.update_idletasks()
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))

def on_window_resize(event):
    if event.widget == root:
        root.after(100, update_chat_layout)

def show_chat_interface():
    welcome_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def toggle_menu():
    if menu_frame.winfo_viewable():
        menu_frame.place_forget()
    else:
        x = three_dots_btn.winfo_x()
        y = three_dots_btn.winfo_y() - 180
        menu_frame.place(x=x, y=y)

def open_text_editor():
    menu_frame.place_forget()
    editor_window = tk.Toplevel(root)
    editor_window.title("✍️ Text Editor")
    editor_window.geometry("800x600")
    editor_window.configure(bg="#1a1a2e")
    text_area = tk.Text(editor_window, bg="#2d3748", fg="white", font=("Arial", 12), wrap=tk.WORD, insertbackground="white")
    text_area.pack(fill="both", expand=True, padx=20, pady=20)
    def send_to_chat():
        content = text_area.get("1.0", tk.END).strip()
        if content:
            user_entry.delete(0, tk.END)
            user_entry.insert(0, content)
            editor_window.destroy()
    send_button = tk.Button(editor_window, text="📤 Send to Chat", bg="#667eea", fg="white", font=("Arial", 12), command=send_to_chat)
    send_button.pack(pady=10)

def voice_input():
    menu_frame.place_forget()
    voice_window = tk.Toplevel(root)
    voice_window.title("🎤 Voice Input")
    voice_window.geometry("400x300")
    voice_window.configure(bg="#1a1a2e")
    voice_label = tk.Label(voice_window, text="🎤 Voice Input", font=("Helvetica", 18, "bold"), fg="white", bg="#1a1a2e")
    voice_label.pack(pady=30)
    status_label = tk.Label(voice_window, text="Click 'Start Recording' to begin", font=("Arial", 12), fg="#b8b8d1", bg="#1a1a2e")
    status_label.pack(pady=10)
    def real_voice_input():
        status_label.configure(text="🎤 Listening...")
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                audio = r.listen(source)
                text = r.recognize_google(audio)
                user_entry.delete(0, tk.END)
                user_entry.insert(0, text)
                voice_window.destroy()
            status_label.config(text="✅ Done!")
        except sr.UnknownValueError:
            status_label.config(text="❌ Could not understand.")
        except Exception as e:
            status_label.config(text=f"⚠️ Error: {e}")
    record_btn = tk.Button(voice_window, text="🎤 Start Recording", bg="#e74c3c", fg="white", font=("Arial", 12), command=real_voice_input)
    record_btn.pack(pady=20)

def image_editor():
    menu_frame.place_forget()
    image_window = tk.Toplevel(root)
    image_window.title("🖼️ Image Tools")
    image_window.geometry("500x400")
    image_window.configure(bg="#1a1a2e")
    title_label = tk.Label(image_window, text="🖼️ Image & Screenshot Tools", font=("Helvetica", 18, "bold"), fg="white", bg="#1a1a2e")
    title_label.pack(pady=30)
    def take_screenshot():
        status_label.configure(text="📸 Screenshot taken! (Demo Mode)")
        image_window.after(2000, lambda: status_label.configure(text="Ready to use image tools"))
    def edit_image():
        status_label.configure(text="🎨 Opening image editor... (Demo Mode)")
        image_window.after(2000, lambda: status_label.configure(text="Ready to use image tools"))
    screenshot_btn = tk.Button(image_window, text="📸 Take Screenshot", bg="#3498db", fg="white", font=("Arial", 12), command=take_screenshot)
    screenshot_btn.pack(pady=10)
    edit_btn = tk.Button(image_window, text="🎨 Edit Image", bg="#9b59b6", fg="white", font=("Arial", 12), command=edit_image)
    edit_btn.pack(pady=10)
    status_label = tk.Label(image_window, text="Ready to use image tools", font=("Arial", 12), fg="#b8b8d1", bg="#1a1a2e")
    status_label.pack(pady=20)

def create_gradient_background(canvas, width, height):
    for i in range(height):
        r = int(138 - (i * 30 / height))
        g = int(43 + (i * 80 / height))
        b = int(226 - (i * 50 / height))
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_rectangle(0, i, width, i+1, outline=color, fill=color)

root = tk.Tk()
root.title("AI Chat Editor")
root.configure(bg="#1a1a2e")
root.attributes('-fullscreen', True)
root.bind('<Escape>', exit_fullscreen)
root.bind('<F11>', toggle_fullscreen)
root.bind('<Configure>', on_window_resize)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

welcome_frame = tk.Frame(root, bg="#0f0f23")
welcome_frame.pack(fill="both", expand=True)
gradient_canvas = tk.Canvas(welcome_frame, highlightthickness=0)
gradient_canvas.pack(fill="both", expand=True)

def update_gradient():
    gradient_canvas.delete("all")
    canvas_width = gradient_canvas.winfo_width()
    canvas_height = gradient_canvas.winfo_height()
    if canvas_width > 1 and canvas_height > 1:
        create_gradient_background(gradient_canvas, canvas_width, canvas_height)
        import random
        for _ in range(20):
            x = random.randint(50, canvas_width-50)
            y = random.randint(50, canvas_height-50)
            size = random.randint(2, 6)
            gradient_canvas.create_oval(x, y, x+size, y+size, fill="white", outline="", stipple="gray25")
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        gradient_canvas.create_text(center_x, center_y - 40, text="Welcome back, Vedant!", font=("Helvetica", 48, "bold"), fill="white", anchor="center")
        gradient_canvas.create_text(center_x, center_y + 20, text="How can I help you today?", font=("Helvetica", 24), fill="#e0e0ff", anchor="center")

gradient_canvas.bind('<Configure>', lambda e: root.after(10, update_gradient))

def on_button_hover(event): get_started_btn.configure(bg="#6c5ce7", relief="raised")
def on_button_leave(event): get_started_btn.configure(bg="#a29bfe", relief="flat")

get_started_btn = tk.Button(gradient_canvas, text="Get Started ✨", font=("Helvetica", 18, "bold"), fg="white", bg="#a29bfe", activebackground="#6c5ce7", activeforeground="white", relief="flat", bd=0, padx=40, pady=15, cursor="hand2", command=show_chat_interface)

def position_button():
    canvas_width = gradient_canvas.winfo_width()
    canvas_height = gradient_canvas.winfo_height()
    if canvas_width > 1 and canvas_height > 1:
        get_started_btn.place(x=canvas_width//2, y=canvas_height//2 + 100, anchor="center")

gradient_canvas.bind('<Configure>', lambda e: root.after(10, lambda: (update_gradient(), position_button())))
get_started_btn.bind("<Enter>", on_button_hover)
get_started_btn.bind("<Leave>", on_button_leave)

main_frame = tk.Frame(root, bg="#0f0f23")

header_frame = tk.Frame(main_frame, bg="#1a1a2e", height=80)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)
header_title = tk.Label(header_frame, text="AI Chat Assistant", font=("Helvetica", 20, "bold"), fg="white", bg="#1a1a2e")
header_title.pack(expand=True)

chat_container = tk.Frame(main_frame, bg="#16213e", relief="flat", bd=0)
chat_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

chat_canvas = tk.Canvas(chat_container, bg="#16213e", highlightthickness=0)
chat_frame = tk.Frame(chat_canvas, bg="#16213e")
scrollbar = tk.Scrollbar(chat_container, orient="vertical", command=chat_canvas.yview, bg="#e0e0e0", troughcolor="#f5f5f5", width=12)
chat_canvas.configure(yscrollcommand=scrollbar.set)
chat_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))

input_container = tk.Frame(main_frame, bg="#1a1a2e", height=80)
input_container.pack(fill="x", side="bottom")
input_container.pack_propagate(False)
bottom_frame = tk.Frame(input_container, bg="#1a1a2e")
bottom_frame.pack(expand=True, fill="both", padx=20, pady=15)

three_dots_btn = tk.Button(bottom_frame, text="⋯", bg="#4a5568", fg="white", font=("Arial", 16, "bold"), relief="flat", bd=0, width=3, height=2, cursor="hand2", command=toggle_menu)
three_dots_btn.pack(side="left", padx=(0, 10))

menu_frame = tk.Frame(bottom_frame, bg="#2d3748", relief="solid", bd=1)

menu_options = [
    ("✍️ Text Editor", open_text_editor),
    ("🎤 Voice Input", voice_input),
    ("🖼️ Edit Image/Screenshot", image_editor)
]

for text, command in menu_options:
    btn = tk.Button(menu_frame, text=text, bg="#2d3748", fg="white", font=("Arial", 11), relief="flat", bd=0, anchor="w", padx=15, pady=8, cursor="hand2", command=command)
    btn.pack(fill="x")
    def on_menu_hover(event, button=btn): button.configure(bg="#4a5568")
    def on_menu_leave(event, button=btn): button.configure(bg="#2d3748")
    btn.bind("<Enter>", on_menu_hover)
    btn.bind("<Leave>", on_menu_leave)

input_frame = tk.Frame(bottom_frame, bg="#2d3748", relief="solid", bd=1)
input_frame.pack(side="left", fill="x", expand=True, ipady=8)

user_entry = tk.Entry(input_frame, font=("Arial", 16), relief="flat", bd=0, bg="#2d3748", fg="white", insertbackground="white")
user_entry.pack(fill="both", expand=True, padx=15)
user_entry.bind("<Return>", lambda event: send_message())

def close_menu_on_click(event):
    if menu_frame.winfo_viewable():
        menu_frame.place_forget()
user_entry.bind("<Button-1>", close_menu_on_click)

voice_btn = tk.Button(menu_frame, text="🎤 Voice", font=("Arial", 12), bg="#1abc9c", fg="white", command=voice_input)
voice_btn.pack(side=tk.LEFT, padx=5)

save_btn = tk.Button(menu_frame, text="💾 Save", font=("Arial", 12), bg="#3498db", fg="white", command=save_chat)
save_btn.pack(side=tk.LEFT, padx=5)

def on_send_hover(event): send_btn.configure(bg="#5a67d8")
def on_send_leave(event): send_btn.configure(bg="#667eea")

send_btn = tk.Button(bottom_frame, text="➤", bg="#667eea", fg="white", font=("Arial", 16, "bold"), relief="flat", bd=0, width=4, height=2, cursor="hand2", command=send_message)
send_btn.pack(side="right", padx=(10, 0))
send_btn.bind("<Enter>", on_send_hover)
send_btn.bind("<Leave>", on_send_leave)

root.mainloop()
