import pandas as pd
import tensorflow as tf
import tensorflow_recommenders as tfrs
import numpy as np
from sklearn.model_selection import train_test_split

# Cargar datos desde CSV
data = pd.read_csv('hoteles.csv')

# Preprocesamiento de datos
unique_hotels = data['hotel_id'].unique()
unique_users = np.arange(len(unique_hotels))

# Mapear ids de hoteles y usuarios en los datos
hotel_to_user_mapping = dict(zip(unique_hotels, unique_users))
user_to_hotel_mapping = dict(zip(unique_users, unique_hotels))

data['user_id'] = data['hotel_id'].map(hotel_to_user_mapping)

# Dividir datos en conjunto de entrenamiento y prueba
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Definir modelo de recomendación


class HotelModel(tfrs.Model):
    def __init__(self):
        super().__init__()
        self.embedding_dimension = 32

        # Definir capas de embedding para usuarios, hoteles, estados y ciudades
        self.hotel_embeddings = tf.keras.layers.Embedding(
            input_dim=len(unique_hotels) + 1,
            output_dim=self.embedding_dimension
        )
        self.user_embeddings = tf.keras.layers.Embedding(
            input_dim=len(unique_users) + 1,
            output_dim=self.embedding_dimension
        )
        self.state_embeddings = tf.keras.layers.Embedding(
            input_dim=len(data['state'].unique()) + 1,
            output_dim=self.embedding_dimension
        )
        self.city_embeddings = tf.keras.layers.Embedding(
            input_dim=len(data['city'].unique()) + 1,
            output_dim=self.embedding_dimension
        )

        # Definir capa de producto punto para calcular similitud entre usuarios y hoteles
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=unique_hotels.tolist()
            )
        )

    def compute_loss(self, features, training=False):
        hotel_embeddings = self.hotel_embeddings(features['hotel_id'])
        user_embeddings = self.user_embeddings(features['user_id'])
        state_embeddings = self.state_embeddings(features['state'])
        city_embeddings = self.city_embeddings(features['city'])

        return self.task(user_embeddings + state_embeddings + city_embeddings, hotel_embeddings)


# Crear dataset de TensorFlow
train_dataset = tf.data.Dataset.from_tensor_slices(dict(train_data))
test_dataset = tf.data.Dataset.from_tensor_slices(dict(test_data))

# Configurar modelo y entrenamiento
model = HotelModel()
model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))

# Entrenar el modelo
model.fit(train_dataset.batch(32), epochs=10)

# Solicitar entrada del usuario para la ciudad y el estado
city = input("Ingrese la ciudad: ")
state = input("Ingrese el estado: ")

# Generar recomendaciones para la ciudad y el estado proporcionados por el usuario
# Asignar un nuevo ID de usuario para la entrada del usuario
user_id = len(unique_users) + 1
city_embedding = model.city_embeddings(
    tf.constant([city]))  # Obtener embedding de la ciudad
state_embedding = model.state_embeddings(
    tf.constant([state]))  # Obtener embedding del estado
user_embedding = model.user_embeddings(
    tf.constant([user_id]))  # Obtener embedding del usuario
query_embedding = user_embedding + city_embedding + \
    state_embedding  # Combinar embeddings

# Obtener las 5 mejores recomendaciones para la entrada del usuario
top_recommendations = model.task.recommend(
    query_embedding, candidates=tf.constant(unique_hotels), k=5)
top_hotel_ids = top_recommendations[0].numpy()

# Imprimir los IDs de los hoteles recomendados
print("Los mejores hoteles recomendados son:")
for hotel_id in top_hotel_ids:
    print(user_to_hotel_mapping[hotel_id])
