import json
from datetime import datetime


class LogNewQSO:
    def __init__(self, call_sign, signal_received, signal_sent):
        self.call_sign = call_sign
        self.signal_received = signal_received
        self.signal_sent = signal_sent

    def write_qso(self, call_sign, signal_received, signal_sent):
        data = {}
        data['QSO'] = []
        data['QSO'].append({
            'Call Sign': call_sign,
            'Signal Sent': signal_sent,
            'Signal Received': signal_received,
            'Time Stamp': str(datetime.utcnow())
            })
        with open('data.json', 'a') as outfile:
            json.dump(data, outfile)

    def read_qso(self):
        file = open("data.json", "r")
        print(file.read())

    '''
    data = file.read()
    print(json.dumps(data, sort_keys=True, indent=4))
    '''


if __name__ == '__main__':


    LogNewQSO.write_qso("","w6cbr", "59", "59")
    LogNewQSO.write_qso("","kg6nui", "48", "37")

    LogNewQSO.read_qso("")
