import json
import os
from datetime import datetime


class LogNewQSO:
    def __init__(self, call_sign, signal_received, signal_sent):
        self.call_sign = call_sign
        self.signal_received = signal_received
        self.signal_sent = signal_sent
        self.data = {}
        self.data['QSO'] = []
        if os.path.exists("data.json"):
            self.read_qso()


    def write_qso(self, call_sign, signal_received, signal_sent):
        self.data['QSO'].append({
            'Call Sign': call_sign,
            'Signal Sent': signal_sent,
            'Signal Received': signal_received,
            'Time Stamp': str(datetime.utcnow())
            })
        with open('data.json', 'w') as outfile:
            json.dump(self.data, outfile)


    def read_qso(self):
        file = open("data.json", "r")
        #listqso = file.read()
        data = file.read()
        #print(data)
        self.data = json.loads(data)


    def build_string(self):
        prettyqso = (json.dumps(self.data, sort_keys=True, indent=4))
        return prettyqso


if __name__ == '__main__':

    log = LogNewQSO("call_sign", "signal_sent", "signal_received")
    log.write_qso("xxvdx", "59", "59")
    #LogNewQSO.write_qso("","kg6nui", "48", "37")

    print(log.build_string())

    '''
        filename as parameter
        split write_qso into 2, create and write
    '''