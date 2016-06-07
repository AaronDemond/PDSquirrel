from django.test import TestCase
from django.core.files import File
from django.contrib.auth import  hashers
from pds_v3.models import AppUser, LawSociety, PdSession, Presenter, Subject
from django.contrib.auth.models import User
from django.test import TestCase, Client

class test_gen(TestCase):

    @classmethod
    def setUpTestData(cls):
        # -- Create law society
        cls.l = LawSociety(name='NS Bar', eligibility ='Good', overview ='VGood', website='bomb.com')
        cls.l.save()

        # -- Create appuser
        password = hashers.make_password("password")
        cls.profile = AppUser.create(first_name='test',last_name='tested', email='aarondemond@dal.ca', password=password,terms=True, society=cls.l.pk)
        cls.profile.stripe_id = 'cus_6lp6xydAhnnT0F'
        cls.profile.is_presenter = True
        cls.profile.save()


        # -- Activate user
        user = User.objects.get(username='aarondemond@dal.ca')
        user.is_active = True
        user.save()

        # -- Create a presenter, link to user
        cls.presenter = Presenter(user=user)
        cls.presenter.save()

        # -- Create a subject
        cls.subject = Subject(name='sub')
        cls.subject.save()

        # -- Create a session
        cls.pd = PdSession(name='test', description='desc', approved=False, price=9.99)
        cls.pd.audio_file = File(open('audio_files/with_rec','r'))
        cls.pd.save()
        cls.pd.subject.add(cls.subject)





    def test_presenter_upload(self):
        c = Client()
        login = c.login(username='aarondemond@dal.ca', password='password')
        audio_file = open('audio_files/with_rec')
        resume = open('attachments/aaron_demond_CV.doc')

        data = { 'name': 'AWESOME',
                'description': 'desc',
                'subject': '1',
                'audio_file': audio_file,
                'p-terms': '1'}


        data2 = { 'name': 'AWESOME2',
                'description': 'desc',
                'subject': '1',
                'audio_file': audio_file } 

        data3 = { 'name': 'AWESOME3',
                'description': 'desc',
                'subject': '1',
                'audio_file': audio_file,
                'p-terms': '1',
                'file-upload-0': resume,
                'file-upload-1': audio_file }

        resp = c.post('/user/presenter/dash/', data, follow=True)
        resp = c.post('/user/presenter/dash/', data2, follow=True)
        resp = c.post('/user/presenter/dash/', data3, follow=True)

        s = PdSession.objects.filter(name='AWESOME').exists()
        s2 = PdSession.objects.filter(name='AWESOME2').exists()
        s3 = PdSession.objects.filter(name='AWESOME3').exists()

        self.assertEqual(s, True) #Valid upload, no attach
        self.assertEqual(s2, False) #Invalid upload (did not accept terms)
        self.assertEqual(s3, True) #Valid, 2 attachments



    def test_detail(self):
        c = Client()
        resp = c.get('/pd/1/')
        self.assertEqual(resp.context['own'], 0)
        self.assertContains(resp, 'Purchase', status_code=200)

    def test_user_exists(self):
        c = Client()
        login = c.login(username='aarondemond@dal.ca', password='password')
        self.assertEqual(login, True)
        self.assertEqual(self.profile.user.first_name, 'test')


