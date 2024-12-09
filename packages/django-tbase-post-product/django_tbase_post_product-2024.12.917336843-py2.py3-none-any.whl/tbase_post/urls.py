from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from .sitemaps import PostSitemap
from . import views
from .views import PromptTaskListView
from .views import PromptTaskView,PromptTaskPostView,PromptTaskPostListView
sitemaps = {
    'posts': PostSitemap,
}
urlpatterns = [
    path('', cache_page(60 *15*1)(views.IndexView.as_view()), name='detail_index'),
    path('last', cache_page(60 * 60)(views.LastUpdateView.as_view()), name='last_index'),
    path('list', views.PostListView.as_view(), name='list'),
    path('detail/<int:pk>/', cache_page(60 *60*24)(views.DetailView.as_view()), name='detail_view'),
    path('tag/<int:pk>/',
         cache_page(60 * 60*24)(views.TagListView.as_view()),
         name='article_list_by_tag'),

    path("prompt/task/", PromptTaskListView.as_view(), name="prompt_task_list"),
    path("prompt/task/<int:pk>/", PromptTaskView.as_view(), name="prompt_task_detail"),
    path("prompt/task/<int:pk>/<int:post_pk>/", PromptTaskPostView.as_view(), 
         name="prompt_task_post"),

    path("prompt/post/<int:post_pk>/", PromptTaskPostListView.as_view(), 
         name="prompt_task_post_list"),

    path('amz/<str:id>/', views.amazon_go, name='amz_go'),
    path('sitemap.xml', 
         sitemap, 
         {'sitemaps': sitemaps}, 
         name='django.contrib.sitemaps.views.sitemap'),  # 网站地图 
    # path('detail/<int:pk>', views.DetailView.as_view(), name='post_view'),
    # path('<int:pk>/', views.PostView.as_view(), name='post'),
]