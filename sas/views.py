from django.shortcuts import render
from django.views import View
from scp import SCPClient
from .mixins import RequestDataMixin
from .utils import Parser
import requests
import paramiko


class DetailDecisionsView(RequestDataMixin, View):
    """ Get -запрос, который позволяет по sourceURI определить подробные параметры решения.
    """
    def __init__(self):
        super(DetailDecisionsView, self).__init__()
        self.sourceURI = '9c529dea-6b72-4fee-bffb-368a75bc07a3/revisions/164159ad-b9df-423b-b304-389c5bbe3859'
        self.signatures_list = []
        self.signatures_dict = {}

    def get(self, request, *args, **kwargs):
        self.get_token()
        response_SAS = requests.get(self.host + 'decisions/flows/' + self.sourceURI, headers=self.headers)
        content = response_SAS.json()
        context = {'title': "Подробные параметры решения", 'content': content['signature']}
        return render(request, 'sas_rtdm/sas_id_data.html', context)


class DecisionsView(RequestDataMixin, View):
    """ Get -запрос, который позволяет по sourceURI определить подробные параметры решения.
    """
    def __init__(self):
        super(DecisionsView, self).__init__()
        self.sourceURI = ''
        self.signatures_list = []
        self.signatures_dict = {}

    def get(self, request, *args, **kwargs):
        self.get_token()
        response_SAS = requests.get(self.host + 'decisions/flows/' + self.sourceURI, headers=self.headers)
        content = response_SAS.json()
        context = {'title': "Параметры решения", 'content': content['items']}
        return render(request, 'sas_rtdm/sas_id_data.html', context)


class CheckRulesSetView(RequestDataMixin, View):
    """ Get -запрос, который позволяет определить все существующие на сервере rule sets.
    """
    def __init__(self):
        super(CheckRulesSetView, self).__init__()

    def get(self, request, *args, **kwargs):
        response_SAS = requests.get(self.host + '/businessRules/ruleSets', headers=self.headers)
        content = response_SAS.json()
        context = {'title': "Наборы правил", 'content': content['items']}
        return render(request, 'sas_rtdm/sas_id_data.html', context)


class CheckLookups(RequestDataMixin, View):
    """ Get -запрос, который позволяет определить все существующие на сервере rule sets.
    """
    def __init__(self):
        super(CheckLookups, self).__init__()

    def get(self, request, *args, **kwargs):
        response_SAS = requests.get(
            self.host + '/referenceData/domains',headers=self.headers)
        content = response_SAS.json()
        context = {'title': "Наборы правил", 'content': content['items']}
        return render(request, 'sas_rtdm/sas_id_data.html', context)


class GetRTDMData(View):
    def __init__(self):
        super(GetRTDMData, self).__init__()
        self.host = '217.73.57.195'
        self.url = 'http://' + self.host + ':7980/SASCIStudio'
        self.user = 'sas'
        self.password = '#Orion123_'
        self.port = 22

    def get(self, request, *args, **kwargs):
        self.download_xml()
        parser = Parser('out.xml')
        content = parser.parse_xml()
        context = {'title': 'Title', 'content': content}
        return render(request, 'sas_rtdm/sas_rtdm_data.html', context)

    def download_xml(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=self.host,
            username=self.user,
            password=self.password,
            port=self.port,
            banner_timeout=400,
            auth_timeout=200)
        stdin, stdout, stderr = client.exec_command('sudo -S rm *')
        stdin.write(self.password + '\n')
        stdin.flush()

        stdin, stdout, stderr = client.exec_command(
            '/opt/sas/sashome/SASMarketingAutomationIntegrationUtilities/6.6/sasmaextract cisample@saspw Orion123 DefaultAuth "HACK" "/opt/sas/sashome/SASMarketingAutomationIntegrationUtilities/6.6/request.xml" "/opt/sas/sashome/SASMarketingAutomationIntegrationUtilities/6.6/out.xml"')
        data = stdout.read() + stderr.read()
        scp = SCPClient(client.get_transport())
        scp.get('/opt/sas/sashome/SASMarketingAutomationIntegrationUtilities/6.6/out.xml')
        client.close()
        scp.close()
        return data.decode('UTF-8')


# def my_custom_sql():
#     a = []
#     with connection.cursor() as cursor:
#         result = cursor.execute('''SELECT
#         TABLE_NAME,
#         COLUMN_NAME,
#         DATA_TYPE,
#         IS_NULLABLE
#         FROM INFORMATION_SCHEMA.COLUMNS
#         WHERE table_name='ADDRESS'
#         ''')
#         for item in result:
#             a.append(item)
#     return a
