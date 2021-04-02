from django.urls import path

from . import views

app_name = 'catalog'
urlpatterns = [
    # TODO: надо добавить проверку на POST
    path('change_lang/', views.change_lang, name='change_lang'),
    # ex: /polls/
    # path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path('<int:productid>/', views.detail, name='detail'),
    path('<str:sku>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
