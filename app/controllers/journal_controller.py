from app.models.journal import JournalModel

def create_journal_entry(user_id, data):
    if "content" not in data or not data["content"]:
        return {"msg": "Content required"}, 400

    entry = JournalModel.create(user_id, data["content"])
    entry["_id"] = str(entry["_id"])
    return {"msg": "Journal saved", "entry": entry}, 201


def get_user_journals(user_id):
    entries = JournalModel.find_by_user(user_id)
    return {"entries": entries}, 200


def update_journal_entry(user_id, entry_id, data):
    if "content" not in data:
        return {"msg": "Content required"}, 400

    result = JournalModel.update_entry(user_id, entry_id, data["content"])
    if result.modified_count == 0:
        return {"msg": "Not found or no permission"}, 404

    return {"msg": "Updated successfully"}, 200


def delete_journal_entry(user_id, entry_id):
    result = JournalModel.delete_entry(user_id, entry_id)
    if result.deleted_count == 0:
        return {"msg": "Not found or no permission"}, 404

    return {"msg": "Deleted successfully"}, 200
