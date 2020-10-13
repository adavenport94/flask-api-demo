try:
    from app import app
    import unittest

except Exception as e:
    print("Missing Modules {}".format(e))


POLICYHOLDER_PAYLOAD = {'gender': 'Female', 'date_of_birth': '2/6/1960', 'ssn': 111223333, 'smoking_status': True,
                        'allergies': 'Nuts, Pollen', 'medical_conditions': 'Asthma, Hypertension'}

INSURED_EVENT_PAYLOAD = {'date_of_incidence': '10/6/2020', 'billed_amount': 250.99, 'covered_amount': 170.49,
                         'type_of_issue': 'Broken Foot', 'policyholder_id': 1}


class TestRoutes(unittest.TestCase):

    def test_healthcheck(self):
        tester = app.test_client(self)
        response = tester.get('/healthcheck')
        self.assertEqual(response.status_code, 200)

    def test_policyholder_create(self):
        tester = app.test_client(self)
        response = tester.post('/policyholder/create_insured', json=POLICYHOLDER_PAYLOAD)
        self.assertEqual(response.status_code, 200)

    def test_policyholder(self):
        tester = app.test_client(self)
        response = tester.get('/policyholder/')
        self.assertEqual(response.status_code, 200)

    def test_insured_event(self):
        tester = app.test_client(self)
        response = tester.get('/insured_event/')
        self.assertEqual(response.status_code, 200)

    def test_insured_event_create(self):
        tester = app.test_client(self)
        response = tester.post('/insured_event/create_insured_event', json=INSURED_EVENT_PAYLOAD)
        self.assertEqual(response.status_code, 200)

    def test_bad_insured_event_create(self):
        tester = app.test_client(self)
        response = tester.get('/insured_event/create_insured_event')
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
