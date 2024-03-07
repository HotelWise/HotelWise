import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from contractions import fix
from google.cloud import storage
from DB_FILES import *

client = storage.Client(project=project_id)
bucket = client.bucket(bucket_name)

user_reviews_dataset = pd.read_parquet(f"gs://{bucket_name}/{file_name_parquet_final}")

def process_nlp():
    def nltk_downloads():
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('vader_lexicon')
    def preprocess_text(text):
        if not text or pd.isnull(text):
            return ''

        text = re.sub(r'[^\w\s]', '', text)

        try:
            text = fix(text)
        except Exception as e:
            print(f"Error al aplicar fix(): {e}")

        tokens = word_tokenize(text)

        negative_hotel_words = ['dirty', 'uncomfortable', 'noisy', 'smelly', 'outdated',
                                'small', 'unfriendly', 'expensive', 'overpriced', 'unhygienic',
                                'unsafe', 'crowded', 'inefficient', 'unorganized', 'rude',
                                'disappointing', 'terrible', 'unreliable', 'dull', 'unresponsive',
                                'unpleasant', 'inattentive', 'unsanitary', 'uninviting', 'dilapidated',
                                'neglected', 'inconvenient', 'unaccommodating', 'problematic'
                                ]

        positive_hotel_words = ['clean', 'comfortable', 'quiet', 'pleasant', 'modern',
                                'spacious', 'friendly', 'affordable', 'luxurious', 'inviting',
                                'safe', 'relaxing', 'efficient', 'organized', 'welcoming',
                                'satisfying', 'excellent', 'reliable', 'enjoyable', 'responsive',
                                'beautiful', 'attentive', 'sanitary', 'inviting', 'well-maintained',
                                'cared-for', 'convenient', 'accommodating', 'problem-free', 'stellar'
                                ]

        stop_words = set(stopwords.words('english'))

        for word in negative_hotel_words:
            stop_words.discard(word)
        for word in positive_hotel_words:
            stop_words.discard(word)

        tokens = [word for word in tokens if word.lower(
        ) not in stop_words and word.isalpha()]

        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]

        return ' '.join(tokens)

    def analizar_sentimiento(texto):
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(texto)
        compound_score = scores['compound']
        if compound_score >= 0.05:
            return 1  # Review Positiva
        else:
            return 0  # Review Negativa

    def summarize_df():
        user_reviews_dataset_Final = user_reviews_dataset[[
            'NAME', 'LATITUDE', 'LONGITUDE', 'CITY', 'COUNTY', 'STATE', 'AMENITIES', 'AVG_RATING', 'CRIME_RATE', 'SENTIMENT_ANALYSIS']]

        summarized_data = user_reviews_dataset_Final.groupby('NAME').agg({
            'LATITUDE': 'first',
            'LONGITUDE': 'first',
            'CITY': 'first',
            'COUNTY': 'first',
            'STATE': 'first',
            'AVG_RATING': 'first',
            'AMENITIES': 'first',
            'SENTIMENT_ANALYSIS': 'sum',
            'CRIME_RATE': 'sum',

        })
        summarized_data = summarized_data.reset_index()
        summarized_data.to_parquet(
            f"gs://{bucket_name}/{file_hoteles_NLP_parquet}", index=False)
        print(f"Parquet file successfully uploaded to GCS: {file_hoteles_NLP_parquet}")

    nltk_downloads()
    user_reviews_dataset['preprocess_text'] = user_reviews_dataset['REVIEWS'].apply(
        preprocess_text)
    user_reviews_dataset['SENTIMENT_ANALYSIS'] = user_reviews_dataset['preprocess_text'].apply(
        analizar_sentimiento)
    summarize_df()
    print("Terminó Funciones NLP")
    