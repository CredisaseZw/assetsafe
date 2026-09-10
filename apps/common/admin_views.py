"""Staff-only Django admin views for external registry lookup."""

from __future__ import annotations

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from apps.common.services.external_registry import ExternalRegistryClient


@staff_member_required
@require_http_methods(["GET", "POST"])
def external_registry_lookup(request):
    """Look up a person or company on the external registry and show results."""
    # Prefill from query string (e.g. links from Individual/Company change forms).
    lookup_type = (
        request.POST.get("lookup_type")
        if request.method == "POST"
        else request.GET.get("lookup_type") or "person"
    ).strip() or "person"
    query = (
        request.POST.get("query")
        if request.method == "POST"
        else request.GET.get("query") or ""
    ).strip()

    context: dict = {
        "title": "External registry lookup",
        "lookup_type": lookup_type,
        "query": query,
        "result": None,
        "configured": ExternalRegistryClient().is_configured,
    }

    if request.method == "POST":
        client = ExternalRegistryClient()
        if not client.is_configured:
            messages.error(
                request,
                "External registry is not configured. Set "
                "EXTERNAL_REGISTRY_BASE_URL, EXTERNAL_REGISTRY_USERNAME, "
                "and EXTERNAL_REGISTRY_TOKEN.",
            )
        elif not query:
            messages.error(request, "Enter a national ID or company search term.")
        elif lookup_type == "company":
            rows = client.search_companies(query)
            if not rows:
                messages.warning(request, "No company found for that search.")
            else:
                context["result"] = {"kind": "company", "rows": rows}
        else:
            rows = client.search_individuals(query)
            if not rows:
                messages.warning(
                    request,
                    "No person found. Use a Zimbabwe national ID "
                    "(e.g. 12-345678-A-12).",
                )
            else:
                context["result"] = {"kind": "person", "rows": rows}

    return render(request, "admin/common/external_registry_lookup.html", context)
