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


    # DB models.py test cases
    # TODO: testcases db models
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
        return callsign

    def test_db_delete(self):
        callsign = self.test_db_read_write()
        read_qso = Qso.query.filter_by(callsign=callsign).first()
        db.session.delete(read_qso)
        db.session.commit()
        print(read_qso)
        check_del_callsign = Qso.query.filter_by(callsign=callsign).first()
        print(check_del_callsign)
        assert (check_del_callsign is None)

    def test_update_db(self):
        callsign = self.test_db_read_write()
        read_qso = Qso.query.filter_by(callsign=callsign).first()
        print(read_qso)
        read_qso.signal_sent = 55
        db.session.commit()
        updated_qso = Qso.query.filter_by(callsign=callsign).first()
        print(updated_qso)
        assert (updated_qso.signal_sent == "55")

    def test_user_create(self):
        assert True

    def test_user_delete(self):
        assert True

    def test_post_create(self):
        assert True

    def test_post_delete(self):
        assert True

    #Forms forms.py test cases
    #TODO: testcase forms
    def test_RegistrationForm (self):
        assert False

    def test_LoginForm(self):
        assert False

    def test_login_form (self):
        assert True

    def test_add_qso_to_db_form(self):
        assert True

    def test_update_account_form(self):
        assert True

    def test_post_form(self):
        assert True