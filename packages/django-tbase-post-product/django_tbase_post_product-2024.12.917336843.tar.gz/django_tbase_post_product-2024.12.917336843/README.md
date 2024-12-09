# django-expand/tbase_post_product

用于产品的文章模块



安装
```bash
pip install django-tbase-post-product
```

```python
# settings.py
 INSTALLED_APPS = [   # 个人应用
     # 基本配置
    # 'tbase_page',
    'tbase_config',
    'tbase_theme_tailwind',
    
    'tbase_post',
    # 'markdownx'
    'martor',
    'taggit',

 ]
```


## 更新
- 2024/05/9
优化内部链接，增加相关链接和上下文链接
- 2024/05/1
注销掉底部广告（banner-amazon-footer）


- 2024/04/13
优化展示

- 2024/03/13
添加post对应提示词列表，添加对应跳转

- 2024/03/12
添加提示词生成


- 2024/02/26
添加低频率链接推荐
修改缓存时间
修改展示链接数目


- 2023/12/22
添加热门链接


- 2023/12/02
添加发布状态字段

- 2023/07/07
加入更新时间,排序默认使用更新时间

- 2023/06/05
优化相关内容查询,模板文件,针对tags内容数目低于10的链接添加nofollow。


- 2023/06/02
加入seo优化，对tags内容过少（小于10）的页面添加noindex






## Getting Started

Download links:

SSH clone URL: ssh://git@git.jetbrains.space/terrychanorg/django-expand/tbase_post_product.git

HTTPS clone URL: https://git.jetbrains.space/terrychanorg/django-expand/tbase_post_product.git



These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

What things you need to install the software and how to install them.

```
Examples
```

## Deployment

Add additional notes about how to deploy this on a production system.

## Resources

Add links to external resources for this project, such as CI server, bug tracker, etc.
