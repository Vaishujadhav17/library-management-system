from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from books.models import Book
from library.models import BookIssue, BookRequest

from .models import UserProfile


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                logout(request)
                return render(
                    request,
                    'login.html',
                    {'error': 'User profile not found'}
                )

            if profile.role == 'LIBRARIAN':
                return redirect('librarian_dashboard')

            return redirect('student_dashboard')

        return render(
            request,
            'login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')

    total_books = Book.objects.count()
    total_students = UserProfile.objects.filter(role='STUDENT').count()
    total_librarians = UserProfile.objects.filter(role='LIBRARIAN').count()
    pending_requests = BookRequest.objects.filter(status='PENDING').count()
    issued_books = BookIssue.objects.filter(status='ISSUED').count()

    total_available = Book.objects.aggregate(
        total=Sum('available_quantity')
    )['total'] or 0

    return render(
        request,
        'admin/dashboard.html',
        {
            'total_books': total_books,
            'total_students': total_students,
            'total_librarians': total_librarians,
            'pending_requests': pending_requests,
            'issued_books': issued_books,
            'total_available': total_available,
        }
    )


@login_required
def librarian_dashboard(request):
    if not UserProfile.objects.filter(
        user=request.user,
        role='LIBRARIAN'
    ).exists():
        return redirect('login')

    return render(request, 'librarian/dashboard.html')


@login_required
def student_dashboard(request):
    if not UserProfile.objects.filter(
        user=request.user,
        role='STUDENT'
    ).exists():
        return redirect('login')

    return render(request, 'student/dashboard.html')