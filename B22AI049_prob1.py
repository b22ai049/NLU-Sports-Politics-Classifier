import re
from datetime import date
import logging

# Setup logging to generate B15CS001_prob1.log automatically
logging.basicConfig(
    filename='B22AI049_prob1.log',
    level=logging.INFO,
    format='%(message)s',
    filemode='a' # Appends each run to the log
)

def log_interaction(user_input, bot_response):
    logging.info(f"User: {user_input}")
    logging.info(f"Chatbot: {bot_response}")
    logging.info("-" * 20)

def calculate_age(dob_str):
    today = date.today()
    # Patterns for: DD-MM-YYYY, YYYY-MM-DD, or "15 Jan 2000"
    patterns = [
        r'(?P<d>\d{1,2})[/-](?P<m>\d{1,2})[/-](?P<y>\d{4})',
        r'(?P<y>\d{4})[/-](?P<m>\d{1,2})[/-](?P<d>\d{1,2})',
        r'(?P<d>\d{1,2})\s+(?P<m>[A-Za-z]+)\s+(?P<y>\d{4})'
    ]
    
    for p in patterns:
        match = re.search(p, dob_str)
        if match:
            try:
                birth_year = int(match.group('y'))
                return today.year - birth_year
            except:
                continue
    return None

def chatbot():
    run_header = f"\n--- Chatbot Run: {date.today()} ---"
    logging.info(run_header)
    print("Reggy++: Hello! What is your full name?")
    
    name_input = input("You: ")
    surname_match = re.search(r'\s+([A-Za-z]+)$', name_input.strip())
    surname = surname_match.group(1) if surname_match else "Friend"
    resp1 = f"Nice to meet you, {surname}!"
    print(f"Reggy++: {resp1}")
    log_interaction(name_input, resp1)

    print("Reggy++: What is your birthday? (e.g., DD-MM-YYYY or 15 Jan 1995)")
    dob_input = input("You: ")
    age = calculate_age(dob_input)
    resp2 = f"I see, you are roughly {age} years old." if age else "That's an interesting date format!"
    print(f"Reggy++: {resp2}")
    log_interaction(dob_input, resp2)

    print("Reggy++: How are you feeling today?")
    mood_input = input("You: ")
    # Regex handles minor typos (e.g., happpy, goooood)
    if re.search(r'h+a+p+y|g+o+o+d|f+i+n+e|o+k', mood_input, re.I):
        resp3 = "I'm glad to hear you're doing well!"
    elif re.search(r's+a+d|b+a+d|u+p+s+e+t|t+i+r+e+d', mood_input, re.I):
        resp3 = "I'm sorry to hear that. I hope your day improves."
    else:
        resp3 = "Thank you for sharing your mood with me."
    
    print(f"Reggy++: {resp3}")
    log_interaction(mood_input, resp3)

if __name__ == "__main__":
    chatbot()