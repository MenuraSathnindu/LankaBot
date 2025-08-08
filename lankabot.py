import tkinter as tk
from tkinter import scrolledtext
import random
import re

# -------------------------------
# LankaBot's knowledge base
# -------------------------------
knowledge_base = {
    # Sinhala keywords
    'හෙලෝ': ['ආයුබෝවන්!', 'ආයුබෝවන්. ඔබට කෙසේද?', 'හෙලෝ, ඔබට උදව් කළ හැකිද?'],
    'කොහොමද': ['මම හොඳින්. ඔබට කෙසේද?', 'මම හොඳින් ඉන්නවා. ස්තූතියි!'],
    'නම්': ['මම කෘතිම බුද්ධිමය වැඩසටහනක්.', 'මට නමක් නැත.', 'මගේ නම ලංකාබොට්.'],
    'කවුද': ['මම ඔබගේ සහායකයා වෙමි.', 'මම කතා කිරීමට සූදානම්.', 'මම ලංකාබොට්, ඔබට උදව් කිරීමට.'],
    'උදව්': ['මම ඔබට උදව් කිරීමට සූදානම්.', 'ඔබට උදව් අවශ්‍යද?', 'ඔව්, මට උදව් කළ හැකිය.'],
    'ස්තුතියි': ['සතුටුයි!', 'කමක් නැහැ.', 'කිසි ප්‍රශ්නයක් නැහැ.'],
    'ආයුබෝවන්': ['ආයුබෝවන්!', 'නැවත හමුවෙමු!'],

    # English keywords
    'hello': ['Hi there!', 'Hello, how can I help you?', 'Greetings!'],
    'how are you': ["I'm doing well, thank you! How about you?", "I'm fine, thanks for asking!"],
    'what is your name': ["I am LankaBot, your AI assistant.", "You can call me LankaBot."],
    'who are you': ["I am an AI assistant designed to help you.", "I'm a chatbot named LankaBot."],
    'help': ["I'm here to assist you.", "How can I help you today?", "Yes, I can help you."],
    'thank you': ["You're welcome!", "No problem!", "Glad to help!"],
    'bye': ["Goodbye!", "See you later!", "Farewell!"],

    # Singlish or Mixed
    'machan': ['මචන්, කොහොමද?', 'මචන්, මොකද වෙන්නේ?', "Hey machan, what's up?"],
    'aiyo': ['අයියෝ, මොකද වුණේ?', 'අයියෝ, කමක් නැහැ.', 'Aiyo, what happened?', 'Aiyo, never mind.'],
    'can': ['ඔව්, පුළුවන්.', 'ඇත්තෙන්ම පුළුවන්.', 'Yes, I can.', 'Sure, can.'],
    'cannot': ['බැහැ.', 'නැහැ, බැහැ.', 'No, cannot.', 'Cannot lah.'],
    'no problem': ['කිසි ප්‍රශ්නයක් නැහැ.', 'කමක් නැහැ.', 'No problem, lah.', "It's fine."],
    'what to do': ['මොනවද කරන්න තියෙන්නේ?', 'අපි මොනවද කරන්නේ?', 'What to do now?', 'What should we do?'],
    'okay': ['හරි.', 'හොඳයි.', 'Okay.', 'Alright.'],
    'wah': ['වාව්!', 'හරිම පුදුමයි!', 'Wah, amazing!', 'Wow!'],
    'dunno': ['දන්නේ නැහැ.', 'මට විශ්වාස නැහැ.', "I don't know.", 'Dunno lah.'],
    'where got': ['කොහෙද තියෙන්නේ?', 'නැහැ, එහෙම නැහැ.', 'Where got?', 'No, not really.'],
    'come on': ['එන්න!', 'ඉක්මන් කරන්න!', 'Come on!', "Let's go!"]
}

# -------------------------------
# Core Chatbot Logic
# -------------------------------
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()

def get_response(user_input):
    cleaned_input = clean_text(user_input)
    words = cleaned_input.split()

    for keyword in knowledge_base:
        if ' ' in keyword and keyword in cleaned_input:
            return random.choice(knowledge_base[keyword])
    for word in words:
        for keyword in knowledge_base:
            if ' ' not in keyword and word.startswith(keyword):
                return random.choice(knowledge_base[keyword])
    return "මට එය තේරුම් ගත නොහැක. ඔබට වෙනත් දෙයක් ඇසිය හැකිද? (I cannot understand that. Can you ask something else?)"

# -------------------------------
# GUI using tkinter
# -------------------------------
def send_message():
    user_msg = user_input.get()
    if user_msg.strip() == "":
        return
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {user_msg}\n")
    response = get_response(user_msg)
    chat_area.insert(tk.END, f"LankaBot: {response}\n\n")
    chat_area.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)
    chat_area.see(tk.END)

# Create GUI window
window = tk.Tk()
window.title("LankaBot 🇱🇰 - Sinhala & English Chatbot")
window.geometry("500x500")
window.resizable(False, False)

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 11))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_input = tk.Entry(window, font=("Arial", 12))
user_input.pack(padx=10, pady=(0, 10), fill=tk.X)
user_input.bind("<Return>", lambda event: send_message())

send_button = tk.Button(window, text="Send", command=send_message, font=("Arial", 11), bg="#4CAF50", fg="white")
send_button.pack(pady=(0, 10))

# Run the GUI
window.mainloop()