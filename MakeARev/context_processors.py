from reviews.models import Category, Brand


def navbar_data(request):
    #if request.user.is_authenticated:
    categories = Category.objects.all()
    brands = Brand.objects.all()
    return {'categories': categories, 'brands': brands}