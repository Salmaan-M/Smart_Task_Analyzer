from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    title = serializers.CharField()
    due_date = serializers.DateTimeField()
    estimated_hours = serializers.FloatField()
    importance = serializers.IntegerField(min_value=1, max_value=10)
    dependencies = serializers.ListField(child=serializers.IntegerField(), required=False)
