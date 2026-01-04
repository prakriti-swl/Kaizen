from django.urls import path
from kaizen_app import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("intro/", views.IntroView.as_view(), name="intro"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("services/", views.ServicesView.as_view(), name="services"),
    path("blog/", views.BlogView.as_view(), name="blog"),
    path("blog-single/", views.BlogSingleView.as_view(), name="blog-single"),
    path("shop/", views.ShopView.as_view(), name="shop"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path("product/<slug:slug>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("new-arrivals/", views.NewArrivalView.as_view(), name="new-arrivals"),
]