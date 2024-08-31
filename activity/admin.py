from django.contrib import admin
from django.utils.html import format_html  #修改日期用
from .models import Event, Program, Zone, Seat, Venue, DiscountCode
from django.forms import TextInput


# Register your models here.
class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1  # 初始显示的空白条目数量
    fields = ['title', 'composer', "description"]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'composer':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class ZoneInline(admin.TabularInline):
    model = Zone
    extra = 3


class DiscountCodeInline(admin.TabularInline):
    model = DiscountCode
    extra = 2

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'code':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        if db_field.name == 'discount':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class SeatsInline(admin.TabularInline):
    model = Seat
    extra = 10  # 初始显示的空白条目数量
    fields = ['seat_num', "zone"]  # 控制显示字段的顺序


class PhotoInline(admin.TabularInline):
    model = Program
    extra = 1  # 初始显示的空白条目数量
    fields = ['title', 'composer', "description"]


# 自定義欄位
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "place", "venue", "on_sell")
    search_fields = ("title", "place")
    inlines = [ProgramInline, ZoneInline, DiscountCodeInline]

    def formatted_date(self, obj):
        # 將日期格式化為 YYYY,M,D
        return format_html(f"{obj.date.year}.{obj.date.month}.{obj.date.day}")

    formatted_date.short_description = 'date'


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['event', 'title']
    search_fields = ['title']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "total_seats"]  # 控制列表显示的字段


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_num']  # 控制显示字段的顺序

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "zone":
            if request.resolver_match.kwargs.get('object_id'):
                event_id = request.resolver_match.kwargs['object_id']
                kwargs["queryset"] = Zone.objects.filter(event_id=event_id)
            else:
                kwargs["queryset"] = Zone.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ["event", "name", "price"]
    inlines = [SeatsInline]