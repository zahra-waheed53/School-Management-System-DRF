from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import Attendance, SchoolTiming
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


@shared_task(name='attendance.tasks.mark_absentees')
def mark_absentees():
    """
    Celery task to mark all users who haven't marked attendance as absent.
    This task checks the dismissal time from SchoolTiming model and only runs
    if current time is past dismissal time.
    
    Note: This task should be scheduled to run frequently (e.g., every hour after noon)
    to respect dynamically configured dismissal times.
    """
    current_time = timezone.now()
    today = current_time.date()
    
    # Check if we've already marked absentees today
    cache_key = f'absentees_marked_{today}'
    if cache.get(cache_key):
        logger.info(f"Absentees already marked for {today}, skipping.")
        return {
            'date': str(today),
            'message': 'Already processed today',
            'skipped': True
        }
    
    # Get active school timing
    timing = SchoolTiming.get_active_timing()
    
    # Check if current time is past dismissal time
    if current_time.time() < timing.dismissal_time:
        logger.info(
            f"Current time {current_time.time()} is before dismissal time "
            f"{timing.dismissal_time}, skipping absentee marking."
        )
        return {
            'date': str(today),
            'message': 'Too early - before dismissal time',
            'current_time': str(current_time.time()),
            'dismissal_time': str(timing.dismissal_time),
            'skipped': True
        }
    
    # Get all active users (students and teachers who should mark attendance)
    # Excluding superusers and staff who may not need to mark attendance
    all_users = User.objects.filter(is_active=True, is_superuser=False)
    
    # Get users who have already marked attendance today
    users_with_attendance = Attendance.objects.filter(
        marked_at__date=today
    ).values_list('user_id', flat=True)
    
    # Find users who haven't marked attendance
    absent_users = all_users.exclude(id__in=users_with_attendance)
    
    # Create absent records for these users
    absent_count = 0
    for user in absent_users:
        Attendance.objects.create(
            user=user,
            status='absent'
        )
        absent_count += 1
    
    # Mark that we've processed absentees for today (cache for 24 hours)
    cache.set(cache_key, True, 60 * 60 * 24)
    
    logger.info(
        f"Marked {absent_count} users as absent for {today}. "
        f"Total users: {all_users.count()}, "
        f"Present/Late: {len(users_with_attendance)}"
    )
    
    return {
        'date': str(today),
        'total_users': all_users.count(),
        'marked_absent': absent_count,
        'already_marked': len(users_with_attendance),
        'dismissal_time': str(timing.dismissal_time),
        'skipped': False
    }

