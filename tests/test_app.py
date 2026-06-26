# def test_app_factory_creates_app():
#     from app import create_app

#     app = create_app()

#     assert app is not None


# def test_homepage_redirects_to_login():
#     from app import create_app

#     app = create_app()
#     client = app.test_client()
#     response = client.get("/")

#     assert response.status_code == 302


def test_pipeline():
    print("Hello, World!")
