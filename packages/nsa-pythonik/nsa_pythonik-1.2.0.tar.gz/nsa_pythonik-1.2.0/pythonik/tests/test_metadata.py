import uuid
import requests_mock
from pythonik.client import PythonikClient
from requests import HTTPError
from pythonik.models.base import ObjectType

from pythonik.models.metadata.views import (
    FieldValue,
    FieldValues,
    MetadataValues,
    ViewMetadata,
)
from pythonik.models.mutation.metadata.mutate import (
    UpdateMetadata,
    UpdateMetadataResponse,
)
from pythonik.specs.metadata import (
    ASSET_METADATA_FROM_VIEW_PATH,
    UPDATE_ASSET_METADATA,
    MetadataSpec,
    ASSET_OBJECT_VIEW_PATH,
    PUT_METADATA_DIRECT_PATH
)


def test_get_asset_metadata():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        model = ViewMetadata()
        data = model.model_dump()
        mock_address = MetadataSpec.gen_url(
            ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id)
        )
        m.get(mock_address, json=data)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.metadata().get_asset_metadata(asset_id, view_id)


def test_get_asset_intercept_404():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        mv = MetadataValues(
            {
                "this_worked_right?": FieldValues(
                    field_values=[FieldValue(value="lets hope")]
                )
            }
        )

        model = ViewMetadata()
        model.metadata_values = mv
        data = model.model_dump()
        mock_address = MetadataSpec.gen_url(
            ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id)
        )
        m.get(mock_address, json=data, status_code=404)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        resp = client.metadata().get_asset_metadata(
            asset_id, view_id, intercept_404=model
        )
        assert resp.data == model


def test_get_asset_intercept_404_raise_for_status():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        mv = MetadataValues(
            {
                "this_worked_right?": FieldValues(
                    field_values=[FieldValue(value="lets hope")]
                )
            }
        )

        model = ViewMetadata()
        model.metadata_values = mv
        data = model.model_dump()
        mock_address = MetadataSpec.gen_url(
            ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id)
        )
        m.get(mock_address, json=data, status_code=404)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        resp = client.metadata().get_asset_metadata(
            asset_id, view_id, intercept_404=model
        )
        # should not raise for status
        try:
            resp.response.raise_for_status()
            # this line should run and the above should not raise for status
            assert True is True
        except Exception as e:
            pass


def test_get_asset_intercept_404_raise_for_status_404():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())

        mv = MetadataValues(
            {
                "this_worked_right?": FieldValues(
                    field_values=[FieldValue(value="lets hope")]
                )
            }
        )

        model = ViewMetadata()
        model.metadata_values = mv
        data = model.model_dump()
        mock_address = MetadataSpec.gen_url(
            ASSET_METADATA_FROM_VIEW_PATH.format(asset_id, view_id)
        )
        m.get(mock_address, json=data, status_code=404)
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        resp = client.metadata().get_asset_metadata(
            asset_id, view_id, intercept_404=model
        )
        # should not raise for status
        exception = None
        try:
            resp.response.raise_for_status_404()
            # this line should run and the above should not raise for status
        except HTTPError as e:
            exception = e

        # assert exception still raised with 404
        assert exception.response.status_code == 404


def test_update_asset_metadata():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())
        payload = {"metadata_values": {"field1": {"field_values": [{"value": "123"}]}}}

        mutate_model = UpdateMetadata.model_validate(payload)
        response_model = UpdateMetadataResponse(
            metadata_values=mutate_model.metadata_values.model_dump()
        )

        mock_address = MetadataSpec.gen_url(
            UPDATE_ASSET_METADATA.format(asset_id, view_id)
        )
        m.put(mock_address, json=response_model.model_dump())
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.metadata().update_asset_metadata(asset_id, view_id, mutate_model)


def test_put_segment_view_metadata():
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        asset_id = str(uuid.uuid4())
        segment_id = str(uuid.uuid4())
        view_id = str(uuid.uuid4())
        
        # Create test payload
        payload = {
            "metadata_values": {
                "field1": {
                    "field_values": [{"value": "123"}]
                }
            }
        }

        mutate_model = UpdateMetadata.model_validate(payload)
        response_model = UpdateMetadataResponse(
            metadata_values=mutate_model.metadata_values.model_dump()
        )

        # Mock the endpoint using the ASSET_OBJECT_VIEW_PATH
        mock_address = MetadataSpec.gen_url(
            ASSET_OBJECT_VIEW_PATH.format(asset_id, "segments", segment_id, view_id)
        )
        m.put(mock_address, json=response_model.model_dump())

        # Make the request
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        client.metadata().put_segment_view_metadata(
            asset_id, segment_id, view_id, mutate_model
        )


def test_put_metadata_direct():
    """Test direct metadata update without a view."""
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        object_type = ObjectType.ASSETS.value
        object_id = str(uuid.uuid4())

        # Create test metadata
        metadata_values = {
            "metadata_values": {
                "test_field": {
                    "field_values": [{"value": "test_value"}]
                }
            }
        }
        metadata = UpdateMetadata.model_validate(metadata_values)

        # Expected response
        response_data = {
            "date_created": "2024-12-10T19:58:25Z",
            "date_modified": "2024-12-10T19:58:25Z",
            "metadata_values": metadata_values["metadata_values"],
            "object_id": object_id,
            "object_type": object_type,
            "version_id": str(uuid.uuid4())
        }

        # Mock the PUT request
        mock_address = MetadataSpec.gen_url(
            PUT_METADATA_DIRECT_PATH.format(object_type, object_id)
        )
        m.put(mock_address, json=response_data)

        # Make the request
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        response = client.metadata().put_metadata_direct(object_type, object_id, metadata)

        # Verify response
        assert response.response.ok
        assert response.data.object_id == object_id
        assert response.data.object_type == object_type
        assert response.data.metadata_values == metadata_values["metadata_values"]


def test_put_metadata_direct_unauthorized():
    """Test direct metadata update with invalid token."""
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = "invalid_token"
        object_type = ObjectType.ASSETS.value
        object_id = str(uuid.uuid4())

        # Create empty metadata
        metadata = UpdateMetadata.model_validate({"metadata_values": {}})

        # Mock the PUT request to return 401
        mock_address = MetadataSpec.gen_url(
            PUT_METADATA_DIRECT_PATH.format(object_type, object_id)
        )
        m.put(mock_address, status_code=401)

        # Make the request
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        response = client.metadata().put_metadata_direct(object_type, object_id, metadata)

        # Verify response
        assert not response.response.ok
        assert response.response.status_code == 401


def test_put_metadata_direct_404():
    """Test direct metadata update with non-existent object."""
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        object_type = ObjectType.ASSETS.value
        object_id = str(uuid.uuid4())

        # Create test metadata
        metadata = UpdateMetadata.model_validate({"metadata_values": {}})

        # Mock the PUT request to return 404
        mock_address = MetadataSpec.gen_url(
            PUT_METADATA_DIRECT_PATH.format(object_type, object_id)
        )
        m.put(mock_address, status_code=404, json={
            "error": "Object not found",
            "message": f"Object {object_id} of type {object_type} not found"
        })

        # Make the request
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        response = client.metadata().put_metadata_direct(object_type, object_id, metadata)

        # Verify response
        assert not response.response.ok
        assert response.response.status_code == 404


def test_put_metadata_direct_invalid_format():
    """Test direct metadata update with invalid metadata format."""
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        object_type = ObjectType.ASSETS.value
        object_id = str(uuid.uuid4())

        # Create test metadata with invalid format
        metadata_values = {
            "metadata_values": {
                "test_field": {
                    # Missing required field_values array
                    "value": "test_value"
                }
            }
        }
        metadata = UpdateMetadata.model_validate({"metadata_values": {}})

        # Mock the PUT request to return 400
        mock_address = MetadataSpec.gen_url(
            PUT_METADATA_DIRECT_PATH.format(object_type, object_id)
        )
        m.put(mock_address, status_code=400, json={
            "error": "Invalid metadata format",
            "message": "Metadata values must contain field_values array"
        })

        # Make the request
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        response = client.metadata().put_metadata_direct(object_type, object_id, metadata)

        # Verify response
        assert not response.response.ok
        assert response.response.status_code == 400


def test_put_metadata_direct_malformed():
    """Test direct metadata update with malformed request."""
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())
        object_type = "invalid_type"  # Invalid object type
        object_id = str(uuid.uuid4())

        # Create test metadata
        metadata = UpdateMetadata.model_validate({"metadata_values": {}})

        # Mock the PUT request to return 400
        mock_address = MetadataSpec.gen_url(
            PUT_METADATA_DIRECT_PATH.format(object_type, object_id)
        )
        m.put(mock_address, status_code=400, json={
            "error": "Invalid request",
            "message": "Invalid object type: must be one of [assets, segments, collections]"
        })

        # Make the request
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        response = client.metadata().put_metadata_direct(object_type, object_id, metadata)

        # Verify response
        assert not response.response.ok
        assert response.response.status_code == 400


def test_put_metadata_direct_forbidden():
    """Test direct metadata update with non-admin user."""
    with requests_mock.Mocker() as m:
        app_id = str(uuid.uuid4())
        auth_token = str(uuid.uuid4())  # Valid token but non-admin user
        object_type = ObjectType.ASSETS.value
        object_id = str(uuid.uuid4())

        # Create test metadata
        metadata = UpdateMetadata.model_validate({"metadata_values": {}})

        # Mock the PUT request to return 403
        mock_address = MetadataSpec.gen_url(
            PUT_METADATA_DIRECT_PATH.format(object_type, object_id)
        )
        m.put(mock_address, status_code=403, json={
            "error": "Forbidden",
            "message": "Admin access required for direct metadata updates"
        })

        # Make the request
        client = PythonikClient(app_id=app_id, auth_token=auth_token, timeout=3)
        response = client.metadata().put_metadata_direct(object_type, object_id, metadata)

        # Verify response
        assert not response.response.ok
        assert response.response.status_code == 403
