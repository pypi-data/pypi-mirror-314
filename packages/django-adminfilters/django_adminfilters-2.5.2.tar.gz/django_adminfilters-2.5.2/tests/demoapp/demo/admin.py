from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.admin import UserAdmin

from adminfilters.autocomplete import AutoCompleteFilter, LinkedAutoCompleteFilter
from adminfilters.combo import ChoicesFieldComboFilter
from adminfilters.depot.widget import DepotManager
from adminfilters.filters import (
    BooleanRadioFilter,
    DjangoLookupFilter,
    IntersectionFieldListFilter,
    NumberFilter,
    QueryStringFilter,
    RelatedFieldCheckBoxFilter,
    RelatedFieldRadioFilter,
    UnionFieldListFilter,
    ValueFilter,
)
from adminfilters.json import JsonFieldFilter
from adminfilters.mixin import AdminAutoCompleteSearchMixin, AdminFiltersMixin
from adminfilters.value import MultiValueFilter

from .models import Artist, Band, City, Country, Region


class DebugChangeList(ChangeList):
    def get_queryset(self, request):
        try:
            return super().get_queryset(request)
        except Exception as e:
            raise Exception(f"{e.__class__.__name__}: {e}")

    def get_filters(self, request):
        try:
            return super().get_filters(request)
        except Exception as e:
            raise Exception(f"{e.__class__.__name__}: {e}")


class DebugMixin:
    def get_changelist(self, request, **kwargs):
        return DebugChangeList


class DemoModelAdmin_RelatedFieldCheckBoxFilter(DebugMixin, ModelAdmin):
    list_display = [f.name for f in Artist._meta.fields]
    list_filter = (("bands", RelatedFieldCheckBoxFilter),)
    search_fields = ("name",)


class DemoModelAdmin_RelatedFieldRadioFilter(DebugMixin, ModelAdmin):
    list_display = [f.name for f in Artist._meta.fields]
    list_filter = (("bands", RelatedFieldRadioFilter),)
    search_fields = ("name",)


class DemoModelAdmin_UnionFieldListFilter(DebugMixin, ModelAdmin):
    # list_display = [f.name for f in Artist._meta.fields]
    list_display = ["name", "last_name", "full_name", "country", "year_of_birth", "active", "_bands"]
    list_filter = (("bands", UnionFieldListFilter),)
    search_fields = ("name",)

    def _bands(self, obj):
        return [b.name for b in obj.bands.all()]


class DemoModelAdmin_IntersectionFieldListFilter(DebugMixin, ModelAdmin):
    list_display = ["name", "last_name", "full_name", "country", "year_of_birth", "active", "_bands"]
    list_filter = (("bands", IntersectionFieldListFilter),)
    search_fields = ("name",)

    def _bands(self, obj):
        return [b.name for b in obj.bands.all()]


class DemoModelFieldAdmin(DebugMixin, AdminFiltersMixin, ModelAdmin):
    list_display = ("char", "integer", "logic", "email", "choices", "date")
    list_filter = (
        QueryStringFilter,
        ("choices", ChoicesFieldComboFilter),
        ("integer", NumberFilter),
    )


class CountryModelAdmin(AdminAutoCompleteSearchMixin, DebugMixin, ModelAdmin):
    list_display = [f.name for f in Country._meta.fields]
    search_fields = ("name",)


class RegionModelAdmin(AdminAutoCompleteSearchMixin, DebugMixin, ModelAdmin):
    list_display = [f.name for f in Region._meta.fields]
    search_fields = ("name",)


class CityModelAdmin(AdminAutoCompleteSearchMixin, DebugMixin, ModelAdmin):
    list_display = [f.name for f in City._meta.fields]
    search_fields = ("name",)


class BandModelAdmin(DebugMixin, ModelAdmin):
    list_display = [f.name for f in Band._meta.fields]
    search_fields = ("name",)
    list_filter = ("genre", ChoicesFieldComboFilter), ("active", BooleanRadioFilter),


class ArtistModelAdmin(DebugMixin, AdminFiltersMixin, ModelAdmin):
    list_display = [f.name for f in Artist._meta.fields]
    list_filter = (
        DepotManager,
        ("country", AutoCompleteFilter),
        ('favourite_city__region__country',
         LinkedAutoCompleteFilter.factory(title='Favourite Country')),
        ("favourite_city__region",
         LinkedAutoCompleteFilter.factory(title="Favourite Region", parent='favourite_city__region__country')),
        ("favourite_city",
         LinkedAutoCompleteFilter.factory(title="Favourite City", parent='favourite_city__region')),
        ("year_of_birth", NumberFilter),
        ("bands__name", MultiValueFilter),
        QueryStringFilter,
        DjangoLookupFilter,
        ("country__name", ValueFilter),
        ("name", MultiValueFilter),
        ("last_name", ValueFilter.factory(lookup_name="istartswith", title="LastName")),
        ("flags", JsonFieldFilter.factory(can_negate=True, options=True)),
        ("active", BooleanRadioFilter),
    )
    search_fields = ("name",)


class IUserAdmin(DebugMixin, AdminFiltersMixin, UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = (("username", ValueFilter.factory(lookup_name="istartswith")),)
