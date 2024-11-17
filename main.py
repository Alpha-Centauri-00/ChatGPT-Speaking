import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from openai import OpenAI

def get_chatgpt_res(prompt):
    try:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"), 
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("An error occurred:", e)
        return f"Error processing your request: {e}"

def add_text_delete_old(text):
    text_widget.config(state=tk.NORMAL)  # Enable editing
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, text)
    text_widget.config(state=tk.DISABLED)  # Disable editing

def on_submit():
    asking = text_field.get()
    if asking.strip() == '':
        return  # Do nothing if the input is empty
    submit_button.config(state=tk.DISABLED)
    add_text_delete_old("Loading...")
    root.after(100, fetch_response, asking)

def fetch_response(asking):
    responding = get_chatgpt_res(asking)
    add_text_delete_old(responding)
    submit_button.config(state=tk.NORMAL)
    text_field.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ask ChatGPT")
    root.geometry("800x600")
    root.minsize(600, 400)
    
    # Set the style
    style = ttk.Style(root)
    style.theme_use('clam')  # Options: 'clam', 'alt', 'default', 'classic'

    # Customize font
    default_font = ('Arial', 12)
    style.configure('TLabel', font=default_font)
    style.configure('TEntry', font=default_font)
    style.configure('TButton', font=default_font)

    # Set up the main frame
    main_frame = ttk.Frame(root, padding="10 10 10 10")
    main_frame.grid(row=0, column=0, sticky="NSEW")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Input label and entry
    input_frame = ttk.Frame(main_frame)
    input_frame.grid(row=0, column=0, columnspan=2, sticky="EW")
    input_frame.columnconfigure(1, weight=1)
    
    input_label = ttk.Label(input_frame, text="Your Question:")
    input_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)
    
    text_field = ttk.Entry(input_frame)
    text_field.grid(row=0, column=1, sticky="EW", padx=5, pady=5)
    text_field.focus()
    
    # Submit button
    submit_button = ttk.Button(main_frame, text="Submit", command=on_submit)
    submit_button.grid(row=0, column=2, sticky="E", padx=5, pady=5)
    
    # Response text widget with scrollbar
    response_frame = ttk.Frame(main_frame)
    response_frame.grid(row=1, column=0, columnspan=3, sticky="NSEW", pady=10)
    response_frame.rowconfigure(0, weight=1)
    response_frame.columnconfigure(0, weight=1)
    
    text_widget = tk.Text(response_frame, wrap="word", state=tk.DISABLED, font=default_font, background="#2e2e2e",foreground="white")
    text_widget.grid(row=0, column=0, sticky="NSEW")
    
    scrollbar = ttk.Scrollbar(response_frame, orient="vertical", command=text_widget.yview)
    scrollbar.grid(row=0, column=1, sticky="NS")
    text_widget['yscrollcommand'] = scrollbar.set

    # Configure weights to make widgets resize with window
    main_frame.rowconfigure(1, weight=1)
    
    # Optional: Add menu bar
    def about():
        messagebox.showinfo("About", "ChatGPT GUI Application\nDeveloped with Tkinter and OpenAI API.")

    menubar = tk.Menu(root)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)

    root.mainloop()
