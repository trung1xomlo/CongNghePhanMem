from app.models import Category, Product, User, Receipt, ReceiptDetails, InfoDetails
from app import db
from flask_login import current_user
from sqlalchemy import func
import hashlib


def load_categories():
    return Category.query.all()


def load_products(category_id=None, kw=None):
    query = Product.query

    if category_id:
        query = query.filter(Product.category_id.__eq__(category_id))

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def info_details(firs_tname,name,email,phone_number,sex,address):
    i = InfoDetails(first_name=firs_tname, name=name, email=email,phone_number=phone_number,sex=sex,address=address)
    db.session.add(i)
    db.session.commit()

def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        try:
            db.session.commit()
        except:
            return False
        else:
            return True
def count_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
                                        .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
                                        .group_by(Category.id).order_by(Category.id).all()
if __name__ == '__main__':
    from app import app
    with app.app_context():
        print(count_by_cate())