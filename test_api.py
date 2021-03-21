from httpserver import app
import flask

def test_baseapi():        
    response = app.test_client().get('/')
    assert response.status_code == 200
    
def test_set():
    with app.test_request_context('/set/aba-1?value=4'):
        assert flask.request.path == '/set/aba-1'
        assert flask.request.args['value'] == '4'

def test_get_all():
    response = app.test_client().get('/get')
    assert response.status_code == 200

def test_get_key():
    response = app.test_client().get('/get/aba-1')
    assert response.status_code == 200

def test_clear():
    response = app.test_client().get('/get')
    assert response.status_code == 200
    