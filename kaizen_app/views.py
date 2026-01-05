from django.utils import timezone as dj_timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Product, Review
from django.http import JsonResponse
from django.views import View
from kaizen_app.forms import ContactForm, ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cutoff_date = dj_timezone.now() - timedelta(days=60)

        context['latest_products'] = Product.objects.filter(
            created_at__gte=cutoff_date
        ).order_by('-created_at')[:8]

        return context


    
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            Review.objects.update_or_create(
                product=self.object,
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment']
                }
            )

        return redirect(self.request.path)

class NewArrivalView(TemplateView):
    template_name = 'new_arrival.html'

    def get(self, request, *args, **kwargs):
        cutoff_date = dj_timezone.now() - timedelta(days=60)

        latest_products = Product.objects.filter(
            created_at__gte=cutoff_date
        ).order_by('-created_at')[:8]

        return render(request, self.template_name, {
            'latest_products': latest_products
        })



