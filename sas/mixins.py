from django.views.generic import View
import requests


class RequestDataMixin(View):
    def __init__(self):
        super(RequestDataMixin, self).__init__()
        self.host = 'http://217.73.57.195/'
        token = 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vbG9jYWxob3N0L1NBU0xvZ29uL3Rva2VuX2tleXMiLCJraWQiOiJsZWdhY3ktdG9rZW4ta2V5IiwidHlwIjoiSldUIn0.eyJqdGkiOiI3ZmZlNzJmM2FhMTM0M2YyOGEwNzdiZWU5NGE3N2I0MSIsImV4dF9pZCI6InVpZD1zYXNkZW1vLG91PXBlb3BsZSxkYz1sb2NhbGhvc3QsZGM9bG9jYWxkb21haW4iLCJzdWIiOiJlOTdjYTQ4OS04YTFlLTRiMGItOWFmNi1kMzRkM2FhNmQ4NGEiLCJzY29wZSI6WyJvcGVuaWQiXSwiY2xpZW50X2lkIjoiaGFjayIsImNpZCI6ImhhY2siLCJhenAiOiJoYWNrIiwiZ3JhbnRfdHlwZSI6InBhc3N3b3JkIiwidXNlcl9pZCI6ImU5N2NhNDg5LThhMWUtNGIwYi05YWY2LWQzNGQzYWE2ZDg0YSIsIm9yaWdpbiI6ImxkYXAiLCJ1c2VyX25hbWUiOiJzYXNkZW1vIiwiZW1haWwiOiJzYXNkZW1vQHVzZXIuZnJvbS5sZGFwLmNmIiwiYXV0aF90aW1lIjoxNjIyMzMzMzEwLCJyZXZfc2lnIjoiOWVhMTdlMDEiLCJpYXQiOjE2MjIzMzMzMTAsImV4cCI6MTYyMjM3NjUwOSwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdC9TQVNMb2dvbi9vYXV0aC90b2tlbiIsInppZCI6InVhYSIsImF1ZCI6WyJoYWNrIiwib3BlbmlkIl19.fHuJnY9XEuSZlXaV6gtMOhxzJ2AGaduyDUS_pOaCmDoOL_zt97H1_DYW4mdIhd7wHVuFXEjtpTWTecBeD86AoGfxam-Vn-RF1gZTCdaOCVodpb1V3Da0A_T-ZR79A1IvtFWma0p33jSJysHL8pI9jEry4NO_IGKecYXfvV_ZNht6USkXuC34LILsMekh4P7gzbIczrrtP3-AtMpnmlT682c2Q9rBJ0yxlsOq7OqnMCkwvwX7Y1tb4OSF_u3pp60vpVg_rpniJF1U2PEUXqw0l7Mx4bEVjyypBZudzAivxI6q7zu9k21CPPDm-wDiRycWSmT-9jv6A0T-GgXsDFRFvQ'
        self.headers = {
            'authorization': 'Bearer ' + token,
            'content-type': "application/json",
        }

    def get_token(self):
        url = 'http://217.73.57.195/SASLogon/oauth/clients/consul?callback=false&serviceId=sas'
        headers = {
            'X-CONSUL-TOKEN': '50a4b0e1-039a-4ef9-ba24-76ffa7e724a8',
        }
        response = requests.post(url, headers)
        access_token = response.text
        print(access_token)
        return access_token
