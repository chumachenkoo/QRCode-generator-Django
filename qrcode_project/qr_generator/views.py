from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import UserView, QRCodeView
from django.contrib import messages
from django.views.decorators.http import require_http_methods


@require_http_methods("GET")
def get_registration(request):
    if 'id' in request.session:
        return HttpResponseRedirect('/account')
    else:
        return render(request, 'registration.html')


@require_http_methods("POST")
def post_registration(request):
    if request.method == 'POST':
        user = UserView(username=request.POST.get('username'),
                        email=request.POST.get('email'),
                        password=request.POST.get('password'))

        if UserView.objects.filter(email=user.email):
            messages.add_message(request, messages.WARNING, 'User has been registered!')
            return render(request, 'registration.html')
        else:
            user.save()
            return HttpResponseRedirect('/get_login')

    return render(request, 'registration.html')


@require_http_methods("GET")
def get_login(request):
    if 'id' in request.session:
        return HttpResponseRedirect('/account')
    else:
        return render(request, 'login.html')


@require_http_methods("POST")
def post_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = UserView.objects.get(email=email)

        if user is not None and password == user.password:
            request.session['id'] = user.id
            return HttpResponseRedirect('/account')

    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/get_login')


def account(request):
    if 'id' in request.session:
        user_id = request.session['id']
        user = UserView.objects.get(id=user_id)
        qr = QRCodeView.decode(user=user)

        return render(request, 'account.html', {'data': user, 'qr_codes': qr})

    return HttpResponseRedirect('/get_login')


def generator(request):
    if 'id' in request.session:
        if request.method == 'POST':
            data = request.POST.get('qr_code')
            user_id = request.session['id']
            qr = QRCodeView.generate(data, user_id)
            qr.save()

            return HttpResponseRedirect('/account')
        else:
            return render(request, 'generator.html')

    return HttpResponseRedirect('/get_login')
