from flask import Flask, render_template, jsonify
import pandas as pd
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os
import json

app = Flask(__name__)

# Load and process data from conversations.json
json_file_path = r"C:\Users\fatii\Desktop\DAV\movie-corpus\conversations.json"

with open(json_file_path, 'r') as file:
    conversation_data = json.load(file)

# Sample data for demonstration (file 2)
data = {
    'movie_name': ['10 things i hate about you'],
    'release_year': ['1999'],
    'rating': ['6.90'],
    'votes': ['62847'],
    'genre': ["['comedy', 'romance']"],
}

df = pd.DataFrame(data)

# Set the path to the Stanford NER jar file
stanford_ner_path = 'C:\\Users\\DELL\\Downloads\\stanford-ner-4.2.0.zip'

# Set the path to the Stanford NER model file
stanford_ner_model_path = 'C:\\Users\\DELL\\Downloads\\stanford-ner-2020-11-17\\stanford-ner-4.2.0.jar'

# Initialize Stanford NER tagger
stanford_ner_tagger = StanfordNERTagger(stanford_ner_model_path, stanford_ner_path, encoding='utf-8')

@app.route('/')
def index():
    return render_template('index.html', processed_data=analyze_reviews(df[['movie_name', 'genre']]))

# Define the route to return processed data as JSON (file 2)
@app.route('/data')
def get_data():
    processed_data = {
        'movie_name': df['movie_name'].tolist(),
        'release_year': df['release_year'].tolist(),
        'rating': df['rating'].tolist(),
        'votes': df['votes'].tolist(),
        'genre': df['genre'].tolist(),
        'ner_results': analyze_reviews(df[['movie_name', 'genre']])
    }
    return jsonify(processed_data)

# Function to analyze reviews using Stanford NER tagger
def analyze_reviews(reviews):
    analyzed_reviews = []
    for _, row in reviews.iterrows():
        # Tokenize the text
        words = word_tokenize(str(row['movie_name']) + ' ' + str(row['genre']))
        # Perform Named Entity Recognition
        ner_results = stanford_ner_tagger.tag(words)
        analyzed_reviews.append(ner_results)
    return analyzed_reviews

if __name__ == '__main__':
    app.run(debug=True)



#------For File 1-----#
# Sample data for demonstration (file 1)
# data = {
#    'ID': ['u0', 'u2', 'u3', 'u4'],
#    'CHARACTER_NAME': ['Bianca', 'Cameron', 'Chastity', 'Joey'],
#    'MOVIE_INDEX': ['m0', 'm1', 'm2', 'm3'],
#    'MOVIE_NAME': ['10 Things I Hate About You', 'Conquest of Paradise'],
#    'GENDER': ['f', 'm', 'f', 'm'],
#    'CREDIT_POSITION': [4, 3, 6, 9],
#}

    # Return processed data as JSON(file 1)
 #   def get_data():
 #   processed_data = {
 #       'IDs': df['ID'].tolist(),
 #       'character_names': df['CHARACTER_NAME'].tolist(),
 #       'movie_indexes': df['MOVIE_INDEX'].tolist(),
 #       'movie_names': df['MOVIE_NAME'].tolist(),
 #       'genders': df['GENDER'].tolist(),
 #       'credit_positions': df['CREDIT_POSITION'].tolist(),
 #   }
 #   return jsonify(processed_data)

#File 1
#def analyze_reviews(reviews):
    # Perform NER using Stanford NER tagger on movie reviews
 #   analyzed_reviews = []
   # for review in reviews:
  #      # Tokenize the review
    #    words = word_tokenize(str(review))  # Ensure the review is converted to a string
     #   # Perform Named Entity Recognition
      #  ner_results = stanford_ner_tagger.tag(words)
       # analyzed_reviews.append(ner_results)
    #return analyzed_reviews
