from django.shortcuts import render
from django.views import View
from django.db import connections
from scp import SCPClient
from .mixins import RequestDataMixin
from .models import SubDiagram, Processes, Input, Output, Diagram, CheckSAS
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
        print(content)
        for item in content:
            print(item, type(item))
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
        response_SAS = requests.get(self.host + '/decisions/flows/bc24bee2-138e-4e2c-9be4-5f343565b9e4/revisions/2c9a6954-b0ca-4128-94e0-11e3c8a1204f' + self.sourceURI, headers=self.headers)
        content = response_SAS.json()
        print(content)
        context = {'title': "Параметры решения", 'content': None}
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
    """ Get -запрос, который позволяет определить все существующие на сервере check lookups.
    """
    def __init__(self):
        super(CheckLookups, self).__init__()

    def get(self, request, *args, **kwargs):
        response_SAS = requests.get(
            self.host + '/referenceData/domains', headers=self.headers)
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
        self.xml_files = [
            'request_main.xml', 'request_result.xml', 'request_client.xml', 'request_doc.xml', 'request_address.xml']

    def get(self, request, *args, **kwargs):
        dead_process = []
        new_check = CheckSAS.objects.create()

        for file in self.xml_files:
            self.download_xml(file=file)
            parser = Parser('out.xml')
            parser.parse_xml(new_check)

        context = self.get_last_check_data()
        for process in context['processes']:
            if process.source == 'Cell':
                dead_process.append(process)

        check_result = self.search_dependencies(request)
        context['dead'] = dead_process
        context['input'] = check_result[0]
        context['output'] = check_result[1]
        context['title'] = 'Check RTDM and MSSQL data'

        return render(request, 'sas_rtdm/index.html', context=context)

    def download_xml(self, file):
        """ Отправляет имя исполняемого xml файла на сервер и загружает out.xml с результатами запроса """
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
            f'/opt/sas/sashome/SASMarketingAutomationIntegrationUtilities/6.6/sasmaextract cisample@saspw Orion123 DefaultAuth "HACK" "/opt/sas/sashome/SASMarketingAutomationIntegrationUtilities/6.6/{file}" "/opt/sas/sashome/SASMarketingAutomationIntegrationUtilities/6.6/out.xml"')
        data = stdout.read() + stderr.read()
        scp = SCPClient(client.get_transport())
        scp.get('/opt/sas/sashome/SASMarketingAutomationIntegrationUtilities/6.6/out.xml')
        client.close()
        scp.close()

        return data.decode('UTF-8')

    @staticmethod
    def get_last_check_data():
        """ Возвращает результаты последней проверки SAS """
        last_check_date = CheckSAS.objects.last()
        diagrams = Diagram.objects.filter(diagram_list=last_check_date)
        sub_diagrams = SubDiagram.objects.filter(diagram__in=diagrams)
        processes = Processes.objects.filter(diagram__in=diagrams)
        input_values = Input.objects.filter(processes__in=processes)
        output_values = Output.objects.filter(processes__in=processes)
        return {
            'last_check_date': last_check_date,
            'diagrams': diagrams,
            'sub_diagrams': sub_diagrams,
            'processes': processes,
            'input_values': input_values,
            'output_values': output_values
        }

    @staticmethod
    def get_mssql_data(request):
        """ Подключается к MSSQL на сервере, выполняет запросы на получение данных """
        table_names = []
        table_results = []
        subject = ''
        with connections['ms'].cursor() as cursor:
            if subject == '':
                items = cursor.execute('''SELECT TABLE_NAME
                                        FROM INFORMATION_SCHEMA.TABLES
                                        WHERE table_type='BASE TABLE' AND TABLE_NAME != 'sysdiagrams'
                                        ''')
                for item in items:
                    table_names.append(item)
            else:
                for item in subject:
                    table_names.append(item)
            for table_name in table_names:
                items = (cursor.execute('''SELECT
                                TABLE_NAME,
                                COLUMN_NAME,
                                DATA_TYPE,
                                IS_NULLABLE
                                FROM INFORMATION_SCHEMA.COLUMNS
                                WHERE table_name={}
                                '''.format('\'' + str(table_name[0]) + '\'')))
                for item in items:
                    table_results.append(item)
        return table_results

    @staticmethod
    def standardization_data_type(type_list):
        """ Приводит значения типов данных в RTDM и MSSQL к одномуц стандарту
        :param type_list: - список данных
        """
        result_list = []
        for value in type_list:
            if value.type == 'data grid':
                refactoring_value = 'data'
            elif value.type == 'date list':
                refactoring_value = 'data'
            elif value.type == 'double list':
                refactoring_value = 'double'
            elif value.type == 'string list':
                refactoring_value = 'string'
            else:
                refactoring_value = value.type
            result_list.append([value.processes.table_name, value.name, refactoring_value])
        return result_list

    def search_dependencies(self, request):
        """ Находит зависимости между данными с БД и c SAS RTDM """
        sql_data = self.get_mssql_data()
        last_check = self.get_last_check_data()
        comparison_input_data_list = []
        comparison_output_data_list = []
        similarity_list = []

        for item in sql_data:
            if item[2] == 'numeric':
                item[2] = 'double'
            if item[2] == 'nvarchar' or item[2] == 'varchar' or item[2] == 'string list':
                item[2] = 'string'
            result_sql_list = [item[0], item[1], item[2]]
            similarity_list.append(result_sql_list)

        refactoring_input_data_list = self.standardization_data_type(last_check['input_values'])
        refactoring_output_data_list = self.standardization_data_type(last_check['output_values'])

        for item in refactoring_input_data_list:
            if item not in similarity_list:
                comparison_input_data_list.append(item)

        for item in refactoring_output_data_list:
            if item not in similarity_list:
                comparison_output_data_list.append(item)

        return [comparison_input_data_list, comparison_output_data_list]
