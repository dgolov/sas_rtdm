from django.db import models


class CheckSAS(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'time create: {}'.format(self.time_create)


class Diagram(models.Model):
    name = models.CharField(max_length=128)
    diagram_list = models.ForeignKey(CheckSAS, on_delete=models.CASCADE)


class SubDiagram(models.Model):
    did = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    source = models.CharField(max_length=128)
    diagram = models.ForeignKey(Diagram, on_delete=models.CASCADE)

    def __str__(self):
        return 'id: {}, name: {}'.format(self.did, self.name)


class Processes(models.Model):
    pid = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    source = models.CharField(max_length=128, default=None)
    table_name = models.CharField(max_length=128)
    diagram = models.ForeignKey(Diagram, on_delete=models.CASCADE)

    def __str__(self):
        return 'id: {}, name: {}, table: {}'.format(self.pid, self.name, self.table_name)


class Input(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    physical_name = models.CharField(max_length=128)
    processes = models.ForeignKey(Processes, on_delete=models.CASCADE)

    def __str__(self):
        return 'name: {} --- type: {}'.format(self.name, self.type)


class Output(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    physical_name = models.CharField(max_length=128)
    processes = models.ForeignKey(Processes, on_delete=models.CASCADE)

    def __str__(self):
        return 'name: {} --- type: {}'.format(self.name, self.type)
