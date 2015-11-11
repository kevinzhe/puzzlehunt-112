from django.db import models
from django.conf import settings


class Team(models.Model):
    name        = models.CharField(max_length = 50)
    curr_puzzle = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, related_name="member")
    team        = models.ForeignKey(Team, related_name="members", blank=True, null=True)

class Puzzle(models.Model):
    title       = models.CharField(max_length = 50)
    subtitle    = models.CharField(max_length = 100)
    authors     = models.CharField(max_length = 200)
    flavortext  = models.TextField()
    solution    = models.TextField(help_text = 'as a Python dictionary')
    time_limit  = models.DurationField(help_text = 'in minutes')
    par_score   = models.IntegerField()
    image       = models.ImageField(upload_to = 'img')
    order       = models.IntegerField()
    def __str__(self):
        return self.title

class Hint(models.Model):
    puzzle      = models.ForeignKey(Puzzle, related_name="hints")
    text        = models.TextField()
    time_shown  = models.DurationField(help_text = 'in minutes')

class PuzzleProgress(models.Model):
    team        = models.ForeignKey(Team, related_name="puzzles_started")
    puzzle      = models.ForeignKey(Puzzle)
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField(null = True, blank = True)

    class Meta:
        unique_together = (('team','puzzle'),)

    @property
    def completed_in(self):
        if self.end_time is None: return None
        return self.end_time - self.start_time

    @property
    def score(self):
        if self.completed_in is None: return None
        timediff = max(int((self.puzzle.time_limit - self.completed_in).total_seconds()) // 60, 0)
        return self.puzzle.par_score + timediff

    def __str__(self):
        return 'Team {team} || Puzzle {puzzle}'.format(team=self.team, puzzle=self.puzzle)
