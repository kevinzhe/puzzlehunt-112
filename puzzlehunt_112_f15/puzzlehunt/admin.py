from django.contrib import admin
from .models import Team, TeamMember, Puzzle, Hint, PuzzleProgress, ValidUser, PuzzleMedia


class HintInline(admin.StackedInline):
    model = Hint
    extra = 1

class PuzzleMediaInline(admin.StackedInline):
    model = PuzzleMedia
    extra = 1

class PuzzleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Meta',
            {'fields': [
                'order',
                'title',
                'subtitle',
                'authors',
            ]}),
        ('Puzzle',
            {'fields': [
                'flavortext',
                'solution',
                'time_limit',
                'par_score',
            ]})
    ]
    inlines = [HintInline, PuzzleMediaInline]

admin.site.register(Puzzle, PuzzleAdmin)

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 4

class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamMemberInline]

admin.site.register(Team, TeamAdmin)

admin.site.register(PuzzleProgress)

admin.site.register(ValidUser)
