from django.db import models
from kira.settings import SHORTCODE_MAX,SHORTCODE_MIN
from .util import create_shortcode
from .validators import validate_url,validate_dot_com
from django_hosts.resolvers import reverse
class KirrUrlManager(models.Manager):
    def all(self,*args,**kwargs):
        qs_main=super(KirrUrlManager,self).all(*args,**kwargs)
        qs=qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self):
        qs=KirrUrl.objects.filter(id__gte=1)
        new_codes =0
        for q in qs:
            q.shortcode=create_shortcode(q)
            print(q.shortcode)
            q.save()
            new_codes += 1
        return "New Codes made:{i}".format(i=new_codes)


class KirrUrl(models.Model):
    url=models.CharField(max_length=220,validators=[validate_url,validate_dot_com])
    shortcode=models.CharField(max_length=SHORTCODE_MAX,blank=True)
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)

    objects=KirrUrlManager()

    def save(self,*args,**kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        super(KirrUrl,self).save(*args,**kwargs)

    def __str__(self):
        return str(self.url)#theis is what get displayed in shortener page

    def get_short_url(self):
        print(self.shortcode)
        url_path = reverse("scode",kwargs={'shortcode':self.shortcode},host='www',scheme='http')
        return  url_path
