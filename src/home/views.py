from django.shortcuts import render,redirect
from .models import Setting,ContactForm,ContactFormMessage,UserProfile
from product.models import Product
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout,authenticate,login
from .form import SignUpForm
from django.http import HttpResponse,HttpResponseRedirect
from order.models import ShopCart
from content.models import Content, Menu, CImages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse
from .utils import account_activation_token
from .tasks import send_email_task
from django.core.mail.backends.smtp import EmailBackend
from django.contrib import messages

def Index(request):
    current_user=request.user
    settings=Setting.objects.get(id=1)
    sliderdata = Product.objects.all()[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id= current_user.id).count()
    menu = Menu.objects.all()  # E ticaret dışı
    news = Content.objects.filter(type='haber').order_by('-id')[:2]  # E ticaret dışı
    announcement=  Content.objects.filter(type='duyuru').order_by('-id')[:2]  # E ticaret dışı
    context = {
        'settings':settings, 'sliderdata':sliderdata,'news':news,'announcement':announcement, 'page': 'home', 'menu':menu
    }
    return render(request,'home/home.html',context)
def aboutus(request):
    settings=Setting.objects.get(id=1)
    context = {
        'settings':settings,
    }
    return render(request,'home/aboutus.html',context)
  
def reference(request):
    settings=Setting.objects.get(id=1)
    context = {
        'settings':settings,
    }
    return render(request,'home/reference.html',context)

def contact(request):
   if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.save()  #save data to table
            # messages.success(request,"Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
        else:
              return HttpResponse(form.errors)   
   else:      
        form = ContactForm
        settings=Setting.objects.get(id=1)
        context={'settings':settings,'form':form  }
        return render(request, 'home/contact.html', context)
      

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password  = request.POST['password']

        user = auth.authenticate(username= username, password = password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.INFO,'Oturum açıldı.')
            return redirect('/')
        else:
            messages.add_message(request, messages.SUCCESS, 'Hatalı username yada parola')
            return redirect('login')
    else:
       
        settings=Setting.objects.get(id=1)
        context={'settings':settings }
        return render(request, 'home/login.html', context)
def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
    settings=Setting.objects.get(id=1)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():           
            form.save()
            backend = EmailBackend(host = settings.smtpserver,port= settings.smtpport, username=settings.smtpemail, password=settings.smtppassword, use_tls=True)
            email= form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)            
            current_user =user           
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/admin.png"
            data.save()
            current_site = get_current_site(request)
            email_body = {
                    'user': current_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(current_user.pk)),
                    'token': account_activation_token.make_token(current_user),
                }
               
            link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'],    
             'token': email_body['token']})
            email_subject = 'Activate your account'   
            activate_url = 'http://'+current_site.domain+link
            email = EmailMessage(
                    email_subject,
                    'Hi '+current_user.username + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [current_user.email],
                    connection=backend
                )  

            # email.send(fail_silently=False)
            send_email_task(email)
            messages.success(request, 'Lütfen emailinize gelen aktivasyon linkine tıklayınız')
            return redirect('login')    
        else:
            # messages.error(request, '')
            return HttpResponse(form.errors)        
    form = SignUpForm()
    
    context={'settings':settings, 'form': form }
    return render(request, 'home/signup.html',context)

def verification(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if not account_activation_token.check_token(user, token):
            return redirect('login'+'?message='+'User already activated')    

        if user.is_active:
            return redirect('login')
        user.is_active = True
        user.save()
    
            # messages.success(request, 'Account activated successfully')
        return redirect('login')   

    except Exception as ex:
            pass

    return redirect('login')
# Eticaret dışı
def menu(request,id):
    content=Content.objects.get(menu_id = id)
    if content:
        link =  'content/'+ str(content.d)       
        return HttpResponseRedirect(link)
    else:
        link ='/'
        return HttpResponseRedirect(link)

def contentdetail(request,id,slug):
    menu= Menu.objects.all()
    content= Content.objects.get(pk=id)
    images = CImages.objects.filter(content_id= id)
    context = {
        'menu':menu, 'content':content, 'images':images
    }
    return render(request,'content_detail.html',context)



