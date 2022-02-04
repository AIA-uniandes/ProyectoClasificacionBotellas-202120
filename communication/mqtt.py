import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code ")
    # en este metodo se deben iniciar las subscribciones  a los topicos deseados del servidor
    # de esta forma renueva las subscripciones si la conexion se pierde
    client.subscribe("bottle")

def connect(host, port, callback):
    mqtt_client = mqtt.Client(client_id="sfgdrtgsdrdefet4tge4t", clean_session=True)
    # asigna los metodos para eventos de on_connect y on_message
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = callback
    # Solicita conectarse a la ip y el puerto especificados
    mqtt_client.connect(host, port, 60)
    mqtt_client.loop_forever()
