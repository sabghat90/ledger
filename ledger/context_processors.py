from .models import Agent


def agent_profile_picture(request):
    if request.user.is_authenticated:
        try:
            profile_picture = request.user.profile_picture
            return {'profile_picture': profile_picture}
        except Agent.DoesNotExist:
            return {'profile_picture': None}
    return {'profile_picture': None}