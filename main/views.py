from django.http import JsonResponse
from django.shortcuts import render
from .models import Item, Box
import json

def main_view(request):
    items = Item.objects.all()
    return render(request, 'main/main.html', {'items': items})

# View to handle adding a new item
def add_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse incoming JSON data
        title = data.get('title')  # Get the title for the new item
        
        if title:
            # Create and save the new Item
            new_item = Item(title=title)
            new_item.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Title is required'})
        
# View to handle deleting a specific item
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)  # Get the item based on the ID
        item.delete()  # Delete the item
        return JsonResponse({'success': True})
    except Item.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})

def add_box(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        value = data.get('value')

        item = Item.objects.get(id=item_id)
        new_box = Box(item=item, value=value)
        new_box.save()

        return JsonResponse({'success': True})

def delete_box(request, box_id):
    box = Box.objects.get(id=box_id)
    box.delete()
    return JsonResponse({'success': True})