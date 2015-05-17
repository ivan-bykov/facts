from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.forms import ModelForm, DateTimeInput
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, \
    Http404
from django.template import RequestContext, loader
from django.utils import timezone

from facts.models import Fact, Item

class DT:
    date = 'Y-m-d'
    time = 'H:i'
    full = '%Y-%m-%d %H:%M'

class Form(ModelForm):
    class Meta:
        model = Item
        fields = Item.fields
        widgets = \
            {
            'tense': DateTimeInput(format=DT.full),
            }

def parse(data):
    rm = False
    try:
        item = int(data['item'])
        try:
            item = Item.objects.get(pk=item)
        except Item.DoesNotExist:
        try:
            fact = int(data['fact'])
        except (KeyError, ValueError, TypeError):
            try:
            except Fact.DoesNotExist:
                fact.save()
    return fact, item, rm

def formdata(item):
    'form data: part or full'
    if item:
        res = {x: getattr(item, x) for x in Item.fields}
        res['exchange'] = res['exchange'].id
    else:
        res = dict.fromkeys(Item.fields, '')
        res['tense'] = timezone.now()
    return res

def index(request):
    if request.method == 'POST':
        fact, item, rm = parse(request.POST)
        if rm:
            form = Form(formdata(item))
            item.delete()
            item = ''
            valid = True
        else:
            form = Form(request.POST)
            valid = form.is_valid()
            if valid:
                item = item if item else Item(fact=fact)
                for field in Item.fields:
                    setattr(item, field, form.cleaned_data[field])
                item.save()
                item = ''
                form = Form(formdata(item))
                return HttpResponseRedirect('/facts/')
    else:
        fact, item, _ = parse(request.GET)
        form = Form(formdata(item))
        valid = True
    facts = Fact.objects.order_by('title')
    facts = [(x, ' selected' if x.id == fact.id else '') for x in facts]
    items = fact.items.order_by('-tense')

    template = loader.get_template('facts/index.html')
    context = RequestContext(request,
        {
        'fact': fact,
        'item': item,
        'facts': facts,
        'items': items,
        'dt': DT,
        'form': form,
        'valid': valid,
        }
        )
    return HttpResponse(template.render(context))

def daysdata():
    now = timezone.now()
    for fact in Fact.objects.order_by('title'):
        if not fact.days:
            continue
        try:
            last = fact.items.latest('tense')
        except Fact.DoesNotExist:
            continue
        event = last.tense + timedelta(days=fact.days)
        delta = now - last.tense
        delta = int(delta.total_seconds() / 24 / 60 / 60)
        yield dict(title=fact.title, event=event, days=fact.days,
            delta=delta, left=fact.days - delta)

def days(request):
    template = loader.get_template('facts/days.html')
    context = RequestContext(request,
        {
        'rows': daysdata(),
        'dt': DT,
        }
        )
    return HttpResponse(template.render(context))

def rest(request):
    rows = list(daysdata())
    for row in rows:
        row['event'] = tuple(row['event'].timetuple())
    return JsonResponse(rows, safe=False)

def data(request, fact_id, field):
    'ordered and unique autocomplete values'
    fact = get_object_or_404(Fact, pk=fact_id)
    if field not in 'a b':
        raise Http404
    tmp = set()  # sqlite collate and other limitation
    dst = []
    for item in fact.items.order_by('-tense'):
        key = getattr(item, field)
        if not key:
            continue
        lower = key.lower()
        if lower in tmp:
            continue
        tmp.add(lower)
        dst.append(key)
    return JsonResponse(dst, safe=False)
