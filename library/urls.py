from django.urls import path

from . import views


urlpatterns = [
    path('student/books/', views.book_list, name='book_list'),
    path('student/books/<int:book_id>/request/', views.request_book, name='request_book'),
    path('student/history/', views.student_history, name='student_history'),
    path('librarian/requests/', views.librarian_requests, name='librarian_requests'),
    path('librarian/requests/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    path('librarian/requests/<int:request_id>/reject/', views.reject_request, name='reject_request'),
    path('librarian/issues/', views.librarian_issues, name='librarian_issues'),
    path('librarian/issues/<int:issue_id>/return/', views.return_book, name='return_book'),
]