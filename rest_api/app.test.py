import unittest
from app import app

URL = 'http://127.0.0.1:5000'

class LinksApiRouting(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client()

    def testGet(self):
        response = self.test_client.get(URL + '/links')
        data = response.get_json()
        assert len(data) == 2
        assert response.status_code == 202

    def testPost(self):
        new_post = {"title": "test", "url": "https://test.test"}
        response = self.test_client.post('/links', json=new_post)
        data = response.get_json()
        assert len(self.test_client.get('/links').get_json()) == 3
        assert data['message'] == 'Success!'
        assert response.status_code == 201


class LinkApiRouting(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client()

    def testGet(self):
        response = self.test_client.get('/link/1')
        data = response.get_json()
        title = data['title']
        url = data['url']
        assert title == 'oop basics'
        assert url == 'htttp://'
        assert response.status_code == 202
    
    def testGetInvalidId(self):
        response = self.test_client.get('/link/999')
        data = response.get_json()
        assert data['message'] == 'not found'
        assert response.status_code == 404

    def testPut(self):
        updated_link = {"title": "new_title", "url":"new_url"}
        response = self.test_client.put('/link/1', json=updated_link)
        data = response.get_json()

        updated_response = self.test_client.get('/link/1')
        updated_data = updated_response.get_json()

        assert (updated_data['title'], updated_data['url']) == ('new_title', 'new_url')
        assert data['message'] == 'success'
        assert response.status_code == 201

    def testPutInvalidId(self):
        updated_link = {"title": "new_title", "url":"new_url"}
        response = self.test_client.put('/link/999', json=updated_link)
        data = response.get_json()


        assert data['message'] == 'not found'
        assert response.status_code == 404

    def testPutInvalidPayload(self):
        updated_link = {"tilte": "new_title", "uli":"new_url"}


        response = self.test_client.put('/link/1', json=updated_link)
        data = response.get_json()


        assert data['message'] == 'invalid payload'
        assert response.status_code == 400
if __name__ == '__main__':
    unittest.main()