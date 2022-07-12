from msilib.schema import Directory
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInLine(admin.StackedInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInLine(admin.StackedInline):
    model = MovieShots
    extra = 1

    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft",)
    list_display_links = ("title",)
    list_filter = ("category", "year",)
    search_fields = ("title", "category__name",)
    inlines = [ReviewInLine, MovieShotsInLine]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["pub", "unpub"]
    readonly_fields = ("get_poster",)

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    get_poster.short_description = "Постер"

    def unpub(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_pub = "1 запись была обнавлена"            
        else:
            message_pub = f"{row_update} записей были обнавлены"
        self.message_user(request, f"{message_pub}")

    def pub(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_pub = "1 запись была обнавлена"            
        else:
            message_pub = f"{row_update} записей были обнавлены"
        self.message_user(request, f"{message_pub}")

    unpub.short_description = "Снять с публикации"
    unpub.allowed_permissions = ("change",)

    pub.short_description = "Опубликовать"
    pub.allowed_permissions = ("change",)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("movie", "name", "email", "parent", "id",)
    readonly_fields = ("name", "email",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={ obj.image.url } width="50" height="60">')

    get_image.short_description = "Изображение"



@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={ obj.image.url } width="50" height="60">')

    get_image.short_description = "Изображение"



admin.site.register(Genre)
admin.site.register(RatingStar)
admin.site.register(Rating)


admin.site.site_title = "Django Movies Admin Page"
admin.site.site_header = "Django Movies Admin Page"