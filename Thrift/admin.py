from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from Thrift.models import *
# Register your models here.


class ImageInline(admin.StackedInline):
    model=ImageProd
    extra = 0
    fk_name = "product"
    can_delete = True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline,]
    list_display = ("shop", "size","price",)
    search_fields = ("size", "shop","price","type","genders",)
    exclude = ("user","sold","sent","accepted",)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.user or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and (request.user == obj.user or request.user.is_superuser):
            return True
        return False

admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("user",)
    exclude = ("user",)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.sold=False
        obj.sent=False
        obj.accepted=False
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.user or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and (request.user == obj.user or request.user.is_superuser):
            return True
        return False

admin.site.register(Order, OrderAdmin)

class CommentInline(admin.StackedInline):
    model=Comment
    extra = 0
    fk_name = "userTo"
    can_delete = True
    exclude = ("user",)
    def has_delete_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj=None):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'userFrom':
            kwargs['widget'] = forms.HiddenInput()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['userFrom'].initial = request.user
        return formset


class CustomUserAdmin(UserAdmin):
    inlines = [CommentInline]
    add_permission = 'auth.add_user'
    fieldsets = UserAdmin.fieldsets + (
        ('Image', {'fields': ('image',)}),
    )
    #filter_horizontal = ('blocked_users',)

    obj = None

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.obj = obj
        return super(CustomUserAdmin, self).get_form(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user==obj:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user==obj:
            return True
        return False

    def has_add_permission(self, request):
        return True

    obj = None

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.obj = obj
        return super(CustomUserAdmin, self).get_form(request, obj, **kwargs)

    #def formfield_for_manytomany(self, db_field, request, **kwargs):
    #    if db_field.name == 'blocked_users':
    #        # Filter the queryset for the foreign key field
    #        kwargs['queryset'] = CustomUser.objects.exclude(id=self.obj.id)
    #    return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(CustomUser, CustomUserAdmin)

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ("user",)
    exclude = ("user",)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and (request.user == obj.user or request.user.is_superuser):
            return True
        return False

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and (request.user == obj.user or request.user.is_superuser):
            return True
        return False

class ColorAdmin(admin.ModelAdmin):
    list_display = ("color",)

    def get_form(self, request, obj=None, **kwargs):
        # Get the form from the parent class
        form = super().get_form(request, obj, **kwargs)

        # Get the existing color choices from the database
        existing_colors = Color.objects.values_list('color', flat=True)

        # Exclude the existing colors from the choices
        choices = [choice for choice in Color.colorList if choice[0] not in existing_colors]

        # Set the filtered choices for the 'color' field in the form
        form.base_fields['color'].choices = choices

        return form

    def has_change_permission(self, request, obj=None):
        if obj and request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and request.user.is_superuser:
            return True
        return False

admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Color, ColorAdmin)

