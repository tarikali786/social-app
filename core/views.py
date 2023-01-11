from django.shortcuts import render,redirect
from .models import Profile,Post,LikePost,FollowersCount
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from itertools import chain
from django.db.models import Q
import random
# Create your views here.




@login_required(login_url='signin')
def index(request):
  
    # get information of  currently login User
    user_object = User.objects.get(username = request.user.username) #here you get user information by username
    
    # user_object + User.objects.get(id= request.user.id) #here you get user information by id same as you can get password and email

    user_profile = Profile.objects.get(user = user_object)
    
    user_following_list =[]
    feed =[]
    
    user_following = FollowersCount.objects.filter(user =request.user.username)
    for users in user_following:
        user_following_list.append(users.user) 
    
    for username in user_following_list:
        feed_lists = Post.objects.filter(user=username)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))
    # get all user
    all_user = User.objects.all()
    user_following_all=[]
    for user in all_user:
        user_list = User.objects.get(username=user.username)
        user_following_all.append(user_list)
    
    new_sugggestions_list = [x for x in list(all_user) if (x not in list(user_following_all)) ]   
    current_user = User.objects.filter(username=request.user.username)  
    final_suggestion_list = [x for x in list(new_sugggestions_list) if (x not in list(current_user) )]
    random.shuffle(final_suggestion_list)
    username_profile = []
    user_profile_list =[]
    
    for users in final_suggestion_list:
        username_profile.append(user.id)
    
    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user = ids)
        user_profile_list.append(profile_list)
    
    suggestions_username_profile_list  = list(chain(*user_profile_list))
    # see all post images/files
    posts = Post.objects.all()
    return render(request,'core/index.html',{'user_profile':user_profile,'posts':posts,'feed_list':feed_list,
                                             'user_profile':user_profile,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            bio = request.POST.get('bio')
            image = request.FILES.get('image')
            location = request.POST.get('location')
            
            
            # save data/userprofile in database 
            user_profile.profileimg = image
            
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            
            # save data/userprofile in database 
            user_profile.profileimg = image 
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()  
        return redirect('/')    
            
    return render(request,'core/setting.html',{'user_profile':user_profile})


@login_required(login_url='signin')
def likePost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id,username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.like_post_username = username
        
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
        
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()    
        return redirect('/')

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST":
        user = request.user.username
        
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')
        
        new_post = Post.objects.create(user = user,image =image,caption=caption)
        new_post.save()
        return redirect('/')
    
    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    
    if request.method == "POST":
        username = request.POST.get('username')
        username_objects = User.objects.filter(username__icontains=username)
        
        username_profile = []
        username_profile_list = []
        for users in username_objects:
            username_profile.append(users.id)
            
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user = ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
        
    return render(request,'core/search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})

@login_required(login_url='signin')
def profile(request,pk):
    user_object = User.objects.get(username =pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts =  Post.objects.filter(user = pk)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk
    
    if FollowersCount.objects.filter(user=user, follower=follower).first():
        button_text = 'Unfollow'
    else:
        button_text  = 'Follow'    
    
    user_followers = len(FollowersCount.objects.filter(user =pk))
    user_following = len(FollowersCount.objects.filter(follower = pk))
    
    # follower_count = len(follow_count)  
      
    context = {'user_object':user_object,
               'user_profile':user_profile,
               'user_posts':user_posts,
               'user_post_length':user_post_length,
               'button_text':button_text,
               'user_followers':user_followers,
               'user_following':user_following
               }
    return render(request,'core/profile.html',context)

@login_required(login_url='signin')
def follow(request):
    if request.method == "POST":
        follower = request.POST.get('follower')
        user = request.POST.get('user')
        if FollowersCount.objects.filter(user=user,follower=follower).first():
            delete_follower = FollowersCount.objects.get(user=user,follower=follower)
            delete_follower.delete()
            return redirect('/profile/'+user)
        
        else:
            new_follower = FollowersCount.objects.create(user=user,follower = follower)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')    
    
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request,'email already exists')
                return render(request,'core/signup.html') 

            elif User.objects.filter(username = username).exists():
                messages.info(request,'Username already exists')
                return render(request,'core/signup.html') 
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                # login user
                user = auth.authenticate(username=username,password=password)
                auth.login(request,user)
                # create Profile for the login user
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model,id_user= user_model.id)
                new_profile.save()
                return redirect('settings') 
        else:
            messages.info(request,'Password not matching')   
            return redirect(request,'core/signup.html') 
            
    return render(request,'core/signup.html')

def signin(request):
    # page='login'
    # if request.user.is_authenticated:
    #     return redirect ('home')
    
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except :
            messages.error(request,'User does not exit')  
        
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)    
            return redirect('/')
        else:
            messages.error(request,'email/username or password does not exit')  
            
    # context={'page':page}
    return render(request,'core/signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

