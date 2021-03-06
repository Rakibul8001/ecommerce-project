from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, BillingAddress
from .forms import CheckoutForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 12
    template_name = "pages/home-page.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "pages/product-page.html"

# Item view by Category


class ItemCategory(ListView):
    model = Item
    template_name = "pages/home-page.html"
    paginate_by = 12

    def get_queryset(self):
        self.category = self.kwargs['category']
        return Item.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(ItemCategory, self).get_context_data(**kwargs)
        context['item_category'] = self.category
        return context


class OrderSummeryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'pages/order_summery.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order.")
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'pages/checkout-page.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                # TODO: add functionality
                # same_shipping_address = form.cleaned_data.get(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_code=zip_code
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: redirect to the selected payment options
                return redirect('core:checkout')
            messages.warning(self.request, "Failed Checkout")
            return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order.")
            return redirect("core:order-summery")


class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'pages/payment.html')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Updated This Item Quantity")
            return redirect("core:order-summery")
        else:
            order.items.add(order_item)
            messages.info(request, "This Item has Added to Your Cart")
            return redirect("core:order-summery")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This Item has Added to Your Cart")
        return redirect("core:order-summery")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.warning(request, "This Item has removed from Your Cart")
            return redirect("core:order-summery")
        else:
            messages.info(request, "This Item was not in Your Cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do no have an active order")
        return redirect("core:product", slug=slug)

# remove single item quantity


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                messages.warning(
                    request, "This Item has removed from Your Cart")
                return redirect("core:order-summery")

            messages.warning(request, "Updated Item Quantity")
            return redirect("core:order-summery")
        else:
            messages.info(request, "This Item was not in Your Cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do no have an active order")
        return redirect("core:product", slug=slug)


# Item search


class ItemSearch(ListView):
    model = Item
    template_name = "pages/home-page.html"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(ItemSearch, self).get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('query')
        return context
