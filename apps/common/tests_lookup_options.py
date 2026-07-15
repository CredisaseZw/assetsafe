from django.test import SimpleTestCase
from rest_framework import serializers

from apps.common.api.lookup_serializers import LookupOptionSerializer


class LookupOptionSerializerTests(SimpleTestCase):
    def test_normalizes_value(self):
        ser = LookupOptionSerializer()
        self.assertEqual(ser.validate_value("Near New"), "near_new")

    def test_rejects_bad_value(self):
        ser = LookupOptionSerializer()
        with self.assertRaises(serializers.ValidationError):
            ser.validate_value("123bad")

    def test_rejects_bad_category(self):
        ser = LookupOptionSerializer()
        with self.assertRaises(serializers.ValidationError):
            ser.validate_category("CustodyType")
