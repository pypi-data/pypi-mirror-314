from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post
from tbase_config.models import General
 
 
#from tbase_post.models import Post
 


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        # return Post.objects.all().order_by("-pk")
        return Post.objects.filter(publish_status="published").order_by("-updated_on")[:100]

    def lastmod(self, obj):
        return obj.created_on

    def location(self, obj):
        return reverse('detail_view', args=[obj.id])
        # return f"http://aa.com/detail{obj.id}"
