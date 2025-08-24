from django.shortcuts import render

def home(request):
    """
    Render the home page of Don's Table.
    Template:
        base.html
    """
    return render(request, 'base.html')