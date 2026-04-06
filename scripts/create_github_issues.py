#!/usr/bin/env python3
"""
create_github_issues.py
=======================
Idempotent script that creates GitHub milestones, labels, and issues for the
AssetSafe MVP (3-week execution plan) using PyGithub.

Usage
-----
    python scripts/create_github_issues.py [--repo OWNER/REPO] [--dry-run]

Prerequisites
-------------
* PyGithub installed: pip install PyGithub
* GITHUB_TOKEN environment variable set with a valid GitHub token
* Repository defaults to GITHUB_REPO_OWNER/GITHUB_REPO_NAME from .env,
  OR pass --repo explicitly.

Options
-------
  --repo       GitHub repository in OWNER/REPO format.
                             Defaults to GITHUB_REPO_OWNER/GITHUB_REPO_NAME from .env.
  --dry-run    Print actions without executing them.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from urllib import error, request

from dotenv import load_dotenv
from github import Github, GithubException, Auth

# Load environment variables from .env file
load_dotenv()

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Label:
    name: str
    color: str  # 6-char hex without '#'
    description: str = ""


@dataclass
class Milestone:
    title: str
    description: str
    due_on: str  # ISO-8601, e.g. "2026-04-27T23:59:59Z"


@dataclass
class Issue:
    title: str
    body: str
    labels: list[str]
    milestone: str  # milestone title
    size: str  # XS / S / M / L / XL
    project: Optional[str] = None  # Project name
    assignee: str = ""  # filled in at runtime


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

SIZE_OPTIONS = {"XS": "XS", "S": "S", "M": "M", "L": "L", "XL": "XL"}

SIZE_TO_ESTIMATED_DURATION = {
    "XS": "<= 0.5 day",
    "S": "1 day",
    "M": "1-2 days",
    "L": "3-5 days",
    "XL": "5+ days",
}

SIZE_TO_ESTIMATE_NUMBER = {
    "XS": 0.5,
    "S": 1.0,
    "M": 2.0,
    "L": 5.0,
    "XL": 8.0,
}

LABELS: list[Label] = [
    # ---- Priority ----
    Label("priority: high", "d93f0b", "Must be completed for MVP"),
    Label("priority: medium", "fbca04", "Important but not blocking"),
    Label("priority: low", "0075ca", "Nice-to-have / post-MVP"),
    # ---- Week ----
    Label("week 1", "e4e669", "Week 1: Core foundation"),
    Label("week 2", "c5def5", "Week 2: Core features"),
    Label("week 3", "bfd4f2", "Week 3: Polish, testing & deployment"),
    # ---- Effort ----
    Label("effort: small", "c2e0c6", "Estimated: ≤ 0.5 day"),
    Label("effort: medium", "fef2c0", "Estimated: 1-2 days"),
    Label("effort: large", "f9d0c4", "Estimated: 3-5 days"),
    # ---- Epic ----
    Label("epic: setup", "1d76db", "Project setup & infrastructure"),
    Label("epic: auth", "0052cc", "Authentication & JWT"),
    Label("epic: users", "5319e7", "User management & RBAC"),
    Label("epic: common", "006b75", "Common app & shared models"),
    Label("epic: individuals", "e11d48", "Individuals app"),
    Label("epic: companies", "be4bdb", "Companies app"),
    Label("epic: clients", "f97316", "Clients abstraction layer"),
    Label("epic: asset-mgmt", "22c55e", "Asset management registry"),
    Label("epic: collateral", "84cc16", "Collateral registry"),
    Label("epic: hire-purchase", "eab308", "Hire purchase registry"),
    Label("epic: testing", "14b8a6", "Testing"),
    Label("epic: deployment", "64748b", "Deployment & DevOps"),
    Label("epic: api-polish", "a855f7", "API polish & finalization"),
    Label("critical-path", "b60205", "Must-do for MVP"),
    Label("nice-to-have", "d4c5f9", "Only if time allows"),
]

# ---------------------------------------------------------------------------
# Milestones
# ---------------------------------------------------------------------------

MILESTONES: list[Milestone] = [
    Milestone(
        title="Week 1 - Core Foundation",
        description="Project setup, authentication, user management, and common models.",
        due_on="2026-04-13T23:59:59Z",
    ),
    Milestone(
        title="Week 2 - Core Features",
        description="Individuals, companies, clients, asset management, collateral, and hire-purchase APIs.",
        due_on="2026-04-20T23:59:59Z",
    ),
    Milestone(
        title="Week 3 - Polish, Testing & Deployment",
        description="Test coverage, Docker, CI/CD, and API polish.",
        due_on="2026-04-27T23:59:59Z",
    ),
]

# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------


def _body(
    description: str,
    acceptance: list[str],
) -> str:
    ac_lines = "\n".join(f"- [ ] {line}" for line in acceptance)
    return textwrap.dedent(
        f"""\
        ## Description
        {description.strip()}

        ## Acceptance Criteria
        {ac_lines}
    """
    )


ISSUES: list[Issue] = [
    # =========================================================================
    # WEEK 1 — EPIC: Project Setup & Infrastructure
    # =========================================================================
    Issue(
        title="[W1] Configure project environment, settings splits, and .env template",
        body=_body(
            description="""\
                Establish a robust, environment-aware settings structure so the project
                can run in development, testing, and production without manual edits.
                Create a documented `.env.example` file covering every required variable.
                Confirm DEBUG, SECRET_KEY, DATABASE_URL, REDIS_URL, and ALLOWED_HOSTS
                are loaded from environment variables via `python-dotenv`.
                Activate the currently commented-out Django apps
                (users, individuals, companies, clients) in INSTALLED_APPS and add
                their URL routes to `core/urls.py`.
            """,
            acceptance=[
                "Settings load correctly from `.env` (no hard-coded secrets).",
                "`.env.example` lists every required variable with a placeholder value.",
                "All eight domain apps (users, individuals, companies, clients, asset_management, collateral, hire_purchase, common) appear in INSTALLED_APPS.",
                "All app URL namespaces are registered in `core/urls.py`.",
                "`python manage.py check` passes with no errors.",
            ],
        ),
        labels=["week 1", "priority: high", "epic: setup", "critical-path"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    Issue(
        title="[W1] Set up PostgreSQL database connection and run baseline migrations",
        body=_body(
            description="""\
                Connect the project to a PostgreSQL database, confirm all existing
                migrations are applied cleanly, and document the database setup steps.
                Resolve any migration conflicts introduced by activating the currently
                disabled apps.  Add a `makemigrations --check` step to the developer
                setup guide so unapplied schema changes are caught early.
            """,
            acceptance=[
                "A fresh `manage.py migrate` completes without errors.",
                "All app migrations are present and consistent (`showmigrations` shows no unapplied items).",
                "DATABASE_URL environment variable drives the database connection.",
                "DB setup instructions are documented in the README.",
            ],
        ),
        labels=["week 1", "priority: high", "epic: setup", "critical-path"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    Issue(
        title="[W1] Configure Celery + Redis for asynchronous task processing",
        body=_body(
            description="""\
                Celery and Redis are already listed as project dependencies.
                Wire them up: add `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`
                to settings, create `core/celery.py`, and register the Celery app
                in `core/__init__.py`.  Ensure the existing task stubs in
                `common/services/tasks.py`, `individuals/services/tasks.py`,
                `companies/services/tasks.py`, and `users/services/` are discoverable.
            """,
            acceptance=[
                "`celery -A core worker --loglevel=info` starts without import errors.",
                "A simple test task (`debug_task`) runs successfully via `delay()`.",
                "CELERY_BROKER_URL and CELERY_RESULT_BACKEND are read from environment variables.",
                "Celery is configured to auto-discover tasks in all installed apps.",
            ],
        ),
        labels=["week 1", "priority: medium", "epic: setup"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    Issue(
        title="[W1] Enable and configure drf-spectacular for OpenAPI documentation",
        body=_body(
            description="""\
                `drf-spectacular` is already installed.  Add `SPECTACULAR_SETTINGS`
                to settings (title, version, description).  Confirm the Swagger UI
                (`/api/docs/`) and ReDoc (`/api/redoc/`) endpoints render correctly
                after all apps are activated.  Add `@extend_schema` decorators to
                ViewSets where the auto-generated schema is ambiguous (custom actions,
                nested serializers).
            """,
            acceptance=[
                "`/api/schema/` returns a valid OpenAPI 3 JSON document.",
                "`/api/docs/` renders Swagger UI listing all registered endpoints.",
                "`/api/redoc/` renders ReDoc UI.",
                "SPECTACULAR_SETTINGS includes title, version, and a meaningful description.",
                "Custom actions (`discharge`, `confirm_closure`, `dashboard`) appear in the schema.",
            ],
        ),
        labels=["week 1", "priority: medium", "epic: setup"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    # =========================================================================
    # WEEK 1 — EPIC: Authentication & JWT
    # =========================================================================
    Issue(
        title="[W1] Implement JWT authentication with HTTP-only cookie strategy",
        body=_body(
            description="""\
                The project already contains `CookieJWTAuthentication` in
                `apps/users/api/authentication.py` and cookie helpers in
                `apps/users/utils/cookies.py`.  Wire these into DRF's
                `DEFAULT_AUTHENTICATION_CLASSES` setting.  Configure
                `SIMPLE_JWT` settings (access token lifetime, refresh token
                lifetime, algorithm, signing key).  Ensure the token blacklist
                is applied on logout.
            """,
            acceptance=[
                "`DEFAULT_AUTHENTICATION_CLASSES` includes `CookieJWTAuthentication`.",
                "SIMPLE_JWT settings are defined in settings and sourced from environment variables where appropriate.",
                "Successful login sets `access` and `refresh` HTTP-only cookies.",
                "Logout blacklists the refresh token and clears both cookies.",
                "Requests to protected endpoints without a valid cookie return 401.",
            ],
        ),
        labels=["week 1", "priority: high", "epic: auth", "critical-path"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    Issue(
        title="[W1] Build user registration, login, and logout API endpoints",
        body=_body(
            description="""\
                The `LoginView` and `LogoutView` already exist in
                `apps/users/api/views.py`.  Complete and stabilise them:
                validate that both views handle all edge cases (wrong password,
                unverified account, token decode error).  Implement a
                `/api/auth/register/` endpoint that creates a new `CustomUser`
                via `UserCreationService`, associates it with a `Client`, and
                sends a verification trigger (Celery task stub is acceptable
                for MVP).  Register all auth URLs under `/api/auth/`.
            """,
            acceptance=[
                "POST `/api/auth/login/` returns 200 and sets JWT cookies on valid credentials.",
                "POST `/api/auth/login/` returns 401 for invalid credentials and 403 for unverified accounts.",
                "POST `/api/auth/logout/` blacklists the refresh token and clears cookies.",
                "POST `/api/auth/register/` creates a user + client and returns 201.",
                "All three endpoints appear in the OpenAPI schema.",
            ],
        ),
        labels=["week 1", "priority: high", "epic: auth", "critical-path"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    Issue(
        title="[W1] Implement role-based access control (RBAC) and seed default roles",
        body=_body(
            description="""\
                The `Role` model and `seed_roles` management command exist in
                `apps/users/`.  Wire the role permission checking into DRF
                custom permission classes (`apps/users/utils/permissions.py`).
                Ensure the following roles are seeded: `admin`, `financier`,
                `individual_client`, `company_client`.  Document what each role
                can and cannot access.
            """,
            acceptance=[
                "`python manage.py seed_roles` creates all default roles without errors.",
                "Custom permission classes (`HasRole`, `IsVerified`) are usable as DRF `permission_classes`.",
                "Protected endpoints return 403 when a user lacks the required role.",
                "The `has_perm` method on `CustomUser` correctly delegates to assigned roles.",
                "Role seeding is idempotent (safe to run multiple times).",
            ],
        ),
        labels=["week 1", "priority: high", "epic: users", "critical-path"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    Issue(
        title="[W1] Add password change and token-refresh endpoints",
        body=_body(
            description="""\
                Implement two additional auth endpoints: (1) `/api/auth/password/change/`
                for authenticated users to change their own password (requires current
                password confirmation), and (2) `/api/auth/token/refresh/` that reads
                the refresh token from the HTTP-only cookie and returns a new access
                token in a cookie.  Update `last_password_change` on the user model
                after a successful change.
            """,
            acceptance=[
                "POST `/api/auth/password/change/` requires authentication and updates the password.",
                "`last_password_change` timestamp is updated on the `CustomUser` record.",
                "POST `/api/auth/token/refresh/` reads the refresh cookie and issues a new access cookie.",
                "Incorrect current password returns 400 with a clear error message.",
            ],
        ),
        labels=["week 1", "priority: high", "epic: auth"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    # =========================================================================
    # WEEK 1 — EPIC: Common App Foundation
    # =========================================================================
    Issue(
        title="[W1] Finalise common shared models (Address, Document, Note) and expose read APIs",
        body=_body(
            description="""\
                The `common` app already contains `Address`, `Document`, `Note`,
                and generic-relation helpers.  Ensure migrations are current,
                add serializers for each model, and expose minimal list/retrieve
                endpoints (no standalone CRUD needed — these are accessed via their
                parent resources).  Confirm the `GenericRelation` fields on
                `Individual` and `Company` work correctly via the API.
            """,
            acceptance=[
                "Migrations for `Address`, `Document`, and `Note` apply cleanly.",
                "Serializers for Address, Document, and Note are defined in `common/api/serializers.py`.",
                "Individual and Company serializers nest or link Address/Document/Note via `GenericRelation`.",
                "`python manage.py check` reports no errors related to content-type or GenericRelation setup.",
            ],
        ),
        labels=["week 1", "priority: high", "epic: common", "critical-path"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    Issue(
        title="[W1] Seed location data and currency reference data",
        body=_body(
            description="""\
                The management commands `seed_locations` and `seed_currencies`
                already exist.  Verify they run without errors against PostgreSQL,
                add them to the developer setup guide, and ensure they are idempotent
                (safe to re-run).  Also verify the `payment_methods` seed command.
            """,
            acceptance=[
                "`python manage.py seed_locations` completes without errors.",
                "`python manage.py seed_currencies` completes without errors.",
                "`python manage.py payment_methods` completes without errors.",
                "All seed commands are idempotent (re-running does not create duplicates).",
                "Setup instructions in README reference all seed commands.",
            ],
        ),
        labels=["week 1", "priority: medium", "epic: common"],
        milestone="Week 1 - Core Foundation",
        size="M",
    ),
    # =========================================================================
    # WEEK 2 — EPIC: Individuals App
    # =========================================================================
    Issue(
        title="[W2] Individual profile CRUD API",
        body=_body(
            description="""\
                Build a RESTful ViewSet (`/api/individuals/`) for the `Individual`
                model.  Support list, retrieve, create, update (partial), and soft-delete
                (set `is_deleted=True`).  Apply pagination (page 25), search on
                `first_name`, `last_name`, `identification_number`, and filter on
                `gender`, `marital_status`, `is_verified`, `is_active`.
                Require authentication; only staff or the owning user may update/delete.
            """,
            acceptance=[
                "GET `/api/individuals/` returns paginated list with search and filter support.",
                "POST `/api/individuals/` creates a new Individual and returns 201.",
                "PATCH `/api/individuals/{id}/` performs partial update.",
                "DELETE `/api/individuals/{id}/` soft-deletes (sets `is_deleted=True`).",
                "Unauthenticated requests return 401.",
                "Endpoint appears in OpenAPI schema.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: individuals", "critical-path"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Individual contact details management API",
        body=_body(
            description="""\
                The `Individual` model references `contact_details` (a reverse
                relation to a ContactDetails model if present, or it must be
                created).  Expose endpoints to add, list, update, and remove
                contact details (mobile, email, WhatsApp) for an individual.
                Nest the URL under `/api/individuals/{id}/contacts/`.
            """,
            acceptance=[
                "GET `/api/individuals/{id}/contacts/` lists all contact records.",
                "POST `/api/individuals/{id}/contacts/` adds a new contact entry.",
                "DELETE `/api/individuals/{id}/contacts/{contact_id}/` removes a contact entry.",
                "Validation ensures at least one contact method (mobile or email) is provided.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: individuals"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Individual document upload and management",
        body=_body(
            description="""\
                Allow uploading and retrieving documents (PDFs, images) for an
                individual via the `Document` GenericRelation on the `Individual`
                model.  Nest under `/api/individuals/{id}/documents/`.  Use
                Django's `ImageField`/`FileField` + `Pillow` (already a dependency).
                Store files in `MEDIA_ROOT`.  Enforce a file-size limit (10 MB) and
                allowed MIME types.
            """,
            acceptance=[
                "POST `/api/individuals/{id}/documents/` uploads a file and returns 201.",
                "GET `/api/individuals/{id}/documents/` lists documents with download URLs.",
                "DELETE `/api/individuals/{id}/documents/{doc_id}/` removes a document.",
                "Files over 10 MB return 400.",
                "Only authenticated users belonging to the same client may upload.",
            ],
        ),
        labels=["week 2", "priority: medium", "epic: individuals"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Individual verification status management",
        body=_body(
            description="""\
                Expose a dedicated action `POST /api/individuals/{id}/verify/`
                that an admin or staff user can call to flip `is_verified=True`.
                Send a Celery notification task (stub acceptable for MVP).
                Also expose `GET /api/individuals/{id}/status/` to retrieve the
                current `is_active`, `is_verified`, and `is_deleted` flags.
            """,
            acceptance=[
                "POST `/api/individuals/{id}/verify/` sets `is_verified=True` and returns 200.",
                "Only staff users can call the verify action (403 for non-staff).",
                "A Celery notification task is dispatched after verification.",
                "GET `/api/individuals/{id}/status/` returns the three status flags.",
            ],
        ),
        labels=["week 2", "priority: medium", "epic: individuals"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    # =========================================================================
    # WEEK 2 — EPIC: Companies App
    # =========================================================================
    Issue(
        title="[W2] Company profile CRUD API",
        body=_body(
            description="""\
                Build a RESTful ViewSet (`/api/companies/`) for the `Company`
                model.  Support list, retrieve, create, update (partial), and
                soft-delete.  Apply pagination, search on `registration_name`,
                `trading_name`, `registration_number`, and filter on
                `legal_status`, `is_verified`, `is_active`.
                Require authentication and appropriate role permissions.
            """,
            acceptance=[
                "GET `/api/companies/` returns paginated, filterable list.",
                "POST `/api/companies/` creates a Company with proper validation.",
                "PATCH `/api/companies/{id}/` performs partial update.",
                "DELETE `/api/companies/{id}/` soft-deletes.",
                "Endpoint appears in OpenAPI schema.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: companies", "critical-path"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Company branch management API",
        body=_body(
            description="""\
                `CompanyBranch` is a child model of `Company` (already exists in
                `apps/companies/models/`).  Expose a nested ViewSet at
                `/api/companies/{id}/branches/` to manage branches: list, create,
                update, delete.  A company must have at least one branch (HEAD OFFICE).
                Branch names must be unique per company.
            """,
            acceptance=[
                "GET `/api/companies/{id}/branches/` returns all branches for a company.",
                "POST `/api/companies/{id}/branches/` creates a branch.",
                "PATCH `/api/companies/{id}/branches/{branch_id}/` updates a branch.",
                "DELETE attempts on the last remaining branch return 400 with an error message.",
                "Branch names are unique within a company (409 on duplicate).",
            ],
        ),
        labels=["week 2", "priority: high", "epic: companies"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Company document upload and contact details management",
        body=_body(
            description="""\
                Mirror the individual document and contact APIs for companies.
                Expose `/api/companies/{id}/documents/` (upload/list/delete) and
                `/api/companies/{id}/contacts/` (add/list/delete contact methods)
                via the `Document` and `Note` GenericRelations already on the
                `Company` model.
            """,
            acceptance=[
                "POST/GET/DELETE `/api/companies/{id}/documents/` work as for individuals.",
                "POST/GET/DELETE `/api/companies/{id}/contacts/` work as for individuals.",
                "File-size and MIME-type validation applies.",
                "Only authenticated users belonging to the company's client may manage data.",
            ],
        ),
        labels=["week 2", "priority: medium", "epic: companies"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    # =========================================================================
    # WEEK 2 — EPIC: Clients App
    # =========================================================================
    Issue(
        title="[W2] Client abstraction layer CRUD API",
        body=_body(
            description="""\
                The `Client` model polymorphically wraps `Individual` or
                `CompanyBranch` via a `GenericForeignKey`.  Build a ViewSet at
                `/api/clients/` supporting list, retrieve, create, update (partial),
                and status transitions.  Include computed fields: `client_type_display`,
                `linked_entity_name`, `linked_entity_id`.
            """,
            acceptance=[
                "GET `/api/clients/` returns paginated list with `client_type`, `status`, and linked entity info.",
                "POST `/api/clients/` creates a Client linked to an Individual or CompanyBranch.",
                "PATCH `/api/clients/{id}/` supports partial update of `status` and `name`.",
                "Endpoint appears in OpenAPI schema with clear type descriptions.",
                "Creating a Client with an already-linked entity returns 409.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: clients", "critical-path"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Client user assignment and status management",
        body=_body(
            description="""\
                Expose two sub-actions on the Client ViewSet:
                (1) `POST /api/clients/{id}/users/` — create and assign a new
                `CustomUser` to this client via `UserCreationService`.
                (2) `PATCH /api/clients/{id}/status/` — transition the client
                status (`ACTIVE`, `INACTIVE`, `SUSPENDED`, `CLOSED`).
                Enforce status-transition rules (e.g. a CLOSED client cannot
                be directly re-activated without admin approval).
            """,
            acceptance=[
                "POST `/api/clients/{id}/users/` creates a linked user and returns 201.",
                "Assigning a user to a client in CLOSED status returns 400.",
                "PATCH `/api/clients/{id}/status/` applies valid status transitions.",
                "Invalid status transitions return 400 with a descriptive error.",
                "Only staff/admin may change client status.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: clients"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    # =========================================================================
    # WEEK 2 — EPIC: Asset Management
    # =========================================================================
    Issue(
        title="[W2] Asset registration CRUD API",
        body=_body(
            description="""\
                `AssetRegistrationViewSet` and serializers already exist in
                `apps/asset_management/`.  Complete and harden the ViewSet:
                ensure the `owner` FK is properly validated (must be an active
                user), apply `StandardResultsSetPagination`, add
                `permission_classes = [IsAuthenticated]`, and confirm all
                field validations (year_of_make range, positive amounts).
                Register the URL under `/api/asset-management/`.
            """,
            acceptance=[
                "GET `/api/asset-management/registrations/` returns paginated, searchable list.",
                "POST creates a registration with owner validation.",
                "PATCH supports partial update.",
                "DELETE soft-deletes or hard-deletes (document the choice).",
                "All filterset_fields and search_fields are functional.",
                "`year_of_make` must be between 1900 and current year + 1.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: asset-mgmt", "critical-path"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Asset management dashboard endpoint",
        body=_body(
            description="""\
                The `AssetRegistrationViewSet` already has a `dashboard` custom
                action stub.  Implement it to return aggregate statistics:
                total assets, breakdown by `asset_type`, total value by currency,
                and count by `condition`.  The endpoint should be
                `GET /api/asset-management/registrations/dashboard/`.
            """,
            acceptance=[
                "GET `/api/asset-management/registrations/dashboard/` returns 200 with aggregated stats.",
                "Response includes: `total_registrations`, `by_asset_type`, `by_condition`, `total_value_by_currency`.",
                "Dashboard data reflects only assets accessible to the authenticated user.",
                "Endpoint is documented in the OpenAPI schema.",
            ],
        ),
        labels=["week 2", "priority: medium", "epic: asset-mgmt"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    # =========================================================================
    # WEEK 2 — EPIC: Collateral Registry
    # =========================================================================
    Issue(
        title="[W2] Collateral registration CRUD API",
        body=_body(
            description="""\
                `CollateralRegistrationViewSet` and serializers already exist.
                Harden and complete the ViewSet: validate that `financier` and
                `debtor` are active users, confirm `total_debt > 0`,
                `agreement_start_date <= agreement_end_date`, and that the
                derived `balance` field is auto-computed on save.
                Register the URL under `/api/collateral/`.
            """,
            acceptance=[
                "GET `/api/collateral/registrations/` returns paginated, searchable list.",
                "POST validates financier/debtor, date range, and positive amounts.",
                "PATCH supports partial update on financial and date fields.",
                "`balance` is automatically computed as `total_debt - total_paid_to_date`.",
                "Filtering by `is_discharged`, `asset_type`, and `financier` works correctly.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: collateral", "critical-path"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Collateral discharge workflow and status lifecycle",
        body=_body(
            description="""\
                The `discharge` custom action already exists on `CollateralRegistrationViewSet`.
                Complete the `CollateralDischargeSerializer` to stamp
                `discharge_confirmed_at` automatically.  Implement a computed
                `status` property on the model that returns `Active`,
                `Pending Discharge Confirmation`, or `Discharged` based on dates
                and the `is_discharged` flag.  Expose this in the list serializer.
            """,
            acceptance=[
                "PATCH `/api/collateral/registrations/{id}/discharge/` sets `is_discharged=True` and stamps `discharge_confirmed_at`.",
                "Calling discharge on an already-discharged record returns 400.",
                "The `status` field in list/detail responses reflects the correct lifecycle state.",
                "Only the financier or staff may discharge a collateral record.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: collateral"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Collateral registry dashboard endpoint",
        body=_body(
            description="""\
                Implement `GET /api/collateral/registrations/dashboard/` using
                `CollateralDashboardSerializer`.  Return: total registrations,
                active count, discharged count, pending-discharge count,
                total debt by currency, breakdown by `asset_type`.
            """,
            acceptance=[
                "Dashboard endpoint returns 200 with the required aggregated fields.",
                "Counts accurately reflect current database state.",
                "Response is documented in the OpenAPI schema.",
            ],
        ),
        labels=["week 2", "priority: medium", "epic: collateral"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    # =========================================================================
    # WEEK 2 — EPIC: Hire Purchase Registry
    # =========================================================================
    Issue(
        title="[W2] Hire purchase registration CRUD API",
        body=_body(
            description="""\
                `HirePurchaseRegistrationViewSet` and serializers exist in
                `apps/hire_purchase/`.  Harden the ViewSet: validate
                `purchase_amount > 0`, `agreement_start_date <= agreement_end_date`,
                and ensure `instalment_day` is 1-28.  Auto-compute `balance` on save.
                Register the URL under `/api/hire-purchase/`.
            """,
            acceptance=[
                "GET `/api/hire-purchase/registrations/` returns paginated, searchable list.",
                "POST validates all required fields including date range and positive amounts.",
                "PATCH supports partial update.",
                "`balance` is automatically computed as `purchase_amount - total_paid_to_date`.",
                "Filtering by `asset_type`, `financier`, `purchaser` works correctly.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: hire-purchase", "critical-path"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Hire purchase closure workflow and lifecycle management",
        body=_body(
            description="""\
                Implement a `confirm_closure` action at
                `PATCH /api/hire-purchase/registrations/{id}/confirm-closure/`.
                This sets `closure_confirmed=True` and stamps a
                `closure_confirmed_at` datetime.  Add a computed `status`
                property (`Active`, `Pending Closure Confirmation`, `Closed`)
                based on `agreement_end_date` and `closure_confirmed`.
                Expose the `status` in list and detail serializers.
            """,
            acceptance=[
                "PATCH `.../confirm-closure/` sets `closure_confirmed=True` and stamps the date.",
                "Calling confirm-closure on an already-closed HP record returns 400.",
                "The `status` field accurately reflects `Active`, `Pending Closure Confirmation`, or `Closed`.",
                "Only the financier or staff may confirm closure.",
            ],
        ),
        labels=["week 2", "priority: high", "epic: hire-purchase"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    Issue(
        title="[W2] Hire purchase dashboard endpoint",
        body=_body(
            description="""\
                Implement `GET /api/hire-purchase/registrations/dashboard/`.
                Return: total registrations, active count, pending-closure count,
                closed count, total purchase value by currency, breakdown by
                `asset_type`.
            """,
            acceptance=[
                "Dashboard endpoint returns 200 with the required aggregated fields.",
                "Counts accurately reflect current database state.",
                "Response is documented in the OpenAPI schema.",
            ],
        ),
        labels=["week 2", "priority: medium", "epic: hire-purchase"],
        milestone="Week 2 - Core Features",
        size="M",
    ),
    # =========================================================================
    # WEEK 3 — EPIC: Testing
    # =========================================================================
    Issue(
        title="[W3] Unit and integration tests for authentication and user management",
        body=_body(
            description="""\
                Write Django test cases covering the auth and user management
                flows: login success/failure, logout token blacklisting, cookie
                handling, registration, RBAC permission checks, password change.
                Use Django's `TestCase` and DRF's `APIClient`.  Target ≥ 80%
                coverage on `apps/users/`.
            """,
            acceptance=[
                "All tests in `apps/users/tests/` pass with `python manage.py test apps.users`.",
                "Login with valid credentials: 200 + cookies set.",
                "Login with invalid credentials: 401.",
                "Logout: cookies cleared + token blacklisted.",
                "Password change with wrong current password: 400.",
                "RBAC: endpoint returns 403 for a user missing the required role.",
                "Coverage ≥ 80% for `apps/users/`.",
            ],
        ),
        labels=["week 3", "priority: high", "epic: testing"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[W3] Unit and integration tests for asset management, collateral, and hire purchase",
        body=_body(
            description="""\
                Write test cases for the three registry apps.  Cover: create a
                valid registration, retrieve list with filters, lifecycle actions
                (discharge, confirm-closure), and dashboard endpoint accuracy.
                Use factory-based fixture helpers or simple model factories to
                reduce boilerplate.
            """,
            acceptance=[
                "All tests pass with `python manage.py test apps.asset_management apps.collateral apps.hire_purchase`.",
                "At least one test per CRUD action for each ViewSet.",
                "Lifecycle action tests verify state transitions and guard against double-transition.",
                "Dashboard tests verify aggregate counts match seeded data.",
                "Coverage ≥ 70% for each registry app.",
            ],
        ),
        labels=["week 3", "priority: high", "epic: testing"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[W3] Unit tests for individuals, companies, and clients apps",
        body=_body(
            description="""\
                Write test cases for the individuals, companies, and clients apps:
                CRUD operations, document upload, contact management, client user
                assignment, and status transitions.
            """,
            acceptance=[
                "All tests pass with `python manage.py test apps.individuals apps.companies apps.clients`.",
                "Individual CRUD: create, retrieve, update, soft-delete.",
                "Document upload: success and file-size rejection.",
                "Company branch uniqueness constraint enforced.",
                "Client status transition: valid and invalid cases tested.",
                "Coverage ≥ 70% for each app.",
            ],
        ),
        labels=["week 3", "priority: high", "epic: testing"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    # =========================================================================
    # WEEK 3 — EPIC: Deployment & DevOps
    # =========================================================================
    Issue(
        title="[W3] Dockerfile and docker-compose for local development and production",
        body=_body(
            description="""\
                Create a `Dockerfile` (multi-stage: builder + runtime) and a
                `docker-compose.yml` that brings up Django, PostgreSQL, Redis,
                and Celery worker with a single `docker compose up`.  Include
                a `docker-compose.override.yml` for dev-only settings
                (DEBUG=True, hot-reload).
            """,
            acceptance=[
                "`docker compose up` starts all services without errors.",
                "Django dev server is accessible at http://localhost:8000.",
                "Database migrations run automatically on container start (`entrypoint.sh`).",
                "Celery worker connects to Redis and starts successfully.",
                "Production `Dockerfile` does not include dev dependencies.",
            ],
        ),
        labels=["week 3", "priority: high", "epic: deployment", "critical-path"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[W3] Production environment configuration and security hardening",
        body=_body(
            description="""\
                Prepare the project for production: set `DEBUG=False`, configure
                `ALLOWED_HOSTS`, add `SECURE_HSTS_SECONDS`, `SECURE_SSL_REDIRECT`,
                `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`.  Configure
                `STATIC_ROOT` and run `collectstatic`.  Document all required
                production environment variables in `.env.example`.
            """,
            acceptance=[
                "Django's deployment checklist (`manage.py check --deploy`) passes with no critical warnings.",
                "HTTPS-only cookie flags are set in production settings.",
                "`collectstatic` runs without errors.",
                "All production environment variables are documented in `.env.example`.",
                "DEBUG is `False` when `DEBUG` env var is not `'True'`.",
            ],
        ),
        labels=["week 3", "priority: high", "epic: deployment"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[W3] Database migration and data seeding automation in entrypoint",
        body=_body(
            description="""\
                Create an `entrypoint.sh` script (used by Docker and/or CI) that:
                (1) waits for PostgreSQL to be ready, (2) runs `migrate`,
                (3) optionally runs `seed_roles`, `seed_locations`,
                `seed_currencies`.  Add a `--seed` flag to control whether
                seeding runs (default: only in non-production environments).
            """,
            acceptance=[
                "`entrypoint.sh` waits for Postgres before running migrate.",
                "Migrations apply cleanly from a blank database.",
                "Seed commands run without error when `SEED_DATA=true`.",
                "Script is idempotent and safe to re-run.",
                "Script is used in `docker-compose.yml` as the service entrypoint.",
            ],
        ),
        labels=["week 3", "priority: high", "epic: deployment"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[W3] GitHub Actions CI/CD pipeline for automated testing",
        body=_body(
            description="""\
                The repository already has GitHub Actions workflows.  Add or
                update a workflow that: (1) installs dependencies via `uv`,
                (2) runs `python manage.py check`, (3) runs the full test suite
                with `python manage.py test`, (4) reports coverage.
                Run on push to `main` and on every pull request.
            """,
            acceptance=[
                "CI workflow triggers on push/PR to `main`.",
                "Workflow installs dependencies and runs all tests.",
                "A failed test causes the workflow to fail with a non-zero exit code.",
                "Coverage report is uploaded as a workflow artifact.",
                "Workflow badge is added to README.",
            ],
        ),
        labels=["week 3", "priority: medium", "epic: deployment"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    # =========================================================================
    # WEEK 3 — EPIC: API Polish & Finalization
    # =========================================================================
    Issue(
        title="[W3] Standardise API error responses and input validation across all endpoints",
        body=_body(
            description="""\
                Implement a DRF custom exception handler in
                `apps/common/utils/` that returns a consistent error envelope:
                `{"status": "error", "message": "...", "errors": {...}}`.
                Register it in `REST_FRAMEWORK` settings as
                `EXCEPTION_HANDLER`.  Review all serializers for missing
                `required`/`blank`/`null` constraints and fix gaps.
            """,
            acceptance=[
                "All validation errors return `{status, message, errors}` envelope.",
                "404 and 405 responses also use the consistent envelope.",
                "The custom exception handler is registered in `REST_FRAMEWORK` settings.",
                "No endpoint returns a raw Django HTML error page for API requests.",
                "At least one test asserts the error envelope format.",
            ],
        ),
        labels=["week 3", "priority: high", "epic: api-polish", "critical-path"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[W3] Wire up all URL routes and activate all apps in settings",
        body=_body(
            description="""\
                Ensure all app URL namespaces are correctly registered in
                `core/urls.py` and all apps are in `INSTALLED_APPS`.  Currently
                `apps.users`, `apps.individuals`, `apps.companies`, and
                `apps.clients` are commented out.  Activate them, resolve any
                migration or import conflicts, and verify end-to-end that the
                full API surface is reachable.
            """,
            acceptance=[
                "All apps appear in `INSTALLED_APPS`.",
                "All app URL namespaces appear in `core/urls.py`.",
                "`python manage.py check` passes with no errors.",
                "`python manage.py showmigrations` shows all migrations applied.",
                "A smoke-test HTTP request to each app's list endpoint returns 200 or 401 (not 404).",
            ],
        ),
        labels=["week 3", "priority: high", "epic: api-polish", "critical-path"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[W3] Final OpenAPI schema review and documentation cleanup",
        body=_body(
            description="""\
                Review the auto-generated OpenAPI schema for accuracy and
                completeness.  Add `@extend_schema` decorators where needed
                to fix missing or incorrect request/response schemas.  Write
                a brief API guide in the README covering authentication flow,
                base URL, and how to obtain tokens.
            """,
            acceptance=[
                "Every endpoint has a correct HTTP method, path, and response schema.",
                "All custom actions document their request body and possible responses.",
                "README includes a section: 'API Quick Start' covering auth and token usage.",
                "No endpoints appear as `{}` (empty schema) in the Swagger UI.",
            ],
        ),
        labels=["week 3", "priority: medium", "epic: api-polish"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    # =========================================================================
    # NICE-TO-HAVE (post-MVP)
    # =========================================================================
    Issue(
        title="[NICE] SMS / email notification service implementation",
        body=_body(
            description="""\
                The Celery task stubs in `common/services/tasks.py`,
                `individuals/services/tasks.py`, `companies/services/tasks.py`
                are empty.  Implement actual email/SMS dispatch using Django's
                email backend and an SMS provider (e.g., Africa's Talking).
                This is a non-blocking nice-to-have for MVP.
            """,
            acceptance=[
                "Verification and status-change events trigger email notifications.",
                "SMS notifications sent for HP/Collateral lifecycle events.",
                "Failed notification tasks are retried via Celery retry mechanism.",
            ],
        ),
        labels=["nice-to-have", "priority: low", "epic: common"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[NICE] Rate limiting on public API endpoints",
        body=_body(
            description="""\
                Apply DRF throttling (`AnonRateThrottle`, `UserRateThrottle`)
                to prevent abuse of the login endpoint and public APIs.
                Configure limits in settings and return `429 Too Many Requests`
                with a `Retry-After` header.
            """,
            acceptance=[
                "Login endpoint is throttled to 10 requests/minute per IP.",
                "Authenticated endpoints are throttled at a sensible rate.",
                "429 response includes `Retry-After` header.",
            ],
        ),
        labels=["nice-to-have", "priority: low", "epic: api-polish"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[NICE] Audit logging for sensitive operations",
        body=_body(
            description="""\
                Use the existing `AuditLog` model in `apps/users/models/audit.py`
                (if present) or create one.  Record who performed what action
                (create/update/delete/lifecycle-change) on registry records,
                user accounts, and client status changes.  Expose a
                staff-only `GET /api/audit-log/` endpoint.
            """,
            acceptance=[
                "Lifecycle actions (discharge, confirm-closure) create audit log entries.",
                "User creation and role assignment are logged.",
                "GET `/api/audit-log/` (staff only) returns paginated log entries.",
                "Audit log is append-only (no delete or update allowed).",
            ],
        ),
        labels=["nice-to-have", "priority: low", "epic: users"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
    Issue(
        title="[NICE] CSV / Excel export for registry records",
        body=_body(
            description="""\
                Add an `export` action to the Asset Management, Collateral, and
                Hire Purchase ViewSets that streams a CSV/Excel file of the
                current filtered queryset.  Use Python's built-in `csv` module
                for CSV and `openpyxl` for Excel (add as a dependency if needed).
            """,
            acceptance=[
                "GET `.../registrations/export/?format=csv` returns a downloadable CSV.",
                "GET `.../registrations/export/?format=xlsx` returns a downloadable Excel file.",
                "Export respects the active search/filter parameters.",
                "File is streamed (not loaded entirely into memory).",
            ],
        ),
        labels=["nice-to-have", "priority: low", "epic: asset-mgmt"],
        milestone="Week 3 - Polish, Testing & Deployment",
        size="M",
    ),
]

# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------


def parse_iso8601_datetime(value: str) -> datetime:
    """Parse ISO-8601 date strings, including trailing Z UTC marker."""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def get_repo_and_github(repo_str: str) -> Any:
    """Get the GitHub repo object using PyGithub."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        sys.exit("Error: GITHUB_TOKEN environment variable not set.")

    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
        owner, repo_name = repo_str.split("/", maxsplit=1)
        user = g.get_user(owner)
        repo = user.get_repo(repo_name)
        print(f"✓ Connected to GitHub repository: {owner}/{repo_name}")
        return repo
    except Exception as e:
        sys.exit(f"Error connecting to GitHub: {e}")


def get_repo(specified: Optional[str]) -> str:
    """Get repo in OWNER/REPO format."""
    if specified:
        return specified

    repo_owner = os.getenv("GITHUB_REPO_OWNER")
    repo_name = os.getenv("GITHUB_REPO_NAME")
    if repo_owner and repo_name:
        return f"{repo_owner}/{repo_name}"

    sys.exit(
        "Error: Set GITHUB_REPO_OWNER and GITHUB_REPO_NAME in .env "
        "or pass --repo OWNER/REPO."
    )


def get_project_number() -> int:
    """Get project number from env, defaulting to 8."""
    raw = os.getenv("GITHUB_PROJECT_NUMBER", "8").strip()
    try:
        number = int(raw)
    except ValueError as e:
        raise ValueError(
            f"Invalid GITHUB_PROJECT_NUMBER '{raw}'. Expected an integer."
        ) from e

    if number <= 0:
        raise ValueError("GITHUB_PROJECT_NUMBER must be greater than zero.")
    return number


def normalize_name(value: str) -> str:
    """Normalize field and option names for tolerant matching."""
    normalized = value.strip().lower()
    for ch in (":", "-", "_"):
        normalized = normalized.replace(ch, " ")
    return " ".join(normalized.split())


def get_estimated_duration(size: str) -> str:
    """Map size codes to human-readable duration estimates."""
    normalized_size = size.strip().upper()
    return SIZE_TO_ESTIMATED_DURATION.get(normalized_size, normalized_size)


def get_estimate_number(size: str) -> float:
    """Map size codes to numeric estimates for number project fields."""
    normalized_size = size.strip().upper()
    return SIZE_TO_ESTIMATE_NUMBER.get(normalized_size, 1.0)


def with_estimated_duration(body: str, size: str) -> str:
    """Append estimated duration to issue body if not already present."""
    marker = "## Estimated Duration"
    if marker in body:
        return body

    duration = get_estimated_duration(size)
    return f"{body.rstrip()}\n\n{marker}\n{duration}\n"


def run_graphql_query(
    query: str, variables: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
    """Run a GitHub GraphQL query with token auth."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable not set.")

    payload = json.dumps({"query": query, "variables": variables or {}}).encode(
        "utf-8"
    )
    req = request.Request(
        "https://api.github.com/graphql",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    try:
        with request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GraphQL HTTP {exc.code}: {details}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"GraphQL connection error: {exc.reason}") from exc

    parsed = json.loads(raw)
    if parsed.get("errors"):
        messages = "; ".join(
            err.get("message", "Unknown GraphQL error") for err in parsed["errors"]
        )
        raise RuntimeError(messages)

    return parsed.get("data", {})


def get_project_context(
    project_owner: str,
    project_number: int,
    default_status: str,
) -> Optional[dict[str, Any]]:
    """Resolve a personal GitHub Project V2 and cache key tracked fields."""
    print(
        f"\n=== Resolving personal Project V2 #{project_number} for user '{project_owner}' ==="
    )
    query = """
    query($login: String!, $projectNumber: Int!) {
      user(login: $login) {
        projectV2(number: $projectNumber) {
          id
          title
          number
          fields(first: 50) {
            nodes {
                            __typename
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
              }
                            ... on ProjectV2Field {
                                id
                                name
                                dataType
                            }
            }
          }
        }
      }
    }
    """

    try:
        data = run_graphql_query(
            query,
            {"login": project_owner, "projectNumber": project_number},
        )
    except RuntimeError as exc:
        print(f"  ⚠  Could not fetch project metadata: {exc}", file=sys.stderr)
        return None

    user_data = data.get("user") or {}
    project = user_data.get("projectV2")
    if not project:
        print(
            "  ⚠  Project not found. Issue creation will continue without project linking.",
            file=sys.stderr,
        )
        return None

    fields: dict[str, dict[str, Any]] = {}
    for node in project.get("fields", {}).get("nodes", []):
        if not isinstance(node, dict):
            continue

        field_type_name = node.get("__typename")
        field_name = node.get("name")
        field_id = node.get("id")
        if not field_name or not field_id:
            continue

        normalized_field_name = normalize_name(field_name)
        field_aliases = {
            "priority": "priority",
            "size": "size",
            "status": "status",
            "duration": "duration",
            "estimate": "duration",
            "estimated": "duration",
            "estimated duration": "duration",
            "estimate duration": "duration",
        }
        canonical_field_name = field_aliases.get(normalized_field_name)
        if not canonical_field_name:
            continue

        if canonical_field_name in fields:
            continue

        if field_type_name == "ProjectV2SingleSelectField":
            options = node.get("options")
            if not options:
                continue

            option_lookup: dict[str, str] = {}
            option_names: dict[str, str] = {}
            for option in options:
                if not isinstance(option, dict):
                    continue
                option_id = option.get("id")
                option_name = option.get("name")
                if not option_id or not option_name:
                    continue
                option_key = normalize_name(option_name)
                option_lookup[option_key] = option_id
                option_names[option_key] = option_name

            fields[canonical_field_name] = {
                "id": field_id,
                "type": "single_select",
                "options": option_lookup,
                "option_names": option_names,
            }
            continue

        if field_type_name == "ProjectV2Field":
            data_type = str(node.get("dataType", "")).upper()
            if data_type != "NUMBER":
                continue

            fields[canonical_field_name] = {
                "id": field_id,
                "type": "number",
            }

    print(f"  ✓ Found project: {project.get('title', 'Unknown')} (#{project_number})")
    required_fields = {"priority", "size", "status"}
    optional_fields = {"duration"}

    for tracked in ("priority", "size", "status", "duration"):
        field = fields.get(tracked)
        if field:
            if field.get("type") == "single_select":
                print(
                    f"    ✓ Field '{tracked}' found with {len(field['options'])} options"
                )
            elif field.get("type") == "number":
                print(f"    ✓ Field '{tracked}' found as number field")
        elif tracked in required_fields:
            print(f"    ⚠  Field '{tracked}' not found; it will be skipped")
        elif tracked in optional_fields:
            print(f"    ℹ  Optional field '{tracked}' not found; duration will stay in issue body only")

    return {
        "id": project.get("id"),
        "title": project.get("title", "Unnamed project"),
        "owner": project_owner,
        "number": project_number,
        "default_status": default_status,
        "fields": fields,
    }


def get_project_item_lookup(project_id: str) -> dict[int, str]:
    """Return issue_number -> project_item_id for issues already on the project."""
    query = """
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          items(first: 100) {
            nodes {
              id
              content {
                ... on Issue {
                  number
                }
              }
            }
          }
        }
      }
    }
    """

    try:
        data = run_graphql_query(query, {"projectId": project_id})
    except RuntimeError as exc:
        print(f"  ⚠  Could not fetch existing project items: {exc}", file=sys.stderr)
        return {}

    lookup: dict[int, str] = {}
    nodes = ((data.get("node") or {}).get("items") or {}).get("nodes") or []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        item_id = node.get("id")
        issue_number = (node.get("content") or {}).get("number")
        if item_id and isinstance(issue_number, int):
            lookup[issue_number] = item_id

    return lookup


def resolve_single_select_option(
    field: dict[str, Any],
    candidates: list[str],
) -> tuple[Optional[str], Optional[str]]:
    """Resolve a project single-select option id by trying candidate names."""
    option_lookup = field.get("options", {})
    option_names = field.get("option_names", {})

    for candidate in candidates:
        candidate_key = normalize_name(candidate)
        if candidate_key in option_lookup:
            return option_lookup[candidate_key], option_names.get(candidate_key, candidate)

    return None, None


def get_priority_candidates(issue: Issue) -> list[str]:
    """Build candidate priority option names from issue labels."""
    priority_level = ""
    for label in issue.labels:
        if label.lower().startswith("priority:"):
            priority_level = label.split(":", maxsplit=1)[1].strip().lower()
            break

    if not priority_level:
        return []

    aliases = {
        "high": ["P0", "P1", "high", "priority high", "p0 critical", "p1 high"],
        "medium": ["P1", "P2", "medium", "priority medium", "p2 medium"],
        "low": ["P2", "low", "priority low", "p3 low"],
    }
    return aliases.get(priority_level, [priority_level, f"priority {priority_level}"])


def get_size_candidates(size: str) -> list[str]:
    """Build candidate size option names from issue size."""
    normalized_size = size.strip().upper()
    aliases = {
        "XS": ["XS", "Extra Small", "X Small", "Small"],
        "S": ["S", "Small", "Effort Small"],
        "M": ["M", "Medium", "Effort Medium"],
        "L": ["L", "Large", "Effort Large"],
        "XL": ["XL", "Extra Large", "X Large", "Large"],
    }
    return aliases.get(normalized_size, [normalized_size])


def get_status_candidates(default_status: str) -> list[str]:
    """Build candidate status option names from configured default."""
    configured = default_status.strip() or "Todo"
    candidates = [configured, configured.replace("-", " "), configured.replace(" ", "")]
    for fallback in ("To Do", "Todo", "Backlog"):
        if fallback not in candidates:
            candidates.append(fallback)
    return candidates


def get_duration_candidates(size: str) -> list[str]:
    """Build candidate duration option names from issue size."""
    normalized_size = size.strip().upper()
    aliases = {
        "XS": ["<= 0.5 day", "0.5 day", "half day", "XS"],
        "S": ["1 day", "S", "Small"],
        "M": ["1-2 days", "2 days", "M", "Medium"],
        "L": ["3-5 days", "3 days", "5 days", "L", "Large"],
        "XL": ["5+ days", "5 days", "XL", "Extra Large"],
    }
    base_duration = get_estimated_duration(size)
    candidates = [base_duration]
    for alias in aliases.get(normalized_size, [normalized_size]):
        if alias not in candidates:
            candidates.append(alias)
    return candidates


def add_issue_to_project(project_id: str, issue_node_id: str) -> Optional[str]:
    """Create a project item from an issue node id and return item id."""
    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item {
          id
        }
      }
    }
    """

    try:
        data = run_graphql_query(
            mutation,
            {"projectId": project_id, "contentId": issue_node_id},
        )
    except RuntimeError as exc:
        print(f"      ⚠  Could not add issue to project: {exc}", file=sys.stderr)
        return None

    item = (data.get("addProjectV2ItemById") or {}).get("item") or {}
    return item.get("id")


def update_project_single_select_field(
    project_id: str,
    item_id: str,
    field_id: str,
    option_id: str,
) -> bool:
    """Set a single-select project field on a project item."""
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(
        input: {
          projectId: $projectId
          itemId: $itemId
          fieldId: $fieldId
          value: {singleSelectOptionId: $optionId}
        }
      ) {
        projectV2Item {
          id
        }
      }
    }
    """

    try:
        run_graphql_query(
            mutation,
            {
                "projectId": project_id,
                "itemId": item_id,
                "fieldId": field_id,
                "optionId": option_id,
            },
        )
        return True
    except RuntimeError as exc:
        print(f"      ⚠  Could not update project field: {exc}", file=sys.stderr)
        return False


def update_project_number_field(
    project_id: str,
    item_id: str,
    field_id: str,
    number_value: float,
) -> bool:
    """Set a number project field on a project item."""
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $number: Float!) {
      updateProjectV2ItemFieldValue(
        input: {
          projectId: $projectId
          itemId: $itemId
          fieldId: $fieldId
          value: {number: $number}
        }
      ) {
        projectV2Item {
          id
        }
      }
    }
    """

    try:
        run_graphql_query(
            mutation,
            {
                "projectId": project_id,
                "itemId": item_id,
                "fieldId": field_id,
                "number": float(number_value),
            },
        )
        return True
    except RuntimeError as exc:
        print(f"      ⚠  Could not update project field: {exc}", file=sys.stderr)
        return False


def apply_project_fields_to_item(
    project_ctx: dict[str, Any],
    item_id: str,
    issue: Issue,
    issue_ref: str,
    dry_run: bool,
) -> None:
    """Apply Priority/Size/Status project field values for an issue."""
    updates = [
        ("priority", get_priority_candidates(issue)),
        ("size", get_size_candidates(issue.size)),
        ("status", get_status_candidates(project_ctx.get("default_status", "Todo"))),
        ("duration", get_duration_candidates(issue.size)),
    ]

    for field_name, candidates in updates:
        field = project_ctx.get("fields", {}).get(field_name)
        if not field:
            continue

        field_type = field.get("type", "single_select")

        if field_type == "number":
            if field_name != "duration":
                print(
                    f"      ⚠  Unsupported number field type for '{field_name}' on {issue_ref}",
                    file=sys.stderr,
                )
                continue

            estimate_value = get_estimate_number(issue.size)
            if dry_run:
                print(
                    f"      [DRY RUN] Would set {field_name.title()}={estimate_value:g} on project item for {issue_ref}"
                )
                continue

            if update_project_number_field(
                project_ctx["id"],
                item_id,
                field["id"],
                estimate_value,
            ):
                print(
                    f"      ✓ Set {field_name.title()}={estimate_value:g} for {issue_ref}"
                )
            continue

        option_id, option_name = resolve_single_select_option(field, candidates)
        if not option_id:
            print(
                f"      ⚠  No matching '{field_name}' option found in project for {issue_ref}",
                file=sys.stderr,
            )
            continue

        if dry_run:
            print(
                f"      [DRY RUN] Would set {field_name.title()}='{option_name}' on project item for {issue_ref}"
            )
            continue

        if update_project_single_select_field(
            project_ctx["id"],
            item_id,
            field["id"],
            option_id,
        ):
            print(f"      ✓ Set {field_name.title()}='{option_name}' for {issue_ref}")


def ensure_issue_linked_to_project(
    issue_obj: Any,
    issue_definition: Issue,
    project_ctx: dict[str, Any],
    project_item_lookup: dict[int, str],
    dry_run: bool,
) -> None:
    """Ensure issue is present on the project and fields are set."""
    issue_number = issue_obj.number
    issue_ref = f"issue #{issue_number}"

    item_id = project_item_lookup.get(issue_number)
    if item_id:
        print(f"      ✓ {issue_ref} already linked to project")
    elif dry_run:
        print(
            f"      [DRY RUN] Would add {issue_ref} to project '{project_ctx['title']}'"
        )
        item_id = "DRY_RUN_ITEM"
    else:
        issue_node_id = getattr(issue_obj, "node_id", "")
        if not issue_node_id:
            print(
                f"      ⚠  Could not resolve node id for {issue_ref}; skipping project link",
                file=sys.stderr,
            )
            return

        item_id = add_issue_to_project(project_ctx["id"], issue_node_id)
        if not item_id:
            print(f"      ⚠  Failed to link {issue_ref} to project", file=sys.stderr)
            return

        project_item_lookup[issue_number] = item_id
        print(f"      ✓ Linked {issue_ref} to project '{project_ctx['title']}'")

    apply_project_fields_to_item(
        project_ctx,
        item_id,
        issue_definition,
        issue_ref,
        dry_run,
    )


def create_labels(repo, dry_run: bool) -> None:
    """Create or update all labels in the repository."""
    print(f"\n=== Creating/updating {len(LABELS)} labels ===")
    for i, label in enumerate(LABELS, start=1):
        print(f"  ({i}/{len(LABELS)}) Label: {label.name}")
        if dry_run:
            print(
                f"    [DRY RUN] Would create label '{label.name}' with color {label.color}"
            )
            continue

        try:
            try:
                existing_label = repo.get_label(label.name)
                existing_label.edit(
                    name=label.name,
                    color=label.color,
                    description=label.description,
                )
                print(f"    ✓ Updated label '{label.name}'")
            except GithubException:
                repo.create_label(
                    name=label.name,
                    color=label.color,
                    description=label.description,
                )
                print(f"    ✓ Created label '{label.name}'")
        except Exception as e:
            print(f"    ⚠  Error creating label '{label.name}': {e}", file=sys.stderr)


def create_milestones(repo, dry_run: bool) -> dict[str, Any]:
    """Create or update milestones and return a dict of title -> milestone object."""
    print(f"\n=== Creating/updating {len(MILESTONES)} milestones ===")
    milestones_dict: dict[str, Any] = {}

    existing_milestones: dict[str, Any] = {}
    if not dry_run:
        try:
            existing_milestones = {
                milestone.title: milestone for milestone in repo.get_milestones(state="all")
            }
        except Exception as e:
            print(f"  ⚠  Could not fetch milestones: {e}", file=sys.stderr)

    for i, milestone in enumerate(MILESTONES, start=1):
        print(f"  ({i}/{len(MILESTONES)}) Milestone: {milestone.title}")

        if dry_run:
            print(f"    [DRY RUN] Would create milestone '{milestone.title}'")
            milestones_dict[milestone.title] = None
            continue

        try:
            if milestone.title in existing_milestones:
                print(f"    ✓ Milestone '{milestone.title}' already exists")
                milestones_dict[milestone.title] = existing_milestones[milestone.title]
            else:
                new_milestone = repo.create_milestone(
                    title=milestone.title,
                    description=milestone.description,
                    due_on=parse_iso8601_datetime(milestone.due_on),
                )
                print(f"    ✓ Created milestone '{milestone.title}'")
                milestones_dict[milestone.title] = new_milestone
                existing_milestones[milestone.title] = new_milestone
        except Exception as e:
            print(f"    ⚠  Error creating milestone '{milestone.title}': {e}", file=sys.stderr)
            milestones_dict[milestone.title] = None

    return milestones_dict


def create_issues(
    repo,
    milestones_dict: dict[str, Any],
    dry_run: bool,
    project_ctx: Optional[dict[str, Any]] = None,
) -> None:
    """Create all issues in the repository and optionally link them to Project V2."""
    print(f"\n=== Creating {len(ISSUES)} issues ===")

    existing_issues_by_title: dict[str, Any] = {}
    try:
        existing_issues_by_title = {
            existing_issue.title: existing_issue
            for existing_issue in repo.get_issues(state="open")
        }
        if existing_issues_by_title:
            print(f"  ℹ  Found {len(existing_issues_by_title)} existing open issues")
    except Exception as e:
        print(f"  ⚠  Could not fetch existing issues: {e}", file=sys.stderr)

    project_item_lookup: dict[int, str] = {}
    if project_ctx and project_ctx.get("id"):
        project_item_lookup = get_project_item_lookup(project_ctx["id"])
        print(
            f"  ℹ  Found {len(project_item_lookup)} issues already linked to project '{project_ctx['title']}'"
        )

    for i, issue in enumerate(ISSUES, start=1):
        print(f"  [{i:02d}/{len(ISSUES)}] {issue.title}")

        github_issue = existing_issues_by_title.get(issue.title)
        issue_existed = github_issue is not None
        issue_body_with_duration = with_estimated_duration(issue.body, issue.size)
        expected_milestone = milestones_dict.get(issue.milestone)

        if github_issue:
            print("    ✓ Issue already exists. Reusing it.")
        elif dry_run:
            print(
                f"    [DRY RUN] Would create issue with {len(issue.labels)} labels and milestone '{issue.milestone}'"
            )
        else:
            try:
                create_kwargs: dict[str, Any] = {
                    "title": issue.title,
                    "body": issue_body_with_duration,
                    "labels": issue.labels,
                }
                if expected_milestone:
                    create_kwargs["milestone"] = expected_milestone
                github_issue = repo.create_issue(**create_kwargs)
                existing_issues_by_title[issue.title] = github_issue
                print(f"    ✓ Created issue: {github_issue.html_url}")
            except Exception as e:
                print(f"    ⚠  Error creating issue '{issue.title}': {e}", file=sys.stderr)
                continue

        if issue_existed and github_issue:
            existing_body = github_issue.body or ""
            body_with_duration = with_estimated_duration(
                existing_body or issue.body,
                issue.size,
            )
            if body_with_duration != existing_body:
                if dry_run:
                    print(
                        f"      [DRY RUN] Would append Estimated Duration to issue #{github_issue.number}"
                    )
                else:
                    try:
                        github_issue.edit(body=body_with_duration)
                        print("      ✓ Added Estimated Duration section")
                    except Exception as e:
                        print(f"      ⚠  Could not update issue body: {e}", file=sys.stderr)

        if github_issue and expected_milestone:
            current_milestone = github_issue.milestone.title if github_issue.milestone else ""
            if current_milestone != issue.milestone:
                if dry_run:
                    print(
                        f"      [DRY RUN] Would assign milestone '{issue.milestone}' to issue #{github_issue.number}"
                    )
                else:
                    try:
                        github_issue.edit(milestone=expected_milestone)
                        print(f"      ✓ Assigned milestone '{issue.milestone}'")
                    except Exception as e:
                        print(f"      ⚠  Could not assign milestone: {e}", file=sys.stderr)

        if project_ctx and project_ctx.get("id") and github_issue:
            ensure_issue_linked_to_project(
                github_issue,
                issue,
                project_ctx,
                project_item_lookup,
                dry_run,
            )
        elif project_ctx and project_ctx.get("id") and dry_run and not github_issue:
            print(
                f"      [DRY RUN] Would add newly-created issue to project '{project_ctx['title']}'"
            )
            apply_project_fields_to_item(
                project_ctx,
                "DRY_RUN_ITEM",
                issue,
                f"new issue '{issue.title}'",
                dry_run=True,
            )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create AssetSafe MVP GitHub issues using PyGithub.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--repo",
        help="OWNER/REPO (default: GITHUB_REPO_OWNER/GITHUB_REPO_NAME from .env)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print actions without executing"
    )
    args = parser.parse_args()

    repo_str = get_repo(args.repo)
    repo_owner, _repo_name = repo_str.split("/", maxsplit=1)

    try:
        project_number = get_project_number()
    except ValueError as exc:
        sys.exit(f"Error: {exc}")

    project_owner = os.getenv("GITHUB_PROJECT_OWNER", repo_owner)
    project_default_status = os.getenv("GITHUB_PROJECT_DEFAULT_STATUS", "Todo")

    print(f"Repository : {repo_str}")
    print(f"Project    : {project_owner}#{project_number} (personal)")
    print(f"Dry-run    : {args.dry_run}")
    print(f"Issues     : {len(ISSUES)}")
    print(f"Milestones : {len(MILESTONES)}")
    print(f"Labels     : {len(LABELS)}")

    # Get repo object
    repo = get_repo_and_github(repo_str)

    # Resolve personal project metadata and project field mappings
    project_ctx = get_project_context(
        project_owner=project_owner,
        project_number=project_number,
        default_status=project_default_status,
    )

    # Create labels, milestones, and issues
    create_labels(repo, args.dry_run)
    milestones_dict = create_milestones(repo, args.dry_run)
    create_issues(
        repo,
        milestones_dict,
        args.dry_run,
        project_ctx=project_ctx,
    )

    print(f"\n✅  Done! Visit https://github.com/{repo_str}/issues to review.")


if __name__ == "__main__":
    main()
