from rest_framework import serializers

class MLDataSerializer(serializers.Serializer):
    strings = serializers.ListField(child=serializers.CharField(), required=False)
    integers = serializers.ListField(child=serializers.IntegerField(), required=False)
    base64_frames = serializers.ListField(child=serializers.CharField(), required=True)  # List of base64-encoded image strings (frames)