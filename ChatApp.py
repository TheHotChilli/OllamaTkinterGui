import tkinter as tk
from tkinter import scrolledtext, messagebox, END, ttk
import tkinter.font as tkFont
import asyncio
from asyncio import Event
from Ollama import Ollama


class ChatApp:
    def __init__(self):
        # model instance
        self.ollama = Ollama(model="llama3")

        # Main GUI window
        self.root = tk.Tk()
        self.root.title("ChatApp for Ollama")
        self.root.state('zoomed')
        self.root.geometry("800x600")

        # Set font and background color
        self.custom_font = tkFont.Font(family="Helvetica", size=12)
        self.root.option_add("*Font", self.custom_font) # set font of all widgets in root
        self.root.configure(bg='#2E2E2E')  # Set a dark background

        # Chat history
        self.chat_history = scrolledtext.ScrolledText(self.root, width=60, height=20, wrap=tk.WORD, 
                                                      bg='#1E1E1E', fg='#D3D3D3', insertbackground='white')
        self.chat_history.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # User input
        self.input_field = scrolledtext.ScrolledText(self.root, width=40, height=4, wrap=tk.WORD, 
                                                     bg='#1E1E1E', fg='#D3D3D3', insertbackground='white')
        self.input_field.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.input_field.bind("<KeyPress-Return>", self.enter_pressed_callback)   

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, bg='#6D8764', fg='white')
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Copy button
        self.copy_button = tk.Button(self.root, text="Copy answer", command=self.copy_to_clipboard, bg='#6D8764', fg='white')
        self.copy_button.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Config button
        self.config_button = tk.Button(self.root, text="Config", command=self.open_config_window, bg='#6D8764', fg='white')
        self.config_button.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")
        
        # Grid configuration to make widgets resize with the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=0)
        self.root.grid_columnconfigure(3, weight=0)

    def send_message(self):
        user_input = self.input_field.get("1.0", END).strip()
        if not user_input.strip():
            messagebox.showwarning("Warning", "Input field cannot be empty.")
            return
        self.chat_history.insert(tk.END, f"{user_input}\n", "user_color")
        self.chat_history.tag_config("user_color", foreground="white")
        response = self.ollama.chat(user_input)
        # response = self.client.generate(model="llama3", prompt=user_input)
        # response = "Test Response"  
        self.chat_history.insert(tk.END, f"{response}\n\n", "assistant_color")
        self.chat_history.tag_config("assistant_color", foreground="#87CEEB")
        self.input_field.delete("1.0", END)
        self.last_response = response  # Store the last response

    def enter_pressed_callback(self, event):
        if event.state == 0:  # only send_message if ENTER is not modified by other keys (e.g ALT+ENTER)
            self.send_message()
            return 'break'  # prevent tkinter to add a newline due to enter 

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.last_response)
        # messagebox.showinfo("Info", "Last response copied to clipboard.")

    def open_config_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Config")

        available_models = self.ollama.list_models()

        tk.Label(config_window, text="Selected Model:").grid(row=0, column=0, padx=10, pady=10)
        
        self.model_var = tk.StringVar(value=self.ollama.model)
        model_dropdown = ttk.Combobox(config_window, textvariable=self.model_var, values=available_models)
        model_dropdown.grid(row=0, column=1, padx=10, pady=10)

        apply_button = tk.Button(config_window, text="Apply", command=self.apply_model_selection)
        apply_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def apply_model_selection(self):
        selected_model = self.model_var.get()
        self.ollama.model = selected_model
        messagebox.showinfo("Info", f"Model changed to {selected_model}")

    def run(self):
        self.root.mainloop()


#----------------------------------------------


class AsyncChatApp:
    def __init__(self):
        # model instance
        self.ollama = Ollama(model="llama3")

        # Main GUI window
        self.root = tk.Tk()
        self.root.title("ChatApp for Ollama")
        self.root.state('zoomed')
        self.root.geometry("800x600")

        # Set font and background color
        self.custom_font = tkFont.Font(family="Helvetica", size=12)
        self.root.option_add("*Font", self.custom_font)  # set font of all widgets in root
        self.root.configure(bg='#2E2E2E')  # Set a dark background

        # Chat history
        self.chat_history = scrolledtext.ScrolledText(self.root, width=60, height=20, wrap=tk.WORD,
                                                      bg='#1E1E1E', fg='#D3D3D3', insertbackground='white')
        self.chat_history.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # User input
        self.input_field = scrolledtext.ScrolledText(self.root, width=40, height=4, wrap=tk.WORD,
                                                     bg='#1E1E1E', fg='#D3D3D3', insertbackground='white')
        self.input_field.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.input_field.bind("<KeyPress-Return>", self.enter_pressed_callback)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, bg='#6D8764', fg='white')
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Copy button
        self.copy_button = tk.Button(self.root, text="Copy answer", command=self.copy_to_clipboard, bg='#6D8764', fg='white')
        self.copy_button.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Grid configuration to make widgets resize with the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=0)

        self.last_response = ""
        self.stop_event = Event()

        # Bind ESC to stop streaming
        self.root.bind("<Escape>", self.stop_streaming)

        # Periodically call the asyncio event loop
        self.root.after(100, self.run_asyncio_loop)

    def send_message(self):
        user_input = self.input_field.get("1.0", tk.END).strip()
        if not user_input.strip():
            messagebox.showwarning("Warning", "Input field cannot be empty.")
            return

        self.chat_history.insert(tk.END, f"{user_input}\n", "user_color")
        self.chat_history.tag_config("user_color", foreground="white")
        self.input_field.delete("1.0", tk.END)

        self.stop_event.clear()
        asyncio.ensure_future(self.handle_response(user_input))
        self.chat_history.insert(tk.END, "\n", "assistant_color")
        self.chat_history.tag_config("assistant_color", foreground="#87CEEB")

    async def handle_response(self, user_input):
        self.last_response = ""
        async for response in self.ollama.achat(prompt=user_input, stream=True):
            if self.stop_event.is_set():
                break
            self.chat_history.insert(tk.END, f"{response}", "assistant_color")
            self.chat_history.tag_config("assistant_color", foreground="#87CEEB")
            self.last_response += response

    def enter_pressed_callback(self, event):
        if event.state == 0:  # only send_message if ENTER is not modified by other keys (e.g ALT+ENTER)
            self.send_message()
            return 'break'  # prevent tkinter to add a newline due to enter

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.last_response)
        # messagebox.showinfo("Info", "Last response copied to clipboard.")

    def stop_streaming(self, event):
        self.stop_event.set()

    def run_asyncio_loop(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.sleep(0))
        except RuntimeError:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = new_loop

        self.root.after(100, self.run_asyncio_loop)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ChatApp()
    app.run()
    # app = AsyncChatApp()
    # asyncio.run(app.run())