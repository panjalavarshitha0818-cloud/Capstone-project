from rest_framework import serializers
from .models import StudyTask

class StudyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyTask
        fields = ['id', 'title', 'description', 'subject', 'priority', 'due_date', 'estimated_time', 'is_completed']
