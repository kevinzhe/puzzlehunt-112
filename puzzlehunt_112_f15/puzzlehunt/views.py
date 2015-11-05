from django.shortcuts import render
from django.http import HttpResponse #tmp
from django.contrib.auth.decorators import login_required
from .models import *


def home(request):
    return render(request, 'puzzlehunt/home.html')

@login_required
def puzzle(request, puzzle_id):
    return HttpResponse(puzzle_id)

@login_required
def puzzle_index(request):
    return render(request, 'puzzlehunt/puzzle-index.html', {'puzzles':Puzzle.objects.all()})
