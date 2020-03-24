import flask
import logQSO


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>HamLog Test API</p>"

#TODO: Create a form to add values
@app.route('/submitqso', methods=['POST'])
def submitQso():
    jsonPost=flask.request.json
    logQSO.write_qso(jsonPost["callSign"],jsonPost["signalReceived"],jsonPost["signalSent"])
    return "<h1>QSO sent</h1>"


@app.route('/showlog', methods=['GET'])
def showlog():
    jsonPost = flask.request.json
    result = logQSO.read_qso()
    return result



app.run()
