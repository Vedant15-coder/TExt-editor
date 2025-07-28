import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import google.generativeai as genai
import speech_recognition as sr
import math
import threading
import time

# ---- CONFIGURE GEMINI ----
genai.configure(api_key="AIzaSyB44yyxyf8atB3Tefp7C2eMczhokKPVGc8")
model = genai.GenerativeModel("gemini-1.5-flash")

class AnimatedTextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Text Editor")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0f0f23")
        
        # Animation variables
        self.animation_step = 0
        self.floating_elements = []
        self.colors = {
            'primary': '#6366f1',
            'secondary': '#8b5cf6',
            'accent': '#06b6d4',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'bg_dark': '#0f0f23',
            'bg_light': '#1e1e3f',
            'text_light': '#f8fafc',
            'text_muted': '#94a3b8',
            'chat_user': '#3b82f6',
            'chat_ai': '#10b981'
        }
        
        self.setup_welcome_screen()
        
    def setup_welcome_screen(self):
        # Main welcome frame with gradient effect
        self.welcome_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.welcome_frame.place(relwidth=1, relheight=1)
        
        # Create animated background elements
        self.canvas = tk.Canvas(
            self.welcome_frame, 
            bg=self.colors['bg_dark'], 
            highlightthickness=0
        )
        self.canvas.place(relwidth=1, relheight=1)
        
        # Create floating geometric shapes
        self.create_floating_elements()
        
        # Welcome text with gradient effect
        self.welcome_label = tk.Label(
            self.welcome_frame,
            text="Welcome back Vedant! ✨",
            font=("Helvetica", 32, "bold"),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light']
        )
        self.welcome_label.place(relx=0.5, rely=0.3, anchor="center")
        
        self.subtitle_label = tk.Label(
            self.welcome_frame,
            text="Your AI-powered writing companion awaits",
            font=("Helvetica", 16),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_muted']
        )
        self.subtitle_label.place(relx=0.5, rely=0.38, anchor="center")
        
        # Animated get started button
        self.get_started_btn = tk.Button(
            self.welcome_frame,
            text="🚀 Get Started",
            font=("Arial", 18, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['text_light'],
            padx=40,
            pady=15,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.launch_chat_interface
        )
        
        # Start animations
        self.animate_welcome_elements()
        self.animate_floating_shapes()
        
    def create_floating_elements(self):
        # Create various floating shapes
        shapes = [
            {'type': 'circle', 'x': 100, 'y': 150, 'size': 30, 'color': self.colors['primary']},
            {'type': 'circle', 'x': 200, 'y': 400, 'size': 20, 'color': self.colors['secondary']},
            {'type': 'circle', 'x': 900, 'y': 200, 'size': 25, 'color': self.colors['accent']},
            {'type': 'rect', 'x': 800, 'y': 500, 'size': 35, 'color': self.colors['success']},
            {'type': 'rect', 'x': 150, 'y': 600, 'size': 28, 'color': self.colors['warning']},
        ]
        
        for shape in shapes:
            if shape['type'] == 'circle':
                element = self.canvas.create_oval(
                    shape['x'], shape['y'], 
                    shape['x'] + shape['size'], shape['y'] + shape['size'],
                    fill=shape['color'], outline="", width=0
                )
            else:
                element = self.canvas.create_rectangle(
                    shape['x'], shape['y'], 
                    shape['x'] + shape['size'], shape['y'] + shape['size'],
                    fill=shape['color'], outline="", width=0
                )
            
            self.floating_elements.append({
                'element': element,
                'base_x': shape['x'],
                'base_y': shape['y'],
                'offset': len(self.floating_elements) * 0.5
            })
    
    def animate_floating_shapes(self):
        for i, shape in enumerate(self.floating_elements):
            # Create floating motion
            offset_x = math.sin(self.animation_step * 0.02 + shape['offset']) * 20
            offset_y = math.cos(self.animation_step * 0.015 + shape['offset']) * 15
            
            self.canvas.coords(
                shape['element'],
                shape['base_x'] + offset_x,
                shape['base_y'] + offset_y,
                shape['base_x'] + offset_x + 30,
                shape['base_y'] + offset_y + 30
            )
        
        self.animation_step += 1
        self.root.after(50, self.animate_floating_shapes)
    
    def animate_welcome_elements(self, step=0):
        if step <= 30:
            # Animate welcome text
            scale = 0.5 + (step / 30) * 0.5
            alpha = step / 30
            
            # Animate button entrance
            if step > 15:
                btn_y = 0.6 - (30 - step) * 0.02
                self.get_started_btn.place(relx=0.5, rely=btn_y, anchor="center")
                
                # Add glow effect to button
                if step % 6 < 3:
                    self.get_started_btn.configure(bg=self.colors['secondary'])
                else:
                    self.get_started_btn.configure(bg=self.colors['primary'])
            
            self.root.after(100, lambda: self.animate_welcome_elements(step + 1))
        else:
            # Final button position and color
            self.get_started_btn.place(relx=0.5, rely=0.55, anchor="center")
            self.get_started_btn.configure(bg=self.colors['primary'])
    
    def launch_chat_interface(self):
        # Fade out welcome screen
        self.fade_out_welcome()
        
    def fade_out_welcome(self, alpha=1.0):
        if alpha > 0:
            # Fade effect simulation
            alpha -= 0.1
            self.root.after(50, lambda: self.fade_out_welcome(alpha))
        else:
            self.welcome_frame.destroy()
            self.setup_chat_interface()
    
    def setup_chat_interface(self):
        # Main chat container
        self.chat_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.chat_frame.place(relwidth=1, relheight=1)
        
        # Header
        self.header = tk.Frame(self.chat_frame, bg=self.colors['bg_light'], height=70)
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)
        
        self.header_label = tk.Label(
            self.header,
            text="✨ AI Writing Assistant",
            font=("Helvetica", 20, "bold"),
            bg=self.colors['bg_light'],
            fg=self.colors['text_light']
        )
        self.header_label.pack(pady=20)
        
        # Chat display area
        self.chat_container = tk.Frame(self.chat_frame, bg=self.colors['bg_dark'])
        self.chat_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Scrollable chat area
        self.chat_canvas = tk.Canvas(self.chat_container, bg=self.colors['bg_dark'], highlightthickness=0)
        self.chat_scrollbar = tk.Scrollbar(self.chat_container, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollable_frame = tk.Frame(self.chat_canvas, bg=self.colors['bg_dark'])
        
        self.chat_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )
        
        self.chat_canvas.create_window((0, 0), window=self.chat_scrollable_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.chat_scrollbar.pack(side="right", fill="y")
        
        # Input area
        self.input_frame = tk.Frame(self.chat_frame, bg=self.colors['bg_light'], height=100)
        self.input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.input_frame.pack_propagate(False)
        
        # Text input
        self.input_text = tk.Text(
            self.input_frame,
            height=3,
            font=("Arial", 12),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light'],
            insertbackground=self.colors['primary'],
            relief=tk.FLAT,
            padx=15,
            pady=10
        )
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        
        # Button container
        self.button_container = tk.Frame(self.input_frame, bg=self.colors['bg_light'])
        self.button_container.pack(side=tk.RIGHT, padx=(5, 10), pady=10)
        
        # Action buttons with modern design
        buttons = [
            ("💬 Send", self.send_message, self.colors['primary']),
            ("✨ Generate", self.generate_text, self.colors['secondary']),
            ("📝 Summarize", self.summarize_text, self.colors['accent']),
            ("✅ Fix Grammar", self.correct_grammar, self.colors['success']),
            ("🎤 Voice", self.voice_input, self.colors['warning']),
            ("💾 Save", self.save_file, self.colors['error'])
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                self.button_container,
                text=text,
                font=("Arial", 10, "bold"),
                bg=color,
                fg=self.colors['text_light'],
                relief=tk.FLAT,
                padx=15,
                pady=8,
                cursor="hand2",
                command=command
            )
            btn.pack(pady=2, fill=tk.X)
            
            # Add hover effects
            self.add_button_hover_effect(btn, color)
        
        # Bind Enter key to send message
        self.input_text.bind("<Return>", lambda e: self.send_message())
        
        # Add welcome message
        self.add_ai_message("Hello! I'm your AI writing assistant. How can I help you today? 🤖✨")
    
    def add_button_hover_effect(self, button, original_color):
        def on_enter(e):
            button.configure(bg=self.lighten_color(original_color))
        
        def on_leave(e):
            button.configure(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def lighten_color(self, color):
        # Simple color lightening (this is a basic implementation)
        color_map = {
            self.colors['primary']: '#7c3aed',
            self.colors['secondary']: '#a855f7',
            self.colors['accent']: '#0891b2',
            self.colors['success']: '#059669',
            self.colors['warning']: '#d97706',
            self.colors['error']: '#dc2626'
        }
        return color_map.get(color, color)
    
    def add_user_message(self, message):
        message_frame = tk.Frame(self.chat_scrollable_frame, bg=self.colors['bg_dark'])
        message_frame.pack(fill=tk.X, pady=(10, 5), padx=20)
        
        # User message (right side)
        user_bubble = tk.Frame(message_frame, bg=self.colors['chat_user'])
        user_bubble.pack(side=tk.RIGHT, padx=(100, 0))
        
        user_label = tk.Label(
            user_bubble,
            text=message,
            font=("Arial", 11),
            bg=self.colors['chat_user'],
            fg=self.colors['text_light'],
            wraplength=400,
            justify=tk.LEFT,
            padx=15,
            pady=10
        )
        user_label.pack()
        
        # Animate message entrance
        self.animate_message_entrance(user_bubble, "right")
        self.scroll_to_bottom()
    
    def add_ai_message(self, message):
        message_frame = tk.Frame(self.chat_scrollable_frame, bg=self.colors['bg_dark'])
        message_frame.pack(fill=tk.X, pady=(5, 10), padx=20)
        
        # AI message (left side)
        ai_bubble = tk.Frame(message_frame, bg=self.colors['chat_ai'])
        ai_bubble.pack(side=tk.LEFT, padx=(0, 100))
        
        ai_label = tk.Label(
            ai_bubble,
            text=message,
            font=("Arial", 11),
            bg=self.colors['chat_ai'],
            fg=self.colors['text_light'],
            wraplength=400,
            justify=tk.LEFT,
            padx=15,
            pady=10
        )
        ai_label.pack()
        
        # Animate message entrance
        self.animate_message_entrance(ai_bubble, "left")
        self.scroll_to_bottom()
    
    def animate_message_entrance(self, widget, direction):
        # Simple slide-in animation
        original_x = widget.winfo_x()
        start_x = -200 if direction == "left" else 200
        
        def animate_step(current_x, target_x, step=0):
            if step < 10:
                new_x = current_x + (target_x - current_x) * 0.3
                widget.place(x=new_x)
                self.root.after(20, lambda: animate_step(new_x, target_x, step + 1))
            else:
                widget.place_forget()
                widget.pack(side=tk.LEFT if direction == "left" else tk.RIGHT, 
                           padx=(0, 100) if direction == "left" else (100, 0))
        
        # Start animation
        widget.pack_forget()
        widget.place(x=start_x)
        animate_step(start_x, original_x)
    
    def scroll_to_bottom(self):
        self.root.after(100, lambda: self.chat_canvas.yview_moveto(1.0))
    
    def send_message(self):
        message = self.input_text.get("1.0", tk.END).strip()
        if message:
            self.add_user_message(message)
            self.input_text.delete("1.0", tk.END)
            
            # Get AI response
            threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()
    
    def get_ai_response(self, message):
        try:
            response = model.generate_content(message)
            self.root.after(0, lambda: self.add_ai_message(response.text))
        except Exception as e:
            self.root.after(0, lambda: self.add_ai_message(f"Sorry, I encountered an error: {str(e)}"))
    
    def generate_text(self):
        message = self.input_text.get("1.0", tk.END).strip()
        if message:
            self.add_user_message(f"Generate: {message}")
            self.input_text.delete("1.0", tk.END)
            threading.Thread(target=self.get_ai_response, args=(f"Generate creative content about: {message}",), daemon=True).start()
    
    def summarize_text(self):
        message = self.input_text.get("1.0", tk.END).strip()
        if message:
            self.add_user_message(f"Summarize: {message}")
            self.input_text.delete("1.0", tk.END)
            threading.Thread(target=self.get_ai_response, args=(f"Summarize this text: {message}",), daemon=True).start()
    
    def correct_grammar(self):
        message = self.input_text.get("1.0", tk.END).strip()
        if message:
            self.add_user_message(f"Fix Grammar: {message}")
            self.input_text.delete("1.0", tk.END)
            threading.Thread(target=self.get_ai_response, args=(f"Correct the grammar of: {message}",), daemon=True).start()
    
    def voice_input(self):
        def record_voice():
            try:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    self.root.after(0, lambda: self.add_ai_message("🎤 Listening... Please speak now!"))
                    audio = recognizer.listen(source, timeout=5)
                
                text = recognizer.recognize_google(audio)
                self.root.after(0, lambda: self.input_text.insert(tk.END, text))
                self.root.after(0, lambda: self.add_ai_message(f"Voice input received: {text}"))
            except sr.UnknownValueError:
                self.root.after(0, lambda: self.add_ai_message("Sorry, I couldn't understand the audio."))
            except sr.RequestError as e:
                self.root.after(0, lambda: self.add_ai_message(f"Speech recognition error: {str(e)}"))
            except Exception as e:
                self.root.after(0, lambda: self.add_ai_message(f"Voice input error: {str(e)}"))
        
        threading.Thread(target=record_voice, daemon=True).start()
    
    def save_file(self):
        # Collect all messages for saving
        messages = []
        for widget in self.chat_scrollable_frame.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Frame):
                    for label in child.winfo_children():
                        if isinstance(label, tk.Label):
                            messages.append(label.cget("text"))
        
        if messages:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if filepath:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(messages))
                self.add_ai_message("💾 Chat saved successfully!")
    
    def run(self):
        self.root.mainloop()

# Create and run the application
if __name__ == "__main__":
    app = AnimatedTextEditor()
    app.run()
