from django import template
from tbase_post.models import Post,Link
from pprint import pprint as pp
from django.db.models import F
from django.db.models import Count
from django.views.decorators.cache import cache_control
from django.core.cache import cache
import random
from django.template.loader import render_to_string
from tbase_post.models import PostSettings
from operator import itemgetter
from django.db.models import Q

from django.template import Library, Template
from django.template import Library, Node, Template, Context

register = template.Library()



# 创建信息
# https://docs.djangoproject.com/zh-hans/4.2/howto/custom-template-tags/


@register.filter
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")


@register.simple_tag( takes_context=True)
def render_html(context,template,*args, **kwargs):
  """
  渲染模板内容为 HTML。

  使用示例
  {% render_html prompt.templ post=post prompt=prompt  %}
  {% render_html 模板 参数1=参数1 参数2=参数2  %}

  """
#   print("render_html",post)
#   pp(post)
#   pp(context)
# #   context = Context({"post":post})
#   pp(template)
  t = Template(template)
  return t.render(context)




# 生成亚马逊推广的banner链接
@register.filter
@register.inclusion_tag("post/extras/amazon_link.html", takes_context=False)
def amazon_link(product_id=None,product_name=None,store_id=None, *args, **kwargs):
    """
     生成亚马逊推广的banner链接


    """
    return {
        "product_id":product_id,
        "store_id":store_id,
        "product_name":product_name,
        # "link": f"/post/amz/{product_id}/" 
           "link":  f"https://www.amazon.com/dp/{product_id}/?tag={store_id}" 
    }





# 生成亚马逊推广的banner链接
@register.filter
@register.inclusion_tag("post/extras/amazon_ads.html", takes_context=False)
def amazon_ads(product_id=None,product_name=None,store_id=None, *args, **kwargs):
    """
     生成亚马逊推广的banner链接


    """
    return {
        "product_id":product_id,
        "store_id":store_id,
        "product_name":product_name,
        # "link": f"/post/amz/{product_id}/" 
           "link":  f"https://www.amazon.com/dp/{product_id}/?tag={store_id}" 
    }
# 生成亚马逊推广的banner链接
@register.simple_tag(takes_context=False)
# @register.inclusion_tag("post/extras/amazon_link.html", takes_context=False)
def amazon_base_link(product_id=None,product_name=None,store_id=None, *args, **kwargs):
    """
     生成亚马逊推广的banner链接


    """
    return f"https://www.amazon.com/dp/{product_id}/?tag={store_id}" 
    # return f"/post/amz/{product_id}/" 
def tags_with_count(tags):
    """
    将标签数量添加到每个标签对象中
    """
    key = "-".join(list(tags.slugs()))
    key=f'tags_with_count_{key}'
    # print("key",key)
    tags_with_count_dict= cache.get(key)
    if tags_with_count_dict is not None:
        return tags_with_count_dict


    # if cache.get(key)
    # 查询每个标签及其数量
    # tags_with_count = tags.through.objects.values('tag__name').annotate(count=Count('tag__name'))

    tags_with_count= cache.get('tags_with_count') 
    if tags_with_count is None:
        tags_with_count = tags.through.objects.values('tag__pk').annotate(count=Count('tag__pk'))
        # print("tags_with_count",tags_with_count)
        cache.set('tags_with_count',tags_with_count, 60*60*24)

    # 将标签数量添加到每个标签对象中
    # tags = [{"tag__name":tag['tag__name'], "count":tag['count']} for tag in tags_with_count]
    # print("tags", context)
    # tags_with_count
    tags_with_count_dict = {}
    for tag in tags_with_count:
        tags_with_count_dict[tag['tag__pk']]=tag['count']
    
    cache.set(key,tags_with_count_dict, 60*60*24)
    return tags_with_count_dict


# tags格式化
@register.simple_tag(takes_context=False)
def tag_names(tags, limit=5,*args, **kwargs):
    """
    获取标签的名称，限制输出个数,可以用于keyword输出
    """
    # print("tags",tags)
    # tags
    # 查询每个标签及其数量
    items_with_count=tags_with_count(tags)
    # print("tags", context)
    names=[]
    i=0
    for  item in tags.all():
        # print("item",item)
        if i>limit:
            break
        # if items_with_count[item.pk]<10:
        #     continue
        names.append(item.name)
        i=i+1
        # print("item",item)
        # print("item", item.name)
        # print("item", item.slug)
        # print("item", item.id)
        # print("item", item.get_absolute_url())
    return {"names":names,
            "names_text":",".join(names)}
    pass


# tags格式化
@register.filter
@register.inclusion_tag("post/extras/tags.html", takes_context=False)
def tags(tags,limit=5, pk=None,*args, **kwargs):
    # print("tags",tags)
    # tags
    # 查询每个标签及其数量
    items_with_count=tags_with_count(tags)
    items=[]
    i=0
    for item in  tags.all():
        if i>limit:
            break
        # if items_with_count[item.pk]<10:
            
        items.append({
            'name':item.name,
            'pk':item.pk,
            'count':items_with_count.get(item.pk),
            'object':item

        })
        i=i+1

    # print("tags", context)
    key = "-".join(list(tags.slugs()))
    return {
        "title":"Tags:",
        # "item_with_count":item_with_count,
        "items":items,
        "tags":tags,
        "pk":key #pk
        }
    pass

# 相关内容推荐
# 根据tags过滤相关内容
"""
主题模板中使用
# 加载
{% load post_extras %}

{% related_post_by_tags tags limit exclude_pk %}

{% related_post_by_tags object.tags 5 %}

"""

@register.inclusion_tag('post/extras/related_post_by_tags.html',
                        takes_context=False)
def related_post_by_tags(tags=[], limit=None,exclude_pk=None):

    config = PostSettings.get_solo()
    limit=config.related_post_limit
    try:
        # page_obj=tags.similar_objects()[-limit:]
        key = "-".join(list(tags.slugs()))
        page_obj=tags.similar_objects()[:limit]
        # slugs = list(tags.slugs())
        # # print("slugs", slugs)
        # # 排除本节点，查询相关的tags
        # if exclude_pk==None:
        #     page_obj = Post.objects.filter(tags__slug__in=slugs).order_by('-pk').distinct()[:limit]
        # else:
        #     page_obj = Post.objects.filter(tags__slug__in=slugs).exclude(
        #         pk=exclude_pk).order_by('-pk').distinct()[:limit]

        # print("page_obj", page_obj)
        return {
            'state': True,
            'link': "context['home_link']",
            'title': "Related Content",
            "page_obj": page_obj,
            "pk":key
            # "content": context
        }
    except Exception as e:
        # print(e)
        return {
            'state': False,
            'link': "context['home_link']",
            'title': "Related Content",
            "page_obj": [],
            # "content": context
        }




@register.inclusion_tag('post/extras/related_post_by_tags_mini.html',
                        takes_context=False)
def related_post_by_tags_mini(tags=[], limit=None,exclude_pk=None):

    config = PostSettings.get_solo()
    # limit=config.related_post_limit
    try:
        # page_obj=tags.similar_objects()[-limit:]
        key = "-".join(list(tags.slugs()))
        page_obj=tags.similar_objects()[:limit]

        return {
            'state': True,
            'link': "context['home_link']",
            'title': "Related Content",
            "page_obj": page_obj,
            "pk":key
            # "content": context
        }
    except Exception as e:
        # print(e)
        return {
            'state': False,
            'link': "context['home_link']",
            'title': "Related Content",
            "page_obj": [],
            # "content": context
        }




@register.inclusion_tag('post/extras/get_previous_next_by_pk.html',
                        takes_context=False)
def get_previous_next_by_pk(do_type="next",pk=0, limit=5):
    """
    关于函数get_previous_next_by_pk(do_type="previous",pk=0, limit=5)

    do_type:
    Fetches 'previous' or 'next' related posts based on primary key.
    主题模板中使用
    # 加载
    
    {% load post_extras %}

    {% get_previous_next_by_pk "previous" 10 5 %}

    {% get_previous_next_by_pk "next" 10 5 %}

    """

    try:
        # operator = Q(pk__lt=pk) if do_type == 'previous' else Q(pk__gt=pk)
        # queryset = Post.objects.filter(operator).order_by('pk')[:limit]
        if do_type == 'previous':
            operator=Q(pk__gt=pk)
            queryset = Post.objects.filter(operator).order_by('pk')[:limit]
        else:
            operator=Q(pk__lt=pk)
            queryset = Post.objects.filter(operator).order_by('-pk')[:limit]
 

        return {
            'state': True,
            # 'link': "context['home_link']",
            # 'title': "Related Content",
            "page_obj": queryset,
            "id":f"get_next_by_pk_{pk}"
            # "content": context
        }
    except Exception as e:
 
        return {
            'state': False,
            # 'link': "context['home_link']",
            # 'title': "Related Content",
            "page_obj": [],
            "id":f"get_next_by_pk_{pk}"
            # "content": context
        }



 






@register.inclusion_tag('post/extras/last_update.html',
                        takes_context=False)
def last_update( limit=5,exclude_pk=None):
    """
    
    
    """
    config = PostSettings.get_solo()
    limit=config.last_update_limit
    try:

        if exclude_pk==None:
            page_obj = Post.objects.filter(Q(publish_status="published")).order_by('-updated_on').distinct()[:limit]
        else:
            page_obj = Post.objects.filter(Q(publish_status="published")).exclude(
                pk=exclude_pk).order_by('-updated_on').distinct()[:limit]

        # print("page_obj", page_obj)
        return {
            'state': True,
            'link': "context['home_link']",
            'title': "Last Update",
            "page_obj": page_obj,
            "pk":"last_update"
            # "content": context
        }
    except Exception as e:
        # print(e)
        return {
            'state': False,
            'link': "context['home_link']",
            'title': "Last Update",
            "page_obj": [],
            "pk":"last_update"
            # "content": context
        }
    






@register.inclusion_tag('post/extras/seo_top_links.html',
                        takes_context=False)
def seo_top_links( limit=5,exclude_pk=None):
    """
    
    用于搜索优化 内部链接
    """

    try:

        page_obj = Link.objects.all().order_by('-updated_on').distinct()[:limit]
        return {
            'state': True,
            'link': "context['home_link']",
            'title': "Top Links",
            "page_obj": page_obj,
            "pk":"seo_top_links"
            # "content": context
        }
    except Exception as e:
        # print(e)
        return {
            'state': False,
            'link': "context['home_link']",
            'title': "Top Links",
            "page_obj": [],
            "pk":"last_updseo_top_linksate"
            # "content": context
        }
    






@register.inclusion_tag('post/extras/hitcount_top_post.html',
                        takes_context=False)
def hitcount_top_post( limit=5,base_id=0,exclude_pk=None):
    """
    
    用于搜索优化 内部链接 固定优化，基于现有的流量统计
    优化top limit*10以内的链接
    """

    try:

        bid=base_id%10
        page_obj = Post.objects.all().order_by('-hit_count_generic__hits').distinct()[bid*limit:(bid+1)*limit]
        # i=4
        # page_obj = list(filter(lambda x: x % 10 == i, page_obj))
        
        # [:limit]
        return {
            'state': True,
            'link': "context['home_link']",
            'title': "Hot",
            "page_obj": page_obj,
            "pk":"hitcount_top_post"
            # "content": context
        }
    except Exception as e:
        # print(e)
        return {
            'state': False,
            'link': "context['home_link']",
            'title': "Hot",
            "page_obj": [],
            "pk":"hitcount_top_post"
            # "content": context
        }
    



@register.inclusion_tag('post/extras/hitcount_lowest_post.html',
                        takes_context=False)
def hitcount_lowest_post( limit=5,base_id=0,exclude_pk=None):
    """
    
    用于搜索优化 内部链接 固定优化，基于现有的流量统计
    优化访问最低的内容 limit*10以内的链接
    """

    try:

        bid=base_id%10
        page_obj = Post.objects.all().order_by('hit_count_generic__hits').distinct()[bid*limit:(bid+1)*limit]
        # i=4
        # page_obj = list(filter(lambda x: x % 10 == i, page_obj))
        
        # [:limit]
        return {
            'state': True,
            'link': "context['home_link']",
            'title': "Explore",
            "page_obj": page_obj,
            "pk":"hitcount_lowest_post"
            # "content": context
        }
    except Exception as e:
        # print(e)
        return {
            'state': False,
            'link': "context['home_link']",
            'title': "Explore",
            "page_obj": [],
            "pk":"hitcount_lowest_post"
            # "content": context
        }
    



# 生成亚马逊推广的banner链接
@register.filter
@register.inclusion_tag("post/extras/youtube_player.html", takes_context=False)
def youtube_player(youtube_id=None,product_name=None,store_id=None, *args, **kwargs):
    """
     生成亚马逊推广的banner链接


    """

    
    return {
        "youtube_id":youtube_id,
        # "store_id":store_id,
        # "product_name":product_name,
        "link":f"https://www.youtube-nocookie.com/embed/{youtube_id}",
    }
