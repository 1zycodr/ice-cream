from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from web import models, forms
from django.contrib.auth import views
from django.views import View


class UserLoginView(views.LoginView):
    template_name = 'login.html'


class UserLogoutView(views.LogoutView):
    next_page = 'index'


class UserRegisterView(generic.FormView):
    form_class = forms.UserRegistrationForm
    template_name = 'register.html'
    success_url = 'success_register'

    def form_valid(self, form):
        form.save(commit=True)
        return super().form_valid(form)


class SuccessRegisterView(generic.TemplateView):
    template_name = 'success_register.html'


class IndexView(generic.ListView):
    template_name = 'index.html'
    model = models.Product
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.cart_set.last() is None:
                models.Cart.objects.create(
                    user=request.user
                )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'categories': models.Category.objects.all()
        })
        return context


class OrderView(generic.ListView):
    template_name = 'orders.html'
    model = models.Order
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.Order.objects.filter(
                user=self.request.user,
            )


class ProductView(generic.ListView):
    template_name = 'product.html'
    model = models.Product
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        qs = super().get_queryset()

        category = self.request.GET.get('category')

        if category is not None:
            if models.Category.objects.filter(pk=category).exists():
                qs = qs.filter(category_id=category)
            else:
                qs = []

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'categories': models.Category.objects.all()
        })
        return context


class ProductCreateView(generic.CreateView):
    template_name = 'product_create.html'
    model = models.Product
    form_class = forms.ProductCreateForm

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.pk})


class ProductDetailView(generic.DetailView):
    template_name = 'product_detail.html'
    model = models.Product
    queryset = models.Product.objects.all()


class ProductUpdateView(generic.UpdateView):
    template_name = 'product_update.html'
    model = models.Product
    form_class = forms.ProductCreateForm

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(generic.DeleteView):
    model = models.Product
    success_url = '/products'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CartView(generic.DetailView):
    model = models.Cart
    template_name = 'cart.html'


class AddToCartView(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            from_url = request.GET.get('from')
            product = request.GET.get('product')

            if product is None:
                return HttpResponseRedirect(reverse('index'))

            cart = request.user.cart_set.last()
            if cart is None:
                cart = models.Cart.objects.create(user=request.user)

            cart_product, created = models.CartProduct.objects.get_or_create(
                product_id=product,
                cart=cart,
            )

            if not created:
                cart_product.quantity += 1
                cart_product.save()

            cart.total_price += cart_product.product.price
            cart.save()

            if from_url is None:
                return HttpResponseRedirect(
                    reverse('cart', kwargs={'pk': cart.pk})
                )
            else:
                from_url, id = from_url.split(',')
                return HttpResponseRedirect(
                    reverse(from_url, kwargs={'pk': id} if id else None)
                )
        else:
            return HttpResponseRedirect(reverse('login'))


class RemoveFromCartView(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            from_url = request.GET.get('from')
            product = request.GET.get('product')

            if product is None:
                return HttpResponseRedirect(reverse('index'))

            cart = request.user.cart_set.last()
            if cart is None:
                cart = models.Cart.objects.create(user=request.user)

            cart_product = models.CartProduct.objects.get(
                product_id=product,
                cart=cart,
            )

            cart.total_price -= cart_product.product.price
            cart.save()

            cart_product.quantity -= 1

            if cart_product.quantity == 0:
                cart_product.delete()
            else:
                cart_product.save()

            if from_url is None:
                return HttpResponseRedirect(
                    reverse('cart', kwargs={'pk': cart.pk})
                )
            else:
                from_url, id = from_url.split(',')
                return HttpResponseRedirect(
                    reverse(from_url, kwargs={'pk': id} if id else None)
                )
        else:
            return HttpResponseRedirect(reverse('login'))


class SaveOrderView(View):

    @staticmethod
    def post(request):
        if request.user.is_authenticated:
            cart = request.POST.get('cart')
            address = request.POST.get('address')

            order = models.Order.objects.create(
                cart_id=cart,
                address=address,
                user=request.user
            )

            models.Cart.objects.create(
                user=request.user
            )

            return HttpResponseRedirect(reverse(
                'order-details', kwargs={'pk': order.pk}
            ))
        else:
            return HttpResponseRedirect(reverse('login'))


class OrderDetailsView(generic.DetailView):
    template_name = 'order.html'
    model = models.Order
    queryset = models.Order.objects.all()
