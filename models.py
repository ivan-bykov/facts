#coding: cp1251

from django.db import models as db

class Exchange(db.Model):
    title = db.CharField(max_length=256)

    def __unicode__(self):
        return self.title

class Fact(db.Model):
    title = db.CharField(max_length=256)
    viewed = db.DateTimeField(auto_now_add=True)
    tense = db.CharField(default=u'Дата', max_length=256)
    cost = db.CharField(default=u'Стоимость', max_length=256)
    exchange = db.CharField(default=u'Валюта', max_length=256)
    a = db.CharField(default=u'Дополнительно А', max_length=256)
    b = db.CharField(default=u'Дополнительно Б', max_length=256)
    days = db.IntegerField(default=0)

    def __unicode__(self):
        return u'%s (%s, %s)' % (self.title, self.a, self.b)

class Item(db.Model):
    fact = db.ForeignKey(Fact, related_name='items')
    tense = db.DateTimeField()
    cost = db.DecimalField(max_digits=16, decimal_places=2)
    exchange = db.ForeignKey(Exchange)
    a = db.CharField(blank=True, max_length=256)
    b = db.CharField(blank=True, max_length=256)

    def __unicode__(self):
        return u'"%s" "%s" %s' % (self.fact.title, self.tense, self.cost)

    fields = tuple('tense cost exchange a b'.split())
