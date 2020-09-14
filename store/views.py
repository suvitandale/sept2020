from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer

def index(request):
    prods = None
    catergory = Category.get_all_categories()
    categoryID=request.GET.get('category')
    if categoryID:
        prods = Product.get_all_products_by_categoryid(categoryID)
    else:
        prods = Product.get_all_products()
    data={}
    data['product'] = prods
    data['categories'] = catergory
    return render(request,'index.html',data)

def validate_fields(customer):
    error_msg = None
    if not len(customer.first_name)>4:
        error_msg ='please enter valid firstname'
    elif not len(customer.last_name)>4:
        error_msg ='please enter valid lastname'
    elif len(customer.phone)!=10 and customer.phone in range(7700000000,9999999999):
        error_msg = 'Please enter 10 digit valid mobile number'
    elif not len(customer.password)>6:
        error_msg = 'Password length should be greater than 6..!!'
    elif customer.isExist():
        error_msg = 'Email ID is Already Registered..!!'
    return error_msg


def signup(request):
    print(request.method)
    if request.method=='POST':
        print(request.POST)
        postdata = request.POST
        if postdata.get('password')==postdata.get('cpassword'):
            customer = Customer(first_name=postdata.get('firstname'),last_name=postdata.get('lastname'),
                                phone=postdata.get('phone'),email=postdata.get('email'),password=postdata.get('password'))
            value = {
                'firstname' : customer.first_name,
                'lastname' : customer.last_name,
                'phone' : customer.phone,
                'email' : customer.email}

            error_msg = validate_fields(customer)
            if not error_msg:
                customer.register()
                return redirect('homepage')
            data = {'value':value,'msg':error_msg}
            return render(request, 'signup.html',data)

        return HttpResponse('Please confirm password and confirm password...!!')

    return render(request,'signup.html')


