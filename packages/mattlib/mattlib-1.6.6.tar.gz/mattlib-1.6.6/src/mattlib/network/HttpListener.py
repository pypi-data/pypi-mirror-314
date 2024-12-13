from flask import Flask, request

class HttpListener:
    def __init__(self, port=8080):
        self.port = port
        self.app = Flask('HttpListener')

    def get_data(self, request):
        return request.get_json()

    def respond_get(self, callback):
        try:
            callback_data = callback(*args)
            if callback_data:
                return callback_data, 204
            else:
                return '', 204
        except Exception as e:
            print(e)
            return 'Bad request', 400

    def respond_post(self, request, callback, args):
        post_data = request.get_json()
        try:
            callback_data = callback(post_data, *args)
            if callback_data:
                return callback_data, 204
            else:
                return '', 204
        except Exception as e:
            print(e)
            return 'Bad request', 400

    def listen(self, callback, args=()):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'GET':
                return self.respond_get(callback)
            if request.method == 'POST':
                return self.respond_post(request, callback, args)

        self.app.run(debug=True,
                     host='0.0.0.0',
                     port=self.port,
                     use_reloader=False)
        
