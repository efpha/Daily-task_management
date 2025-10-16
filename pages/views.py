from django.shortcuts import render, redirect


def home(req):
    #if user logged in send to dashboard
    if 'access_token' in req.session:
        return redirect('dashboard_page')
    return render(req, 'pages/home.html')

def dashboard_page(req):
    #make sure the user is logged in
    if 'access_token' not in req.session:
        return redirect('login_page')
    name = req.session.get('name', 'Guest')
    return render(req, 'pages/dashboard.html', { 'name': name})