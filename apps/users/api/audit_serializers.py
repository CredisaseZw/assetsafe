"""
Serializer for the AuditLog model — read-only, staff-only endpoint.
"""

from rest_framework import serializers

from apps.users.models.audit import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    created_by_username = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "timestamp",
            "created_by",
            "created_by_username",
            "action",
            "resource_type",
            "resource_id",
            "details",
            "ip_address",
            "user_agent",
            "success",
        ]
        read_only_fields = fields

    def get_created_by_username(self, obj) -> str | None:
        return obj.created_by.username if obj.created_by else None
