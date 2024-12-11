from arkindex_cli.commands.export.entities import retrieve_transcription_entities
from arkindex_export import open_database


def test_export_entities_no_filters(export_db_path):
    open_database(export_db_path)
    assert list(
        retrieve_transcription_entities("http://instance.teklia.com/", None, [])
    ) == [
        {
            "transcription_id": "traid1",
            "element_id": "b53a8dbd-3135-4540-87f0-e08a9a396e11",
            "element_url": "http://instance.teklia.com/element/b53a8dbd-3135-4540-87f0-e08a9a396e11",
            "entity_id": "9a3e09e2-cdd1-401d-aaf0-68bc7ef79d62",
            "entity_value": "entityname2",
            "entity_type": "entitytype1",
            "confidence": None,
            "entity_metas": "{'a': 'b', 'c': 'ddd'}",
            "offset": 3,
            "length": 5,
        },
        {
            "transcription_id": "traid2",
            "element_id": "ccc04dfe-39af-4118-bb56-3aaf0350ba8b",
            "element_url": "http://instance.teklia.com/element/ccc04dfe-39af-4118-bb56-3aaf0350ba8b",
            "entity_id": "cc79949a-07b4-40fb-934b-0a593d483b1d",
            "entity_value": "entityname1",
            "entity_type": "entitytype1",
            "confidence": None,
            "entity_metas": None,
            "offset": 2,
            "length": 6,
        },
        {
            "transcription_id": "traid4",
            "element_id": "a87884d1-5233-4207-9b02-66bbe494da84",
            "element_url": "http://instance.teklia.com/element/a87884d1-5233-4207-9b02-66bbe494da84",
            "entity_id": "9a3e09e2-cdd1-401d-aaf0-68bc7ef79d62",
            "entity_value": "entityname2",
            "entity_type": "entitytype1",
            "confidence": 0.3,
            "entity_metas": "{'a': 'b', 'c': 'ddd'}",
            "offset": 2,
            "length": 10,
        },
        {
            "element_id": "a87884d1-5233-4207-9b02-66bbe494da84",
            "element_url": "http://instance.teklia.com/element/a87884d1-5233-4207-9b02-66bbe494da84",
            "entity_id": "cc79949a-07b4-40fb-934b-0a593d483b1d",
            "entity_metas": None,
            "entity_type": "entitytype1",
            "entity_value": "entityname1",
            "confidence": 0.12,
            "length": 8,
            "offset": 12,
            "transcription_id": "traid4",
        },
        {
            "transcription_id": "traid4",
            "element_id": "a87884d1-5233-4207-9b02-66bbe494da84",
            "element_url": "http://instance.teklia.com/element/a87884d1-5233-4207-9b02-66bbe494da84",
            "entity_id": "d3a344e8-e5c2-4ce8-9acd-3663163ba07b",
            "entity_value": "entityname3",
            "entity_type": "entitytype2",
            "confidence": 1,
            "entity_metas": None,
            "offset": 8,
            "length": 4,
        },
        {
            "transcription_id": "traid5",
            "element_id": "7605faf7-b316-423e-b2c1-b6d845dba4bd",
            "element_url": "http://instance.teklia.com/element/7605faf7-b316-423e-b2c1-b6d845dba4bd",
            "entity_id": "670d3fd0-5dd5-4e9f-a888-d573354dab31",
            "entity_value": "entityname4",
            "entity_type": "entitytype3",
            "confidence": None,
            "entity_metas": None,
            "offset": 15,
            "length": 8,
        },
        {
            "transcription_id": "traid6",
            "element_id": "ccc04dfe-39af-4118-bb56-3aaf0350ba8b",
            "element_url": "http://instance.teklia.com/element/ccc04dfe-39af-4118-bb56-3aaf0350ba8b",
            "entity_id": "d3a344e8-e5c2-4ce8-9acd-3663163ba07b",
            "entity_value": "entityname3",
            "entity_type": "entitytype2",
            "confidence": 0.96,
            "entity_metas": None,
            "offset": 4,
            "length": 6,
        },
    ]


def test_export_entities_type_filter(export_db_path):
    open_database(export_db_path)
    assert list(
        retrieve_transcription_entities("http://instance.teklia.com/", "page", [])
    ) == [
        {
            "transcription_id": "traid4",
            "element_id": "a87884d1-5233-4207-9b02-66bbe494da84",
            "element_url": "http://instance.teklia.com/element/a87884d1-5233-4207-9b02-66bbe494da84",
            "entity_id": "9a3e09e2-cdd1-401d-aaf0-68bc7ef79d62",
            "entity_value": "entityname2",
            "entity_type": "entitytype1",
            "confidence": 0.3,
            "entity_metas": "{'a': 'b', 'c': 'ddd'}",
            "offset": 2,
            "length": 10,
        },
        {
            "element_id": "a87884d1-5233-4207-9b02-66bbe494da84",
            "element_url": "http://instance.teklia.com/element/a87884d1-5233-4207-9b02-66bbe494da84",
            "entity_id": "cc79949a-07b4-40fb-934b-0a593d483b1d",
            "entity_metas": None,
            "entity_type": "entitytype1",
            "entity_value": "entityname1",
            "confidence": 0.12,
            "length": 8,
            "offset": 12,
            "transcription_id": "traid4",
        },
        {
            "transcription_id": "traid4",
            "element_id": "a87884d1-5233-4207-9b02-66bbe494da84",
            "element_url": "http://instance.teklia.com/element/a87884d1-5233-4207-9b02-66bbe494da84",
            "entity_id": "d3a344e8-e5c2-4ce8-9acd-3663163ba07b",
            "entity_value": "entityname3",
            "entity_type": "entitytype2",
            "confidence": 1,
            "entity_metas": None,
            "offset": 8,
            "length": 4,
        },
    ]


def test_export_entities_worker_version_filter(export_db_path):
    open_database(export_db_path)
    assert list(
        retrieve_transcription_entities(
            "http://instance.teklia.com/", None, ["worker_id2"]
        )
    ) == [
        {
            "transcription_id": "traid2",
            "element_id": "ccc04dfe-39af-4118-bb56-3aaf0350ba8b",
            "element_url": "http://instance.teklia.com/element/ccc04dfe-39af-4118-bb56-3aaf0350ba8b",
            "entity_id": "cc79949a-07b4-40fb-934b-0a593d483b1d",
            "entity_value": "entityname1",
            "entity_type": "entitytype1",
            "confidence": None,
            "entity_metas": None,
            "offset": 2,
            "length": 6,
        },
        {
            "transcription_id": "traid5",
            "element_id": "7605faf7-b316-423e-b2c1-b6d845dba4bd",
            "element_url": "http://instance.teklia.com/element/7605faf7-b316-423e-b2c1-b6d845dba4bd",
            "entity_id": "670d3fd0-5dd5-4e9f-a888-d573354dab31",
            "entity_value": "entityname4",
            "entity_type": "entitytype3",
            "confidence": None,
            "entity_metas": None,
            "offset": 15,
            "length": 8,
        },
    ]


def test_export_entities_all_filters(export_db_path):
    open_database(export_db_path)
    assert (
        retrieve_transcription_entities(
            "http://instance.teklia.com/", "page", ["worker_id2"]
        )
        == []
    )
