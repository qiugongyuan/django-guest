from django.test import TestCase
from sign.models import Event,Guest

# Create your tests here.
class  ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1,name="oneplus 3 event",status=True,limit=200,
                             address="shenzhen",start_time='2021-07-05')
        Guest.objects.create(id=1,event_id=1,realname='kara',phone='18511852667',
        Email='kara@tom.com',sign=False)


    def test_event_models(self):
        #python manage.py test sign.tests.ModelTest.test_event_models
        result=Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address,"Beijing")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result=Guest.objects.get(phone='18511852667')
        self.assertEqual(result.realname,'kara')
        self.assertFalse(result.sign)