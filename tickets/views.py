from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Ticket, TicketComment
from django.core.exceptions import PermissionDenied

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    context = {
        'tickets': tickets,
        'total_tickets': tickets.count(),
        'open_tickets': tickets.filter(status='open').count(),
    }
    return render(request, 'dashboard.html', context)

def search_tickets(request):
    if not request.user.is_authenticated:
        return render(request, 'search.html', {'tickets': []})

    user_params = request.GET.dict()
    user_params = {k: v for k, v in user_params.items() if v}

    if request.user.is_superuser:
        if user_params:
            try:
                query = Q(**user_params)
                tickets = Ticket.objects.filter(query)
            except Exception as e:
                tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.all()
    else:
        if user_params:
            try:
                if 'created_by__username' in user_params:
                    if user_params['created_by__username'].lower() != request.user.username.lower():
                        return render(request, 'search.html', {'tickets': [], 'search_params': request.GET})
                else:
                    return render(request, 'search.html', {'tickets': [], 'search_params': request.GET})

                query = Q(**user_params)
                tickets = Ticket.objects.filter(query)

            except Exception as e:
                tickets = Ticket.objects.filter(created_by=request.user)
        else:
            tickets = Ticket.objects.filter(created_by=request.user)

    context = {
        'tickets': tickets,
        'search_params': request.GET,
    }
    return render(request, 'search.html', context)

@login_required
def create_ticket(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')

        if title and description:
            ticket = Ticket.objects.create(
                title=title,
                description=description,
                priority=priority,
                created_by=request.user
            )
            return redirect('ticket_detail', ticket_id=ticket.id)

    return render(request, 'create_ticket.html')

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    comments = ticket.comments.all()

    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('comment')
        if content:
            TicketComment.objects.create(
                ticket=ticket,
                author=request.user,
                content=content
            )
            return redirect('ticket_detail', ticket_id=ticket_id)

    return render(request, 'ticket_detail.html', {
        'ticket': ticket,
        'comments': comments
    })

@login_required
def export_data(request):
    if request.method == 'POST':
        data_type = request.POST.get('data_type', 'tickets')
        fields = request.POST.get('fields', 'id,title,status').split(',')

        if data_type == 'tickets':
            data = list(Ticket.objects.filter(created_by=request.user).values(*fields))
        elif data_type == 'users' and request.user.is_superuser:
            data = list(User.objects.values(*fields))
        elif data_type == 'comments':
            data = list(TicketComment.objects.filter(author=request.user).values(*fields))
        else:
            data = []

        import json
        return render(request, 'export.html', {
            'data': json.dumps(data, indent=2, ensure_ascii=False),
            'data_type': data_type,
            'fields': fields
        })

    return render(request, 'export.html')
