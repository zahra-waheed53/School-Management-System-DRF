from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.utils import timezone
from django.db.models import Q
from .models import FaceEncoding, Attendance, SchoolTiming
from attendance.serializers import (
    FaceEncodingSerializer, AttendanceSerializer, MarkAttendanceSerializer,
    SchoolTimingSerializer
)


class FaceEncodingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def register_face(self, request):
        """Register or update user's face encoding"""
        serializer = FaceEncodingSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Face registered successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check_registration(self, request):
        """Check if user has registered face"""
        try:
            FaceEncoding.objects.get(user=request.user)
            return Response({'registered': True})
        except FaceEncoding.DoesNotExist:
            return Response({'registered': False})


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(user=user)

    @action(detail=False, methods=['post'])
    def mark_attendance(self, request):
        """Mark attendance using face recognition"""
        serializer = MarkAttendanceSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def today_attendance(self, request):
        """Get today's attendance record"""
        today = timezone.now().date()
        attendance = Attendance.objects.filter(
            user=request.user,
            marked_at__date=today
        ).first()

        if attendance:
            serializer = self.get_serializer(attendance)
            return Response(serializer.data)
        return Response(
            {'message': 'No attendance marked for today'},
            status=status.HTTP_404_NOT_FOUND
        )

    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        """Get monthly attendance report"""
        month = request.query_params.get('month', timezone.now().month)
        year = request.query_params.get('year', timezone.now().year)

        records = Attendance.objects.filter(
            user=request.user,
            marked_at__month=month,
            marked_at__year=year
        )

        serializer = self.get_serializer(records, many=True)
        stats = {
            'present': records.filter(status='present').count(),
            'absent': records.filter(status='absent').count(),
            'late': records.filter(status='late').count(),
            'total_days': records.count(),
        }

        return Response({
            'stats': stats,
            'records': serializer.data
        })


class SchoolTimingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing school timings.
    
    IMPORTANT: Only ONE timing can be active at any time.
    - When creating/updating a timing with is_active=True, all other timings are automatically deactivated
    - Cannot deactivate the only active timing (must activate another one first)
    
    Permissions:
    - Admin users: Full access (create, update, delete)
    - Authenticated users: Read-only access (list, retrieve, view active)
    """
    queryset = SchoolTiming.objects.all()
    serializer_class = SchoolTimingSerializer
    
    def get_permissions(self):
        """
        Admin-only for write operations (create, update, delete)
        Authenticated users for read operations (list, retrieve)
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'set_active']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Create a new timing. If is_active=True, other timings will be deactivated."""
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            if response.data.get('is_active'):
                response.data['info'] = 'This timing is now active. All other timings have been deactivated.'
        return response
    
    def update(self, request, *args, **kwargs):
        """Update timing. If is_active is set to True, other timings will be deactivated."""
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            if response.data.get('is_active'):
                response.data['info'] = 'This timing is now active. All other timings have been deactivated.'
        return response
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get the currently active school timing"""
        timing = SchoolTiming.get_active_timing()
        serializer = self.get_serializer(timing)
        return Response({
            'timing': serializer.data,
            'info': 'This is the currently active timing used for attendance status determination.'
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def set_active(self, request, pk=None):
        """
        Set a specific timing as active.
        This will automatically deactivate all other timings.
        """
        timing = self.get_object()
        
        # Get previously active timing for the message
        previous_active = SchoolTiming.objects.filter(is_active=True).exclude(pk=timing.pk).first()
        
        timing.is_active = True
        timing.save()  # This will deactivate other timings automatically
        
        serializer = self.get_serializer(timing)
        
        message = f'✅ Timing "{timing.name}" is now active.'
        if previous_active:
            message += f' Previous timing "{previous_active.name}" has been deactivated.'
        
        return Response({
            'message': message,
            'timing': serializer.data,
            'info': 'Only one timing can be active at a time. All attendance operations now use this timing.'
        })
