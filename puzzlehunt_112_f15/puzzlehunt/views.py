from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpResponseForbidden    
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from puzzlehunt.models import *
from django.views.generic import View
from django import forms
import json


class StartPuzzleHuntView(View):

    @method_decorator(login_required)
    def post(self, request):
        code = request.POST.get("code")
        if (code == "taco tuesdays"):
            team = request.user.member.team
            team.curr_puzzle = 1
            team.save()
            return HttpResponseRedirect("/p/")
        else:
            return HttpResponseRedirect("/p/")

class PuzzleView(View):

    @method_decorator(login_required)
    def get(self, request, puzzle_id):
        # Get the team
        try: team = TeamMember.objects.get(user=request.user).team
        except TeamMember.DoesNotExist: return redirect(home)
        # Get the puzzle+hints
        puzzle = get_object_or_404(Puzzle, order=puzzle_id)
        hints = Hint.objects.filter(puzzle=puzzle)
        if team.curr_puzzle < puzzle.order:
            return HttpResponseRedirect('/p')
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
            'order':        puzzle.order,
            'title':        puzzle.title,
            'subtitle':     puzzle.subtitle,
            'flavortext':   puzzle.flavortext,
            'par_score':    puzzle.par_score,
            'solution':     puzzle.solution,
            'start_time':   progress.start_time,
            'end_time':     progress.end_time,
            'completed_in': str(progress.completed_in).split('.',2)[0],
            'score':        progress.score,
            'par_duration_human': puzzle.time_limit,
            'par_duration': int(puzzle.time_limit.total_seconds()),
            'hints':        hints,
        }
        return render(request, 'puzzlehunt/puzzle.html', template_info)

    @method_decorator(login_required)
    def post(self, request, puzzle_id):
        # get and validate the team
        team = request.user.member.team
        if team is None:
            return HttpResponseForbidden(json.dumps({'error': 'No team in request'}), content_type='application/json')
        try: puzzle_id = int(puzzle_id)
        except: return HttpResponse(json.dumps({'error': 'Invalid puzzle id'}), content_type='application/json')
        if team.curr_puzzle < puzzle_id:
            return HttpResponseForbidden(json.dumps({'error': 'Team hasn\'t reached this puzzle yet'}), content_type='application/json')
        # validate the solution
        user_soln = request.POST.get('solution', None)
        if user_soln is None:
            return HttpResponse(json.dumps({'error': 'solution field does not exist'}), content_type='application/json')
        if type(user_soln) is not str:
            return HttpResponse(json.dumps({'error': 'solution is not a string'}), content_type='application/json')
        # check correctness
        try: puzzle = Puzzle.objects.get(order = puzzle_id)
        except Puzzle.DoesNotExist: return HttpResponse(json.dumps({'error': 'Puzzle does not exist'}), content_type='application/json')
        correct = user_soln == puzzle.solution
        response = {
            'correct': correct,
        }
        progress = PuzzleProgress.objects.get(team=team, puzzle=puzzle)
        if correct and progress.end_time is None:
            progress.end_time = now()
            progress.save()
            team.curr_puzzle += 1
            team.save()
            response['completed_in'] = str(progress.completed_in).split('.',2)[0]
            response['solution'] = puzzle.solution
            response['score'] = progress.score
        return HttpResponse(json.dumps(response), content_type='application/json')

class PuzzleHintView(View):
    @method_decorator(login_required)
    def get(self, request, puzzle_id, hint_id):
        # Get the puzzle
        try: puzzle = Puzzle.objects.get(order=puzzle_id)
        except Puzzle.DoesNotExist: return HttpResponseNotFound(json.dumps({'error': 'Puzzle does not exist'}), content_type='application/json')
        # Get the team's progress
        try: progress = PuzzleProgress.objects.get(puzzle=puzzle, team=request.user.member.team)
        except PuzzleProgress.DoesNotExist: return HttpResponseForbidden(json.dumps({'error': 'Team has not started puzzle yet'}), content_type='application/json')
        # Get the hint
        try: hint = Hint.objects.get(puzzle=puzzle, id=hint_id)
        except Hint.DoesNotExist: return HttpResponseNotFound(json.dumps({'error': 'Hint for puzzle does not exist'}), content_type='application/json')
        # Determine if it's time to show it yet
        if (now() - progress.start_time) < hint.time_shown: return HttpResponseForbidden(json.dumps({'error': 'Team does not have access to hint yet'}), content_type='application/json')
        return HttpResponse(json.dumps({'text':hint.text}), content_type='application/json')

class RegistrationView(View):
    def get(self, request):
        return render(request, 'puzzlehunt/register.html')

    def post(self, request):
        name = request.POST.get("name", None)
        andrewID = request.POST.get("andrewID", None)
        pw1 = request.POST.get("pw1", None)
        pw2 = request.POST.get("pw2", None)
        error_msg = ""
        if (not name or type(name) is not str): error_msg = "Enter a Name"
        elif (not andrewID or type(andrewID) is not str): error_msg = "Enter an AndrewID"
        elif (not pw1 or type(pw1) is not str): error_msg = "Enter a password"
        elif (not pw2 or type(pw2) is not str): error_msg = "Re-enter your password"
        elif (pw1 != pw2): error_msg = "Passwords do not match"
        try:
            User.objects.get(username=andrewID)
            error_msg = "AndrewID already registered"
        except User.DoesNotExist:
            pass
        try:
            role = ValidUser.objects.get(andrew_id=andrewID).role
        except ValidUser.DoesNotExist:
            error_msg = "Invalid AndrewID"
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
        if role == ValidUser.ROLE_AUTHOR:
            user.is_staff = True
            user.user_permissions.add(Permission.objects.get(codename='add_puzzle'))
            user.user_permissions.add(Permission.objects.get(codename='change_puzzle'))
            user.user_permissions.add(Permission.objects.get(codename='delete_puzzle'))
            user.user_permissions.add(Permission.objects.get(codename='add_hint'))
            user.user_permissions.add(Permission.objects.get(codename='change_hint'))
            user.user_permissions.add(Permission.objects.get(codename='delete_hint'))
            user.user_permissions.add(Permission.objects.get(codename='add_puzzlemedia'))
            user.user_permissions.add(Permission.objects.get(codename='change_puzzlemedia'))
            user.user_permissions.add(Permission.objects.get(codename='delete_puzzlemedia'))
        user.save()
        member = TeamMember(user=user)
        member.save()
        auth = authenticate(username=andrewID, password=pw1)
        login(request, auth)
        return HttpResponseRedirect("/")

class JoinTeamView(View):
    @method_decorator(login_required)
    def get(self, request):
        teams = Team.objects.all()
        full_teams, unfull_teams = [], []
        for team in teams:
            num_members = len(team.members.all())
            t_obj = {
                "name": team.name,
                "id": team.id,
                "spots_left": 4-num_members,
                "has_passcode": team.passcode is not None
            }
            if num_members >= 4:
                full_teams.append(t_obj)
            else:
                unfull_teams.append(t_obj)
        has_team = bool(request.user.member.team)
        has_error = bool(request.GET.get('error'))
        context = {
            "full_teams": full_teams,
            "unfull_teams": unfull_teams,
            "has_team": has_team,
            "has_error": has_error
        }
        return render(request, 'puzzlehunt/join_team.html', context)

class JoinTeamID(View):
    @method_decorator(login_required)
    def get(self, request, teamID, error=None):
        return self.addTeamMember(request, teamID, error=error)

    def post(self, request, teamID):
        passcode = request.POST.get('passcode')
        return self.addTeamMember(request, teamID, passcode)

    def addTeamMember(self, request, teamID, passcode=None, error=None):
        if not teamID.isdigit():
            return HttpResponseRedirect("/jointeam")
        teamID = int(teamID)
        member = request.user.member

        # already has a team
        if (member.team): return HttpResponseRedirect("/")
        # team doesnt exist
        if (not Team.objects.filter(id=teamID)): return HttpResponseRedirect("/jointeam")
        
        team = Team.objects.get(id=teamID)
        # team has 4 members already
        if (len(team.members.all()) >= 4): return HttpResponseRedirect("/jointeam")

        if team.passcode is not None:
            context = { "team": team, } 
            if passcode is None:
                return render(request, 'puzzlehunt/team_passcode.html', context)
            if passcode != team.passcode:
                context['error'] = "Incorrect passcode"
                return render(request, 'puzzlehunt/team_passcode.html', context)

        member.team = team
        member.save()
        return HttpResponseRedirect("/")

def home(request):
    context = {}
    context["has_team"] = request.user.is_authenticated() and bool(request.user.member.team)
    if (context["has_team"]):
        context["team_id"] = request.user.member.team.id
    return render(request, 'puzzlehunt/home.html', context)

class MakeTeamView(View):
    @method_decorator(login_required)
    def post(self, request):
        member = request.user.member
        if (member.team): return HttpResponseRedirect("/jointeam")
        team_name = request.POST.get("team_name")
        if (not team_name): return HttpResponseRedirect("/jointeam")
        if Team.objects.filter(name=team_name): return HttpResponseRedirect("/jointeam?error=true")
        passcode = request.POST.get("passcode")
        if passcode == '':
            passcode = None
        team = Team(name=team_name, passcode=passcode)
        team.save()
        member.team = team
        member.save()
        return HttpResponseRedirect("/")

class TeamPageView(View):
    @method_decorator(login_required)
    def get(self, request):
        team = request.user.member.team
        if team is None:
            return HttpResponseRedirect("/jointeam")
        context = {}
        context["team"] = team
        context["members"] = team.members.all() 
        context['progress'] = []
        for prog in PuzzleProgress.objects.filter(team=team):
            context["progress"].append({
                'puzzle': prog.puzzle,
                'completed_in': str(prog.completed_in).split('.',2)[0],
                'score': prog.score
            })
        context['puzzles_completed'] = team.puzzles_completed
        context['total_puzzles'] = Puzzle.objects.count()
        if context['total_puzzles'] > 0:
            context['percent_complete'] = context['puzzles_completed']/context['total_puzzles']*100
        else:
            context['percent_complete'] = 0
        return render(request, 'puzzlehunt/teampage.html', context)

@login_required
def puzzle_index(request):
    team = request.user.member.team
    if team is None:
        return HttpResponseRedirect("/jointeam")
    if (team.curr_puzzle == 0):
        context = {}
        context["teamID"] = team.id
        return render(request, 'puzzlehunt/startpuzzlehunt.html', context)

    puzzles = Puzzle.objects.all().order_by('order')
    progress = PuzzleProgress.objects.filter(team=team)
    for puzzle in puzzles:
        try: puzzle.score = progress.get(puzzle=puzzle).score
        except PuzzleProgress.DoesNotExist: pass
    context = {
        'puzzles': puzzles,
        'team': team
    }
    return render(request, 'puzzlehunt/puzzle-index.html', context)

class ScoreboardView(View):
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request):
        teams = [] 
        for team in Team.objects.all():
            if team.puzzles_completed > 0:
                teams.append({
                    'score': team.score,
                    'puzzles_completed': team.puzzles_completed,
                    'name': team.name
                })
        teams.sort(key=lambda t: t['score'], reverse=True)
        context = {
            'teams': teams
        }
        return render(request, 'puzzlehunt/scoreboard.html', context)

