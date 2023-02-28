from rest_framework import serializers
from proyecto.models.general import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields= '__all__'