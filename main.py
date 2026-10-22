from src.chatbot import load_data, ask_dataset_agent

def main():
    print("Loading Pakistani Smartphone Sentiment Dataset...")
    df = load_data()
    
    if df is not None:
        print("Data successfully loaded!")
        print("Pakistani Tech Review Sentiment Agent is active.")
        print("Type 'exit' or 'quit' to close the program.")
        
        while True:
            user_query = input("\nApna sawal likhein: ")
            if user_query.lower() in ['exit', 'quit']:
                print("Closing program. Goodbye!")
                break
            if user_query.strip() == "":
                continue
            ask_dataset_agent(user_query, df)

if __name__ == "__main__":
    main()