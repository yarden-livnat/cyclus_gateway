import unittest
import json
from testing.base import BaseTestCase



def register_user(self):
    return self.client.post(
        '/api/admin/register',
        data=json.dumps(dict(
            username='test',
            password='123456'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            username='test',
            password='123456'
        )),
        content_type='application/json'
    )

class TestAuthBlueprint(BaseTestCase):

    def test_registered_user_login(self):
            """ Test for login of registered-user login """
            with self.client:
                # user registration
                user_response = register_user(self)
                response_data = json.loads(user_response.data.decode())
                self.assertTrue(response_data['Authorization'])
                self.assertEqual(user_response.status_code, 201)

                # registered user login
                login_response = login_user(self)
                login_data = json.loads(login_response.data.decode())
                self.assertTrue(login_data['Authorization'])
                self.assertEqual(login_response.status_code, 200)

                # unregister user
                access_token = login_data['Authorization']['access_token']
                response = self.client.delete(
                    '/api/admin/unregister',
                    headers=dict(
                        Authorization='Bearer ' + access_token
                    )
                )
                data = json.loads(response.data.decode())
                self.assertTrue(data['status'] == 'success')
                self.assertEqual(response.status_code, 200)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            user_response = register_user(self)
            register_data = json.loads(user_response.data.decode())
            self.assertTrue(register_data['Authorization'])
            self.assertEqual(user_response.status_code, 201)

            # registered user login
            login_response = login_user(self)
            login_data = json.loads(login_response.data.decode())
            self.assertTrue(login_data['Authorization'])
            self.assertEqual(login_response.status_code, 200)

            # valid token logout
            access_token = login_data['Authorization']['access_token']
            response = self.client.post(
                '/api/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + access_token
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

            # unregister user
            login_response = login_user(self)
            login_data = json.loads(login_response.data.decode())
            self.assertTrue(login_data['Authorization'])
            self.assertEqual(login_response.status_code, 200)

            access_token = login_data['Authorization']['access_token']
            response = self.client.delete(
                '/api/admin/unregister',
                headers=dict(
                    Authorization='Bearer ' + access_token
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
