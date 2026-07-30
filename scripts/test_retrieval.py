# This tests the RAG pipeline from end to end
from src.retrieval.service import RetrievalService


def main():

    retrieval = RetrievalService()

    while True:

        query = input("\nQuestion (or 'exit'): ")

        if query.lower() == "exit":
            break

        answer = retrieval.answer(query)

        print("\nAnswer:")
        print("-" * 80)
        print(answer)
        print("-" * 80)


if __name__ == "__main__":
    main()