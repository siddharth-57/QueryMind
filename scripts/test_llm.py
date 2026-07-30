from src.llm.service import LLMService


def main():

    llm_service = LLMService()

    while True:

        prompt = input("\nEnter prompt (or 'exit'): ")

        if prompt.lower() == "exit":
            break

        response = llm_service.generate(prompt)

        print("\nResponse:")
        print("-" * 80)
        print(response)
        print("-" * 80)


if __name__ == "__main__":
    main()