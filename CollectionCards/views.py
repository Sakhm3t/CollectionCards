from datetime import timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView, DeleteView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import *
from .models import *
from .serializers import BonusCardSerializer


def task(request):
    """Method shows initial task"""
    if "error_message" in request.session:
        del request.session["error_message"]
    return render(request, 'CollectionCards/base.html')


def generation(request):
    """Method generates form for new card generation"""
    form = GenerationForm()
    error_message = request.session["error_message"] if "error_message" in request.session else None
    return render(request, 'CollectionCards/GenerateForm.html', {'form': form, 'error_message': error_message})


def card_creation(request):
    """Method gets parameters of new cards and save new cards to database"""
    number_of_cards = request.POST['number_of_cards']
    series_of_cards = request.POST['series_of_cards']
    validity = request.POST['validity']
    try:
        number_of_cards = int(number_of_cards)
        if number_of_cards < 0 or number_of_cards > 1000:
            raise ValueError("Number is out of range")
    except:
        request.session["error_message"] = "Количество карт должно быть целым числом больше нуля"
        return redirect("CollectionCards:generate")

    for n in range(number_of_cards):
        a = BonusCard(card_series=series_of_cards,
                      date_of_issue=datetime.now(),
                      expiration_date=datetime.now() + timedelta(days=int(validity)),
                      sum_money=0,
                      card_status='active'
                      )
        a.save()
    template_vars = {'number_of_cards': number_of_cards,
                     'validity': validity,
                     'series_of_cards': series_of_cards}

    return render(request, 'CollectionCards/process.html', template_vars)


class CardListView(generic.ListView):
    """Class shows card list"""
    model = BonusCard
    queryset = BonusCard.objects.all().order_by('card_number')
    paginate_by = 20
    template_name = 'CollectionCards/card_list.html'


class CardDetailView(generic.DetailView):
    """Class shows details of one card"""
    model = BonusCard
    pk_url_kwarg = 'pk'
    template_name = 'CollectionCards/card_detail.html'
    context_object_name = 'card'

    def post(self, request, *args, **kwargs):
        a = BonusCard.objects.get(card_number=kwargs['pk'])
        if 'card_status' in request.POST:
            a.card_status = request.POST['card_status']
            a.save()
        return redirect(request.path)

    def get_context_data(self, **kwargs):
        """ Method has been overridden to add `PurchaseHistory` to the template context """
        context = super().get_context_data(**kwargs)
        ph = PurchaseHistory.objects.filter(bonus_card__card_number=self.kwargs['pk'])
        context['purr'] = ph
        return context


class CardUpdateView(UpdateView):
    """Update one card details"""
    model = BonusCard
    template_name = 'CollectionCards/card_edit.html'
    pk_url_kwarg = 'pk'
    fields = ['card_status']
    context_object_name = 'card'


class CardDeleteView(DeleteView):
    """Delete one card"""
    model = BonusCard
    template_name = 'CollectionCards/card_delete.html'
    success_url = reverse_lazy('CollectionCards:full_list')

def clear_error_mess(request):
    if "error_mess" in request.session:
        del request.session["error_mess"]

def searching(request):
    """Method shows form for card searching"""
    form = SearchingForm()
    error_mess = request.session["error_mess"] if "error_mess" in request.session else None
    result = render(request, 'CollectionCards/card_searching.html', {'form': form, 'error_mess': error_mess})
    clear_error_mess(request)
    return result

def search_result(request):
    """Method shows searching results"""
    # Getting searching parameters from the user
    if request.method == "POST":
        if request.POST['card_number']:
            try:
                card_number = int(request.POST['card_number'])
                if card_number < 0 or card_number > 1000000000000000:
                    raise ValueError("Number is out of range")
            except:
                request.session["error_mess"] = "Номер карты должен быть положительным целым числом"
                return redirect("CollectionCards:list_for_search")

        filter_kv = dict()
        filter_kv['card_number'] = request.POST['card_number']
        filter_kv['card_series'] = request.POST['card_series']
        filter_kv['card_status'] = request.POST['card_status']
        filter_kv['sum_money'] = request.POST['sum_money']

        filter_kv = {key: filter_kv[key] for key in filter_kv if filter_kv[key] != ''}

        fields = ('date_of_issue', 'expiration_date', 'date_of_use')

        for field in fields:
            post_value = request.POST[field]
            if post_value:
                try:
                    parsed_date = datetime.strptime(post_value, '%Y-%m')
                    filter_kv[field + '__year'] = parsed_date.date().year
                    filter_kv[field + '__month'] = parsed_date.date().month
                    clear_error_mess(request)
                except:
                    request.session["error_mess"] = "Дата должна иметь формат: yyyy-mm"
                    return redirect("CollectionCards:list_for_search")
        request.session['filter_kv'] = filter_kv
    else:
        filter_kv = request.session['filter_kv']
    # Pagination
    if filter_kv:
        card_list = BonusCard.objects.filter(**filter_kv).order_by('card_number')
        page_number = request.GET.get('page')
        paginator = Paginator(card_list, 20)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
    else:
        request.session["error_mess"] = "Не выбрано ни одного параметра поиска"
        return redirect("CollectionCards:list_for_search")

    return render(request, 'CollectionCards/card_list.html',
                  {'object_list': page_obj, 'page_obj': page_obj, 'paginator': paginator})


def actualize_db(request):
    """Database update (expired cards)"""
    count = BonusCard.actualize_database()
    template_vars = {'number_of_cards': count}
    return render(request, 'CollectionCards/actualise_db.html', template_vars)


@api_view(['GET', 'PATCH'])
def expired_card_api_view(request):
    """Experimental method for using rest api """
    if request.method == 'GET':
        cards = BonusCard.objects.filter(~Q(card_status="active"))
        serializer = BonusCardSerializer(cards, many=True)
        return Response({"message": "Got some data!", "data": serializer.data})
    if request.method == 'PATCH':
        return Response({"message2": "Got some ANOTHER data!", "data": request.data})
    return Response({"message": "Hello, world!"})
