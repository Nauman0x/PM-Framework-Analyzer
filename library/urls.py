from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('section/<int:section_id>/', views.section_detail, name='section_detail'),
    path('search/', views.search_topics, name='search_topics'),
    path('compare/', views.compare_topic, name='compare_topic'),
    path('analyze/', views.analyze_topics, name='analyze_topics'),
    path('analyze/process/', views.analyze_topics_process, name='analyze_topics_process'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
]
