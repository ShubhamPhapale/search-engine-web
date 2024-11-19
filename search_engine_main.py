import os
from search_engine import SearchEngine
from corpus import fetch_and_save_articles

def load_corpus(folder_path):
    """
    Load a domain-specific corpus from a folder of text files.
    Each text file in the folder represents one document.
    """
    corpus = []
    try:
        # List all files in the directory
        files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        # print(files)
        # Read each file in the folder
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            # print("path : ", file_path)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                # Read the content of the file and strip leading/trailing whitespace
                content = file.read().strip()
                if content:
                    corpus.append(content)
        
        print(f"Loaded {len(corpus)} documents from {folder_path}.")
        return corpus
    
    except FileNotFoundError:
        print(f"Error: Folder not found at {folder_path}. Please provide a valid folder path.")
        return []
    except Exception as e:
        print(f"Error loading corpus: {e}")
        return []

def get_user_query():
    """Prompt the user for a search query."""
    return input("\nEnter your search query: ")

def main():
    print("                                      === Domain-Specific Search Engine ===")

    # Step 1: Load the corpus

    domain = input("Enter the domain you want to search on : ")

    corpus_folder = "/Users/shubhamsarjeraophapale/IR Assignment 5/" + domain.replace(' ', '_')

    if not os.path.exists(corpus_folder):
        print(f"Corpus folder not found at {corpus_folder}. Fetching articles from Wikipedia...")
        fetch_and_save_articles(domain, num_articles=50)
        print("Articles fetched and saved successfully!")

    corpus = load_corpus(corpus_folder)
    # print(corpus)

    if not corpus:
        print("No documents loaded. Exiting...")
        return

    engine = SearchEngine(corpus_folder + ".pkl")
    
    # Step 2: Build the index
    # print("\nBuilding index...")
    engine.build_index(corpus)
    # print("Index built successfully!")

    # Step 3: Interact with the user for searching
    while True:
        query = get_user_query()
        if query.lower() in ['exit', 'quit']:
            print("Exiting the search engine. Goodbye!")
            break
        
        results = engine.search(query)
        if results:
            print("\nSearch Results:")
            for rank, (doc_id, score) in enumerate(results[:5], start=1):
                doc_name = corpus[doc_id]  # Get the document name
                # print(f"Rank {rank}: Document {doc_name}, Score: {score:.2f}")
                print(f"Rank {rank}: Document {doc_id}, Score: {score:.2f}")
                # print(f"Content: {corpus[doc_id]}")
                print("-" * 50)
        else:
            print("No relevant documents found for your query.")
        
        # Optionally ask if the user wants to search again
        continue_search = input("\nDo you want to perform another search? (yes/no): ").strip().lower()
        if continue_search not in ['yes', 'y']:
            print("Exiting the search engine. Goodbye!")
            break

if __name__ == "__main__":
    main()
