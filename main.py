from runner import LLMAgent
def main():
    """Main function to run the agent."""
    print("Starting LLM Agent...")
    print("=" * 50)

    try:
        agent = LLMAgent()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return

    print("Agent initialized successfully.\n")
    print("Type your question or 'exit' to quit.")
    print("=" * 50)

    while True:
        try:
            query = input("\nYour query: ").strip()
            if query.lower() in ["quit", "exit", "q"]:
                print("Exiting agent.")
                break

            if not query:
                continue

            print("-" * 50)
            response = agent.run(query)
            print("-" * 50)
            print("\nResponse:\n")
            print(response)

        except KeyboardInterrupt:
            print("\nExiting agent.")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()
