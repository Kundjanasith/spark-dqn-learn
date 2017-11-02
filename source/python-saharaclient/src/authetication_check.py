from keystoneauth1.identity import v2
from keystoneauth1 import session
from saharaclient import client

AUTH_URL = "http://cloud.lsr.nectec.or.th:5000/v2.0"
USERNAME = "apivadee"
PASSWORD = "Apivadee#1234!"
PROJECT_ID = "90d7715e9a7d4a2b94a1cc216c68c898"

auth = v2.Password(auth_url=AUTH_URL,
                   username=USERNAME,
                   password=PASSWORD,
                   tenant_name=PROJECT_ID)

ses = session.Session(auth=auth)

sahara = client.Client('1.1', session=ses)