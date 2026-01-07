from django.utils import timezone as dj_timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Product, Review
from django.http import JsonResponse
from django.views import View
from kaizen_app.forms import ContactForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_reviews = self.object.reviews.count()
        context['reviews'] = self.object.reviews.all()[:4]
        context['total_reviews'] = min(total_reviews, 20)

        return context


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



class SubmitReviewView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if request.user.is_authenticated:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')  

            Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )

        return redirect('product-detail', pk=pk)


class LoadMoreReviewsView(View):
    def get(self, request, pk):
        offset = int(request.GET.get('offset', 0))
        LIMIT = 4
        MAX_REVIEWS = 20

        total_reviews = Review.objects.filter(product_id=pk).count()
        remaining_allowed = max(0, MAX_REVIEWS - offset)
        load_count = min(LIMIT, remaining_allowed)

        reviews = Review.objects.filter(product_id=pk)\
            .order_by('-created_at')[offset:offset + load_count]

        data = []
        for review in reviews:
            data.append({
                'username': review.user.userprofile.username,
                'image': review.user.userprofile.image.url if hasattr(review.user, 'userprofile') else '',
                'rating': review.rating,
                'message': review.comment,
            })

        return JsonResponse({
            'reviews': data,
            'loaded_count': offset + len(data),
            'total_reviews': min(total_reviews, MAX_REVIEWS),
            'has_more': offset + len(data) < min(total_reviews, MAX_REVIEWS)
        })