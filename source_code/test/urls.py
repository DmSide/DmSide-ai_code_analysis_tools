from django.conf.urls import url
from test import views
from lib.server_tuning import execution_at_startup

urlpatterns = [
    # ************* Test functions *************
    url(r'^$', views.index, name='index'),
    url(r'^test_exception_work/?$', views.test_exception_work),
    url(r'^prepare_db/?$', views.prepare_db),
    url(r'^get_accounts_list/?$', views.get_accounts_list),
    url(r'^get_account/?$', views.get_account),
    url(r'^delete_account/?$', views.delete_account),
    url(r'^check_path/?$', views.check_path),
    url(r'^get_languages_list/?$', views.get_languages_list),
    url(r'^add_language/?$', views.add_language),
    url(r'^remove_language/?$', views.remove_language),
    url(r'^update_language/?$', views.update_language),
    url(r'^add_repositories/?$', views.add_repositories),
    url(r'^task_repositories/?$', views.task_repositories),
]

execution_at_startup()
