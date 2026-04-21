from rest_framework import serializers
from apps.clients.models.models import Client
from apps.individuals.models import Individual
from apps.companies.models import CompanyBranch
from django.contrib.contenttypes.models import ContentType


class MinimalClientSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="get_client_type_display")
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = Client
        fields = ["id", "name", "type", "status"]
        read_only_fields = fields


class IndividualClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = ["id", "full_name", "identification_number", "email", "mobile_phone"]


class CompanyBranchClientSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.registration_name")

    class Meta:
        model = CompanyBranch
        fields = ["id", "branch_name", "company_name", "is_headquarters"]


class FullClientSerializer(serializers.ModelSerializer):
    client_details = serializers.SerializerMethodField()
    type = serializers.CharField(source="get_client_type_display")
    status = serializers.CharField(source="get_status_display")
    has_users = serializers.SerializerMethodField()
    subscriptions = serializers.CharField(source="get_subscriptions", allow_null=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "type",
            "status",
            "client_details",
            "external_client_id",
            "date_created",
            "date_modified",
            "has_users",
            "subscriptions",
        ]
        read_only_fields = fields

    def get_client_details(self, obj):
        if obj.is_individual_client:
            from apps.individuals.api.serializers import IndividualSerializer

            return IndividualSerializer(obj.linked_individual).data
        elif obj.is_company_client:
            from apps.companies.api.serializers import CompanyBranchSerializer

            return CompanyBranchSerializer(obj.linked_company_branch).data
        return None

    def get_has_users(self, obj):
        return obj.users.exists()


class ClientCreateUpdateSerializer(serializers.ModelSerializer):
    individual_id = serializers.IntegerField(write_only=True, required=False)
    company_branch_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "client_type",
            "status",
            "individual_id",
            "company_branch_id",
        ]

    def validate(self, data):
        individual_id = data.get("individual_id")
        company_branch_id = data.get("company_branch_id")

        if not individual_id and not company_branch_id:
            raise serializers.ValidationError(
                "Either individual_id or company_branch_id must be provided"
            )

        if individual_id and company_branch_id:
            raise serializers.ValidationError(
                "Cannot provide both individual_id and company_branch_id"
            )

        return data

    def create(self, validated_data):
        individual_id = validated_data.pop("individual_id", None)
        company_branch_id = validated_data.pop("company_branch_id", None)

        if individual_id:
            try:
                individual = Individual.objects.get(pk=individual_id)
                validated_data["client_content_type"] = (
                    ContentType.objects.get_for_model(Individual)
                )
                validated_data["client_object_id"] = individual.id
                if "name" not in validated_data:
                    validated_data["name"] = individual.full_name
            except Individual.DoesNotExist:
                raise serializers.ValidationError(
                    f"Individual with id {individual_id} does not exist."
                )
        elif company_branch_id:
            try:
                company_branch = CompanyBranch.objects.get(pk=company_branch_id)
                validated_data["client_content_type"] = (
                    ContentType.objects.get_for_model(CompanyBranch)
                )
                validated_data["client_object_id"] = company_branch.id
                if "name" not in validated_data:
                    validated_data["name"] = (
                        company_branch.branch_name
                        or company_branch.company.registration_name
                    )
            except CompanyBranch.DoesNotExist:
                raise serializers.ValidationError(
                    f"CompanyBranch with id {company_branch_id} does not exist."
                )

        return super().create(validated_data)
