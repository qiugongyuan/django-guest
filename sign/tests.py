from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User
from sign.models import Event
from sign.models import Guest
# Create your tests here.
#python manage.py test
#python manage.py test sign
#python manage.py test sign.tests
#python manage.py test sign.tests.ModuleTest
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


# "测试登录首页"

class IndexPageTest(TestCase):

    def test_index_page_render_index_template(self):
        responese=self.client.get('/index/')
        self.assertEqual(responese.status_code,200)
        self.assertTemplateUsed(responese,'index.html')
"测试登录动作"
class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','test')
        #setUp()初始化方法中，调用User.objects.create_user()创建登录用户数据
    def test_add_admin(self):#测试添加用户
        user=User.objects.get(username="admin")
        self.assertEqual(user.username,'admin')
        self.assertEqual(user.email,"admin@mail.com")

    def test_login_action_username_password_null(self):
        test_data={'username':'','password':''}
        response=self.client.post('/login_action/',data=test_data)
        #通过post方法请求/login_action/路径测试登录功能
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)
        #assertIn（）方法断言返回的HTML页面中是否有包含’username or password error!‘


    def test_login_action_username_password_error(self):
        test_data={'username':'admin','password':'error'}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)

    def test_login_action_username_password_success(self):
        test_data={'username':'admin','password':'test'}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,302)
        #用户登录成功之后，通过HttpResponseRedirect()重定向到了/event_manage/，所以状态码是302


#发布会管理
class EventManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','test')
        Event.objects.create(id=3,name="oneplus 3 event", status=True, limit=200,
                             address="shenzhen", start_time='2021-06-30 07:44:06')
        test_data={'username':'admin','password':'test'}
        self.client.post('/login_action/',data=test_data)


    def test_add_event_data(self):
        event=Event.objects.get(name='oneplus 3 event')
        self.assertEqual(event.address,'shenzhen')


    def test_event_manage_success(self):
        response=self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        print(response.content)
        self.assertIn(b'oneplus 3 event',response.content)
        self.assertIn(b'shenzhen',response.content)

    def test_event_manage_search_success(self):
        response=self.client.post('/search_name/',{"name":'oneplus 3 event'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'oneplus 3 event',response.content)
        self.assertIn(b'oneplus 3 event',response.content)

#测试嘉宾管理页面

class GuestManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','test')
        Event.objects.create(id=3, name="oneplus 3 event", status=True, limit=200,
                             address="shenzhen", start_time='2021-06-30 07:44:06')

        Guest.objects.create(event_id=3, realname='xiaoran', phone='18511852667',
                             Email='kara@tom.com', sign=0)
        test_data = {'username': 'admin', 'password': 'test'}
        self.client.post('/login_action/', data=test_data)


    def test_add_Guest_data(self):
        guest=Guest.objects.get(realname='xiaoran')
        self.assertEqual(guest.phone,'18511852667')



    def test_guest_manage_success(self):
        response=self.client.post('/guest_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'xiaoran',response.content)
        self.assertIn(b'18511852667',response.content)

    def test_guest_manage_search_success(self):
        response = self.client.post('/search_phone/', {"phone": '18511852667'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaoran', response.content)
        self.assertIn(b'18511852667', response.content)
#测试用户签到
class SignIndexActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','test')
        Event.objects.create(id=2, name="oneplus 2 event", status=True, limit=200,
                             address="shenzhen", start_time='2021-06-30 07:44:06')
        Event.objects.create(id=1, name="oneplus 1 event", status=True, limit=200,
                             address="Beijing", start_time='2021-06-30 07:44:06')

        Guest.objects.create(event_id=1, realname='xiaoran', phone='18511852667',
                             Email='kara1@tom.com', sign=0)
        Guest.objects.create(event_id=2, realname='rankun', phone='15330235989',
                             Email='kara2@tom.com', sign=1)
        test_data = {'username': 'admin', 'password': 'test'}
        self.client.post('/login_action/', data=test_data)

    def test_sign_index_action_phone_null(self):
      responese=self.client.post('/sign_index_action/1/',{'phone':''})
      self.assertEqual(responese.status_code,200)
      self.assertIn(b'phone error',responese.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        response=self.client.post('/sign_index_action/1/',{'phone':'15330235989'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'phone error', response.content)

    def test_sign_index_action_user_sign_has(self):
        response=self.client.post('/sign_index_action/2/',{'phone':'15330235989'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user has sign in', response.content)

    def test_sign_index_action_sign_success(self):
        response=self.client.post('/sign_index_action/1/',{'phone':'18511852667'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign in success', response.content)
        self.assertIn(b'18511852667',response.content)
        print(response.content)
        self.assertIn(b'xiaoran',response.content)















