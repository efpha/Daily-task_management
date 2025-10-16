from django.shortcuts import render, redirect


def home(req):
    return render(req, 'pages/home.html')

def dashboard_page(req):
    #make sure the user is logged in
    if 'access_token' not in req.session:
        return redirect('login_page')
    return render(req, 'pages/dashboard.html')