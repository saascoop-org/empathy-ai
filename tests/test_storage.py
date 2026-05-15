from empathy_engine.storage.interaction_store import InteractionStore, SCHEMA_VERSION


def test_interaction_store_persists_anonymized_result(tmp_path):
    db_path = tmp_path / "interactions.sqlite3"
    store = InteractionStore(db_path)

    record_id = store.save(
        "[PERSON] asked for clarification.",
        {"response": {"bridge_message": "Ask what would help."}},
        "Useful and safe",
    )

    assert record_id == 1
    assert db_path.exists()


def test_interaction_store_reads_lists_and_deletes_records(tmp_path):
    db_path = tmp_path / "interactions.sqlite3"
    store = InteractionStore(db_path)

    first_id = store.save(
        "[PERSON] asked for clarification.",
        {"interaction": "[PERSON] asked for clarification."},
        "Useful and safe",
    )
    second_id = store.save(
        "[PERSON] asked for more context.",
        {"interaction": "[PERSON] asked for more context."},
        "Partially useful",
    )

    assert store.schema_version() == SCHEMA_VERSION

    stored = store.get(first_id)
    assert stored.id == first_id
    assert stored.feedback == "useful_safe"

    records = store.list()
    assert [record.id for record in records] == [second_id, first_id]
    assert records[0].feedback == "partially_useful"

    assert store.delete(first_id) == 1
    assert store.get(first_id) is None

    assert store.delete_all() == 1
    assert store.list() == []


def test_interaction_store_list_does_not_create_database(tmp_path):
    db_path = tmp_path / "interactions.sqlite3"
    store = InteractionStore(db_path)

    assert store.list() == []
    assert store.get(1) is None
    assert not db_path.exists()


def test_interaction_store_does_not_store_raw_interaction_key(tmp_path):
    db_path = tmp_path / "interactions.sqlite3"
    store = InteractionStore(db_path)

    record_id = store.save(
        "[PERSON] anonymized text.",
        {
            "raw_interaction": "Maria Silva emailed maria@example.com.",
            "interaction": "[PERSON] anonymized text.",
        },
        "Not useful",
    )

    stored = store.get(record_id)
    assert "raw_interaction" not in stored.result_json
    assert stored.feedback == "not_useful"
