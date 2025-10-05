from django.shortcuts import render

# Create your views here.
import base64
import cv2
import numpy as np
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import MLDataSerializer

class ReceiveMLDataView(APIView):
    def post(self, request):
        serializer = MLDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract data
        strings = serializer.validated_data.get('strings', [])
        integers = serializer.validated_data.get('integers', [])
        base64_frames = serializer.validated_data['base64_frames']

        # Decode base64 frames to images
        frames = []
        for b64_frame in base64_frames:
            img_data = base64.b64decode(b64_frame)
            np_arr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is not None:
                frames.append(frame)

        if not frames:
            return Response({"error": "No valid frames provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Assemble frames into a video (assuming same dimensions; adjust FPS as needed)
        height, width, _ = frames[0].shape
        video_path = 'output_video.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, 30.0, (width, height))  # 30 FPS

        # Apply AR effects (simple example: detect faces and overlay a red circle)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        for frame in frames:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.circle(frame, (x + w//2, y + h//2), w//2, (0, 0, 255), 2)  # Red circle overlay
            out.write(frame)

        out.release()

        # Use strings/integers if needed (e.g., metadata logging)
        print(f"Received strings: {strings}, integers: {integers}")

        # Return success (or video URL if hosted)
        return Response({"message": "Video processed and AR effects applied", "video_path": video_path})