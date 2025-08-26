from django.shortcuts import render

def home(request):
    """
    Render the home page of Don's Table.
    Template:
        base.html
    """
    return render(request, 'base.html')

def contact(request):
    """
    Render the contact page of Don's Table.
    Template:
        contact.html
    """
    return render(request, "contact.html")