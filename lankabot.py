import random
import re

# LankaBot's knowledge base.
# This dictionary contains keywords and their corresponding responses
# in Sinhala, English, and common Singlish phrases.
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

    # Common Singlish/Mixed-language expressions (focusing on keywords that trigger responses)
    'machan': ['මචන්, කොහොමද?', 'මචන්, මොකද වෙන්නේ?', 'Hey machan, what\'s up?'],
    'aiyo': ['අයියෝ, මොකද වුණේ?', 'අයියෝ, කමක් නැහැ.', 'Aiyo, what happened?', 'Aiyo, never mind.'],
    'can': ['ඔව්, පුළුවන්.', 'ඇත්තෙන්ම පුළුවන්.', 'Yes, I can.', 'Sure, can.'],
    'cannot': ['බැහැ.', 'නැහැ, බැහැ.', 'No, cannot.', 'Cannot lah.'],
    'no problem': ['කිසි ප්‍රශ්නයක් නැහැ.', 'කමක් නැහැ.', 'No problem, lah.', 'It\'s fine.'],
    'what to do': ['මොනවද කරන්න තියෙන්නේ?', 'අපි මොනවද කරන්නේ?', 'What to do now?', 'What should we do?'],
    'okay': ['හරි.', 'හොඳයි.', 'Okay.', 'Alright.'],
    'wah': ['වාව්!', 'හරිම පුදුමයි!', 'Wah, amazing!', 'Wow!'],
    'dunno': ['දන්නේ නැහැ.', 'මට විශ්වාස නැහැ.', 'I don\'t know.', 'Dunno lah.'],
    'where got': ['කොහෙද තියෙන්නේ?', 'නැහැ, එහෙම නැහැ.', 'Where got?', 'No, not really.'],
    'come on': ['එන්න!', 'ඉක්මන් කරන්න!', 'Come on!', 'Let\'s go!']
}

def clean_text(text):
    """
    Cleans the input text by removing punctuation and converting to lowercase.
    This helps in matching keywords regardless of case or surrounding punctuation.
    """
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.strip().lower() # Convert to lowercase for consistent matching

def get_response(user_input):
    """
    Takes a user's input, cleans it, checks for keywords, and returns a random
    pre-defined response from the knowledge base.
    """
    cleaned_input = clean_text(user_input)
    words = cleaned_input.split()

    # Iterate through the words to find a match in the knowledge base
    # This approach prioritizes multi-word phrases first, then single words.
    # For more complex matching, consider a more sophisticated NLP library.
    
    # Try matching multi-word phrases first
    for keyword in knowledge_base:
        if ' ' in keyword and keyword in cleaned_input:
            return random.choice(knowledge_base[keyword])

    # Then try matching single words or words that start with a keyword
    for word in words:
        for keyword in knowledge_base:
            if ' ' not in keyword and word.startswith(keyword):
                return random.choice(knowledge_base[keyword])

    # If no keyword is found, return a default response
    return "මට එය තේරුම් ගත නොහැක. ඔබට වෙනත් දෙයක් ඇසිය හැකිද? (I cannot understand that. Can you ask something else?)"


def chat_bot():
    """
    The main loop for the chat bot (LankaBot).
    """
    print("හෙලෝ! මට කතා කරන්න. (Hello! Talk to me.)")
    print("ඔබට ඉංග්‍රීසි, සිංහල හෝ සිංග්ලිෂ් භාවිතා කළ හැක. (You can use English, Sinhala, or Singlish.)")
    print("පිටවීමට 'quit' කියලා ටයිප් කරන්න. (Type 'quit' to exit.)")

    while True:
        user_input = input("ඔබ / You: ")
        if user_input.lower() == 'quit':
            print("ලංකාබොට්: ආයුබෝවන්! / LankaBot: Goodbye!")
            break

        response = get_response(user_input)
        print(f"ලංකාබොට් / LankaBot: {response}")

# Run the chatbot
if __name__ == "__main__":
    chat_bot()