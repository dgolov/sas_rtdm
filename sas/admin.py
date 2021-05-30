from django.contrib import admin
from .models import SubDiagram, Processes, Input, Output, Diagram, CheckSAS


@admin.register(SubDiagram)
class SubDiagramAdmin(admin.ModelAdmin):
    list_display = ['did', 'name', 'source', 'diagram']


@admin.register(Processes)
class ProcessesAdmin(admin.ModelAdmin):
    list_display = ['pid', 'name', 'source', 'table_name', 'diagram']


@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'physical_name', 'processes']


@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'physical_name', 'processes']


@admin.register(Diagram)
class DiagramAdmin(admin.ModelAdmin):
    list_display = ['name', 'diagram_list']


@admin.register(CheckSAS)
class CheckSASAdmin(admin.ModelAdmin):
    list_display = ['time_create']
