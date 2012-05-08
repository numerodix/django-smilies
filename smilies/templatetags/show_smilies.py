from os.path import abspath
from os.path import dirname
from os.path import join
import re

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from blog.models import Entry

register = template.Library()


def init_smilies():
    data_file = join(dirname(abspath(__file__)), '..', 'data', 'smilies.dat')
    lines = open(data_file).readlines()

    dct = {}
    for line in lines:
        chunks = re.split('\s+', line.strip())
        imgname = chunks[0]
        for alias in chunks[1:]:
            dct[alias] = imgname

    # sort by longest alias to match greedily
    aliases = sorted(dct, reverse=True, key=lambda a: len(a))
    rx = '(%s)' % '|'.join([re.escape(a) for a in aliases])

    # match at the start of a line or after a space
    rx = re.compile('(^|\s)' + rx)

    return dct, rx
SMILIES_DICT, SMILIES_RX = init_smilies()

@register.filter
def show_smilies(value, autoescape=None):
    def repl(match):
        alias = match.group(0).strip()
        imgname = SMILIES_DICT.get(alias) or ''
        return (' <img class="wp-smiley" src="%s">' %
                join(settings.STATIC_URL, 'smilies', imgname))

    value = SMILIES_RX.sub(repl, value)

    value = mark_safe(value)
    return value
show_smilies.is_safe = True
show_smilies.needs_autoescape = True
show_smilies = stringfilter(show_smilies)
