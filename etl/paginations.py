from rest_framework.pagination import CursorPagination


class StudentListPagination(CursorPagination):
    ordering = 'username'
    page_size = 2


class PostListPagination(CursorPagination):
    ordering = '-created_at'
    page_size = 10
