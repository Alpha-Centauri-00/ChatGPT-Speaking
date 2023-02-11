import os
import pygame
import requests
import threading
import tkinter as tk
from gtts import gTTS



def generate_speech(text):
    selected_language = language.get()
    
    if selected_language == "English":
        langu = "en"
    elif selected_language == "Germany":
        langu = "de"
    
    if os.path.exists("sample_response.mp3"):
        os.remove("sample_response.mp3")
    tts = gTTS(text=text, lang=langu)
    tts.save("sample_response.mp3")



def get_chatgpt_res(prompt):

    """
    To sign up for an API key, follow these steps:

        1. Go to the OpenAI API website: https://openai.com/
        2. Click on the "Sign Up" button in the top right corner of the page.
        3. Fill out the registration form with your personal information, such as your name, email address, and password.
        4. Agree to the terms of service.
        5. Verify your email address by clicking on the confirmation link sent to your email.
        6. Log in to your OpenAI API account.
        7. Generate a new API key by clicking on the "Create Key" button.
        8. Name your API key and give it a description.
        9. Once you have created the API key, you can copy it and use it in your applications to access OpenAI's GPT-3 API.

    With your API key, you can start using OpenAI's GPT-3 API in your own applications and projects.
    """
    api_key = "YOUR_API_IN_HERE!"
    model = "text-davinci-003"
    endpoint = f"https://api.openai.com/v1/engines/{model}/completions"

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    data = {
    "prompt": prompt,
    "max_tokens": 128,
    "temperature": 0.5,
    }
    resp = requests.post(endpoint, headers=headers, json=data)


    if resp.status_code == 200:
        # Extract the response text from the API response
        response_text = resp.json()["choices"][0]["text"]
        #print(response_text)
        return response_text
    else:
        # If the API request was not successful, print the error message
        print("Request failed with status code:", resp.status_code)


def add_text_delete_old(text):
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, text)


def on_submit():
    
    Asking = text_field.get()
    responding = get_chatgpt_res(Asking)
    res = str.strip(responding)
    add_text_delete_old(res)
    
    generate_speech(responding)
    
    # Start a new thread to play the sound
    t = threading.Thread(target=play_answer)
    t.start()


def play_answer():
    pygame.mixer.init() # initialise the pygame

    pygame.mixer.music.load("sample_response.mp3")
    pygame.mixer.music.play(loops=0)
    
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
    pygame.quit()


def stop_answer():
    pygame.mixer.init()
    pygame.mixer.music.stop()
    


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ask ChatGPT (text-davinci-003)")
    root.geometry("1000x700")
    root.iconbitmap("logo.ico")

    text_field = tk.Entry(root, width=70)
    text_field.grid(row=0, column=0, columnspan=2, padx=5, pady=20, sticky="nsew")

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    icon = tk.PhotoImage(file="speaker.png")
    submit_button["compound"] = tk.RIGHT
    submit_button["image"] = icon
    submit_button.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

    stop_button = tk.Button(root, text="Stop", command=stop_answer)
    icon2 = tk.PhotoImage(file="icons8-stop-64.png")
    stop_button["compound"] = tk.RIGHT
    stop_button["image"] = icon2
    stop_button.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

    text_widget = tk.Text(root)
    text_widget.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=10)

    # create dropdown list
    language = tk.StringVar(root)
    language.set("English")
    language_dropdown = tk.OptionMenu(root, language, "English", "Germany")
    language_dropdown.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")
    
    root.mainloop()