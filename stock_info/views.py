from django.shortcuts import render

# Create your views here.

def stock_view(request):

    context = {}
    query_dict = request.GET
    query = query_dict.get('q')
    

    return render(request, 'stock_info/stock_info.html', context=context)