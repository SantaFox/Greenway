from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill


class ProductSmallThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(120, 80)]
    format = 'JPEG'
    options = {'quality': 60}


class ProductMediumThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(300, 200)]
    format = 'JPEG'
    options = {'quality': 60}


class ProductBigThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(450, 300)]
    format = 'JPEG'
    options = {'quality': 80}


class AdminThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(90, 60)]
    format = 'JPEG'
    options = {'quality': 60}


register.generator('products:product_big_thumbnail', ProductBigThumbnailSpec)
register.generator('products:product_medium_thumbnail', ProductMediumThumbnailSpec)
register.generator('products:product_small_thumbnail', ProductSmallThumbnailSpec)
