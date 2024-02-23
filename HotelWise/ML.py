import pandas as pd
import tensorflow as tf
import tensorflow_recommenders as tfrs
import numpy as np
from sklearn.model_selection import train_test_split

# Cargar datos desde CSV
data = pd.read_csv('hoteles.csv')

# Preprocesamiento de datos
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Definir modelo de recomendación
class HotelModel(tfrs.Model):
    def __init__(self):
        super().__init__()
        self.embedding_dimension = 32

        # Definir capas de embedding para estados y ciudades
        self.state_embeddings = tf.keras.layers.Embedding(
            input_dim=len(data['state'].unique()) + 1,
            output_dim=self.embedding_dimension
        )
        self.city_embeddings = tf.keras.layers.Embedding(
            input_dim=len(data['city'].unique()) + 1,
            output_dim=self.embedding_dimension
        )

        # Capa para concatenar las embeddings de estado y ciudad
        self.concat_layer = tf.keras.layers.Concatenate(axis=1)

        # Capas densas para procesar los datos de entrada
        self.dense1 = tf.keras.layers.Dense(64, activation='relu')
        self.dense2 = tf.keras.layers.Dense(32, activation='relu')

        # Capa de salida para la recomendación
        self.output_layer = tf.keras.layers.Dense(
            1)  # Una salida para rating o sentimiento

    def call(self, inputs):
        # Obtener embeddings de estado y ciudad
        state_embeddings = self.state_embeddings(inputs['state'])
        city_embeddings = self.city_embeddings(inputs['city'])

        # Concatenar embeddings de estado y ciudad
        concatenated = self.concat_layer([state_embeddings, city_embeddings])

        # Procesar datos de entrada a través de capas densas
        x = self.dense1(concatenated)
        x = self.dense2(x)

        # Capa de salida para la recomendación
        return self.output_layer(x)


# Crear dataset de TensorFlow
train_dataset = tf.data.Dataset.from_tensor_slices((
    {'state': train_data['state'], 'city': train_data['city']},
    {'rating': train_data['rating'], 'sentimiento': train_data['sentimiento']}
))
test_dataset = tf.data.Dataset.from_tensor_slices((
    {'state': test_data['state'], 'city': test_data['city']},
    {'rating': test_data['rating'], 'sentimiento': test_data['sentimiento']}
))

# Configurar modelo y entrenamiento
model = HotelModel()
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mean_squared_error')

# Entrenar el modelo
model.fit(train_dataset.shuffle(len(train_data)).batch(32), epochs=10)

# Solicitar entrada del usuario para la ciudad y el estado
city = input("Ingrese la ciudad: ")
state = input("Ingrese el estado: ")

# Generar recomendaciones para la ciudad y el estado proporcionados por el usuario
# Crear un batch con la entrada del usuario
user_input = {'state': np.array([state]), 'city': np.array([city])}
# Obtener la predicción del modelo
predicted_rating = model(user_input).numpy()[0][0]

print("La calificación predicha para la ciudad {} y el estado {} es: {}".format(
    city, state, predicted_rating))
