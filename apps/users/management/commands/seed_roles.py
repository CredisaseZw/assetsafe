# users/management/commands/seed_roles.py

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from apps.users.models.models import Role


class Command(BaseCommand):
    help = (
        "Seeds initial roles and assigns relevant permissions for the AssetSafe system."
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting roles seeding..."))

        roles_data = [
            {
                "name": "admin",
                "description": "System Administrator with full access to the entire system.",
                "permissions": "__ALL__",
            },
            {
                "name": "financier",
                "description": "Registers and manages assets, collateral, hire purchase agreements, and clients.",
                "permissions": [
                    "asset_management.add_assetregistration",
                    "asset_management.change_assetregistration",
                    "asset_management.delete_assetregistration",
                    "asset_management.view_assetregistration",
                    "clients.add_client",
                    "clients.change_client",
                    "clients.delete_client",
                    "clients.view_client",
                    "collateral.add_collateralregistration",
                    "collateral.change_collateralregistration",
                    "collateral.delete_collateralregistration",
                    "collateral.view_collateralregistration",
                    "companies.add_company",
                    "companies.change_company",
                    "companies.delete_company",
                    "companies.view_company",
                    "companies.add_companybranch",
                    "companies.change_companybranch",
                    "companies.delete_companybranch",
                    "companies.view_companybranch",
                    "companies.add_companyprofile",
                    "companies.change_companyprofile",
                    "companies.delete_companyprofile",
                    "companies.view_companyprofile",
                    "companies.add_contactperson",
                    "companies.change_contactperson",
                    "companies.delete_contactperson",
                    "companies.view_contactperson",
                    "hire_purchase.add_hirepurchaseregistration",
                    "hire_purchase.change_hirepurchaseregistration",
                    "hire_purchase.delete_hirepurchaseregistration",
                    "hire_purchase.view_hirepurchaseregistration",
                    "individuals.add_employmentdetail",
                    "individuals.change_employmentdetail",
                    "individuals.delete_employmentdetail",
                    "individuals.view_employmentdetail",
                    "individuals.add_individual",
                    "individuals.change_individual",
                    "individuals.delete_individual",
                    "individuals.view_individual",
                    "individuals.add_individualaccounts",
                    "individuals.change_individualaccounts",
                    "individuals.delete_individualaccounts",
                    "individuals.view_individualaccounts",
                    "individuals.add_individualcontactdetail",
                    "individuals.change_individualcontactdetail",
                    "individuals.delete_individualcontactdetail",
                    "individuals.view_individualcontactdetail",
                    "individuals.add_nextofkin",
                    "individuals.change_nextofkin",
                    "individuals.delete_nextofkin",
                    "individuals.view_nextofkin",
                    "users.add_customuser",
                    "users.change_customuser",
                    "users.view_customuser",
                ],
            },
            {
                "name": "company_client",
                "description": "Company client accessing the system to view their registered assets, collateral and agreements. Can manage sub-users.",
                "permissions": [
                    "asset_management.view_assetregistration",
                    "collateral.view_collateralregistration",
                    "hire_purchase.view_hirepurchaseregistration",
                    "companies.view_company",
                    "companies.view_companybranch",
                    "companies.view_companyprofile",
                    "companies.view_contactperson",
                    # Permissions specific to managing users under their client
                    "users.add_customuser",
                    "users.change_customuser",
                    "users.view_customuser",
                ],
            },
            {
                "name": "individual_client",
                "description": "Individual client accessing the system to view their registered assets, collateral and agreements.",
                "permissions": [
                    "asset_management.view_assetregistration",
                    "collateral.view_collateralregistration",
                    "hire_purchase.view_hirepurchaseregistration",
                    "individuals.view_employmentdetail",
                    "individuals.view_individual",
                    "individuals.view_individualaccounts",
                    "individuals.view_individualcontactdetail",
                    "individuals.view_nextofkin",
                    "users.view_customuser",
                ],
            },
        ]

        try:
            with transaction.atomic():
                for role_info in roles_data:
                    role_name = role_info["name"]
                    permissions_list = role_info["permissions"]
                    description = role_info.get("description", "")

                    role, created = Role.objects.get_or_create(
                        name=role_name, defaults={"description": description}
                    )

                    if not created and role.description != description:
                        role.description = description
                        role.save()

                    if created:
                        self.stdout.write(f"  Role '{role_name}' created.")
                    else:
                        self.stdout.write(
                            f"  Role '{role_name}' already exists. Updating permissions..."
                        )

                    role.permissions.clear()

                    if permissions_list == "__ALL__":
                        all_permissions = Permission.objects.all()
                        role.permissions.set(all_permissions)
                        self.stdout.write(
                            f"    Assigned ALL permissions to '{role_name}'."
                        )
                    else:
                        for perm_string in permissions_list:
                            try:
                                app_label, codename = perm_string.split(".")
                                permission = Permission.objects.get(
                                    content_type__app_label=app_label, codename=codename
                                )
                                role.permissions.add(permission)
                            except Permission.DoesNotExist:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"    Warning: Permission '{perm_string}' not found. Skipping."
                                    )
                                )
                            except ValueError:
                                self.stdout.write(
                                    self.style.ERROR(
                                        f"    Error: Invalid permission format '{perm_string}'. Expected 'app_label.codename'. Skipping."
                                    )
                                )

                        self.stdout.write(
                            f"    Assigned specific permissions to '{role_name}'."
                        )

            self.stdout.write(
                self.style.SUCCESS("\nRoles seeding completed successfully!")
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"An error occurred during roles seeding: {e}")
            )
            raise CommandError(f"Seeding failed: {e}")
