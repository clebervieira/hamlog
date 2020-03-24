import json
from datetime import datetime


def write_qso(call_sign, signal_received, signal_sent):
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


def read_qso():
    file = open("data.json", "r")
    print(file.read())


'''
    data = file.read()
    print(json.dumps(data, sort_keys=True, indent=4))
'''

if __name__ == '__main__':

    write_qso("w6cbr", "59", "59")
    write_qso("kg6nui", "48", "37")

    read_qso()