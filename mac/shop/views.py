from django.shortcuts import render
from django.db import models
from .models import product,Order, OrderUpdate,Contact
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
#from PayTm import Checksum
#import PaytmChecksum
MERCHANT_KEY = 'Your-Merchant-Key-Here'

# Create your views here.
from django.http import HttpResponse


def index(request):
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower() :
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds, 'msg' : ""}
    if len(allProds) == 0 :
        params = {'msg': "please make sure to spell correctly"}

    return render(request, 'shop/search.html', params)


def aboutus(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method=="POST":
        print(request)
        name= request.POST.get('name', '')
        email= request.POST.get('email', '')
        phone= request.POST.get('phone', '')
        desc= request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, "shop/contact.html" , {'thank': thank})


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps( {"status":"success", "updates": updates, "itemJson" :  order[0].items_json} , default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')


    return render(request, 'shop/tracker.html')

def productViews(request, myid):
    # Fetch the product using the id
    Product = product.objects.filter(id=myid)
    return render(request, 'shop/productView.html', {'product':Product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        orders = Order(items_json=items_json, name=name, email=email, address=address, city=city,state=state, zip_code=zip_code, phone=phone, amount=amount)
        orders.save()
        update = OrderUpdate(order_id=orders.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = orders.order_id
        #return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        #request paytm to transfer the amount to your account after payment by user
        param_dict={

            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(Order.Order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
       # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
        
    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    # here paytm send you post request
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
