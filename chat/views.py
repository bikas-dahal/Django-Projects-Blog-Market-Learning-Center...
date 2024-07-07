from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from courses.models import Course


@login_required
def course_chat_room(request, course_id):
    try:
        # retrieve course with given id joined by the current user
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # user is not a student of the course or course does not exist
        return HttpResponse('<h1>Not enrolled yet, Enroll to course to join chat.</h1>')
    
    # retrieve chat history
    latest_messages = course.chat_messages.select_related(
        'user'
    ).order_by('-id')[:10]
    latest_messages = reversed(latest_messages)
    # print(latest_messages)

    return render(request, 'chat/room.html', {
        'course': course, 
        'latest_messages': latest_messages
    }
    )