from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$',                          
        views.home,
        name='puzzlehunt-home'),
    url(r'^p/$',
        views.PuzzleIndex.as_view(),
        name='puzzle-index'),
    url(r'^p/start/',
        views.StartPuzzleHuntView.as_view()),
    url(r'^p/(?P<puzzle_id>[0-9]+)/$',
        views.PuzzleView.as_view(),
        name='puzzle'),
    url(r'^p/(?P<puzzle_id>[0-9]+)/hint/(?P<hint_id>[0-9]+)$',
        views.PuzzleHintView.as_view(),
        name='puzzle-hint'),
    url(r'^register',
        views.RegistrationView.as_view(),
        name='register'),
    url(r'jointeamid/(?P<teamID>[A-Za-z0-9-_]+)$',
        views.JoinTeamID.as_view()),
    url(r'^jointeam',
        views.JoinTeamView.as_view()),
    url(r'^maketeam',
        views.MakeTeamView.as_view()),
    url(r'^teampage',
        views.TeamPageView.as_view()),
    url(r'^scoreboard',
        views.ScoreboardView.as_view()),
    url(r'^login$',
        auth_views.login,
        {'template_name':'login.html', 'extra_context':{'next':'/'}},
        name='login'),
    url(r'^logout$',
        auth_views.logout,
        {'next_page': views.home},
        name='logout'),
]
