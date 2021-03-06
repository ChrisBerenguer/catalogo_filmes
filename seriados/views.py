from blog import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import SerieForm, TemporadaForm
from .models import Episodio, Serie, Temporada


def prepare_data_list(objects, fields_name):
    labels = list()
    for field_name in fields_name:
        field = objects.model._meta.get_field(field_name)
        labels.append(field.verbose_name)

    rows = list()
    for _object in objects:
        row = dict()
        rows.append(row)
        row['pk'] = _object.pk
        row['data'] = list()
        for field_name in fields_name:
            row['data'].append(getattr(_object, field_name))

    return labels, rows


def prepare_data_detail(_object, fields_name):
    data = model_to_dict(_object)
    rows = list()
    for field_name in fields_name:
        field = _object._meta.get_field(field_name)
        rows.append({'label': field.verbose_name, 'value': data[field_name]})
    return rows


def serie_list(request):
    objects = Serie.objects.all()
    labels, rows = prepare_data_list(objects, ['nome'])
    context = {
        'title': "Series",
        'labels': labels,
        'rows': rows,
        'detail_url': 'seriados:serie_details',
    }
    return render(request, 'list.html', context)


def serie_details(request, pk):
    _object = get_object_or_404(Serie, pk=pk)
    context = {
        'title': "Serie",
        'data': prepare_data_detail(_object, ['nome']),
    }
    return render(request, 'details.html', context)


@login_required
@permission_required('seriados.add_serie', raise_exception=True)
def serie_insert(request):
    if request.method == 'GET':
        form = SerieForm()
    elif request.method == 'POST':
        form = SerieForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            obj = Serie(nome=nome)
            obj.save()
            return HttpResponseRedirect(reverse(
                'seriados:serie_details',
                kwargs={'pk': obj.pk}
            ))

    return render(request, 'form_base.html', {
        'form': form,
        'target_url': 'seriados:serie_insert',
    })


class TemporadaListView(ListView):
    template_name = 'temporada_list.html'
    model = Temporada

    def get_queryset(self):
        search = self.request.GET.get('search', "")

        return super().get_queryset().filter(serie__nome__contains=search)


class TemporadaDetail(DetailView):
    template_name = "temporada_details.html"
    model = Temporada


class TemporadaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('seriados.view_temporada',
                           'seriados.change_temporada')
    template_name = 'form_generic.html'
    model = Temporada
    fields = ['serie', 'numero']


class TemporadaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'seriados.add_temporada'
    template_name = 'form_generic.html'
    form_class = TemporadaForm


class TemporadaDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "temporada_confirm_delete.html"
    model = Temporada

    def get_success_url(self):
        return reverse('seriados:temporada_list')


def episodio_list(request):
    search = request.GET.get('search', "")
    objects = Episodio.objects.filter(titulo__contains=search)
    labels, rows = prepare_data_list(objects, ['titulo', 'data'])
    context = {
        'title': "Epis??dios",
        'labels': labels,
        'rows': rows,
        'detail_url': 'seriados:episodio_details',
    }
    return render(request, 'list.html', context)


def episodio_details(request, pk):
    _object = get_object_or_404(Episodio, pk=pk)
    context = {
        'title': "Epis??dio",
        'data': prepare_data_detail(_object, ['titulo', 'data', 'temporada']),
    }
    return render(request, 'details.html', context)


class EpisodioCreateView(CreateView):
    template_name = 'form_generic.html'
    model = Episodio
    fields = ['temporada', 'data', 'titulo']


def episodio_nota_list(request, nota):
    objects = Episodio.objects.filter(reviewepisodio__nota=nota)
    context = {'objects': objects, 'nota': nota}
    return render(request, 'episodio_nota_list.html', context)


class EpisodioBuscaListView(ListView):
    template_name = 'episodio_busca_list.html'
    model = Episodio

    def get_queryset(self):
        search = self.request.GET.get('search', "")
        q = Q(titulo__contains=search) | Q(
            temporada__serie__nome__contains=search)

        for term in search.split():
            q = q | Q(titulo__contains=term)
            q = q | Q(temporada__serie__nome__contains=term)
            try:
                i_term = int(term)
            except ValueError:
                pass
            else:
                q = q | Q(temporada__numero=i_term)

        qs = super().get_queryset().filter(q)
        print(qs.query)
        return qs


class Contact(TemplateView):
    template_name = 'contact.html'


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})


# View do blog

'''class BlogView(Blog):
    def get(self, request):
        return render(request, 'blog/post/base.html', {})'''
