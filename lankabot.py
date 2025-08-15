import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext
import random, re, os, pickle, difflib, time
from dataclasses import dataclass, field
from typing import List, Dict

# ML deps
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -------------------------------
# Rule-based knowledge base (kept)
# -------------------------------
knowledge_base = {
    'හෙලෝ': ['ආයුබෝවන්!', 'ආයුබෝවන්. ඔබට කෙසේද?', 'හෙලෝ, ඔබට උදව් කළ හැකිද?'],
    'කොහොමද': ['මම හොඳින්. ඔබට කෙසේද?', 'මම හොඳින් ඉන්නවා. ස්තූතියි!'],
    'නම්': ['මම කෘතිම බුද්ධිමය වැඩසටහනක්.', 'මට නමක් නැත.', 'මගේ නම ලංකාබොට්.'],
    'කවුද': ['මම ඔබගේ සහායකයා වෙමි.', 'මම කතා කිරීමට සූදානම්.', 'මම ලංකාබොට්, ඔබට උදව් කිරීමට.'],
    'උදව්': ['මම ඔබට උදව් කිරීමට සූදානම්.', 'ඔබට උදව් අවශ්‍යද?', 'ඔව්, මට උදව් කළ හැකිය.'],
    'ස්තුතියි': ['සතුටුයි!', 'කමක් නැහැ.', 'කිසි ප්‍රශ්නයක් නැහැ.'],
    'ආයුබෝවන්': ['ආයුබෝවන්!', 'නැවත හමුවෙමු!'],

    'hello': ['Hi there!', 'Hello, how can I help you?', 'Greetings!'],
    'how are you': ["I'm doing well, thank you! How about you?", "I'm fine, thanks for asking!"],
    'what is your name': ["I am LankaBot, your AI assistant.", "You can call me LankaBot."],
    'who are you': ["I am an AI assistant designed to help you.", "I'm a chatbot named LankaBot."],
    'help': ["I'm here to assist you.", "How can I help you today?", "Yes, I can help you."],
    'thank you': ["You're welcome!", "No problem!", "Glad to help!"],
    'bye': ["Goodbye!", "See you later!", "Farewell!"],

    'machan': ['මචන්, කොහොමද?', 'මචන්, මොකද වෙන්නේ?', "Hey machan, what's up?"],
    'aiyo': ['අයියෝ, මොකද වුණේ?', 'අයියෝ, කමක් නැහැ.', 'Aiyo, what happened?', 'Aiyo, never mind.'],
    'can': ['ඔව්, පුළුවන්.', 'ඇත්තෙන්ම පුළුවන්.', 'Yes, I can.', 'Sure, can.'],
    'cannot': ['බැහැ.', 'නැහැ, බැහැ.', 'No, cannot.', 'Cannot lah.'],
    'no problem': ['කිසි ප්‍රශ්නයක් නැහැ.', 'කමක් නැහැ.', 'No problem, lah.', "It's fine."],
    'what to do': ['මොනවද کرنا තියෙන්නේ?', 'අපි මොනවද කරන්නේ?', 'What to do now?', 'What should we do?'],
    'okay': ['හරි.', 'හොඳයි.', 'Okay.', 'Alright.'],
    'wah': ['වාව්!', 'හරිම පුදුමයි!', 'Wah, amazing!', 'Wow!'],
    'dunno': ['දන්නේ නැහැ.', 'මට විශ්වාස නැහැ.', "I don't know.", 'Dunno lah.'],
    'where got': ['කොහෙද තියෙන්නේ?', 'නැහැ, එහෙම නැහැ.', 'Where got?', 'No, not really.'],
    'come on': ['එන්න!', 'ඉක්මන් කරන්න!', 'Come on!', "Let's go!"]
}

# -------------------------------
# Intent training data (extend freely)
# -------------------------------
intents: Dict[str, Dict[str, List[str]]] = {
    "greet": {
        "examples": [
            "hello", "hi", "hey", "hey there", "good morning", "good evening",
            "හෙලෝ", "ආයුබෝවන්", "hello bot", "hi bot"
        ],
        "responses": [
            "Hello! How can I help?", "හෙලෝ! මොකද්ද මං උදවු කරන්නේ?",
            "Hi there 👋"
        ]
    },
    "how_are_you": {
        "examples": [
            "how are you", "how's it going", "koyi vidihakda", "කොහොමද", "mage yaluwo kohomada?"
        ],
        "responses": [
            "I'm doing well! How about you?", "මම හොඳි. ඔබට කොහොමද?",
        ]
    },
    "ask_name": {
        "examples": [
            "what is your name", "who are you", "oya ge nama mokakda", "මගේ නම කුමක්ද?"
        ],
        "responses": [
            "I'm LankaBot 😄", "මම ලංකාබොට්!"
        ]
    },
    "thanks": {
        "examples": ["thanks", "thank you", "bohoma sthuthi", "ස්තුතියි"],
        "responses": ["You're welcome!", "කමක් නෑ!", "Glad to help!"]
    },
    "goodbye": {
        "examples": ["bye", "goodbye", "see you", "බායි", "ආයුබෝවන්"],
        "responses": ["Goodbye! 👋", "නැවත හම්බෙමු!", "See you later!"]
    },
    "help": {
        "examples": ["help", "can you help me", "මට උදව් කරන්න", "help me"],
        "responses": ["Sure—tell me what you need.", "ඔබට මොකද්ද ඕනේ කියන්න."]
    },
}

# -------------------------------
# Utilities
# -------------------------------
def clean_text(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s]", "", s, flags=re.UNICODE)
    return s

def fuzzy_candidates(text: str, keys: List[str], cutoff: float = 0.82) -> List[str]:
    text = clean_text(text)
    return difflib.get_close_matches(text, keys, n=3, cutoff=cutoff)

@dataclass
class NLUModel:
    vectorizer: TfidfVectorizer
    clf: LogisticRegression
    labels: List[str]

MODEL_PATH = "model.pkl"
VECT_PATH = "vectorizer.pkl"

def build_training_corpus(intents_dict: Dict[str, Dict[str, List[str]]]):
    X, y = [], []
    for label, spec in intents_dict.items():
        for ex in spec["examples"]:
            X.append(clean_text(ex))
            y.append(label)
    return X, y

def train_or_load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(VECT_PATH):
        with open(MODEL_PATH, "rb") as f1, open(VECT_PATH, "rb") as f2:
            clf = pickle.load(f1)
            vectorizer = pickle.load(f2)
        labels = sorted(set(build_training_corpus(intents)[1]))
        return NLUModel(vectorizer, clf, labels)

    X, y = build_training_corpus(intents)
    vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=1, max_df=1.0)
    Xv = vectorizer.fit_transform(X)
    clf = LogisticRegression(max_iter=1000)
    clf.fit(Xv, y)
    with open(MODEL_PATH, "wb") as f1, open(VECT_PATH, "wb") as f2:
        pickle.dump(clf, f1)
        pickle.dump(vectorizer, f2)
    return NLUModel(vectorizer, clf, sorted(set(y)))

nlu = train_or_load_model()

# -------------------------------
# Dialogue Manager with memory
# -------------------------------
@dataclass
class DialogueState:
    history: List[Dict[str, str]] = field(default_factory=list)
    max_len: int = 10

    def add(self, who: str, text: str):
        self.history.append({"who": who, "text": text})
        if len(self.history) > self.max_len:
            self.history.pop(0)

state = DialogueState()

def rule_based_response(user_input: str) -> str:
    cleaned = clean_text(user_input)
    words = cleaned.split()
    # phrase-first
    for kw in knowledge_base:
        if " " in kw and kw in cleaned:
            return random.choice(knowledge_base[kw])
    # single words
    for w in words:
        for kw in knowledge_base:
            if " " not in kw and w.startswith(kw):
                return random.choice(knowledge_base[kw])
    # fuzzy backoff across keys
    fuzz = fuzzy_candidates(cleaned, list(knowledge_base.keys()), cutoff=0.86)
    if fuzz:
        return random.choice(knowledge_base[fuzz[0]])
    return "මට එය තේරුම් ගත නොහැක. වෙනස් විදිහට පැහැදිලි කරන්න පුලුවන්ද?"

def nlu_predict(text: str):
    Xv = nlu.vectorizer.transform([clean_text(text)])
    probs = nlu.clf.predict_proba(Xv)[0]
    labels = nlu.clf.classes_
    best_i = probs.argmax()
    return labels[best_i], float(probs[best_i])

def respond(user_input: str) -> str:
    intent, conf = nlu_predict(user_input)

    # Confidence threshold
    THRESH = 0.62
    if conf >= THRESH and intent in intents:
        resp = random.choice(intents[intent]["responses"])
    else:
        resp = rule_based_response(user_input)

    # Tiny personalization using memory (example)
    if any(word in clean_text(user_input) for word in ["name", "nama", "නම"]):
        # If user earlier said "I'm <name>"
        for turn in reversed(state.history):
            if turn["who"] == "user" and re.search(r"\bi(?: am|’m|m)\s+(\w+)|මම\s+(\w+)", turn["text"], flags=re.I):
                m = re.search(r"\bi(?: am|’m|m)\s+(\w+)", turn["text"], flags=re.I)
                name = m.group(1) if m else None
                if name:
                    resp += f" Nice to meet you, {name}!"
                    break

    return resp

# -------------------------------
# GUI (CustomTkinter)
# -------------------------------
def type_out(text_widget, text, delay=8):
    text_widget.config(state=tk.NORMAL)
    for ch in text:
        text_widget.insert(tk.END, ch)
        text_widget.see(tk.END)
        text_widget.update_idletasks()
        time.sleep(delay/1000.0)
    text_widget.insert(tk.END, "\n\n")
    text_widget.config(state=tk.DISABLED)

def send_message():
    user_msg = user_input.get()
    if user_msg.strip() == "":
        return
    state.add("user", user_msg)

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {user_msg}\n")
    chat_area.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)
    chat_area.see(tk.END)

    bot_reply = respond(user_msg)
    state.add("bot", bot_reply)

    # Typing indicator effect
    send_button.configure(state="disabled", text="Typing…")
    window.after(200, lambda: (type_out(chat_area, f"LankaBot: {bot_reply}", delay=5),
                               send_button.configure(state="normal", text="Send")))

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("LankaBot 🇱🇰 — Smarter Offline AI")
window.geometry("560x600")
window.resizable(False, False)

main_frame = ctk.CTkFrame(window, corner_radius=12)
main_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

chat_area = scrolledtext.ScrolledText(
    main_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12),
    bg="#1f1f1f", fg="#f5f5f5", insertbackground="white", relief=tk.FLAT, height=22
)
chat_area.pack(padx=10, pady=(10, 8), fill=tk.BOTH, expand=True)

input_frame = ctk.CTkFrame(main_frame)
input_frame.pack(fill=tk.X, padx=10, pady=(2, 10))

user_input = ctk.CTkEntry(input_frame, placeholder_text="Type your message…", font=("Arial", 12))
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
user_input.bind("<Return>", lambda e: send_message())

send_button = ctk.CTkButton(input_frame, text="Send", command=send_message, corner_radius=8, width=90)
send_button.pack(side=tk.RIGHT)

window.mainloop()