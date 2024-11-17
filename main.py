import os
import tkinter as tk
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
            model="gpt-4o",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("An error occurred:", e)
        return f"Error processing your request: {e}"

def add_text_delete_old(text):
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, text)

def on_submit():
    asking = text_field.get()
    responding = get_chatgpt_res(asking)
    add_text_delete_old(responding)
    


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ask ChatGPT")
    root.geometry("1000x700")
    
    # Comment out if you don't have the icon file
    root.iconbitmap("logo.ico")

    text_field = tk.Entry(root, width=70)
    text_field.grid(row=0, column=0, columnspan=3, padx=5, pady=20, sticky="nsew")

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button["compound"] = tk.RIGHT
    submit_button.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

    
    
    text_widget = tk.Text(root)
    text_widget.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

    root.mainloop()
