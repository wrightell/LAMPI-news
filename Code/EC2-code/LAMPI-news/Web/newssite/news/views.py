from django.http import JsonResponse, Http404
from .models import NewsItem
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.shortcuts import render

@ensure_csrf_cookie
def reading_list(request):
    news_items = NewsItem.objects.all()
    return render(request, 'news/reading_list.html',{'news_items':news_items})

def delete_news_item(request, pk):
    if request.method == 'POST':
        try:
            news_item = get_object_or_404(NewsItem, pk=pk)
            news_item.delete()
            return JsonResponse({'status': 'success'})
        except NewsItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
