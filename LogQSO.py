import json


def write_qso(call_sign, signal_received, signal_sent):
    data = {}
    data['QSO'] = []
    data['QSO'].append({
        'Call Sign': call_sign,
        'Signal Sent': signal_sent,
        'Signal Received': signal_received
    })
    with open('data.txt', 'a') as outfile:
        json.dump(data, outfile)


write_qso("w6cbr", "59", "59")
write_qso("kg6nui", "48", "37")
