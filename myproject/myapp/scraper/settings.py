import os, sys


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 
                      "myproject.settings")
# sys.path.insert(0, os.path.join(PROJECT_ROOT, "../../.."))

BOT_NAME = 'myapp'

SPIDER_MODULES = ["dynamic_scraper.spiders",
                  "myapp.scraper",]
USER_AGENT = "%s/%s" % (BOT_NAME, '1.0')


ITEM_PIPELINES = {
    # 'dynamic_scraper.pipelines.DjangoImagesPipeline': 300,
    'myapp.scraper.pipelines.MyImagesPipeline': 300,
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'myapp.scraper.pipelines.DjangoWriterPipeline': 800,
}

IMAGES_STORE = os.path.join(PROJECT_ROOT, '../thumbnails')

IMAGES_THUMBS = {
    'small': (170, 170),
}
