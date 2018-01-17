# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.utils.misc import md5sum

class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s/%s' % (request.meta['subdir'], image_guid)

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            image_url = 'http:{0}'.format(image_url) if 'http:' not in image_url else image_url
            yield scrapy.Request(url=image_url, meta={'subdir': item['title']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_urls'] = image_paths
        return item

    def check_gif(self, image):
        if image.format == 'GIF':
            return True
        # The library reads GIF87a and GIF89a versions of the GIF file format.
        return image.info.get('version') in ['GIF89a', 'GIF87a']

    def persist_gif(self, path, data, info):
        root, ext = os.path.splitext(path)
        path = '%s.gif' % path
        absolute_path = self.store._get_filesystem_path(path)
        self.store._mkdir(os.path.dirname(absolute_path), info)
        f = open(absolute_path, 'wb')   # use 'b' to write binary data.
        f.write(data)

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            if path.startswith('full') and self.check_gif(image):
                # Save gif from response directly.
                self.persist_gif(path, response.body, info)
            else:
                self.store.persist_file(path, buf, info, meta={'width': width, 'height': height}, headers={'Content-Type': 'image/jpeg'})
        return checksum