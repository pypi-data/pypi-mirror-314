from django.contrib import admin
from django.db import models
# Register your models here.
from .models import Post,AmazonSettings,PostSettings,Link
 
# from markdownx.admin import MarkdownxModelAdmin
# from markdownx.widgets import AdminMarkdownxWidget
from martor.widgets import AdminMartorWidget
from solo.admin import SingletonModelAdmin
from django.utils.safestring import mark_safe
from django.utils.safestring import SafeText

from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import path





def make_published(modeladmin, request, queryset):
    # 设为发布
    make_published.short_description = "批量设为发布"
    queryset.update(publish_status='published')
def make_draft(modeladmin, request, queryset):
    # 批量设为草稿
    make_draft.short_description = "批量设为草稿"
    queryset.update(publish_status='draft')

def make_trash(modeladmin, request, queryset):
    # 设为trash
    make_trash.short_description = "批量设为垃圾内容"
    queryset.update(publish_status='trash')

 

from .models import Prompt, PromptTask, PromptTaskPrompt

class PromptInline(admin.TabularInline):
    model = PromptTaskPrompt
    def get_prompt_title(self, obj):
        return obj.prompt.title

    def get_prompt_description(self, obj):
        return obj.prompt.description

    readonly_fields = ('get_prompt_title', 'get_prompt_description')


class PromptTaskAdmin(admin.ModelAdmin):
    inlines = [PromptInline]
    list_display = ('title','pk','task_list_data',)
    readonly_fields=('task_list_data',)
    search_fields =('title', 'pk','description')  # 设置搜索字段
    def task_list_data(self, obj):
        try:
            url = reverse('prompt_task_detail', args=[obj.id])
            return mark_safe(f'<a href="{url}">任务列表</a>')
        except:
            return mark_safe(f'')
 
 
    


admin.site.register(Prompt)
admin.site.register(PromptTask, PromptTaskAdmin)


    

class LinkAdmin(admin.ModelAdmin):
## 链接，用于搜索优化，手动配置内链接
    save_on_top = True
    list_display = ('title','url','updated_on')
admin.site.register(Link, LinkAdmin)





class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title','image_data',
                    'task_list_data',
        'formatted_hit_count',
        'publish_status','updated_on','product_name','product_id','youtube_id')
    list_filter = (['updated_on','publish_status']) # 过滤字段
    search_fields =('title', 'product_name','product_id')  # 设置搜索字段
    ordering = ('-updated_on','product_name','product_id','hit_count_generic__hits')
    # 设置批量处理
    actions = [make_published,make_draft,make_trash]
    # formfield_overrides = {
    #     models.TextField: {'widget': AdminMarkdownxWidget},
    # }
    fieldsets = (
          ('基本', {
                'fields': ['title']
            }),
            ('产品信息', {
                'fields': ('product_name', 'product_id', 'article_img','image_data',
                            'youtube_id','youtube_player','publish_status'
                            ),
            }),
            ('seo优化', {
                'fields': ('tags', 'meta_keywords', 'meta_description'),
            }),
            ('内容', {
                'fields': ['content'],
            }),
            ('资料', {
                'fields': ['data'],
            }),
        )

    readonly_fields=('image_data','youtube_player','task_list_data',)


    def formatted_hit_count(self, obj):
        # print(dir(obj))
        # print(obj.hit_count_generic())
        hit_count = HitCount.objects.get_for_object(obj)
        return hit_count.hits
    #     return obj.current_hit_count() if obj.current_hit_count() > 0 else '-'
    # formatted_hit_count.admin_order_field = 'hit_count'
    # formatted_hit_count.short_description = 'Hits'




    def image_data(self, obj):
        return mark_safe(f'<img width="100px" class="list_img_article_img" src="{obj.article_img}">')


    def youtube_player(self, obj):
        return SafeText(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{obj.youtube_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>')
 
 

    def task_list_data(self, obj):
        """
        跳转到post对应的提示词列表
        """
        try:
            url = reverse('prompt_task_post_list', args=[obj.id])
            return mark_safe(f'<a href="{url}">提示列表</a>')
        except:
            return mark_safe(f'')
 
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMartorWidget
        },
    }








#
#    def make_published(self, request, queryset):
#        # 设为发布
#        queryset.update(publish_status='published')
#
#
#
#
#    def make_published(self, request, queryset):
#        # 设为发布
#        queryset.update(publish_status='published')
#






admin.site.register(Post, PostAdmin)

class AmazonSettingsAdmin(SingletonModelAdmin):
    # form = ConfigurationForm):
    # form = ConfigurationForm
    # list_display = ('site_title', 'maintenance_mode')
    # 编辑页面字段定制
    # fieldsets = [
    #     ("Base information", {
    #         'fields': [
    #             'store_id'
    #         ]
    #     }),
       
    # ]
    pass
# 注册配置页面
admin.site.register(AmazonSettings, AmazonSettingsAdmin)




class PostSettingsAdmin(SingletonModelAdmin):
    """
    Post 相关设置信息 后台管理页面
    
    """
    # form = ConfigurationForm):
    # form = ConfigurationForm
    # list_display = ('site_title', 'maintenance_mode')
    # 编辑页面字段定制
    # fieldsets = [
    #     ("Base information", {
    #         'fields': [
    #             'store_id'
    #         ]Post
    #     }),
       
    # ]
    pass
# 注册配置页面
admin.site.register(PostSettings, AmazonSettingsAdmin)






# class PostAdmin(MarkdownxModelAdmin):
#     list_display = ('title', 'created_on')
#     pass
# # admin.site.register(Post, PostAdmin)
# admin.site.register(Post, PostAdmin)
