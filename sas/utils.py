from .models import SubDiagram, Processes, Input, Output, Diagram
from xml.dom import minidom


class Parser:
    def __init__(self, path):
        self.dom = minidom.parse(path)
        self.dom.normalize()

    @staticmethod
    def get_variable_info(variable_list):
        """ Проходит по элементу входящих или исходящих переменных процесса
            и извлекает из него название переменной и ее тип данных и имя в диаграме
        :param variable_list: - элемент документа xml
        :return: название, тип данных и имя в диаграмме
        """
        for item in variable_list:
            name = item.getElementsByTagName('Name')
            variable_type = item.getElementsByTagName('TypeDescription')
            physical_name = item.getElementsByTagName('PhysicalName')
            name = name[0].childNodes[0].nodeValue
            variable_type = variable_type[0].childNodes[0].nodeValue
            physical_name = physical_name[0].childNodes[0].nodeValue
            yield name, variable_type, physical_name

    def get_self_diagrams_info(self) -> list:
        """ Получение информации о диаграмах """
        diagrams_list = []
        diagram_node = self.dom.getElementsByTagName('SubDiagramNodeDataDO')

        for item in diagram_node:
            diagram_id = item.getAttribute('objid')
            name = item.getElementsByTagName('NodeName')
            name = name[0].childNodes[0].nodeValue
            request_vars = item.getElementsByTagName('ValueTypeVarInfoDO')
            for elem in request_vars:
                source_name = elem.getElementsByTagName('VarInfoSourceName')
                source_name = source_name[0].childNodes[0].nodeValue

            diagrams_list.append({
                'id': diagram_id,
                'name': name,
                'source': source_name,
            })

        return diagrams_list

    def get_processes_info(self) -> list:
        processes_list = []
        process_node = self.dom.getElementsByTagName('ProcessNodeDataDO')

        for item in process_node:
            input_result_list = []
            output_result_list = []
            # Название процесса
            process_name = item.getElementsByTagName('NodeName')
            process_name = process_name[0].childNodes[0].nodeValue
            # ID процесса
            process_id = item.getElementsByTagName('Process')
            process_id = process_id[0].getAttribute('objid')
            # Тип входящих данных
            input_variable_list = item.getElementsByTagName('InputVariableList')
            for input_var in input_variable_list:
                IBVariableDO = input_var.getElementsByTagName('IBVariableDO')
                for in_variable_name, in_variable_type, in_physical_name in self.get_variable_info(IBVariableDO):
                    input_result_list.append((in_variable_name, in_variable_type, in_physical_name))
            # Тип исходящих данных
            output_variable_list = item.getElementsByTagName('OutputVariableList')
            for output_var in output_variable_list:
                IBVariableDO = output_var.getElementsByTagName('IBVariableDO')
                for out_variable_name, out_variable_type, out_physical_name in self.get_variable_info(IBVariableDO):
                    output_result_list.append((out_variable_name, out_variable_type, out_physical_name))
            # На кого ссылается
            var_info_source_name = item.getElementsByTagName('OutputNodeName')
            var_info_source_name = var_info_source_name[0].childNodes[0].nodeValue
            # Имя таблицы
            table_name = item.getElementsByTagName('TableName')
            table_name = table_name[0].childNodes[0].nodeValue

            processes_list.append({
                'id': process_id,
                'name': process_name,
                'input': input_result_list,
                'output': output_result_list,
                'source': var_info_source_name,
                'table_name': table_name,
            })

        return processes_list

    def parse_xml(self, new_check) -> dict:
        FlowDO = self.dom.getElementsByTagName('FlowDO')
        diagram_name = FlowDO[0].getElementsByTagName('EventName')
        diagram_name = diagram_name[0].childNodes[0].nodeValue[:-6]
        sub_diagrams_list = self.get_self_diagrams_info()
        processes_list = self.get_processes_info()
        self.create_models(diagram_name, processes_list, sub_diagrams_list, new_check)
        return {
            'processes': processes_list,
            'subdiagrams': sub_diagrams_list,
        }

    @staticmethod
    def create_models(diagram_name, processes_list, sub_diagrams_list, new_check):
        diagram = Diagram.objects.create(name=diagram_name, diagram_list=new_check)
        for sub_diagram in sub_diagrams_list:
            SubDiagram.objects.create(
                did=sub_diagram['id'],
                name=sub_diagram['name'],
                source=sub_diagram['source'],
                diagram=diagram)

        for process in processes_list:
            Diagram.objects.filter(name=process['source'])
            new_process = Processes.objects.create(
                pid=process['id'],
                name=process['name'],
                source=process['source'],
                table_name=process['table_name'],
                diagram=diagram)
            for item_input in process['input']:
                Input.objects.create(
                    name=item_input[0],
                    type=item_input[1],
                    physical_name=item_input[2],
                    processes=new_process)
            for item_output in process['output']:
                Output.objects.create(
                    name=item_output[0],
                    type=item_output[1],
                    physical_name=item_output[2],
                    processes=new_process)
