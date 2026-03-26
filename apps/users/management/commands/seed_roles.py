# users/management/commands/seed_roles.py

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from apps.users.models.models import Role 

class Command(BaseCommand):
    help = 'Seeds initial roles and assigns relevant permissions for the property management system.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting roles seeding...'))

        roles_data = [
            {
                'name': 'Admin',
                'description': 'Full administrative access to the entire system.',
                'permissions': '__ALL__', 
            },
            {
                'name': 'Superintendent',
                'description': 'Oversees building operations and maintenance, often with limited system access.',
                'permissions': [
                    'maintenance.add_maintenancerequest',
                    'maintenance.change_maintenancerequest',
                    'maintenance.view_maintenancerequest',
                    'maintenance.view_servicevendor', 
                    'properties.view_property',
                    'properties.view_unit',
                    'communications.add_message',
                    'communications.view_message',
                ]
            },
            {
                'name':'General User',
                'description':'Performs general system tasks',
                'permissions': [
                    'maintenance.view_maintenancerequest',
                    'properties.view_property',
                    'properties.view_unit',
                    'communications.view_message',
                ]
            },
            {
                'name': 'Accountant',
                'description': 'Manages all financial aspects, including invoices, payments, bank reconciliations, and financial reports.',
                'permissions': [
                    # Accounting Module
                    'accounting.add_chartofaccounts', 'accounting.change_chartofaccounts', 'accounting.delete_chartofaccounts', 'accounting.view_chartofaccounts',
                    'accounting.add_journalentry', 'accounting.change_journalentry', 'accounting.delete_journalentry', 'accounting.view_journalentry',
                    'accounting.add_bankreconciliation', 'accounting.change_bankreconciliation', 'accounting.delete_bankreconciliation', 'accounting.view_bankreconciliation',
                    'accounting.add_currency', 'accounting.change_currency', 'accounting.delete_currency', 'accounting.view_currency',
                    'accounting.add_salesitem', 'accounting.change_salesitem', 'accounting.delete_salesitem', 'accounting.view_salesitem',
                    'accounting.add_salescategory', 'accounting.change_salescategory', 'accounting.delete_salescategory', 'accounting.view_salescategory',
                    'accounting.add_vatsetting', 'accounting.change_vatsetting', 'accounting.delete_vatsetting', 'accounting.view_vatsetting',
                    'accounting.add_accountsector', 'accounting.change_accountsector', 'accounting.delete_accountsector', 'accounting.view_accountsector',
                    'accounting.add_generalledgeraccount', 'accounting.change_generalledgeraccount', 'accounting.delete_generalledgeraccount', 'accounting.view_generalledgeraccount',
                    'accounting.add_ledgertransaction', 'accounting.change_ledgertransaction', 'accounting.delete_ledgertransaction', 'accounting.view_ledgertransaction',
                    'accounting.add_transactiontype', 'accounting.change_transactiontype', 'accounting.delete_transactiontype', 'accounting.view_transactiontype',
                    # Core Payment/Invoice/Cash models
                    'accounting.add_invoice', 'accounting.change_invoice', 'accounting.delete_invoice', 'accounting.view_invoice',
                    'accounting.add_cashsale', 'accounting.change_cashsale', 'accounting.delete_cashsale', 'accounting.view_cashsale',
                    'accounting.add_creditnote', 'accounting.change_creditnote', 'accounting.delete_creditnote', 'accounting.view_creditnote',
                    'accounting.add_payment', 'accounting.change_payment', 'accounting.delete_payment', 'accounting.view_payment',
                    'accounting.add_paymentmethod', 'accounting.change_paymentmethod', 'accounting.delete_paymentmethod', 'accounting.view_paymentmethod',
                    'accounting.add_cashbook', 'accounting.change_cashbook', 'accounting.delete_cashbook', 'accounting.view_cashbook',
                    'accounting.add_cashbookentry', 'accounting.change_cashbookentry', 'accounting.delete_cashbookentry', 'accounting.view_cashbookentry',
                    'accounting.add_transactionlineitem', 'accounting.change_transactionlineitem', 'accounting.delete_transactionlineitem', 'accounting.view_transactionlineitem',
                    'accounting.add_currencyrate', 'accounting.change_currencyrate', 'accounting.delete_currencyrate', 'accounting.view_currencyrate',
                    'leases.view_lease',
                    'companies.view_company',
                    'individuals.view_individual', 
                ]
            },
            {
                'name': 'Property Manager',
                'description': 'Oversees property operations, including leases, tenants, maintenance, and basic financials.',
                'permissions': [
                    # Properties & Units Module
                    'properties.add_property', 'properties.change_property', 'properties.delete_property', 'properties.view_property',
                    'properties.add_unit', 'properties.change_unit', 'properties.delete_unit', 'properties.view_unit',

                    # Leases Module
                    'leases.add_lease', 'leases.change_lease', 'leases.delete_lease', 'leases.view_lease',
                    'leases.add_rentalapplication', 'leases.change_rentalapplication', 'leases.delete_rentalapplication', 'leases.view_rentalapplication',

                    # Individuals (Tenants, Applicants) & Companies (Landlords, Vendors) Module
                    'individuals.add_individual', 'individuals.change_individual', 'individuals.delete_individual', 'individuals.view_individual',
                    'companies.add_company', 'companies.change_company', 'companies.delete_company', 'companies.view_company',

                    # Payments/Invoices (Limited - for recording/viewing rent, not full accounting setup)
                    'accounting.add_payment', 'accounting.change_payment', 'accounting.view_payment',
                    'accounting.add_invoice', 'accounting.change_invoice', 'accounting.view_invoice', 
                    'accounting.add_cashsale', 'accounting.change_cashsale', 'accounting.view_cashsale', 
                    'accounting.view_creditnote', 
                    'accounting.view_paymentmethod', 
                    'accounting.view_cashbook', 
                    'accounting.view_cashbookentry',
                    'accounting.view_transactionlineitem', 
                    # Maintenance Module
                    'maintenance.add_maintenancerequest', 'maintenance.change_maintenancerequest', 'maintenance.delete_maintenancerequest', 'maintenance.view_maintenancerequest',
                    'maintenance.add_servicevendor', 'maintenance.change_servicevendor', 'maintenance.delete_servicevendor', 'maintenance.view_servicevendor',
                    'communications.add_message', 'communications.change_message', 'communications.view_message',
                    'documents.add_document', 'documents.change_document', 'documents.delete_document', 'documents.view_document',
                    'users.view_customuser',
                ]
            },
            {
                'name': 'Lease Administrator',
                'description': 'Specializes in lease agreements, renewals, and tenant applications.',
                'permissions': [
                    'leases.add_lease', 'leases.change_lease', 'leases.delete_lease', 'leases.view_lease',
                    'leases.add_rentalapplication', 'leases.change_rentalapplication', 'leases.delete_rentalapplication', 'leases.view_rentalapplication',
                    
                    'individuals.add_individual', 'individuals.change_individual', 'individuals.view_individual', 
                    
                    'properties.view_property', 'properties.view_unit', 
                    
                    'documents.add_document', 'documents.change_document', 'documents.delete_document', 'documents.view_document', 
                    
                    'communications.add_message', 'communications.view_message',
                    
                    'accounting.view_invoice', 
                    'accounting.view_payment', 
                ]
            },
            {
                'name': 'Maintenance Coordinator',
                'description': 'Manages maintenance requests, assigns tasks to vendors, and tracks progress.',
                'permissions': [
                    'maintenance.add_maintenancerequest', 'maintenance.change_maintenancerequest', 'maintenance.delete_maintenancerequest', 'maintenance.view_maintenancerequest',
                    'maintenance.add_servicevendor', 'maintenance.change_servicevendor', 'maintenance.delete_servicevendor', 'maintenance.view_servicevendor',
                    'properties.view_property', 'properties.view_unit',
                    'individuals.view_individual', 
                    'companies.view_company', 
                    'communications.add_message', 'communications.change_message', 'communications.view_message',
                    'accounting.view_invoice', 
                    'accounting.view_payment',
                ]
            },
            {
                'name': 'Tenant',
                'description': 'For system users who are tenants. Can view their own property/lease details, make payments, and submit maintenance requests.',
                'permissions': [
                    'properties.view_property',
                    'leases.view_lease', 
                    'accounting.add_payment', 'accounting.view_payment', 
                    'accounting.view_invoice',
                    'maintenance.add_maintenancerequest', 'maintenance.view_maintenancerequest', 
                    'documents.view_document',
                    'users.change_customuser', 'users.view_customuser', 
                    'communications.add_message', 'communications.view_message',
                ]
            },
            {
                'name': 'Agent',
                'description': 'Manages property listings, interacts with prospective tenants, and handles leads.',
                'permissions': [
                    'listings.add_listing', 'listings.change_listing', 'listings.delete_listing', 'listings.view_listing',
                    'leads.add_lead', 'leads.change_lead', 'leads.delete_lead', 'leads.view_lead',
                    
                    'properties.view_property', 'properties.view_unit', 
                    
                    'leases.add_rentalapplication', 'leases.change_rentalapplication', 'leases.view_rentalapplication', 
                    
                    'individuals.add_individual', 'individuals.change_individual', 'individuals.view_individual', 
                    
                    'communications.add_message', 'communications.change_message', 'communications.view_message',
                    'marketing.add_campaign', 'marketing.change_campaign', 'marketing.view_campaign',
                    
                    'accounting.view_salesitem', 
                ]
            },
            {
                'name': 'Analytics Manager',
                'description': 'Has comprehensive access to all data for reporting and analytical purposes.',
                'permissions': [
                    'reports.view_report', 
                    'properties.view_property', 'properties.view_unit',
                    'leases.view_lease', 'leases.view_rentalapplication',
                    
                    'accounting.view_payment', 'accounting.view_invoice', 'accounting.view_cashsale', 'accounting.view_creditnote',
                    'accounting.view_transactionlineitem', 'accounting.view_paymentmethod', 'accounting.view_cashbook', 'accounting.view_cashbookentry',
                    'accounting.view_chartofaccounts', 'accounting.view_journalentry', 'accounting.view_bankreconciliation', 'accounting.view_budget',
                    'accounting.view_currency', 'accounting.view_salesitem','accounting.view_vatsetting',
                    'accounting.view_currencyrate',
                    
                    'maintenance.view_maintenancerequest', 'maintenance.view_servicevendor',
                    'individuals.view_individual',
                    'companies.view_company',
                    'users.view_customuser',
                    'listings.view_listing',
                    'leads.view_lead',
                    'communications.view_message',
                    'documents.view_document',
                    'marketing.view_campaign',
                ]
            },
            {
                'name': 'Executive',
                'description': 'High-level oversight; typically view-only access to all critical business data and reports.',
                'permissions': [
                    # Similar to Analytics Manager, but perhaps without "add/change/delete" permissions for core data
                    # This role mostly relies on "view" permissions and custom report permissions
                    'properties.view_property', 'properties.view_unit',
                    'leases.view_lease', 'leases.view_rentalapplication',
                    
                    'accounting.view_payment', 'accounting.view_invoice', 'accounting.view_cashsale', 'accounting.view_creditnote',
                    'accounting.view_transactionlineitem', 'accounting.view_cashbook', 'accounting.view_cashbookentry',
                    'accounting.view_chartofaccounts', 'accounting.view_journalentry', 'accounting.view_bankreconciliation', 'accounting.view_budget',
                    'accounting.view_currency', 'accounting.view_salesitem',
                    
                    'maintenance.view_maintenancerequest', 'maintenance.view_servicevendor',
                    'individuals.view_individual',
                    'companies.view_company',
                    'users.view_customuser',
                    'listings.view_listing',
                    'leads.view_lead',
                    'communications.view_message',
                    'documents.view_document',
                    'marketing.view_campaign',
                ]
            },
            {
                'name': 'Vendor',
                'description': 'Limited access for service vendors to view assigned maintenance tasks and update status.',
                'permissions': [
                    'maintenance.view_maintenancerequest',
                    'maintenance.change_maintenancerequest', 
                    'communications.add_message', 'communications.view_message', 
                    'documents.view_document', 
                    'accounting.view_invoice',
                    'accounting.view_payment', 
                ]
            },
            {
                'name': 'Landlord',
                'description': 'Allows property owners to view their property details, financial statements, and tenant information.',
                'permissions': [
                    'properties.view_property', 
                    'properties.view_unit', 
                    'leases.view_lease', 
                    'individuals.view_individual', 
                    
                    'accounting.view_payment',
                    'accounting.view_invoice', 
                    'accounting.view_cashsale', 
                    'accounting.view_creditnote', 
                    'accounting.view_journalentry', 

                    'maintenance.view_maintenancerequest',
                    'documents.view_document',

                ]
            },
            {
                'name': 'Read-Only User',
                'description': 'Can view most non-sensitive data but cannot make any changes.',
                'permissions': [
                    'properties.view_property',
                    'properties.view_unit',
                    'leases.view_lease',
                    'leases.view_rentalapplication',
                    'individuals.view_individual',
                    'companies.view_company',
                    
                    'accounting.view_payment', 'accounting.view_invoice', 'accounting.view_cashsale', 'accounting.view_creditnote',
                    'accounting.view_paymentmethod', 'accounting.view_transactionlineitem', 'accounting.view_cashbook', 'accounting.view_cashbookentry',
                    'accounting.view_chartofaccounts', 'accounting.view_journalentry', 'accounting.view_bankreconciliation', 'accounting.view_budget',
                    'accounting.view_currency', 'accounting.view_salesitem', 'accounting.view_vatsetting',
                    'accounting.view_currencyrate',
                    
                    'maintenance.view_maintenancerequest',
                    'maintenance.view_servicevendor',
                    'users.view_customuser',
                    'documents.view_document',
                    'listings.view_listing',
                    'leads.view_lead',
                    'communications.view_message',
                    'marketing.view_campaign',
                    'django_admin_log.view_logentry',
                ]
            }
        ]

        with transaction.atomic():
            self.stdout.write(self.style.NOTICE('Fetching all existing permissions for validation...'))
            all_db_permissions = {
                f"{p.content_type.app_label}.{p.codename}": p
                for p in Permission.objects.select_related('content_type').all()
            }
            
            for role_data in roles_data:
                role_name = role_data['name']
                permissions_to_assign_objects = []

                self.stdout.write(f"\nProcessing role: '{role_name}'")

                if role_data['permissions'] == '__ALL__':
                    permissions_to_assign_objects = list(all_db_permissions.values())
                    self.stdout.write(f"  Role '{role_name}': Assigning ALL {len(permissions_to_assign_objects)} existing permissions.")
                else:
                    for perm_codename in role_data['permissions']:
                        if perm_codename in all_db_permissions:
                            permissions_to_assign_objects.append(all_db_permissions[perm_codename])
                        else:
                            self.stdout.write(self.style.WARNING(
                                f"  Permission '{perm_codename}' does not exist in the database. "
                                f"Skipping for role '{role_name}'. Make sure the app and model are migrated, "
                                f"and custom permissions are defined."
                            ))
                
                role, created = Role.objects.get_or_create(
                    name=role_name,
                    defaults={'description': role_data['description'], 'is_active': True}
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"  Created role: '{role.name}'"))
                else:
                    self.stdout.write(self.style.WARNING(f"  Role '{role.name}' already exists."))
                    if role.description != role_data['description']:
                        role.description = role_data['description']
                        role.save()
                        self.stdout.write(f"  Updated description for role '{role.name}'.")

                role.permissions.set(permissions_to_assign_objects)
                self.stdout.write(f"  Assigned {len(permissions_to_assign_objects)} permissions to role '{role.name}'.")

        self.stdout.write(self.style.SUCCESS('\nRoles seeding completed successfully!'))