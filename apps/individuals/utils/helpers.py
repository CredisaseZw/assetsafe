from apps.individuals.models.models import (
    EmploymentDetail,
    IndividualAccounts,
    IndividualContactDetail,
    NextOfKin,
)
from apps.common.models.models import Address, Document, Note


def update_upsert(model, lookup, data, extra=None):
    obj = model.objects.filter(**lookup).first()
    if obj:
        for key, val in data.items():
            setattr(obj, key, val)
        obj.save()
        return obj
    else:
        params = {**lookup, **data}
        if extra:
            params.update(extra)
        return model.objects.update_or_create(**params)


def individual_contact_helper(instance, contact_data):
    for contact in contact_data:
        contact_id = contact.get("id")
        phone_number = contact.get("phone_number")

        lookup_kwargs = {"individual": instance}
        if contact_id:
            lookup_kwargs["id"] = contact_id
        elif phone_number:
            lookup_kwargs["phone_number"] = phone_number

        update_upsert(IndividualContactDetail, lookup_kwargs, contact)

    return None


def create_address_helper(content_type, address_data, object_id):
    for address in address_data:
        Address.objects.create(
            content_type=content_type,
            object_id=object_id,
            suburb=address.get("suburb"),
            street_address=address.get("street_address"),
            address_type=address.get("address_type", "physical"),
            is_primary=address.get("is_primary", False),
        )
    return None


def individual_employment_details_helper(instance, employment_data):
    for employment in employment_data:
        employment_id = employment.get("id")
        lookup = (
            {"id": employment_id, "individual": instance}
            if employment_id
            else {"individual": instance}
        )
        update_upsert(EmploymentDetail, lookup, employment)
    return None


def individual_next_of_kin_helper(instance, kin_data):
    for kin in kin_data:
        kin_id = kin.get("id")
        lookup = (
            {"id": kin_id, "individual": instance}
            if kin_id
            else {"individual": instance}
        )
        update_upsert(NextOfKin, lookup, kin)
    return None


def individual_documents_helper(content_type, documents_data, object_id):
    for document in documents_data:
        document_id = document.get("id")
        lookup = (
            {"id": document_id, "content_type": content_type, "object_id": object_id}
            if document_id
            else {
                "content_type": content_type,
                "object_id": object_id,
                "file": document.get("file"),
                "document_type": document.get("document_type"),
            }
        )
        update_upsert(Document, lookup, **document)
    return None


def individual_notes_helper(content_type, notes_data, object_id):
    for note in notes_data:
        note_id = note.get("id")
        lookup = (
            {"id": note_id, "content_type": content_type, "object_id": object_id}
            if note_id
            else {"id": note_id, "content_type": content_type, "object_id": object_id}
        )
        update_upsert(Note, lookup, note)
    return None


def individual_account_details_helper(instance, account_data):
    accounts = [account_data] if isinstance(account_data, dict) else account_data
    for account in accounts:
        account_id = account.get("id")
        lookup = (
            {"id": account_id, "individual": instance}
            if account_id
            else {"individual": instance}
        )
        update_upsert(IndividualAccounts, lookup, account)
    return None
