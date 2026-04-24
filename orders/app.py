
from pathlib import Path
import yaml
from fastapi import FastAPI

# from orders.api import api
app = FastAPI(debug=True, open_url='/openapi/orders.json', docs_url='/docs/orders') 

# we load the API specification using pyYAML
oas_doc = yalm.safe_load(
    (path(__file__).parent / '..oas.yaml').read_text()
)

# we override FastAPI's openapi property so tht it returns our api specification
app.openapi = lambda: oas_doc


from orders.api import api