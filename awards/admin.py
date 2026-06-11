from django.contrib import admin
from .models import Event, AwardSection, Category, Nominee, Vote
from .models import Nomination
from django.contrib import messages

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'event_date',
        'venue',
        'is_active'
    )


@admin.register(AwardSection)
class AwardSectionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'section'
    )
    list_filter = ('section',)


@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'category',
        'organization',
        'votes',
        'is_active'
    )

    list_filter = (
        'category',
        'is_active'
    )

    search_fields = (
        'full_name',
        'organization'
    )

admin.site.register(Vote)

@admin.action(description="Approve nominations")
def approve_nominations(modeladmin, request, queryset):

    for nomination in queryset:

        print("Processing:", nomination.nominee_name)

        if not nomination.processed:

            nominee = Nominee.objects.create(
                category=nomination.category,
                full_name=nomination.nominee_name,
                photo=nomination.photo,
                bio=nomination.bio,
                organization=nomination.organization
            )

            print("Created:", nominee.full_name)

            nomination.approved = True
            nomination.processed = True
            nomination.save()

@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):

    list_display = (
        'nominee_name',
        'category',
        'approved'
    )

    actions = [
        approve_nominations
    ]