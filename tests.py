from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase
from facts.models import Fact, Item, Exchange
from facts.views import parse

class Test(TestCase):
    def testParse(self):
        f, i, rm = parse({})
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 0)
        self.assertIsInstance(f, Fact)
        self.assertFalse(i)
        self.assertFalse(rm)

        f, i, rm = parse(dict(fact=f.id))
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 0)
        self.assertIsInstance(f, Fact)
        self.assertFalse(i)
        self.assertFalse(rm)

        f, i, rm = parse(dict(fact=f.id, item=None))
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 0)
        self.assertIsInstance(f, Fact)
        self.assertFalse(i)
        self.assertFalse(rm)

        f, i, rm = parse(dict(fact=f.id, item=None, delete=''))
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 0)
        self.assertIsInstance(f, Fact)
        self.assertFalse(i)
        self.assertFalse(rm)

        e = Exchange(title='e')
        e.save()
        i = Item(fact=f, tense=timezone.now(), cost=1, exchange=e)
        i.save()
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Exchange.objects.count(), 1)

        f, i, rm = parse(dict(item=i.id))
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Exchange.objects.count(), 1)
        self.assertIsInstance(f, Fact)
        self.assertIsInstance(i, Item)
        self.assertFalse(rm)

        f, i, rm = parse(dict(fact=f.id, item=i.id))
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Exchange.objects.count(), 1)
        self.assertIsInstance(f, Fact)
        self.assertIsInstance(i, Item)
        self.assertFalse(rm)

        f, i, rm = parse(dict(item=i.id, delete=''))
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Exchange.objects.count(), 1)
        self.assertIsInstance(f, Fact)
        self.assertIsInstance(i, Item)
        self.assertTrue(rm)

        f, i, rm = parse(dict(fact=f.id, item=i.id, delete=''))
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Exchange.objects.count(), 1)
        self.assertIsInstance(f, Fact)
        self.assertIsInstance(i, Item)
        self.assertTrue(rm)

    def testView(self):
        r = self.client.get(reverse('facts:index'))
        self.assertEqual(r.status_code, 200)
        self.assertIn('selected>test</option', r.content)
        self.assertEqual(r.context['fact'].id, 1)
        self.assertFalse(r.context['item'])
        self.assertEqual(len(r.context['facts']), 1)
        self.assertEqual(len(r.context['items']), 0)
        self.assertTrue(r.context['valid'])

        f = r.context['fact']
        e = Exchange(title='e')
        e.save()
        i0 = Item(fact=f, tense=timezone.now(), cost=1, exchange=e)
        i0.save()
        i1 = Item(fact=f, tense=timezone.now(), cost=1, exchange=e)
        i1.save()
        i2 = Item(fact=f, tense=timezone.now(), cost=1, exchange=e)
        i2.save()
        self.assertEqual(Fact.objects.count(), 1)
        self.assertEqual(Item.objects.count(), 3)
        self.assertEqual(Exchange.objects.count(), 1)

        post = dict(fact=f.id, item=i1.id, delete='')
        r = self.client.post(reverse('facts:index'), post)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(list(Fact.objects.all()), [f])
        self.assertEqual(list(Item.objects.all()), [i0, i2])
        self.assertEqual(list(Exchange.objects.all()), [e])

        post = dict(fact=f.id, item=(i2.id + 10), delete='')
        r = self.client.post(reverse('facts:index'), post)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(list(Fact.objects.all()), [f])
        self.assertEqual(list(Item.objects.all()), [i0, i2])
        self.assertEqual(list(Exchange.objects.all()), [e])

        get = dict(fact=f.id, item=i2.id)
        r = self.client.get(reverse('facts:index'), get)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(list(Fact.objects.all()), [f])
        self.assertEqual(list(Item.objects.all()), [i0, i2])
        self.assertEqual(list(Exchange.objects.all()), [e])

    def testJson(self):
        f = Fact(title='f')
        f.save()
        e = Exchange(title='e')
        e.save()
        i0 = Item(fact=f, tense=timezone.now(), cost=1, exchange=e, a='2')
        i0.save()
        i1 = Item(fact=f, tense=timezone.now(), cost=1, exchange=e, a='1')
        i1.save()
        i2 = Item(fact=f, tense=timezone.now(), cost=1, exchange=e, a='2')
        i2.save()
        r = self.client.get('/facts/%s/a/' % f.id)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, '["2", "1"]')

        r = self.client.get('/facts/%s/b/' % f.id)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, '[]')

        r = self.client.get('/facts/%s/c/' % f.id)
        self.assertEqual(r.status_code, 404)

        r = self.client.get('/facts/%s/tense/' % f.id)
        self.assertEqual(r.status_code, 404)
