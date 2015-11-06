from django.contrib import admin
from .models import Team, TeamMember, Puzzle, Hint, PuzzleProgress


class HintInline(admin.StackedInline):
    model = Hint
    extra = 1

class PuzzleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Meta',
            {'fields': [
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
                'image'
            ]})
    ]
    inlines = [HintInline]

admin.site.register(Puzzle, PuzzleAdmin)


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 4

class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamMemberInline]

admin.site.register(Team, TeamAdmin)

admin.site.register(PuzzleProgress)
