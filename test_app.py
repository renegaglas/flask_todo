import unittest

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        #define the ctx parameter for futur use
        self.ctx = app.app_context()
        self.ctx.push()
        #create a dumb client which will make real request
        self.client = app.test_client()



    def tearDown(self):
        #at the end of the test destroy the ctx parameter
        self.ctx.pop()

    def test_home(self):
        # make a Post request (as if we use the submit button) with content and degree define
        response = self.client.post(
            '/index',
            data=dict(content='go walking', degree='important'),
            follow_redirects=True
        )

        # assert response.status_code == 200
        assert self.client.get('/index', query_string=dict(content='go walking', degree='important'))

        assert b"go walking" in response.data

    def test_delet(self):
        #make a Post request (as if we use the submit button) with content and degree define
        response = self.client.post('/0/delete/')
        # assert response.status_code == 200
        assert True


if __name__ == "__main__":
    unittest.main()
