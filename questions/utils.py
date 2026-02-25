from django.utils import timezone


def time_ago(dt):
    """
    Convert datetime to human-readable relative time.
    Returns: "Just now", "5 minutes ago", "2 hours ago", etc.
    """
    if dt is None:
        return "Unknown"
    
    now = timezone.now()
    
    # Make both datetimes timezone-aware
    if timezone.is_aware(dt):
        diff = now - dt
    else:
        # If dt is naive, assume it's in the same timezone as now
        diff = now - timezone.make_aware(dt)
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 2592000:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"

