from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.views import View
# Create your views here.
from analytics.models import ClickEvent
from .models import KirrUrl
from .forms import SubmitUrlForm
#def kirr_redirect_view(request,shortcode,*args,**kwargs):
#    obj=get_object_or_404(KirrUrl,shortcode=shortcode)
    #return HttpResponse("hello {sc}".format(sc=obj.url))
#    return HttpResponseRedirect(obj.url)

class HomeView(View):
    def get(self,request,*arg,**kwargs):
        the_form=SubmitUrlForm()
        context = {
        "title":"Kirr.co",
        "form":the_form
        }
        return render(request,"shortener/home.html",context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "Kirr.co",
            "form": form
        }
        template = "shortener/home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = KirrUrl.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already_exists.html"

        return render(request, template ,context)


class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = KirrUrl.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        #ClickEvent.objects.create_event(obj)
        return HttpResponseRedirect(obj.url)
