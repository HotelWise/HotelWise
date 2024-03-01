import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from contractions import fix

# Descargar recursos (ejecutar una vez)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')


def process_nlp():
    project_id = "hotelwiseweb"
    bucket_name = "hotelwise_db"
    user_reviews_content = "HotelesUnificado_Final.parquet"

    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    user_reviews_dataset = pd.read_parquet(
        f"gs://{bucket_name}/{user_reviews_content}")


def preprocess_text(text):
    if not text or pd.isnull(text):  # Verificar si el texto está vacío o es nulo
        return ''

    # Eliminar emojis y caracteres especiales
    # Se pueden tokenizar los emojis con metodos mas robustos
    # que ayuden a manejarlos, pero se elije eliminarlos
    text = re.sub(r'[^\w\s]', '', text)

    # Arreglo de contracciones
    try:
        text = fix(text)  # Intentar usar la función fix()
    except Exception as e:
        print(f"Error al aplicar fix(): {e}")

    # Tokenización
    tokens = word_tokenize(text)

    # Palabras clave adicionales, positivas y negativas para mejorar el análisis
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

    # Obtener stopwords y agregar palabras con connotación positiva y negativa
    stop_words = set(stopwords.words('english'))

    for word in negative_hotel_words:
        stop_words.discard(word)
    for word in positive_hotel_words:
        stop_words.discard(word)

    # Eliminación de stopwords y puntuación no necesarios
    tokens = [word for word in tokens if word.lower(
    ) not in stop_words and word.isalpha()]

    # Lematización
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return ' '.join(tokens)


user_reviews_dataset['preprocess_text'] = user_reviews_dataset['reviews'].apply(
    preprocess_text)


def analizar_sentimiento(texto):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(texto)
    compound_score = scores['compound']
    if compound_score >= 0.05:
        return 1  # Review Positiva
    else:
        return 0  # Review Negativa


user_reviews_dataset['sentiment_analysis'] = user_reviews_dataset['preprocess_text'].apply(
    analizar_sentimiento)


def summarize_df():
    user_reviews_dataset_Final = user_reviews_dataset[[
        'name', 'latitude', 'longitude', 'city', 'county', 'avg_rating', 'security', 'sentiment_analysis']]

    summarized_data = user_reviews_dataset_Final.groupby('name').agg({
        'latitude': 'first',
        'longitude': 'first',
        'county': 'first',
        'city': 'first',
        'avg_rating': 'sum',
        'sentiment_analysis': 'sum',
        'security': 'sum',

    })
    summarized_data = summarized_data.reset_index()
    summarized_data.head()

    summarized_data.to_parquet('Hoteles_NLP_NLTK.parquet')
