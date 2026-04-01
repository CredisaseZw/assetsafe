import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.common.models.models import Country, Province, City, Suburb
from apps.common.seeding.location_data import COUNTRIES_DATA, PROVINCES_DATA, CITIES_DATA, SUBURBS_DATA

class Command(BaseCommand):
    help = 'Seeds initial geographical data (Countries, Provinces, Cities, Suburbs).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting geographical data seeding..."))

        # --- Seed Countries ---
        with transaction.atomic():
            for data in COUNTRIES_DATA:
                country, created = Country.objects.update_or_create(
                    code=data['code'],
                    defaults={
                        'name': data['name'],
                        'slug': data['slug'],
                        'dial_code': data['dial_code'],
                        'currency_code': data['currency_code'],
                        'currency_name': data['currency_name'],
                        'is_active': data['is_active'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Country: {country.name}"))
                else:
                    self.stdout.write(self.style.MIGRATE_HEADING(f"Updated Country: {country.name}"))

        self.stdout.write(self.style.NOTICE("Countries seeding complete."))

        # --- Seed Provinces ---
        with transaction.atomic():
            for data in PROVINCES_DATA:
                try:
                    country = Country.objects.get(code=data['country_code'])
                except Country.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Country with code '{data['country_code']}' not found for Province '{data['province_name']}'. Skipping."))
                    continue

                province, created = Province.objects.update_or_create(
                    country=country,
                    code=data['province_code'],
                    defaults={
                        'name': data['province_name'],
                        'slug': data['province_slug'],
                        'is_active': True,
                        'approved': bool(data['approved']),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Province: {province.name} ({country.name})"))
                else:
                    self.stdout.write(self.style.MIGRATE_HEADING(f"Updated Province: {province.name} ({country.name})"))

        self.stdout.write(self.style.NOTICE("Provinces seeding complete."))

        # --- Seed Cities ---
        with transaction.atomic():
            for data in CITIES_DATA:
                try:
                    country = Country.objects.get(code=data['country_code'])
                    province = Province.objects.get(country=country, slug=data['province_slug'])
                except (Country.DoesNotExist, Province.DoesNotExist):
                    self.stdout.write(self.style.ERROR(f"Country/Province not found for City '{data['city_name']}'. Skipping."))
                    continue

                city, created = City.objects.update_or_create(
                    province=province,
                    slug=data['city_slug'],
                    defaults={
                        'name': data['city_name'],
                        'is_active': True,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created City: {city.name} ({province.name})"))
                else:
                    self.stdout.write(self.style.MIGRATE_HEADING(f"Updated City: {city.name} ({province.name})"))

        self.stdout.write(self.style.NOTICE("Cities seeding complete."))

        # --- Seed Suburbs ---
        with transaction.atomic():
            for data in SUBURBS_DATA:
                try:
                    country = Country.objects.get(code=data['country_code'])
                    province = Province.objects.get(country=country, slug=data['province_slug'])
                    city = City.objects.get(province=province, slug=data['city_slug'])
                except (Country.DoesNotExist, Province.DoesNotExist, City.DoesNotExist):
                    self.stdout.write(self.style.ERROR(f"Country/Province/City not found for Suburb '{data['suburb_name']}'. Skipping."))
                    continue

                suburb, created = Suburb.objects.update_or_create(
                    city=city,
                    slug=data['suburb_slug'],
                    defaults={
                        'name': data['suburb_name'],
                        'is_active': True,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created Suburb: {suburb.name} ({city.name})"))
                else:
                    self.stdout.write(self.style.MIGRATE_HEADING(f"Updated Suburb: {suburb.name} ({city.name})"))

        self.stdout.write(self.style.NOTICE("Suburbs seeding complete."))
        self.stdout.write(self.style.SUCCESS("Geographical data seeding finished successfully!"))