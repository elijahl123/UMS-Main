from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CourseSerializer, AssignmentSerializer
from courses.models import Course
from homework.models import HomeworkAssignment


class CourseApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(user=request.user.id)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignmentApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        assignments = HomeworkAssignment.objects.filter(course__user=request.user)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
