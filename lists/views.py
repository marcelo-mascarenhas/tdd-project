from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')

    return render(request, 'home.html')

def test_only_saves_items_when_necessary(self):
    self.client.get('/')
    self.assertEqual(Item.objects.count(), 0)