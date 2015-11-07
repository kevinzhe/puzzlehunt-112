from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from puzzlehunt.models import Puzzle, PuzzleProgress, Hint, Team, TeamMember
from django.views.generic import View
from django import forms


class PuzzleSolutionForm(forms.Form):
    solution = forms.CharField()

class PuzzleView(View):

    @method_decorator(login_required)
    def get(self, request, puzzle_id):
        # Get the team
        try: team = TeamMember.objects.get(user=request.user).team
        except TeamMember.DoesNotExist: return redirect(home)
        # Get the puzzle+hints
        puzzle = get_object_or_404(Puzzle, order=puzzle_id)
        hints = Hint.objects.filter(puzzle=puzzle)
        # Get the progress
        try: progress = PuzzleProgress.objects.get(puzzle=puzzle, team=team)
        except PuzzleProgress.DoesNotExist:
            progress = PuzzleProgress(
                team        = team,
                puzzle      = puzzle,
                start_time  = now()
            )
            progress.save()
        for hint in hints:
            hint.can_show = progress.start_time+hint.time_shown < now()
            hint.time_to_show = int((progress.start_time+hint.time_shown).timestamp())
        # Render the view
        template_info = {
            'form':         PuzzleSolutionForm(),
            'order':        puzzle.order,
            'title':        puzzle.title,
            'subtitle':     puzzle.subtitle,
            'flavortext':   puzzle.flavortext,
            'par_score':    puzzle.par_score,
            'start_time':   progress.start_time,
            'end_time':     progress.end_time,
            'completed_in': progress.completed_in, 
            'score':        progress.score,
            'par_duration_human': puzzle.time_limit,
            'par_duration': int(puzzle.time_limit.total_seconds()),
            'hints':        hints,
        }
        return render(request, 'puzzlehunt/puzzle.html', template_info)

    @method_decorator(login_required)
    def post(self, request, puzzle_id):
        try: team = TeamMember.objects.get(user=request.user).team
        except TeamMember.DoesNotExist: return redirect(home)

class RegistrationView(View):
    def get(self, request):
        return render(request, 'puzzlehunt/register.html')

    def post(self, request):
        name = request.POST.get("name", None)
        andrewID = request.POST.get("andrewID", None)
        pw1 = request.POST.get("pw1", None)
        pw2 = request.POST.get("pw2", None)
        error_msg = ""
        if (not name): error_msg = "Enter a Name"
        elif (not andrewID): error_msg = "Enter an AndrewID"
        elif (not pw1): error_msg = "Enter a password"
        elif (not pw2): error_msg = "Re-enter your password"
        elif (pw1 != pw2): error_msg = "Passwords do not match"
        if (error_msg):
            return render(request, 'puzzlehunt/register.html',
                {
                    'error_msg': error_msg,
                    'name': name,
                    'andrew': andrewID,
                    'pw1': pw1,
                    'pw2': pw2
                })
        email = "%s@andrew.cmu.edu" % andrewID
        user = User.objects.create_user(andrewID, email, pw1)
        user.first_name = name
        user.save()
        authenticate(username=andrewID, password=pw1)
        return HttpResponseRedirect("/")

def home(request):
    return render(request, 'puzzlehunt/home.html')


@login_required
def puzzle_index(request):
    puzzles = Puzzle.objects.all().order_by('order')
    return render(request, 'puzzlehunt/puzzle-index.html', {'puzzles':puzzles})

