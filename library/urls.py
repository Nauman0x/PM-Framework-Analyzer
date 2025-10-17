from django.urls import path
from . import views

urlpatterns = [
    # Phase 1: PDF Extraction & AI Analysis
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('section/<int:section_id>/', views.section_detail, name='section_detail'),
    path('search/', views.search_topics, name='search_topics'),
    path('compare/', views.compare_topic, name='compare_topic'),
    path('analyze/', views.analyze_topics, name='analyze_topics'),
    path('analyze/process/', views.analyze_topics_process, name='analyze_topics_process'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    
    # Phase 2: Process Design & Tailoring
    path('scenarios/', views.scenarios_list, name='scenarios_list'),
    path('scenario/<int:scenario_id>/', views.scenario_detail, name='scenario_detail'),
    path('process/<int:template_id>/', views.process_template_detail, name='process_template_detail'),
    path('process/<int:template_id>/diagram/', views.process_diagram, name='process_diagram'),
    path('scenario/<int:scenario_id>/generate/', views.generate_process, name='generate_process'),
    path('scenario/<int:scenario_id>/generate/ai/', views.generate_process_ai, name='generate_process_ai'),
]

