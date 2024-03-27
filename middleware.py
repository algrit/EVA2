from django.core.exceptions import ObjectDoesNotExist

from education.models import CourseSubscription, TestAttempt, Test


class UpdateCourseSubScore:
    """This middleware class checks and update score and pass-status of course subscription.
    To write this check here is not optimal and even bad (now course_sub model updates on every action on site),
    but I wanted to learn Middleware stuff and understand how's it work
    Maybe I should transfer this logic to view.func before release"""
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        if request.user.is_authenticated:
            user = request.user
            try:
                course_subs = CourseSubscription.objects.filter(user=user, active=1)
            except ObjectDoesNotExist:
                return response
            for course_sub in course_subs:
                try:
                    tests_in_courses = Test.objects.filter(course__id=course_sub.course.id)
                except ObjectDoesNotExist:
                    continue
                status_dict = {test.id: 1 for test in tests_in_courses if
                    TestAttempt.objects.filter(user=user, course_attempt=course_sub, test=test, test_passed=1).exists()}
                course_sub.course_score = round(len(status_dict) / len(tests_in_courses) * 100)
                if course_sub.course_score == 100:
                    course_sub.course_passed = True
                course_sub.save()
        return response
