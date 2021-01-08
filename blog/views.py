from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.models import Post,Comments
from django.urls import reverse_lazy
from blog.forms import PostForm,CommentsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)


class AboutView(TemplateView):
    template_name='about.html'


class PostListView(ListView):
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class MyPostsView(ListView):
    template_name='my_posts.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model=Post


# class CreatePostView(LoginRequiredMixin,CreateView):
#     login_url='/login/'
#     redirect_field_name='blog/post_detail.html'
#     form_class=PostForm
#     model=Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class=PostForm
    model=Post


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).filter( published_date__isnull=True).order_by('created_date')




###############################################################################################
###############################################################################################

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)



@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method== 'POST':
        form=CommentsForm(request.POST)
        if form.is_valid():
            comments=form.save(commit=False)
            comments.post=post
            comments.save()
            return redirect('post_detail',pk=pk)   
    else:
        form=CommentsForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    # print(pk)
    comment=get_object_or_404(Comments,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comments,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)




def CreatePostView(request): 
    form = PostForm(request.POST or None, request.FILES or None) 
    if request.method =='POST': 
          
        if form.is_valid(): 
              
            obj = form.save(commit = False) 
            obj.author = request.user; 
            obj.save() 
            form = PostForm()  
            return redirect('post_detail',obj.pk)
          
    return render(request, 'post_form.html', {'form':form}) 

