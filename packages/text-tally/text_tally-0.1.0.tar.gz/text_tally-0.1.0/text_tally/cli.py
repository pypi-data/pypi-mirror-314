import argparse
import os
from collections import Counter

def analyze_text(text):
    """Count the number of words in a text string and return the 5 most common words.
    
    Args:
        text (str): The text to analyze
    
    Returns:
        dict: A dictionary with the word count and most common words
    """
    words = text.split()
    word_count = len(words)
    most_common_words = Counter(words).most_common(5)
    return {"word_count": word_count, 
            "most_common_words": most_common_words}

def print_analysis(analysis):
    """Print the analysis to the screen.
    
    Args:
        analysis (dict): The analysis to print
    """
    print(f"Word count: {analysis['word_count']}")
    print(f"Most common words: {analysis['most_common_words']}")

def save_analysis(analysis, output_file):
    """Save the analysis to a text file.
    
    Args:
        output_file (str): The path to save the file to
        analysis (dict): The dictionary containing analysis data
    """
    try:
        with open(output_file, 'w') as file:
            file.write(f"Word count: {analysis['word_count']}\n")
            file.write(f"Most common words: {analysis['most_common_words']}\n")
    except Exception as e:
        print(f"An error occurred while saving the analysis: {e}")

def main():
    """
    Entry point for the text-tally CLI.

    $ poetry run text-tally <fileName>
    output: Word count with number, Most common words with list

    $ poetry run text-tally <fileName> --output_file <New fileName> 
    output: Word count with number, Most common words with list, new file
    
    """
    parser = argparse.ArgumentParser(description="Count words in a text file")
    
    # Default file path
    parser.add_argument("text_file", type=str, help="The text file to process", nargs='?')
    parser.add_argument("--output_file", type=str, help="Output file for saving analysis", default="analysis.txt")
    args = parser.parse_args()

    # Check if input file exists
    if not args.text_file:
        print("Error: No text file provided. Please specify a text file.")
        return
    
    if not os.path.exists(args.text_file):
        print(f"Error: file not found: {args.text_file}\nPut file in text-tally folder")
        return

    try:
        with open(args.text_file, "r",encoding="utf-8") as file:
            text = file.read()
            analysis = analyze_text(text)
            print_analysis(analysis)
            save_analysis(analysis, args.output_file)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()