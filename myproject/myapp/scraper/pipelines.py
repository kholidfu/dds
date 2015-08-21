from django.db.utils import IntegrityError
from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime
from scrapy.contrib.pipeline.images import ImagesPipeline
from dynamic_scraper.pipelines import DjangoImagesPipeline
import os


class MyImagesPipeline(DjangoImagesPipeline):

    def __init__(self, *args, **kwargs):
        super(MyImagesPipeline, self).__init__(*args, **kwargs)

    def get_media_requests(self, item, info):
        # this is the downloader
        img_elem = info.spider.scraper.get_image_elem()
        print
        print '=============================='
        print item[img_elem.scraped_obj_attr.name]
        print '=============================='
        print
        if img_elem.scraped_obj_attr.name in item and item[img_elem.scraped_obj_attr.name]:
                if not hasattr(self, 'conf'):
                    self.conf = info.spider.conf
                return Request(item[img_elem.scraped_obj_attr.name])

    def image_key(self, url):
        print '*************************************'
        fext = os.path.splitext(os.path.basename(url))[-1]
        fname = "-".join(os.path.basename(url).split('-'))
        print '*************************************'
        return "full/%s" % fname + fext


    # def thumb_key(self, url, thumb_id):
    #     print '********************************'
    #     fext = os.path.splitext(os.path.basename(url))[-1]
    #     fname = "-".join(os.path.basename(url).split('-'))
    #     return "full/%s" % fname + fext


class DjangoWriterPipeline(object):

    def process_item(self, item, spider):
        try:
            item['news_website'] =  spider.ref_object

            checker_rt = SchedulerRuntime(runtime_type='C')
            checker_rt.save()
            item['checker_runtime'] = checker_rt

            item.save()
            spider.action_successful = True
            spider.log("Item saved.", log.INFO)

        except IntegrityError, e:
            spider.log(str(e), log.ERROR)
            raise DropItem("Missing attribute.")

        return item
