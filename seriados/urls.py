from django.urls import path, re_path, include, register_converter

from django.views.generic import TemplateView

from . import views

app_name = 'seriados'

urlpatterns = [
   path('serie/', views.serie_list, name='serie_list'),
   path('serie/<int:pk>/', views.serie_details, name='serie_details'),
   path('serie/inserir/', views.serie_insert, name='serie_insert'),

   path('temporada/', views.TemporadaListView.as_view(), name='temporada_list'),
   path('temporada/<int:pk>/', views.TemporadaDetail.as_view(), name='temporada_details'),
   path('temporada/<int:pk>/editar/', views.TemporadaUpdateView.as_view(), name='temporada_update'),
   path('temporada/<int:pk>/excluir/', views.TemporadaDeleteView.as_view(), name='temporada_excluir'),
   path('temporada/inserir/', views.TemporadaCreateView.as_view(), name='temporada_insert'),

   path('episodio/', views.episodio_list, name='episodio_list'),
   path('episodio/<int:pk>/', views.episodio_details, name='episodio_details'),
   path('episodio/inserir/', views.EpisodioCreateView.as_view(), name='episodio_insert'),

   path('episodio/nota/<str:nota>/', views.episodio_nota_list,
       name='episodio_nota_list'),


   path('sobre/', TemplateView.as_view(template_name="about.html"), name='about'),
   path('contato/', views.Contact.as_view(), name='contact'),

   

   path('', views.HomeView.as_view(), name='home'),

   

]


