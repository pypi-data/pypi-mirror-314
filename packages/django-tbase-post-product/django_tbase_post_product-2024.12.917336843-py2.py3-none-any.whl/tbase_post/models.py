from django.db import models
import django
# Create your models here.

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

# from markdownfield.models import MarkdownField, RenderedMarkdownField
# from markdownfield.validators import VALIDATOR_STANDARD
# from markdownx.models import MarkdownxField
from martor.models import MartorField
from taggit.managers import TaggableManager
from solo.models import SingletonModel

from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
 
from django.db import models


class Prompt(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    prompt_text = models.TextField("提示文本")
    templ = models.TextField(
        "模板文件",
        default="""
            {{ post.data | safe }} 
            ---
            {{ prompt.prompt_text }} 

        """,
        help_text="""
模板文件可以使用 Jinja2 语法编写。

以下是一个示例模板：

```
资料

{{ post.data | safe }} 
---
提示词
{{ prompt.prompt_text }}
```

可以使用以下变量：

post包含Post字段
prompt包含当前提示词内容

        """,
    )

    def __str__(self):
        return self.title



class PromptTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    prompts = models.ManyToManyField(Prompt, 
                                     through='PromptTaskPrompt',
                                    #  default=[1]
                                     )
    
    def __str__(self):
        return f"{self.pk} : {self.title}"



class PromptTaskPrompt(models.Model):

    prompt_task = models.ForeignKey(PromptTask, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.prompt_task} - {self.prompt}"

 

 
class Link(models.Model):
    title =  models.CharField("标题",max_length=255,)
    url = models.URLField("URL",max_length=255, default='', null=True, blank=True)
    updated_on = models.DateTimeField("更新时间",auto_now=True)
    
    def __str__(self):
        return self.title
    
class Post(models.Model):
    title = models.CharField("标题",max_length=255,)
    # slug = models.SlugField(
    #     unique=True,
    #     max_length=255,
    # )
    # content = models.TextField()
    content = MartorField("内容")
    PUBLISH_STATUS_CHOICES = [
        ('published', '发布'),
        ('draft', '草稿'),
        ('trash', '垃圾桶'),
    ]
    publish_status = models.CharField(max_length=10,choices=PUBLISH_STATUS_CHOICES,default='published')


    created_on = models.DateTimeField("创建时间",auto_now_add=True)
    updated_on = models.DateTimeField("更新时间",auto_now=True)
    article_img = models.CharField("图片",
                           max_length=255,
                           blank=True,
                           help_text="""
                           可以将图片上传到https://box.maomihezi.com/

                            不要填写?x-oss-process=style/mini_auto，用于后期自动处理图片
                           """
                           )
    product_name = models.CharField("推广产品名字",
                           max_length=255,
                           blank=True,
                           help_text="""
                           产品名 便于
                           """
                           )

    product_id = models.CharField("推广产品id",
                           max_length=255,
                           blank=True,
                           help_text="""填写亚马逊的产品id，用于产生产品链接,
                           比如：https://www.amazon.com/Audio-Wireless-Bluetooth-Earbuds-Charging/dp/B07R7DT3JV/
                           id则为B07R7DT3JV
                           
                           """
                           )
    youtube_id = models.CharField("Youtube id",
                           max_length=64,
                           blank=True,
                           help_text="""youtube视频id
                           
                           """
                           )
    # author = models.TextField()
    # text = MarkdownField(rendered_field='text_rendered', use_editor=False, use_admin_editor=True,validator=VALIDATOR_STANDARD)
    # text_rendered = RenderedMarkdownField(default='')
    tags = TaggableManager("标签")
    meta_keywords = models.CharField("meta keywords",
                           max_length=128,
                           blank=True,
                           help_text="""
                            关键词,用于搜索引擎优化使用,关键词使用英文逗号分割
                           """
                           )
    meta_description = models.CharField("meta description",
                           max_length=255,
                           blank=True,
                           help_text="""
                            用于搜索引擎优化使用
                           """
                           )
    data=models.TextField("背景资料",blank=True,default="")
    
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')


    def get_absolute_url(self):
        return reverse('detail_view', args=[self.pk])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = slugify(self.title)
        # self.updated_on = django.timezone.now()
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-updated_on']
        # fields=['product_id']


        def __unicode__(self):
            return self.title
        


class AmazonSettings(SingletonModel):
    """
    亚马逊推广配置页面
    """
    store_id = models.CharField("亚马逊联盟推广id",
                                    max_length=32,
                                    null=True,
                                    blank=True,
                                    default=None,
                                    help_text="""
                                    亚马逊的推广id，用于生成推广链接，可以通过https://affiliate-program.amazon.com/home 注册。
                                    
                                    """)


    ads_sidebar = models.TextField("ads_sidebar",
                                    # max_length=32,
                                    null=True,
                                    blank=True,
                                    default=None,
                                    help_text="""
                                    广告1: 右侧边栏
                                    
                                    """)

    ads_content1 = models.TextField("ads_content1",
                                    # max_length=32,
                                    null=True,
                                    blank=True,
                                    default=None,
                                    help_text="""
                                    广告2: 主要内容之后
                                    
                                    """)



    ads_list1 = models.TextField("ads_list1",
                                    # max_length=32,
                                    null=True,
                                    blank=True,
                                    default=None,
                                    help_text="""
                                    广告3:  列表广告
                                    
                                    """)


    def __str__(self):
        return "Amazon Settings"

    class Meta:
        verbose_name = "Amazon Settings"






class PostSettings(SingletonModel):
    """
    配置发布内容
    """
    last_update_limit=models.IntegerField('最后更新数目',default=10)
    related_post_limit=models.IntegerField('相关推荐数目', default=10)
    pass



    # store_id = models.CharField("亚马逊联盟推广id",
    #                                 max_length=32,
    #                                 null=True,
    #                                 blank=True,
    #                                 default=None,
    #                                 help_text="""
    #                                 亚马逊的推广id，用于生成推广链接，可以通过https://affiliate-program.amazon.com/home 注册。
                                    
    #                                 """)


    # ads_sidebar = models.TextField("ads_sidebar",
    #                                 # max_length=32,
    #                                 null=True,
    #                                 blank=True,
    #                                 default=None,
    #                                 help_text="""
    #                                 广告1: 右侧边栏
                                    
    #                                 """)

    # ads_content1 = models.TextField("ads_content1",
    #                                 # max_length=32,
    #                                 null=True,
    #                                 blank=True,
    #                                 default=None,
    #                                 help_text="""
    #                                 广告2: 主要内容之后
                                    
    #                                 """)



    # ads_list1 = models.TextField("ads_list1",
    #                                 # max_length=32,
    #                                 null=True,
    #                                 blank=True,
    #                                 default=None,
    #                                 help_text="""
    #                                 广告3:  列表广告
                                    
    #                                 """)


    def __str__(self):
        return "Post Settings"

    class Meta:
        verbose_name = "Post Settings"
