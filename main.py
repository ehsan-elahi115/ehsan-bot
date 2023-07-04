import aiml
from py2neo import Graph
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Initialize AIML kernel
kernel = aiml.Kernel()

# Load AIML files
kernel.learn("startup.xml")
kernel.respond("LOAD AIML B")

# Connect to Neo4j database
graph = Graph("bolt://localhost:7687", username="your_username", password="your_password")

# Web scraping function
def scrape_data(query):
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Extract desired data from the web page using BeautifulSoup

    # Store data in Neo4j
    # Create Neo4j nodes and relationships as per your requirements

    return extracted_data

# Tokenization function
def tokenize_input(input_text):
    sentences = sent_tokenize(input_text)
    tokens = [word_tokenize(sentence) for sentence in sentences]
    return tokens

# Main chatbot function
def chatbot():
    print('Chatbot: Hi! How can I assist you today?')
    while True:
        user_input = input('User: ')
        tokenized_input = tokenize_input(user_input)

        for sentence_tokens in tokenized_input:
            joined_tokens = ' '.join(sentence_tokens)
            neo4j_response = graph.run("MATCH (n) WHERE n.text CONTAINS $query RETURN n.text", query=joined_tokens).data()

            if neo4j_response:
                print('Chatbot:', neo4j_response[0]['n.text'])
            else:
                aiml_response = kernel.respond(joined_tokens)

                if aiml_response:
                    print('Chatbot:', aiml_response)
                    # Store new information in Neo4j
                    graph.run("CREATE (n:Data {text: $text})", text=aiml_response)
                else:
                    # Web scrape data
                    scraped_data = scrape_data(joined_tokens)
                    if scraped_data:
                        print('Chatbot:', scraped_data)
                        # Store new information in Neo4j
                        graph.run("CREATE (n:Data {text: $text})", text=scraped_data)
                    else:
                        print('Chatbot: Sorry, I cannot find any relevant information.')

        if user_input.lower() == 'bye':
            break

# Run the chatbot
chatbot()