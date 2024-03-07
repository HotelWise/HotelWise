import requests


def send_data():
    selected_state = input("Ingrese Estado deseado: ")
    selected_city = input("Ingrese Ciudad deseada: ")

    cloud_function_url = "https://us-central1-hotelwiseweb.cloudfunctions.net/ML_HTML"
    payload = {
        "state": selected_state,
        "city": selected_city
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(cloud_function_url, json=payload, headers=headers)
    print("\nCódigo de Estado:", response.status_code)
    if response.status_code == 200:
        print("Cloud Function activado correctamente!")
        try:
            response_json = response.json()
            formatted_response = "\n".join(
                [f"{key}: {value}" for key, value in response_json.items()])

            print("Contenido de la Respuesta:\n")
            print(formatted_response)
            print("\n")
        except ValueError:
            print("Contenido de la Respuesta (raw):",
                  response.content.decode('utf-8'))
    else:
        print("Error activando la Cloud Function. Código de Estado:",
              response.status_code)
        print("Error en Contenido de la Respuesta:",
              response.content.decode('utf-8'))


send_data()
