import base64

def get_message(envelope, decode=True):
    if envelope == None:
        raise Exception("no Pub/Sub message received")

    try:
        pubsub_message = envelope["message"]
        if decode:
            message = base64.b64decode(pubsub_message["data"])\
                .decode("utf-8")\
                .strip()
        else:
            message = pubsub_message['data']
        return message
    except:
        raise Exception("invalid Pub/Sub message format")
