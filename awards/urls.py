from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('categories/', views.categories, name='categories'),
    path('nominees/', views.nominees, name='nominees'),
    path('vote/', views.vote, name='vote'),
    path('results/', views.results, name='results'),
    path('contact/', views.contact, name='contact'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('vote/<int:nominee_id>/', views.vote_nominee, name='vote_nominee'),
    path('results/', views.results, name='results'),
    path('nominee/<int:pk>/', views.nominee_detail, name='nominee_detail'),
    path('vote-success/', views.vote_success, name='vote_success'),
    path('nominate/', views.nominate, name='nominate'),
    path('nomination-success/', views.nomination_success, name='nomination_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
]