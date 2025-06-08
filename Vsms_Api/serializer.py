from rest_framework import serializers
from vsmsapp.models import StudentRegistration

class Sr_Serializer(serializers.ModelSerializer):
    class Meta:

        model = StudentRegistration
        fields = '__all__'