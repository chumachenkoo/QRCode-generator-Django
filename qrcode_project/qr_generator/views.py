from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import UserView, QRCodeView


def registration(request):
    if 'id' in request.session:
        return HttpResponseRedirect('/account')

    elif request.method == 'POST':
        UserView.objects.create(username=request.POST.get('username'),
                                email=request.POST.get('email'),
                                password=request.POST.get('password'))

        return render(request, 'login.html')

    return render(request, 'registration.html')


def login(request):
    if 'id' in request.session:
        return HttpResponseRedirect('/account')

    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = UserView.objects.get(email=email)

        if user is not None and password == user.password:
            request.session['id'] = user.id
            return HttpResponseRedirect('/account')

    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return render(request, 'login.html')


def account(request):
    if 'id' in request.session:
        user_id = request.session['id']
        user = UserView.objects.get(id=user_id)
        qr = QRCodeView.decode(user=user)

        return render(request, 'account.html', {'data': user, 'qr_codes': qr})

    return render(request, 'login.html')


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

    return HttpResponseRedirect('/login')
