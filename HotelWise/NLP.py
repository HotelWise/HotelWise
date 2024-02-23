from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import tensorflow as tf
import pandas as pd

data = pd.read_csv('hoteles.csv')

# Preprocesamiento de datos
reviews = data['reviews'].values

# Tokenización y secuenciación

# Vocabulario máximo de 10000 palabras
tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')
tokenizer.fit_on_texts(reviews)
sequences = tokenizer.texts_to_sequences(reviews)
# Limitar la longitud máxima de las secuencias a 100 palabras
padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post')

# División de datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    padded_sequences, labels, test_size=0.2, random_state=42)

# Construccion del modelo de análisis de sentimientos
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(10000, 16, input_length=100),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Evaluación del modelo
loss, accuracy = model.evaluate(X_test, y_test)
print("Accuracy: {:.2f}%".format(accuracy * 100))

# Predicción de sentimientos
predictions = model.predict_classes(X_test)

# Agregar resultados como una nueva columna en el dataframe
data['sentimiento_predicho'] = ['positivo' if pred ==
                                1 else 'negativo' for pred in predictions]
