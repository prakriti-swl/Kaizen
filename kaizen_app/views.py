from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Product
from django.http import JsonResponse
from django.views import View
from kaizen_app.forms import ContactForm

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"
    
class IntroView(TemplateView):
    template_name = "home/intro.html"

    def intro(request):
        return render(request, 'home/intro.html')
    
class AboutView(TemplateView):
    template_name = "about.html"

    def about(request):
        return render(request, 'about.html')
    
class ContactView(View):
    template_name = "contact.html"

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "Message sent successfully!"})
        else:
            # Collect missing fields
            missing_fields = [field for field in form.errors]
            message = "Message wasn't sent. Please fill: " + ", ".join(missing_fields)
            return JsonResponse({"status": "error", "message": message})
    
class ServicesView(TemplateView):
    template_name = "home/services.html"

    def services(request):
        return render(request, 'home/services.html')
    
class BlogView(TemplateView):
    template_name = "home/blog.html"

    def blog(request):
        return render(request, 'home/blog.html')
    
class BlogSingleView(TemplateView):
    template_name = "home/blog-single.html"

    def blog_single(request):
        return render(request, 'home/blog-single.html')
    

class ShopView(TemplateView):
    template_name = "shop.html"

    def shop(request):
        return render(request, 'shop.html')


class ProductListView(ListView):
    model = Category
    template_name = 'products.html'
    context_object_name = 'categories'

    # Prefetch related products for efficiency
    def get_queryset(self):
        return Category.objects.prefetch_related('products').all()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

