import os
import tkinter as tk
from tkinter import messagebox
import time
import threading
from PIL import Image, ImageTk, ImageSequence
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# -------------------------------
# Initialize Ollama via LangChain
# -------------------------------
model_name = "llama3"
llama_chat = ChatOllama(model=model_name)  

# -------------------------------
# Typing animation
# -------------------------------
def type_text(widget, text, delay=0.03):
    widget.config(state='normal')
    for char in text:
        widget.insert(tk.END, char)
        widget.update()
        time.sleep(delay)
    widget.insert(tk.END, "\n\n")
    widget.config(state='disabled')
    widget.yview(tk.END)

# -------------------------------
# Send message
# -------------------------------
def send_message(event=None):
    user_input = user_entry.get()
    if not user_input.strip():
        return

    chat_box.config(state='normal')
    chat_box.insert(tk.END, f"You: {user_input}\n", "user")
    chat_box.config(state='disabled')
    chat_box.yview(tk.END)
    user_entry.delete(0, tk.END)

    threading.Thread(target=get_ai_response, args=(user_input,)).start()

# -------------------------------
# Get AI response with flirty tone
# -------------------------------
def get_ai_response(user_input):
    prompt = (
        f"Chat with Samrat. Start every response with a playful pick-up line, "
        "keep the tone cute, flirty, and loving. "
        "Never say you are AI. Make every reply fun and sweet."
    )

    try:
        response = llama_chat.invoke([HumanMessage(content=f"{prompt}\nUser: {user_input}")])
        ai_text = response.content
    except Exception as e:
        ai_text = f"Error: {str(e)}"

    root.after(0, lambda: type_text(chat_box, f"Prashamsa 💖: {ai_text}"))

# -------------------------------
# Tkinter GUI
# -------------------------------
root = tk.Tk()
root.title("💌 Chat with Prashamsa 💌")
root.state('zoomed')
root.config(bg="#ffe6f2")

# -------------------------------
# Animated GIF
# -------------------------------
def load_gif(label, filepath):
    img = Image.open(filepath)
    frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA')) for frame in ImageSequence.Iterator(img)]
    def animate(counter=0):
        label.config(image=frames[counter])
        root.after(100, lambda: animate((counter + 1) % len(frames)))
    animate()

avatar_label = tk.Label(root, bg="#ffe6f2")
avatar_label.pack(side=tk.RIGHT, padx=10)
load_gif(avatar_label, "prashamsa.gif")  # Replace with your GIF path

# -------------------------------
# Chat box
# -------------------------------
chat_box = tk.Text(root, wrap=tk.WORD, bg="#fff0f5", fg="#d6006c",
                   font=("Helvetica", 14), state='disabled', padx=10, pady=10)
chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

chat_box.tag_config("user", foreground="#ff3399", justify='right')
chat_box.tag_config("ai", foreground="#b30059", justify='left')

# -------------------------------
# Input frame
# -------------------------------
input_frame = tk.Frame(root, bg="#ffe6f2")
input_frame.pack(fill=tk.X, padx=10, pady=10)

user_entry = tk.Entry(input_frame, font=("Helvetica", 14))
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
user_entry.focus()
user_entry.bind("<Return>", send_message)

send_button = tk.Button(input_frame, text="Send 💌", command=send_message,
                        bg="#ff66b3", fg="white", font=("Helvetica", 12, "bold"))
send_button.pack(side=tk.LEFT)

# -------------------------------
# Voice & Video Call buttons
# -------------------------------
def voice_call():
    messagebox.showinfo("Voice Call", "📞 Starting voice call with Prashamsa...")

def video_call():
    messagebox.showinfo("Video Call", "🎥 Starting video call with Prashamsa...")

call_frame = tk.Frame(root, bg="#ffe6f2")
call_frame.pack(fill=tk.X, padx=10, pady=5)

voice_button = tk.Button(call_frame, text="Voice Call 📞", command=voice_call,
                         bg="#ff3399", fg="white", font=("Helvetica", 12, "bold"))
voice_button.pack(side=tk.LEFT, padx=5)

video_button = tk.Button(call_frame, text="Video Call 🎥", command=video_call,
                         bg="#b30059", fg="white", font=("Helvetica", 12, "bold"))
video_button.pack(side=tk.LEFT, padx=5)

# -------------------------------
# Greet Samrat on startup
# -------------------------------
def greet_user():
    greeting = "Hey Samrat! 💖 Ready for some fun chat? 😘"
    type_text(chat_box, f"Prashamsa 💖: {greeting}")

root.after(500, greet_user)

# -------------------------------
# Start GUI
# -------------------------------
root.mainloop()