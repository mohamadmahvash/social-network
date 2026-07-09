from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Relation


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/User_login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in', extra_tags='success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.warning(request, 'username/password is wrong', extra_tags='warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    # login_url = "/account/login/"

    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out', extra_tags='success')
        return redirect('home:home')


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/user_register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            messages.success(request, 'Registered Successfully.', extra_tags='success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'account/user_profile.html'

    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        # because of related name
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, self.template_name, {'user': user, 'posts': posts, 'is_following': is_following})


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, f'You are already following {user.username}.', extra_tags='danger')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, f'You are now following {user.username}.', extra_tags='success')
        return redirect('account:user_profile', user_id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, f'You are unfollowing {user.username}.', extra_tags='success')
        else:
            messages.error(request, f'You are not following {user.username}.', extra_tags='danger')
        return redirect('account:user_profile', user_id)
