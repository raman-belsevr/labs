from flask import Flask, request
from flask_restful import Resource, Api
from pilot import Pilot

app = Flask(__name__)
api = Api(app)


class PilotAction(Resource):

    def __init__(self):
        self.action_switcher = {
            "init": self.handle_init(),
            "status": self.handle_status(),
            "fly": self.handle_fly(),
            "land": self.handle_land(),
            "off": self.handle_off()
        }
        self.pilot = Pilot()

    def handle_init(self, data):
        self.pilot.start()

    def handle_status(self, data):
        self.pilot.status(self)

    def handle_fly(self, data):
        self.pilot.fly(data)

    def handle_land(self, data):
        self.pilot.land(data)

    def handle_off(self, data):
        self.pilot.end(data)

    def get(self, action_id):
        action = self.action_switcher.get(action_id)
        data = request.form['data']
        return {action_id: action(data)}

api.add_resource(PilotAction, '/<string:action_id>')

if __name__ == '__main__':
    app.run(debug=True)

