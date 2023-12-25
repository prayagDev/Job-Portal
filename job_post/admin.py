from django.contrib import admin
from job_post.models import Post, Category
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'employer_link', 'created_date', 'updated_date']

    def employer_link(self, obj):
        employer_url = reverse("admin:auth_user_change", args=[obj.employer.id])
        return mark_safe(f'<a href="{employer_url}">{obj.employer}</a>')
    
    employer_link.short_description = 'Employer'

admin.site.register(Category)
