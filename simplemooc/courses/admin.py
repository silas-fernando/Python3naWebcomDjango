from django.contrib import admin

from .models import Course, Enrollment, Announcement, Comment, Lesson, Material

class CourseAdmin(admin.ModelAdmin):

	list_display = ['name', 'slug', 'start_date', 'created_at']
	search_fields = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

# Material sempre será cadastrado inline, ou seja, junto com o model principal que nesse caso é Lesson.
class MaterialInlineAdmin(admin.StackedInline): # Stacked indica a disposição dos campos do model inline.

	model = Material

class LessonAdmin(admin.ModelAdmin):

	list_display = ['name', 'number', 'course', 'release_date']
	search_fields = ['name', 'description']
	list_filter = ['created_at']

	inlines = [
		MaterialInlineAdmin
	]

admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment, Material])
admin.site.register(Lesson, LessonAdmin)