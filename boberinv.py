from app import create_app, db
from app.models import User, Buyer, Rate, Item, Invoice


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Buyer': Buyer, 'Rate': Rate, 'Item': Item,
            'Invoice': Invoice}

