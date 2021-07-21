from django.db import models as db

class Exchange(db.Model):
    title = db.CharField(max_length=256)

    def __unicode__(self):
        return self.title

    __str__ = __unicode__

class Fact(db.Model):
    title = db.CharField(max_length=256)
    viewed = db.DateTimeField(auto_now_add=True)
    tense = db.CharField(default='Дата', max_length=256)
    cost = db.CharField(default='Стоимость', max_length=256)
    exchange = db.CharField(default='Валюта', max_length=256)
    a = db.CharField(default='Дополнительно А', max_length=256)
    b = db.CharField(default='Дополнительно Б', max_length=256)
    days = db.IntegerField(default=0)

    def __unicode__(self):
        return '%s (%s, %s)' % (self.title, self.a, self.b)

    __str__ = __unicode__

class Item(db.Model):
    fact = db.ForeignKey(Fact, db.CASCADE, related_name='items')
    tense = db.DateTimeField()
    cost = db.DecimalField(max_digits=16, decimal_places=2)
    exchange = db.ForeignKey(Exchange, db.SET_NULL, null=True)
    a = db.CharField(blank=True, max_length=256)
    b = db.CharField(blank=True, max_length=256)

    def __unicode__(self):
        return '"%s" "%s" %s' % (self.fact.title, self.tense, self.cost)

    __str__ = __unicode__
    fields = tuple('tense cost exchange a b'.split())
