from django.contrib import admin
from django.utils.html import format_html  #修改日期用
from .models import Event, Program, Zone, Seat, Venue, DiscountCode, Player, ZoneForNumberRow, SeatForNumberRow
from django.forms import TextInput


# Register your models here.
class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1  # 初始显示的空白条目数量
    fields = ['title', 'composer', "description"]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'composer':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        if db_field.name == 'title':
            kwargs['widget'] = TextInput(attrs={'size': "15"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 3  # 初始显示的空白条目数量
    fields = ['title', 'name']

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'title':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class ZoneInline(admin.TabularInline):
    model = Zone
    extra = 3

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'size': "10"})
        if db_field.name == 'eng_name':
            kwargs['widget'] = TextInput(attrs={'size': "10"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class SeatsInline(admin.TabularInline):
    model = Seat
    extra = 30  # 初始显示的空白条目数量
    fields = ['seat_num', "price", "color", "not_sell", "is_chair", "zone", "is_sold"]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'seat_num':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class PhotoInline(admin.TabularInline):
    model = Program
    extra = 1  # 初始显示的空白条目数量
    fields = ['title', 'composer', "description"]


class DiscountCodeInline(admin.TabularInline):
    model = DiscountCode
    extra = 2

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'code':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        if db_field.name  == 'discount':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class ZoneForNumInline(admin.TabularInline):
    model = ZoneForNumberRow
    extra = 3

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'name':
            kwargs['widget'] = TextInput(attrs={'size': "10"})
        if db_field.name == 'eng_name':
            kwargs['widget'] = TextInput(attrs={'size': "10"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class SeatsForNumInline(admin.TabularInline):
    model = SeatForNumberRow
    extra = 30  # 初始显示的空白条目数量
    fields = ["row_num", 'seat_num', "price", "color", "not_sell", "is_chair", "zone"]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'seat_num':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


# 自定義欄位
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "venue", "on_sell")
    search_fields = ("title", "venue")
    inlines = [ProgramInline, PlayerInline, ZoneInline, DiscountCodeInline, ZoneForNumInline]

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
    list_display = ['seat_num', "is_sold"]
    search_fields = ["seat_num"]

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
    list_display = ["event", "name", "area", "price"]
    inlines = [SeatsInline]
    ordering = ["-price", "area"]  # 按價錢（price）排列
    search_fields = ['event__title']


@admin.register(ZoneForNumberRow)
class ZoneForNumberRowAdmin(admin.ModelAdmin):
    list_display = ["event", "name", "area", "price"]
    inlines = [SeatsForNumInline]
    ordering = ["-price", "area"]  # 按價錢（price）排列
    search_fields = ['event__title']


@admin.register(SeatForNumberRow)
class SeatForNumberRowAdmin(admin.ModelAdmin):
    list_display = ["row_num", 'seat_num', "is_sold"]
    search_fields = ["seat_num", "row_num"]
