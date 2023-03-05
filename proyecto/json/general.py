from rest_framework import serializers
from proyecto.models.general import Proyecto
from proyecto.models.general import Gantt

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields= '__all__'

class GanttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gantt
        fields= '__all__'