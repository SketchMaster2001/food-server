import enum

<<<<<<< HEAD
from food import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlalchemy, json


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


=======
from food import db
import sqlalchemy, json


>>>>>>> 82dea622c1503a7a61508b8f7a0640537beecc33
class DictType(sqlalchemy.types.TypeDecorator):

    impl = sqlalchemy.Text()

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class CategoryTypes(enum.Enum):
    Pizza = 1
    Bento_Box = 2
    Sushi = 3
    Fish = 4
    Seafood = 5
    Western = 6
    Fast_Food = 7
    Curry = 8
    Party_Food = 9
    Drinks = 10
    Others = 11
<<<<<<< HEAD

    @classmethod
    def choices(cls):
        return [(choice, choice.name.replace("_", " ")) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)
=======
>>>>>>> 82dea622c1503a7a61508b8f7a0640537beecc33


class Shops(db.Model):
    name = db.Column(db.String, nullable=False)
    category_code = db.Column(db.Enum(CategoryTypes), nullable=False)
    description = db.Column(db.String, nullable=False)
    shop_code = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    wait_time = db.Column(db.Integer, nullable=False)
<<<<<<< HEAD
=======
    open = db.Column(db.Boolean, nullable=False)
>>>>>>> 82dea622c1503a7a61508b8f7a0640537beecc33
    address = db.Column(db.String, nullable=False)
    amenity = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)


class MenuList(db.Model):
    menu_code = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    title = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    shop_code = db.Column(db.Integer, db.ForeignKey("shops.shop_code"), nullable=False)


class ItemList(db.Model):
    item_code = db.Column(db.Integer, nullable=False, primary_key=True)
    menu_code = db.Column(
        db.Integer, db.ForeignKey("menu_list.menu_code"), nullable=False
    )
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)


<<<<<<< HEAD
class Orders(db.Model):
    zip_code = db.Column(db.String, primary_key=True, nullable=False)
    basket = db.Column(DictType, nullable=False)


class User(db.Model, UserMixin):
    # Used to login to the Admin Panel
    id = db.Column(db.Integer, primary_key=True, default=1)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
=======
class User(db.Model):
    zip_code = db.Column(db.String, primary_key=True, nullable=False)
    basket = db.Column(DictType, nullable=False)
>>>>>>> 82dea622c1503a7a61508b8f7a0640537beecc33
