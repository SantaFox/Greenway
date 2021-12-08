from django import template
from django.urls import reverse
from products.views import *

register = template.Library()

# https://djangosnippets.org/snippets/10420/


@register.filter
def get_model_name(obj):
    return obj._meta.model_name


@register.filter
def internal_links(value):
    """
    Takes a markdown textfield, and searches for internal links in the format:

    {{film:alien-1979}}

    ...where "film" is the designation for a model,
    and "alien-1979" is the slug for a given object

    NOTE: Process BEFORE markdown

    If it is inside a markdown link,
    it will resolve with the link text as intended:

    [the first Alien movie]({{film:alien-1979}})
    [the first Alien movie](/cinedex/film/alien-1979/)

    If it is by itself, it will resolve to a linked name:

    {{film:alien-1979}}
    [Alien (1979)](/cinedex/film/alien-1979/)

    :param value:
    :return:
    """
    try:
        import re

        # Pattern(s) inside a markdown link first
        # e.g. [link text here]({{film:alien-1979}})
        pattern = '\[.+\]\({{\S+:\S+}}\)'
        p = re.compile(pattern)
        text_linked = p.sub(localurl_markdown, value)

        # After we replace those, find pattern(s) by itself
        # e.g. {{film:alien-1979}}
        pattern = '{{\S+:\S+}}'
        p = re.compile(pattern)
        # replace the captured pattern(s) with the new markdown link
        return p.sub(localurl, text_linked)
    except:
        # Link lookups fail individually, but just in case there's
        # some massive failure, just display the original text
        return value


def localurlpattern(string):
    # Strip off the {{ and }}
    string = string[2:-2]
    # Separate the link type and the slug
    link_type, link_slug = string.split(":")

    # figure out what view we need to display for the link_type
    # Dictionary contains lookup as - link_type: viewname
    # "viewname can be a string containing the Python path to the view object, a URL pattern name, or the callable view object."
    # see https://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse
    link_types_views = {
        'film':     'film_detail',
        'person':   'person_detail',
        'company':  'company_detail',
        'term':     'term_detail',
    }

    # TODO: Maybe add error handling for a bad link_type, and try to look it up anyway
    link_url = reverse(link_types_views[link_type], args=(link_slug,))
    entity = get_object_or_404(Entity, slug=link_slug)
    if link_type == 'film':
        # If it's a film, the name should be in italics and include the year.
        link_name = "*" + entity.name + "* (" + str(entity.release_date.year) + ")"
    else:
        link_name = entity.name

    # Return name and link_url as part of a dictionary
    link_dict = {'name': link_name, 'url': link_url}
    return link_dict


def localurl(match):
    string = match.group()

    try:
        link_dict = localurlpattern(string)
        markdown_link = "[" + link_dict['name'] + "](" + link_dict['url'] + ")"
        return markdown_link

    except:
        # The lookup has failed, so let's send back a notice that it's broken
        print('Broken internal_links localurl to ' + string)
        markdown_link = "[***[broken link to " + string[2:-2] + "]***](#" + string[2:-2] + ")"
        return markdown_link


def localurl_markdown(match):
    string = match.group()
    markdown_link = ""
    # Grab the link text and link pattern
    p_obj = re.search(r'\[(.+)\]\(({{\S+:\S+}})\)', string)

    try:
        if p_obj:
            link_dict = localurlpattern(p_obj.group(2))
            markdown_link = "[" + p_obj.group(1) + "](" + link_dict['url'] + ")"
        return markdown_link

    except:
        # The lookup has failed, so let's send back a notice that it's broken
        print('Broken internal_links localurl_markdown to ' + string)
        if p_obj:
            markdown_link = "[" + p_obj.group(1) + " ***[broken link to " + p_obj.group(2)[2:-2] + "]***](#" + p_obj.group(2)[2:-2] + ")"
            return markdown_link
        else:
            return string
