from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill


class ProductSmallThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(120, 80)]
    format = 'JPEG'
    options = {'quality': 60}


class ProductBigThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(450, 300)]
    format = 'JPEG'
    options = {'quality': 80}


class AdminThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(320, 240)]
    format = 'JPEG'
    options = {'quality': 60}


register.generator('products:product_big_thumbnail', ProductBigThumbnailSpec)
register.generator('products:product_small_thumbnail', ProductSmallThumbnailSpec)
