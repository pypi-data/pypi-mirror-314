from django.shortcuts import render
from django.views import View

# Create your views here.
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import ensure_csrf_cookie
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from hitcount.views import HitCountDetailView

from urllib.parse import urlencode
from taggit.models import TaggedItem
from taggit.models import Tag
from django.views.generic.base import TemplateView
from django.template import Template
from django.views import generic
from django.views.decorators.cache import cache_page
# from django.core.cache import caches
from django.core.cache import cache
from django.db.models import Q
from . import models

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import ListView
 
from django.views.generic import DetailView

from .models import PromptTask, Post,Prompt


 
class PromptTaskListView(PermissionRequiredMixin,ListView):
    """
    提示词任务列表
    """
    permission_required = 'post.permission_prompt'
    model = PromptTask
    template_name = "post/prompt_task_list.html"
    context_object_name = "all_tasks"
 
class PromptTaskView(PermissionRequiredMixin,ListView):
    
    """
    单个任务对应的post
    
    """
    permission_required = 'post.permission_prompt'
    model = Post
    template_name = "post/prompt_task_detail.html"
    context_object_name = "all_posts"
    paginate_by = 50
    ordering = ['-updated_on']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prompt = Prompt.objects.get(pk=self.kwargs["pk"])
        # context["templ"] = """
        # <h1>这是一个标题</h1>
        # <p>这是一个段落</p>

        # <p>Post 标题：{{ post.title }}</p>
        # <p>Post 内容：{{ post.content }}</p>
        # """
        context["prompt"] = prompt
        return context
    


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         prompt = Prompt.objects.get(pk=self.kwargs["pk"])
#         print("prompt",prompt)
#         context["prompt"] = prompt
#         return context



#     def get_queryset(self):
#         # retrieve the tag from the URL
#         tag_slug = self.kwargs['pk']
 
        
#         # get the tag object based on the slug
#         tag = Tag.objects.get(pk=tag_slug)
#         # filter articles based on the tag
 
# #        articles = self.model.objects.filter(tags=tag)
#         articles = self.model.objects.filter(Q(tags=tag)& Q(publish_status="published"))
#         # if len(articles)<500:
#         #     print("No articles")
#             # return Http404('project list dose not exist')
#         cache.set(key,articles,60*60*25)
#         return articles

#     def get_context_data(self, *args, **kwargs):
#         """

#         """
#         context = super().get_context_data(**kwargs)
#         # 获取tag的标签
#         tag_slug = self.kwargs['pk']
#         tag = Tag.objects.get(pk=tag_slug)
      
#         context['pk'] = self.kwargs['pk']
#         # print("context", context)
   
#         if len(context['object_list'])<10:
#             print("No")
#             context['meta'] = {
#             'noindex':True
#             }
#             # return Http404('project list dose not exist')
#             # return View.defaults.page_not_found()
#             # raise Http404("Poll does not exist")
#         else:
#             context['meta'] = {
#             'noindex':False
#              }
#         return context
    




 
class PromptTaskPostView(PermissionRequiredMixin,DetailView):
    permission_required = 'post.permission_prompt'
    model = PromptTask
    template_name = "post/prompt_task_post_detail.html"

    # def render_to_response(self, context):
    #     # 动态生成模板
    #     template = Template(self.objecttempl)
    #     context = Context({"object": self.object})
    #     return render(request, template, context)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs["post_pk"])
        # context["templ"] = """
        # <h1>这是一个标题</h1>
        # <p>这是一个段落</p>

        # <p>Post 标题：{{ post.title }}</p>
        # <p>Post 内容：{{ post.content }}</p>
        # """
        context["post"] = post
        return context
 
    # template = Template(template_source)

# class DetailView(TemplateView):

#     # def get(self, request, pk, *args, **kwargs):
#     #     return HttpResponse(f'Hello, World!{pk}')
#     template_name = "detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['latest_articles'] = Article.objects.all()[:5]
#         return context





 
class PromptTaskPostListView(PermissionRequiredMixin,ListView):
    """
    单个post对应的提示词任务列表
    """
    permission_required = 'post.permission_prompt'
    model = PromptTask
    template_name = "post/prompt_task_post_list.html"
    context_object_name = "all_tasks"
    paginate_by = 50
 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs["post_pk"])
        context["post"] = post
        return context



class PostListView(generic.ListView):
    model = models.Post
    template_name = 'post_list.html'
    context_object_name = 'post'


class PostMixinDetailView(object):
    """
    Mixin to save us some typing.  Adds context for us!
    """
    model = models.Post

    def get_context_data(self, **kwargs):
        context = super(PostMixinDetailView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()[:5]
        context['post_views'] = ["ajax", "detail", "detail-with-count"]
        return context





# @cache_page(60*2)
# class DetailView(generic.DetailView,HitCountDetailView):
class DetailView(HitCountDetailView):
    template_name = 'post/detail.html'
    # context_object_name = 'post'
    # def get(request, pk):
    #     """Return the last five published questions."""
    #     return Post.objects.get(id=pk)
    model = models.Post
    context_object_name = 'detail'
    ordering = ['-updated_on']
    count_hit = True

    def get_queryset(self):
        # 限制已发布内容
        content = self.model.objects.filter(Q(publish_status="published"))
        return content
    # # 控制访问权限
    # @method_decorator(login_required)
    # @method_decorator(permission_required('dashboard.view_server'))
    # def get(self, request, *args, **kwargs):
    #     print("kwargs", kwargs)
    #     # context = self.model.objects.get(id=pk)
    #     context = super().get_context_data(**kwargs)
    #     # context['now'] = timezone.now()
    #     return context

    def get_context_data(self, *args, **kwargs):
        # print("kwargs",kwargs)
        # context = Post.objects.get(id=pk)
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # context['title'] = "Post Details"
        # print(context['object'].publish_status)
        # context.update({
        #     'popular_posts': models.Post.objects.order_by('-hit_count_generic__hits')[:3],
        #     })
        return context










# class PostDetailJSONView(PostMixinDetailView, DetailView):
#     template_name = 'blog/post_ajax.html'

#     @classmethod
#     def as_view(cls, **initkwargs):
#         view = super(PostDetailJSONView, cls).as_view(**initkwargs)
#         return ensure_csrf_cookie(view)


class PostCountHitDetailView(PostMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True




# @cache_page(60*2)
class IndexView(generic.ListView):

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse('Hello, World! index')

    template_name = 'post/blog_index.html'
    model = models.Post
    paginate_by = 10
    ordering = ['-updated_on']

    def get_queryset(self):
        # 限制已发布内容
        content = self.model.objects.filter(Q(publish_status="published"))
        return content

    # context_object_name = 'model_list'
    # def get(self, request, *args, **kwargs):
    #     return HttpResponse('Hello, World! index')
    #     # return {}
    def get_context_data(self, *args, **kwargs):
        # print("kwargs",kwargs)
        # context = Post.objects.get(id=pk)
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # context['title'] = "Post Details"
        # print(context)
        return context
    
    
# @cache_page(60*2)
class LastUpdateView(generic.ListView):
    """
    最后更新页面
    """

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse('Hello, World! index')

    template_name = 'post/last_index.html'
    model = models.Post
    paginate_by = 100
    ordering = ['-updated_on']

    def get_queryset(self):
        # 限制已发布内容
        content = self.model.objects.filter(Q(publish_status="published"))
        return content


    # context_object_name = 'model_list'
    # def get(self, request, *args, **kwargs):
    #     return HttpResponse('Hello, World! index')
    #     # return {}
    def get_context_data(self, *args, **kwargs):
        # print("kwargs",kwargs)
        # context = Post.objects.get(id=pk)
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # context['title'] = "Post Details"
        # print(context)
        return context
# @cache_page(60*60)
class TagListView(generic.ListView):
    model = models.Post
    template_name = 'post/article_list_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 20
    ordering = ['-updated_on']
    def get_queryset(self):
        # retrieve the tag from the URL
        tag_slug = self.kwargs['pk']

        key=f'article_tag_{tag_slug}'
        articles=cache.get(key)
        if articles is not None: 
            return articles
        
        # get the tag object based on the slug
        tag = Tag.objects.get(pk=tag_slug)
        # filter articles based on the tag
 
#        articles = self.model.objects.filter(tags=tag)
        articles = self.model.objects.filter(Q(tags=tag)& Q(publish_status="published"))
        # if len(articles)<500:
        #     print("No articles")
            # return Http404('project list dose not exist')
        cache.set(key,articles,60*60*25)
        return articles

    def get_context_data(self, *args, **kwargs):
        """

        """
        context = super().get_context_data(**kwargs)
        # 获取tag的标签
        tag_slug = self.kwargs['pk']
        tag = Tag.objects.get(pk=tag_slug)
        context['title'] = f"{tag}-{context['page_obj']}"
        context['pk'] = self.kwargs['pk']
        # print("context", context)
   
        if len(context['object_list'])<10:
            print("No")
            context['meta'] = {
            'noindex':True
            }
            # return Http404('project list dose not exist')
            # return View.defaults.page_not_found()
            # raise Http404("Poll does not exist")
        else:
            context['meta'] = {
            'noindex':False
             }
        return context
    

def amazon_go(request,id):
    """
    
    跳转到亚马逊
    
    """
 
    response = HttpResponse("", status=302)
    querydict={}

    amazon=models.AmazonSettings()
    a=amazon.get_solo()

    querydict['tag']=a.store_id

    # print(querydict)
    q=urlencode(querydict)
    response['Location'] = f"https://www.amazon.com/dp/{id}/?{q}"
    return response




