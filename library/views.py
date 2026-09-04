from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import UserProfile
from books.models import Book, Category

from .models import BookIssue, BookRequest


def has_role(user, role):
    try:
        return UserProfile.objects.get(user=user).role == role
    except UserProfile.DoesNotExist:
        return False


@login_required
def book_list(request):
    if not has_role(request.user, 'STUDENT'):
        return redirect('login')

    books = Book.objects.select_related('category').all()
    categories = Category.objects.all()

    search = request.GET.get('search')
    category = request.GET.get('category')

    if search:
        books = books.filter(title__icontains=search)

    if category:
        books = books.filter(category_id=category)

    return render(
        request,
        'student/books.html',
        {
            'books': books,
            'categories': categories,
        }
    )


@login_required
def request_book(request, book_id):
    if not has_role(request.user, 'STUDENT'):
        return redirect('login')

    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)

        existing_request = BookRequest.objects.filter(
            student=request.user,
            book=book,
            status='PENDING'
        ).exists()

        if not existing_request and book.available_quantity > 0:
            BookRequest.objects.create(
                student=request.user,
                book=book
            )

    return redirect('book_list')


@login_required
def student_history(request):
    if not has_role(request.user, 'STUDENT'):
        return redirect('login')

    requests = BookRequest.objects.select_related(
        'book',
        'book__category'
    ).filter(
        student=request.user
    )

    issues = BookIssue.objects.select_related('book').filter(
        student=request.user
    )

    return render(
        request,
        'student/history.html',
        {
            'requests': requests,
            'issues': issues,
        }
    )


@login_required
def librarian_requests(request):
    if not has_role(request.user, 'LIBRARIAN'):
        return redirect('login')

    requests = BookRequest.objects.select_related(
        'student',
        'book',
        'book__category'
    ).filter(
        status='PENDING'
    )

    return render(
        request,
        'librarian/requests.html',
        {'requests': requests}
    )


@login_required
def approve_request(request, request_id):
    if not has_role(request.user, 'LIBRARIAN'):
        return redirect('login')

    if request.method == 'POST':
        with transaction.atomic():
            book_request = get_object_or_404(
                BookRequest.objects.select_related('book'),
                id=request_id
            )

            book = Book.objects.select_for_update().get(
                id=book_request.book_id
            )

            if (
                book_request.status == 'PENDING'
                and book.available_quantity > 0
            ):
                BookIssue.objects.create(
                    student=book_request.student,
                    book=book,
                    due_date=date.today() + timedelta(days=14)
                )

                book.available_quantity -= 1
                book.save(update_fields=['available_quantity'])

                book_request.status = 'APPROVED'
                book_request.save(update_fields=['status'])

    return redirect('librarian_requests')


@login_required
def reject_request(request, request_id):
    if not has_role(request.user, 'LIBRARIAN'):
        return redirect('login')

    if request.method == 'POST':
        book_request = get_object_or_404(
            BookRequest,
            id=request_id
        )

        if book_request.status == 'PENDING':
            book_request.status = 'REJECTED'
            book_request.save(update_fields=['status'])

    return redirect('librarian_requests')


@login_required
def librarian_issues(request):
    if not has_role(request.user, 'LIBRARIAN'):
        return redirect('login')

    issues = BookIssue.objects.select_related(
        'student',
        'book'
    ).filter(
        status='ISSUED'
    )

    return render(
        request,
        'librarian/issues.html',
        {'issues': issues}
    )


@login_required
def return_book(request, issue_id):
    if not has_role(request.user, 'LIBRARIAN'):
        return redirect('login')

    if request.method == 'POST':
        with transaction.atomic():
            issue = get_object_or_404(
                BookIssue.objects.select_related('book'),
                id=issue_id
            )

            if issue.status == 'ISSUED':
                book = Book.objects.select_for_update().get(
                    id=issue.book_id
                )

                issue.return_date = date.today()
                issue.status = 'RETURNED'
                issue.save(
                    update_fields=[
                        'return_date',
                        'status'
                    ]
                )

                book.available_quantity += 1
                book.save(
                    update_fields=['available_quantity']
                )

    return redirect('librarian_issues')