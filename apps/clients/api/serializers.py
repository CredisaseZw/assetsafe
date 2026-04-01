from rest_framework import serializers
from apps.clients.models.models import Client
from apps.individuals.models import Individual
from apps.companies.models import CompanyBranch
from django.contrib.contenttypes.models import ContentType

class MinimalClientSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_client_type_display')
    status = serializers.CharField(source='get_status_display')
    
    class Meta:
        model = Client
        fields = ['id', 'name', 'type', 'status']
        read_only_fields = fields

class IndividualClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = ['id', 'full_name', 'identification_number', 'email', 'mobile_phone']

class CompanyBranchClientSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.registration_name')
    
    class Meta:
        model = CompanyBranch
        fields = ['id', 'branch_name', 'company_name', 'is_headquarters']
class FullClientSerializer(serializers.ModelSerializer):
    client_details = serializers.SerializerMethodField()
    type = serializers.CharField(source='get_client_type_display')
    status = serializers.CharField(source='get_status_display')
    has_users = serializers.SerializerMethodField()
    subscriptions = serializers.CharField(source='get_subscriptions', allow_null=True)
    
    
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'type', 'status', 'client_details',
            'external_client_id', 'date_created', 'date_modified',
            'has_users', 'subscriptions'
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
            'id', 'name', 'client_type', 'status', 
            'individual_id', 'company_branch_id'
        ]
    
    def validate(self, data):
        individual_id = data.get('individual_id')
        company_branch_id = data.get('company_branch_id')
        
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
        individual_id = validated_data.pop('individual_id', None)
        company_branch_id = validated_data.pop('company_branch_id', None)

        if individual_id:
            self.create_object_helper(Individual, individual_id, validated_data)
        elif company_branch_id:
            self.create_object_helper(CompanyBranch, company_branch_id, validated_data)
        return super().create(validated_data)

    def create_object_helper(self, model_class, object_id, validated_data):
        content_type = ContentType.objects.get_for_model(model_class)
        validated_data['client_content_type'] = content_type
        validated_data['client_object_id'] = object_id