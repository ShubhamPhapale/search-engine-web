import wikipedia
import os
import argparse

def fetch_and_save_articles(query, num_articles=10):
    # Create a folder named after the domain/topic
    domain_dir = query.replace(' ', '_')  # Replace spaces with underscores to form the directory name
    domain_dir = "../../" + domain_dir  # Save the folder in the parent directory
    if not os.path.exists(domain_dir):
        os.makedirs(domain_dir)

    # Search for related articles based on the query
    print(f"Searching for articles related to '{query}'...")
    try:
        search_results = wikipedia.search(query, results=num_articles)
        print(f"Found {len(search_results)} articles.")
    except wikipedia.exceptions.HTTPError as e:
        print(f"Error fetching articles: {e}")
        return

    # Fetch and save each article's content
    for idx, title in enumerate(search_results, start=1):
        try:
            # Fetch the content of the article
            page = wikipedia.page(title)
            content = page.content
            
            # Save the article as a text file in the domain folder
            filename = f"{title.replace(' ', '_')}.txt"
            file_path = os.path.join(domain_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print(f"Saved article '{title}' as {filename}")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"DisambiguationError: Multiple pages found for '{title}', skipping.")
        except wikipedia.exceptions.PageError as e:
            print(f"PageError: Article '{title}' not found.")
        except Exception as e:
            print(f"Error fetching or saving '{title}': {e}")

def main():
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description='Fetch Wikipedia articles for a specific domain and save them as text files.')
    
    # Define command-line arguments
    parser.add_argument('domain', type=str, help='The domain/topic to search for articles.')
    parser.add_argument('num_articles', type=int, help='The number of articles to retrieve.', default=10)

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to fetch and save articles
    fetch_and_save_articles(args.domain, args.num_articles)

if __name__ == "__main__":
    main()
