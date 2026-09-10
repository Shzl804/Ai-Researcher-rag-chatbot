from app.main import app


def test_documents_upload_route_is_exposed():
    paths = {route.path for route in app.routes}
    assert "/documents/upload" in paths
