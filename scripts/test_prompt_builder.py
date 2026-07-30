from src.retrieval.prompt_builder import PromptBuilder


def main():

    query = "What is PostgreSQL?"

    contexts = [
        "PostgreSQL is an open-source relational database.",
        "It supports SQL and ACID transactions.",
    ]

    prompt = PromptBuilder.build(
        query=query,
        contexts=contexts,
    )

    print(prompt)


if __name__ == "__main__":
    main()