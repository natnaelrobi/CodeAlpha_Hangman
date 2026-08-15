import datetime
import random

BOT_RESPONSES = {
    "hello": ["Hello! Welcome to the CodeAlpha Chatbot. How can I assist you today?",
              "Hi there! What can I help you with?", "Greetings! How may I help you?"],
    "hi": ["Hello! Welcome to the CodeAlpha Chatbot. How can I assist you today?",
           "Hi there! What can I help you with?"],
    "how are you": ["I'm just a Python program, but I'm running smoothly and ready to help!",
                    "Doing great! Thanks for asking. How are you doing?"],
    "help": ["I can answer basic questions! Try asking me about 'time', 'codealpha', 'python', or just say 'hello'."],
    "codealpha": [
        "CodeAlpha is an internship program providing technical tasks to help students build practical programming experience."],
    "python": ["Python is a high-level, interpreted programming language known for its readability and versatility."],
    "bye": ["Goodbye! Have a wonderful day ahead.", "See you later! Feel free to return if you have more questions.",
            "Bye! Keep coding!"]
}

FALLBACK_RESPONSES = [
    "I'm sorry, I didn't quite catch that. Type 'help' to see what I can do.",
    "Could you please rephrase that? I am a rule-based chatbot with limited vocabulary.",
    "That's interesting! Unfortunately, I don't have a programmed response for that yet. Type 'help' for options."
]


class Chatbot:
    normalize_input = lambda self, text: text.lower().strip()

    def __init__(self):
        self.session_active = True

    def get_response(self, user_input):
        cleaned_input = self.normalize_input(user_input)

        if not cleaned_input:
            return "Please type something so we can chat!"

        if "time" in cleaned_input or "date" in cleaned_input:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"The current system date and time is: {current_time}"

        for keyword, responses in BOT_RESPONSES.items():
            if keyword in cleaned_input:
                return random.choice(responses)

        return random.choice(FALLBACK_RESPONSES)

    def start_chat(self):
        print("=" * 50)
        print("      CODEALPHA PYTHON INTERNSHIP        ")
        print("         TASK 4: BASIC CHATBOT           ")
        print("=" * 50)
        print("Chatbot: Hello! Type 'bye', 'exit', or 'quit' at any time to end our chat.\n")

        while self.session_active:
            try:
                user_input = input("You: ")

                if self.normalize_input(user_input) in ["bye", "exit", "quit"]:
                    goodbye_msg = random.choice(BOT_RESPONSES["bye"])
                    print(f"Chatbot: {goodbye_msg}")
                    self.session_active = False
                    break

                response = self.get_response(user_input)
                print(f"Chatbot: {response}\n")

            except (KeyboardInterrupt, EOFError):
                print("\n\nChatbot: Session interrupted. Goodbye!")
                self.session_active = False
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}\n")


if __name__ == "__main__":
    bot = Chatbot()
    bot.start_chat()