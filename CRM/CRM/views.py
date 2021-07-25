from django.shortcuts import render


def main_index(request):
    name = ["Oleg", "Vasya", "Petya"]
    return render(request, 'API/index.html', context={'names': name})
