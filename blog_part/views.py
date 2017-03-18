from django.shortcuts import render
from django.views.generic import ListView, FormView, View, DetailView, CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .form import CommentForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 59317a9c1512716b091ae014b2f6d4553c9afc6c
# origin2

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog_part:detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog_part:detail', pk=post_pk)

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog_part:detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog_part/add_comment.html', {'form': form})


class PostList(ListView):
    
    model = Post
    template_name = 'blog_part/posts.html'
    context_object_name = 'post_list'
    paginate_by = 4
    queryset = Post.objects.all().order_by('-id')

class CommentList(ListView):
    form_class = CommentForm
    template_name = "blog_part/all_comment.html"
    queryset = Post.objects.all().order_by('-pub_date')

class LoginFormView(FormView):

    form_class = AuthenticationForm
    # Similarly registration, use authentication pattern
    template_name = "blog_part/login.html"
    # link for redirect after successful authentication

    success_url = "/"

    def form_valid(self, form):
        # Get the user object based on the entered data in the form.
        self.user = form.get_user()
        # Perform user authentication.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):

    def get(self, request):
        # Perform output for the user requesting this view.
        logout(request)
        # After that redirect the user to the main page.
        return redirect('/')


class RegisterFormView(FormView):

    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "blog_part/signup.html"

    def form_valid(self, form):
        # create user if form is valid
        form.save()
        # call the base class method
        return super(RegisterFormView, self).form_valid(form)


class ShowPost(DetailView):

    model = Post
    template_name = 'blog_part/detail.html'
    

# class AddComment(CreateView):
    
#     model = Comment
#     template_name = 'blog_part/add_comment.html'
#     form_class = CommentForm
#     # http_method_names = ['post']

#     def get_success_url(self):
#         return reverse('blog_part:detail')

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.save()        
#         return HttpResponseRedirect(self.get_success_url())