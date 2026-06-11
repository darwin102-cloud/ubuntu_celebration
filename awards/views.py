from django.shortcuts import render, redirect
from .models import Event
from .models import Category
from .models import AwardSection
from .models import Nominee
from django.shortcuts import get_object_or_404
from .forms import VoteForm
from .forms import NominationForm
from .models import Vote
from .models import Nomination
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    return render(request, 'awards/home.html')

def about(request):
    return render(request, 'awards/about.html')

def categories(request):
    return render(request, 'awards/categories.html')

def nominees(request):
    return render(request, 'awards/nominees.html')

def vote(request):
    return render(request, 'awards/vote.html')

def results(request):
    return render(request, 'awards/results.html')

def contact(request):
    return render(request, 'awards/contact.html')

from .models import Nominee

def home(request):

    event = Event.objects.filter(
        is_active=True
    ).first()

    total_categories = Category.objects.count()

    total_nominees = Nominee.objects.filter(
        is_active=True
    ).count()

    total_votes = sum(
        nominee.votes
        for nominee in Nominee.objects.all()
    )

    leaders = Nominee.objects.filter(
        is_active=True
    ).order_by('-votes')[:5]

    return render(
        request,
        'awards/home.html',
        {
            'event': event,
            'total_categories': total_categories,
            'total_nominees': total_nominees,
            'total_votes': total_votes,
            'leaders': leaders,
        }
    )

def categories(request):

    sections = AwardSection.objects.prefetch_related(
        'categories'
    )

    return render(
        request,
        'awards/categories.html',
        {
            'sections': sections
        }
    )


def category_detail(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk
    )

    nominees = category.nominees.filter(
        is_active=True
    )

    return render(
        request,
        'awards/category_detail.html',
        {
            'category': category,
            'nominees': nominees
        }
    )


def nominees(request):

    query = request.GET.get('q')

    nominees = Nominee.objects.filter(
        is_active=True
    )

    if query:
        nominees = nominees.filter(
            full_name__icontains=query
        )

    return render(
        request,
        'awards/nominees.html',
        {
            'nominees': nominees,
            'query': query
        }
    )


def vote_nominee(request, nominee_id):

    nominee = get_object_or_404(
        Nominee,
        id=nominee_id
    )

    if request.method == 'POST':

        form = VoteForm(request.POST)

        if form.is_valid():

            vote = form.save(commit=False)

            vote.nominee = nominee

            vote.save()

            nominee.votes += vote.votes
            nominee.save()

            return redirect('vote_success')

    else:

        form = VoteForm()

    return render(
        request,
        'awards/vote.html',
        {
            'form': form,
            'nominee': nominee
        }
    )

def results(request):

    categories = Category.objects.all()

    for category in categories:

        category.sorted_nominees = (
            category.nominees
            .filter(is_active=True)
            .order_by('-votes')
        )

    return render(
        request,
        'awards/results.html',
        {
            'categories': categories
        }
    )

def nominee_detail(request, pk):

    nominee = get_object_or_404(
        Nominee,
        pk=pk,
        is_active=True
    )

    return render(
        request,
        'awards/nominee_detail.html',
        {
            'nominee': nominee
        }
    )

def vote_success(request):
    return render(
        request,
        'awards/vote_success.html'
    )

def nominate(request):

    if request.method == 'POST':

        form = NominationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                'nomination_success'
            )

    else:

        form = NominationForm()

    return render(
        request,
        'awards/nominate.html',
        {
            'form': form
        }
    )

def nomination_success(request):
    return render(
        request,
        'awards/nomination_success.html'
    )

@staff_member_required
def dashboard(request):

    total_categories = Category.objects.count()

    total_nominees = Nominee.objects.count()

    total_votes = Vote.objects.count()

    pending_nominations = Nomination.objects.filter(
        approved=False
    ).count()

    approved_nominations = Nomination.objects.filter(
        approved=True
    ).count()

    top_nominees = Nominee.objects.order_by(
        '-votes'
    )[:5]

    context = {
        'total_categories': total_categories,
        'total_nominees': total_nominees,
        'total_votes': total_votes,
        'pending_nominations': pending_nominations,
        'approved_nominations': approved_nominations,
        'top_nominees': top_nominees,
    }

    return render(
        request,
        'awards/dashboard.html',
        context
    )