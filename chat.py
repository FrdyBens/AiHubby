import os
import json
import datetime
from groq import Groq

# Initialize the Groq client with the API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_conversation(jsonpath):
    if os.path.exists(jsonpath):
        with open(jsonpath, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Handle case where JSON is empty or contains invalid JSON
                return []
    else:
        return []

def save_conversation(jsonpath, conversation):
    with open(jsonpath, "w") as f:
        json.dump(conversation, f, indent=4)

# Generate a timestamp-based filename
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
default_jsonpath = f"conversation_{timestamp}.json"

# Load existing conversation from the JSON file if it exists
conversation = load_conversation(default_jsonpath)

def save_chat():
    custom_name = input(f"Default file name is {default_jsonpath}. Do you want to save it with a different name? (y/n): ")
    if custom_name.lower() == 'y':
        return input("Enter the new file name (without extension): ") + ".json"
    else:
        return default_jsonpath

# Continuous conversation loop
while True:
    user_input = input("Type your message: ")

    if user_input == "/help":
        help_option = input('''Here are the Commands:
Options       Commands
Save          save
Start NewChat new
Exit          exit
Back          back
What would you like to do?: ''')
        if help_option == "save":
            jsonpath = save_chat()
            save_conversation(jsonpath, conversation)
            print(f"Conversation saved to {jsonpath}.")
        elif help_option == "new":
            save_name = input("Would you like to save the current chat before starting a new one? (y/n): ")
            if save_name.lower() == 'y':
                jsonpath = save_chat()
                save_conversation(jsonpath, conversation)
                print(f"Conversation saved to {jsonpath}.")
            new_chat_name = input("Enter the new chat name (without extension): ") + ".json"
            jsonpath = new_chat_name
            conversation = []
            save_conversation(jsonpath, conversation)
            print(f"Started a new chat with the name {new_chat_name}.")
        elif help_option == "exit":
            print("Thank you so much for using My AI. I hope you enjoyed it because I know I did.")
            break
        elif help_option == "back":
            continue

    elif user_input == "/quit":
        print("Exiting...")
        break

    elif user_input == "/save":
        jsonpath = save_chat()
        save_conversation(jsonpath, conversation)
        print(f"Conversation saved to {jsonpath}.")

    elif user_input == "/newChat":
        new_chat_name = input("Enter the new chat name (without extension): ") + ".json"
        jsonpath = new_chat_name
        conversation = []
        save_conversation(jsonpath, conversation)
        print(f"Started a new chat with the name {new_chat_name}.")

    elif user_input == "/SystemC":
        system_message = input("Enter your system message: ")
        conversation = [msg for msg in conversation if msg["role"] != "system"]
        if system_message:
            conversation.insert(0, {"role": "system", "content": system_message})

    else:
        user_message = user_input
        conversation.append({"role": "user", "content": user_message})

        chat_completion = client.chat.completions.create(
            messages=conversation,
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False
        )

        assistant_message = chat_completion.choices[0].message.content
        print(assistant_message)
        conversation.append({"role": "assistant", "content": assistant_message})

    save_conversation(jsonpath, conversation)
