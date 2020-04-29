import random
import string
from ..dummy import DummyTest
from app.models import Qso
from app import db


# example class that will host tests
class SimpleTests(DummyTest):

    def dummySetup(self):
        self.simple = True

    def test_harness(self):
        # basic check of the test infrastructure
        assert(self.simple)
        self.assertRaisesException(lambda : self.net.show(), msgExpect = "show")

    def test_db_read_write(self):
        letters = string.ascii_letters
        callsign = (''.join(random.choice(letters) for i in range (10)))
        signal_sent = 59
        signal_received = 59
        custom_sent = 59
        custom_received = 59
        frequency_used = "14.225"

        q = Qso(callsign=callsign,  signal_sent=signal_sent, signal_received=signal_received, custom_sent=custom_sent, custom_received=custom_received, frequency_used=frequency_used)

        db.session.add(q)
        db.session.commit()

        read_qso = Qso.query.filter_by(callsign=callsign).first()
        assert (read_qso == q)

