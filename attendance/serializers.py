from rest_framework import serializers
from .models import FaceEncoding, Attendance, SchoolTiming
import face_recognition
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from django.utils import timezone
import base64
from datetime import time


class FaceEncodingSerializer(serializers.ModelSerializer):
    face_image = serializers.ImageField(write_only=True)

    class Meta:
        model = FaceEncoding
        fields = ['face_image']

    def create(self, validated_data):
        user = self.context['request'].user
        face_image = validated_data.get('face_image')

        img = Image.open(face_image)
        img_rgb = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        face_encodings = face_recognition.face_encodings(img_rgb)

        if not face_encodings:
            raise serializers.ValidationError("No face detected in the image.")

        encoding = face_encodings[0]

        FaceEncoding.objects.filter(user=user).delete()

        face_obj = FaceEncoding.objects.create(
            user=user,
            encoding=encoding.tobytes(),
            face_image=face_image
        )
        return face_obj


class SchoolTimingSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = SchoolTiming
        fields = [
            'id', 'name', 'arrival_time', 'late_threshold', 
            'dismissal_time', 'is_active', 'created_at', 
            'updated_at', 'created_by'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def validate_is_active(self, value):
        """
        Validate is_active field.
        Note: Only one timing can be active at a time.
        Setting this to True will automatically deactivate all other timings.
        """
        # When deactivating, ensure at least one other timing is active
        if not value and self.instance and self.instance.is_active:
            other_active = SchoolTiming.objects.filter(
                is_active=True
            ).exclude(pk=self.instance.pk).exists()
            
            if not other_active:
                raise serializers.ValidationError(
                    "Cannot deactivate the only active timing. "
                    "Please activate another timing first."
                )
        
        return value
    
    def validate(self, data):
        """Validate timing relationships"""
        arrival = data.get('arrival_time')
        late = data.get('late_threshold')
        dismissal = data.get('dismissal_time')
        
        # Get existing values if updating
        if self.instance:
            arrival = arrival or self.instance.arrival_time
            late = late or self.instance.late_threshold
            dismissal = dismissal or self.instance.dismissal_time
        
        if arrival and late:
            if late <= arrival:
                raise serializers.ValidationError({
                    'late_threshold': "Late threshold must be after arrival time"
                })
        
        if late and dismissal:
            if dismissal <= late:
                raise serializers.ValidationError({
                    'dismissal_time': "Dismissal time must be after late threshold"
                })
        
        return data
    
    def create(self, validated_data):
        """
        Create a new timing.
        If is_active=True, this will automatically deactivate all other timings.
        """
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Update timing.
        If is_active is set to True, this will automatically deactivate all other timings.
        """
        return super().update(instance, validated_data)


class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    marked_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'user', 'status', 'marked_at']


class MarkAttendanceSerializer(serializers.Serializer):
    image = serializers.CharField(help_text="Base64 encoded image")

    def _get_school_timing(self):
        """Get active school timing from database"""
        return SchoolTiming.get_active_timing()

    def _determine_status(self, current_time):
        """
        Determine attendance status based on current time and school timing
        - Before or at LATE_THRESHOLD: Present
        - After LATE_THRESHOLD: Late
        """
        timing = self._get_school_timing()
        current_time_only = current_time.time()
        
        if current_time_only <= timing.late_threshold:
            return 'present'
        else:
            return 'late'

    def validate_image(self, value):
        try:
            img_data = base64.b64decode(value)
            img_array = np.frombuffer(img_data, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is None:
                raise serializers.ValidationError("Invalid image format")

            return img
        except Exception as e:
            raise serializers.ValidationError(f"Error decoding image: {str(e)}")

    def create(self, validated_data):
        user = self.context['request'].user
        face_img = validated_data.get('image')

        rgb_frame = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if not face_encodings:
            raise serializers.ValidationError("No face detected in the image.")

        try:
            user_face = FaceEncoding.objects.get(user=user)
            known_encoding = np.frombuffer(user_face.encoding, dtype=np.float64)
        except FaceEncoding.DoesNotExist:
            raise serializers.ValidationError(
                "No face encoding found for this user. Please register your face first."
            )

        captured_encoding = face_encodings[0]
        match = face_recognition.compare_faces(
            [known_encoding], captured_encoding, tolerance=0.6
        )

        if not match[0]:
            raise serializers.ValidationError("Face does not match. Access denied.")

        current_time = timezone.now()
        attendance_status = self._determine_status(current_time)

        attendance, created = Attendance.objects.get_or_create(
            user=user,
            marked_at__date=current_time.date(),
            defaults={'status': attendance_status}
        )

        if not created:
            return {
                'message': 'Attendance already marked today',
                'user': user.username,
                'status': attendance.status,
                'marked_at': attendance.marked_at
            }

        return {
            'message': 'Attendance marked successfully',
            'user': user.username,
            'status': attendance.status,
            'marked_at': attendance.marked_at
        }
