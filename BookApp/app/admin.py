from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import Category, Product, UserRole, Tag
from app import app, db, dao
from flask_login import logout_user, current_user
from flask import redirect
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductModelView(AuthenticatedModelView):
    column_filters = ['name', 'price']
    column_searchable_list = ['name', 'description']
    column_exclude_list = ['image', 'description']
    can_view_details = True
    can_export = True
    column_labels = {
        'name': 'Tên sản phẩm',
        'price': 'Gía',
        'description': 'Mô tả'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
    page_size = 3


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_by_cate()
        return self.render('admin/index.html', msg='stats')
admin = Admin(app=app, name='Quản trị bán hàng', template_mode='bootstrap4')
admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
admin.add_view(ProductModelView(Product, db.session, name='Sản phẩm'))
admin.add_view(AuthenticatedModelView(Tag, db.session, name='Tag'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
