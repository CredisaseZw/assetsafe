#!/usr/bin/env python3
"""
create_github_issues.py
=======================
Idempotent script that creates GitHub milestones, labels, and issues for the
AssetSafe MVP (3-week execution plan) using the ``gh`` CLI.

Usage
-----
    python scripts/create_github_issues.py [--repo OWNER/REPO] [--assignee USERNAME] [--dry-run]

Prerequisites
-------------
* GitHub CLI (gh) installed and authenticated: https://cli.github.com/
* Run from the root of the cloned repository, OR pass --repo explicitly.

Options
-------
  --repo       GitHub repository in OWNER/REPO format.
               Defaults to the remote of the current git checkout.
  --assignee   GitHub username to assign every issue to.
               Defaults to the currently authenticated gh user.
  --dry-run    Print commands without executing them.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Label:
    name: str
    color: str   # 6-char hex without '#'
    description: str = ""


@dataclass
class Milestone:
    title: str
    description: str
    due_on: str   # ISO-8601, e.g. "2026-04-27T23:59:59Z"


@dataclass
class Issue:
    title: str
    body: str
    labels: list[str]
    milestone: str        # milestone title
    priority: str         # High / Medium / Low
    effort: str           # Small / Medium / Large
    duration: str
    dependencies: str     # free-text
    assignee: str = ""    # filled in at runtime


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

LABELS: list[Label] = [
    # ---- Priority ----
    Label("priority: high",   "d93f0b", "Must be completed for MVP"),
    Label("priority: medium", "fbca04", "Important but not blocking"),
    Label("priority: low",    "0075ca", "Nice-to-have / post-MVP"),
    # ---- Week ----
    Label("week 1", "e4e669", "Week 1: Core foundation"),
    Label("week 2", "c5def5", "Week 2: Core features"),
    Label("week 3", "bfd4f2", "Week 3: Polish, testing & deployment"),
    # ---- Effort ----
    Label("effort: small",  "c2e0c6", "Estimated: ≤ 0.5 day"),
    Label("effort: medium", "fef2c0", "Estimated: 1–2 days"),
    Label("effort: large",  "f9d0c4", "Estimated: 3–5 days"),
    # ---- Epic ----
    Label("epic: setup",          "1d76db", "Project setup & infrastructure"),
    Label("epic: auth",           "0052cc", "Authentication & JWT"),
    Label("epic: users",          "5319e7", "User management & RBAC"),
    Label("epic: common",         "006b75", "Common app & shared models"),
    Label("epic: individuals",    "e11d48", "Individuals app"),
    Label("epic: companies",      "be4bdb", "Companies app"),
    Label("epic: clients",        "f97316", "Clients abstraction layer"),
    Label("epic: asset-mgmt",     "22c55e", "Asset management registry"),
    Label("epic: collateral",     "84cc16", "Collateral registry"),
    Label("epic: hire-purchase",  "eab308", "Hire purchase registry"),
    Label("epic: testing",        "14b8a6", "Testing"),
    Label("epic: deployment",     "64748b", "Deployment & DevOps"),
    Label("epic: api-polish",     "a855f7", "API polish & finalization"),
    Label("critical-path",        "b60205", "Must-do for MVP"),
    Label("nice-to-have",         "d4c5f9", "Only if time allows"),
]

# ---------------------------------------------------------------------------
# Milestones
# ---------------------------------------------------------------------------

MILESTONES: list[Milestone] = [
    Milestone(
        title="Week 1 – Core Foundation",
        description="Project setup, authentication, user management, and common models.",
        due_on="2026-04-13T23:59:59Z",
    ),
    Milestone(
        title="Week 2 – Core Features",
        description="Individuals, companies, clients, asset management, collateral, and hire-purchase APIs.",
        due_on="2026-04-20T23:59:59Z",
    ),
    Milestone(
        title="Week 3 – Polish, Testing & Deployment",
        description="Test coverage, Docker, CI/CD, and API polish.",
        due_on="2026-04-27T23:59:59Z",
    ),
]

# ---------------------------------------------------------------------------
# Issues
# ---------------------------------------------------------------------------

def _body(description: str, acceptance: list[str], priority: str,
          effort: str, duration: str, dependencies: str) -> str:
    ac_lines = "\n".join(f"- [ ] {line}" for line in acceptance)
    return textwrap.dedent(f"""\
        ## Description
        {description.strip()}

        ## Acceptance Criteria
        {ac_lines}

        ## Priority
        {priority}

        ## Estimated Effort
        {effort}

        ## Duration
        {duration}

        ## Dependencies
        {dependencies if dependencies else "None"}
    """)


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
                "All six domain apps (users, individuals, companies, clients, asset_management, collateral, hire_purchase, common) appear in INSTALLED_APPS.",
                "All app URL namespaces are registered in `core/urls.py`.",
                "`python manage.py check` passes with no errors.",
            ],
            priority="High",
            effort="Small",
            duration="0.5 day",
            dependencies="None",
        ),
        labels=["week 1", "priority: high", "epic: setup", "critical-path"],
        milestone="Week 1 – Core Foundation",
        priority="High",
        effort="Small",
        duration="0.5 day",
        dependencies="None",
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
            priority="High",
            effort="Small",
            duration="0.5 day",
            dependencies="#1 – Environment configuration",
        ),
        labels=["week 1", "priority: high", "epic: setup", "critical-path"],
        milestone="Week 1 – Core Foundation",
        priority="High",
        effort="Small",
        duration="0.5 day",
        dependencies="#1",
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
            priority="Medium",
            effort="Small",
            duration="0.5 day",
            dependencies="#1 – Environment configuration",
        ),
        labels=["week 1", "priority: medium", "epic: setup"],
        milestone="Week 1 – Core Foundation",
        priority="Medium",
        effort="Small",
        duration="0.5 day",
        dependencies="#1",
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
            priority="Medium",
            effort="Small",
            duration="0.5 day",
            dependencies="#1 – Environment configuration",
        ),
        labels=["week 1", "priority: medium", "epic: setup"],
        milestone="Week 1 – Core Foundation",
        priority="Medium",
        effort="Small",
        duration="0.5 day",
        dependencies="#1",
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
            priority="High",
            effort="Small",
            duration="1 day",
            dependencies="#1 – Environment configuration",
        ),
        labels=["week 1", "priority: high", "epic: auth", "critical-path"],
        milestone="Week 1 – Core Foundation",
        priority="High",
        effort="Small",
        duration="1 day",
        dependencies="#1",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#5 – JWT cookie authentication",
        ),
        labels=["week 1", "priority: high", "epic: auth", "critical-path"],
        milestone="Week 1 – Core Foundation",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#5",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#6 – Registration & login endpoints",
        ),
        labels=["week 1", "priority: high", "epic: users", "critical-path"],
        milestone="Week 1 – Core Foundation",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#6",
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
            priority="High",
            effort="Small",
            duration="0.5 day",
            dependencies="#5, #6 – Auth endpoints",
        ),
        labels=["week 1", "priority: high", "epic: auth"],
        milestone="Week 1 – Core Foundation",
        priority="High",
        effort="Small",
        duration="0.5 day",
        dependencies="#5, #6",
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
            priority="High",
            effort="Small",
            duration="0.5 day",
            dependencies="#2 – Database & migrations",
        ),
        labels=["week 1", "priority: high", "epic: common", "critical-path"],
        milestone="Week 1 – Core Foundation",
        priority="High",
        effort="Small",
        duration="0.5 day",
        dependencies="#2",
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
            priority="Medium",
            effort="Small",
            duration="0.5 day",
            dependencies="#2 – Database & migrations",
        ),
        labels=["week 1", "priority: medium", "epic: common"],
        milestone="Week 1 – Core Foundation",
        priority="Medium",
        effort="Small",
        duration="0.5 day",
        dependencies="#2",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#9 – Common models, #7 – RBAC",
        ),
        labels=["week 2", "priority: high", "epic: individuals", "critical-path"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#9, #7",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#11 – Individual CRUD API",
        ),
        labels=["week 2", "priority: high", "epic: individuals"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#11",
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
            priority="Medium",
            effort="Medium",
            duration="1 day",
            dependencies="#11 – Individual CRUD API",
        ),
        labels=["week 2", "priority: medium", "epic: individuals"],
        milestone="Week 2 – Core Features",
        priority="Medium",
        effort="Medium",
        duration="1 day",
        dependencies="#11",
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
            priority="Medium",
            effort="Small",
            duration="0.5 day",
            dependencies="#11 – Individual CRUD API, #3 – Celery setup",
        ),
        labels=["week 2", "priority: medium", "epic: individuals"],
        milestone="Week 2 – Core Features",
        priority="Medium",
        effort="Small",
        duration="0.5 day",
        dependencies="#11, #3",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#9 – Common models, #7 – RBAC",
        ),
        labels=["week 2", "priority: high", "epic: companies", "critical-path"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#9, #7",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#15 – Company CRUD API",
        ),
        labels=["week 2", "priority: high", "epic: companies"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#15",
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
            priority="Medium",
            effort="Medium",
            duration="1 day",
            dependencies="#15 – Company CRUD API, #13 – Individual document upload",
        ),
        labels=["week 2", "priority: medium", "epic: companies"],
        milestone="Week 2 – Core Features",
        priority="Medium",
        effort="Medium",
        duration="1 day",
        dependencies="#15, #13",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#11 – Individuals API, #15 – Companies API",
        ),
        labels=["week 2", "priority: high", "epic: clients", "critical-path"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#11, #15",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#18 – Client CRUD API, #7 – RBAC",
        ),
        labels=["week 2", "priority: high", "epic: clients"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#18, #7",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#2 – Migrations, #5 – Auth",
        ),
        labels=["week 2", "priority: high", "epic: asset-mgmt", "critical-path"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#2, #5",
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
            priority="Medium",
            effort="Small",
            duration="0.5 day",
            dependencies="#20 – Asset CRUD API",
        ),
        labels=["week 2", "priority: medium", "epic: asset-mgmt"],
        milestone="Week 2 – Core Features",
        priority="Medium",
        effort="Small",
        duration="0.5 day",
        dependencies="#20",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#2 – Migrations, #5 – Auth",
        ),
        labels=["week 2", "priority: high", "epic: collateral", "critical-path"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#2, #5",
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
            priority="High",
            effort="Small",
            duration="0.5 day",
            dependencies="#22 – Collateral CRUD API",
        ),
        labels=["week 2", "priority: high", "epic: collateral"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Small",
        duration="0.5 day",
        dependencies="#22",
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
            priority="Medium",
            effort="Small",
            duration="0.5 day",
            dependencies="#22 – Collateral CRUD API",
        ),
        labels=["week 2", "priority: medium", "epic: collateral"],
        milestone="Week 2 – Core Features",
        priority="Medium",
        effort="Small",
        duration="0.5 day",
        dependencies="#22",
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
                and ensure `instalment_day` is 1–28.  Auto-compute `balance` on save.
                Register the URL under `/api/hire-purchase/`.
            """,
            acceptance=[
                "GET `/api/hire-purchase/registrations/` returns paginated, searchable list.",
                "POST validates all required fields including date range and positive amounts.",
                "PATCH supports partial update.",
                "`balance` is automatically computed as `purchase_amount - total_paid_to_date`.",
                "Filtering by `asset_type`, `financier`, `purchaser` works correctly.",
            ],
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#2 – Migrations, #5 – Auth",
        ),
        labels=["week 2", "priority: high", "epic: hire-purchase", "critical-path"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#2, #5",
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
            priority="High",
            effort="Small",
            duration="0.5 day",
            dependencies="#25 – HP CRUD API",
        ),
        labels=["week 2", "priority: high", "epic: hire-purchase"],
        milestone="Week 2 – Core Features",
        priority="High",
        effort="Small",
        duration="0.5 day",
        dependencies="#25",
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
            priority="Medium",
            effort="Small",
            duration="0.5 day",
            dependencies="#25 – HP CRUD API",
        ),
        labels=["week 2", "priority: medium", "epic: hire-purchase"],
        milestone="Week 2 – Core Features",
        priority="Medium",
        effort="Small",
        duration="0.5 day",
        dependencies="#25",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#5, #6, #7, #8 – Auth & user endpoints",
        ),
        labels=["week 3", "priority: high", "epic: testing"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#5, #6, #7, #8",
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
            priority="High",
            effort="Large",
            duration="2 days",
            dependencies="#20–#27 – Registry APIs",
        ),
        labels=["week 3", "priority: high", "epic: testing"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="High",
        effort="Large",
        duration="2 days",
        dependencies="#20-#27",
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
            priority="High",
            effort="Large",
            duration="1.5 days",
            dependencies="#11–#19 – Individuals, companies, clients APIs",
        ),
        labels=["week 3", "priority: high", "epic: testing"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="High",
        effort="Large",
        duration="1.5 days",
        dependencies="#11-#19",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="#1, #2, #3 – Environment, DB, Celery",
        ),
        labels=["week 3", "priority: high", "epic: deployment", "critical-path"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="#1, #2, #3",
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
            priority="High",
            effort="Medium",
            duration="0.5 day",
            dependencies="#1 – Environment setup, #32 – Docker setup",
        ),
        labels=["week 3", "priority: high", "epic: deployment"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="High",
        effort="Medium",
        duration="0.5 day",
        dependencies="#1, #32",
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
            priority="High",
            effort="Small",
            duration="0.5 day",
            dependencies="#32 – Docker setup",
        ),
        labels=["week 3", "priority: high", "epic: deployment"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="High",
        effort="Small",
        duration="0.5 day",
        dependencies="#32",
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
            priority="Medium",
            effort="Small",
            duration="0.5 day",
            dependencies="#28–#30 – Tests written",
        ),
        labels=["week 3", "priority: medium", "epic: deployment"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="Medium",
        effort="Small",
        duration="0.5 day",
        dependencies="#28-#30",
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
            priority="High",
            effort="Medium",
            duration="1 day",
            dependencies="All Week 2 endpoints completed",
        ),
        labels=["week 3", "priority: high", "epic: api-polish", "critical-path"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="High",
        effort="Medium",
        duration="1 day",
        dependencies="All Week 2 issues",
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
            priority="High",
            effort="Small",
            duration="0.5 day",
            dependencies="#1 – Environment setup",
        ),
        labels=["week 3", "priority: high", "epic: api-polish", "critical-path"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="High",
        effort="Small",
        duration="0.5 day",
        dependencies="#1",
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
            priority="Medium",
            effort="Small",
            duration="0.5 day",
            dependencies="#4 – drf-spectacular setup, all Week 2 endpoints",
        ),
        labels=["week 3", "priority: medium", "epic: api-polish"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="Medium",
        effort="Small",
        duration="0.5 day",
        dependencies="#4, all Week 2 issues",
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
            priority="Low",
            effort="Large",
            duration="2 days",
            dependencies="#3 – Celery setup",
        ),
        labels=["nice-to-have", "priority: low", "epic: common"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="Low",
        effort="Large",
        duration="2 days",
        dependencies="#3",
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
            priority="Low",
            effort="Small",
            duration="0.5 day",
            dependencies="#6 – Auth endpoints",
        ),
        labels=["nice-to-have", "priority: low", "epic: api-polish"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="Low",
        effort="Small",
        duration="0.5 day",
        dependencies="#6",
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
            priority="Low",
            effort="Large",
            duration="2 days",
            dependencies="All core APIs complete",
        ),
        labels=["nice-to-have", "priority: low", "epic: users"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="Low",
        effort="Large",
        duration="2 days",
        dependencies="All core APIs",
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
            priority="Low",
            effort="Medium",
            duration="1 day",
            dependencies="#20, #22, #25 – Registry APIs",
        ),
        labels=["nice-to-have", "priority: low", "epic: asset-mgmt"],
        milestone="Week 3 – Polish, Testing & Deployment",
        priority="Low",
        effort="Medium",
        duration="1 day",
        dependencies="#20, #22, #25",
    ),
]


# ---------------------------------------------------------------------------
# GitHub CLI helpers
# ---------------------------------------------------------------------------

def _run(cmd: list[str], dry_run: bool, capture: bool = False) -> Optional[str]:
    """Execute a gh CLI command, optionally printing it instead."""
    if dry_run:
        print("DRY-RUN:", " ".join(cmd))
        return None
    result = subprocess.run(cmd, capture_output=capture, text=True)
    if result.returncode != 0:
        # Print but don't abort — some errors are non-fatal (e.g. label already exists)
        print(f"  ⚠  Command failed (exit {result.returncode}): {result.stderr.strip()}", file=sys.stderr)
        return None
    return result.stdout.strip() if capture else None


def get_repo(specified: Optional[str]) -> str:
    if specified:
        return specified
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit("Could not determine repo from git remote. Pass --repo OWNER/REPO.")
    url = result.stdout.strip()
    # Handles https://github.com/owner/repo and git@github.com:owner/repo
    if "github.com" in url:
        url = url.replace("git@github.com:", "").replace("https://github.com/", "")
        url = url.removesuffix(".git")
        return url
    sys.exit(f"Unexpected remote URL format: {url}. Pass --repo OWNER/REPO.")


def get_assignee(specified: Optional[str]) -> str:
    if specified:
        return specified
    result = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit("Could not determine current gh user. Pass --assignee USERNAME.")
    return result.stdout.strip()


def create_labels(repo: str, dry_run: bool) -> None:
    print("\n=== Creating labels ===")
    for label in LABELS:
        print(f"  Label: {label.name}")
        _run([
            "gh", "label", "create", label.name,
            "--repo", repo,
            "--color", label.color,
            "--description", label.description,
            "--force",   # update if already exists
        ], dry_run)


def create_milestones(repo: str, dry_run: bool) -> dict[str, int]:
    """Create milestones and return a mapping of title -> number."""
    print("\n=== Creating milestones ===")
    title_to_number: dict[str, int] = {}
    for ms in MILESTONES:
        print(f"  Milestone: {ms.title}")
        output = _run([
            "gh", "api",
            f"repos/{repo}/milestones",
            "--method", "POST",
            "-f", f"title={ms.title}",
            "-f", f"description={ms.description}",
            "-f", f"due_on={ms.due_on}",
        ], dry_run, capture=True)
        if output:
            try:
                data = json.loads(output)
                title_to_number[ms.title] = data["number"]
            except (json.JSONDecodeError, KeyError):
                pass
    # Also fetch existing milestones to fill in any that already existed
    if not dry_run:
        existing = subprocess.run(
            ["gh", "api", f"repos/{repo}/milestones", "--jq", ".[] | {title: .title, number: .number}"],
            capture_output=True, text=True,
        )
        if existing.returncode == 0:
            for line in existing.stdout.strip().splitlines():
                try:
                    obj = json.loads(line)
                    title_to_number.setdefault(obj["title"], obj["number"])
                except (json.JSONDecodeError, KeyError):
                    pass
    return title_to_number


def create_issues(
    repo: str,
    assignee: str,
    milestone_map: dict[str, int],
    dry_run: bool,
) -> None:
    print(f"\n=== Creating {len(ISSUES)} issues (assignee: {assignee}) ===")
    for i, issue in enumerate(ISSUES, start=1):
        print(f"  [{i:02d}/{len(ISSUES)}] {issue.title}")
        cmd = [
            "gh", "issue", "create",
            "--repo", repo,
            "--title", issue.title,
            "--body", issue.body,
            "--assignee", assignee,
        ]
        for label in issue.labels:
            cmd += ["--label", label]
        milestone_number = milestone_map.get(issue.milestone)
        if milestone_number:
            cmd += ["--milestone", str(milestone_number)]
        _run(cmd, dry_run)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create AssetSafe MVP GitHub issues via the gh CLI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--repo", help="OWNER/REPO (default: detected from git remote)")
    parser.add_argument("--assignee", help="GitHub username to assign issues to (default: current gh user)")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    args = parser.parse_args()

    repo = get_repo(args.repo)
    assignee = get_assignee(args.assignee)

    print(f"Repository : {repo}")
    print(f"Assignee   : {assignee}")
    print(f"Dry-run    : {args.dry_run}")
    print(f"Issues     : {len(ISSUES)}")
    print(f"Milestones : {len(MILESTONES)}")
    print(f"Labels     : {len(LABELS)}")

    create_labels(repo, args.dry_run)
    milestone_map = create_milestones(repo, args.dry_run)
    create_issues(repo, assignee, milestone_map, args.dry_run)

    print("\n✅  Done! Visit https://github.com/{}/issues to review.".format(repo))


if __name__ == "__main__":
    main()
