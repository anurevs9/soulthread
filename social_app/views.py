import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Message, Forum, ForumPost, Media, FriendRequest, Profile, Story, Suggestion, Recommendation, \
    Comment
from .forms import (
    CustomUserCreationForm, CustomLoginForm, PostForm, MessageForm,
    ForumForm, ForumPostForm, MediaUploadForm, ProfileForm, AccountForm, CommentForm, FollowUserForm
)
from rest_framework import generics, permissions, status
from .serializers import PostSerializer, CommentSerializer, ForumSerializer, ForumPostSerializer, MediaSerializer, \
    FollowUnfollowSerializer


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'social_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'social_app/login.html', {'form': form})



def home(request):
    current_year = datetime.now().year
    posts = Post.objects.all().order_by('-created_at')
    suggested_users = []
    recommended_posts = []
    stories = []

    if request.user.is_authenticated:
        user = request.user

        profile = user.profile
        following_users = profile.following.all()

        queryset = User.objects.exclude(id=user.id)


        following_ids = following_users.values_list('id', flat=True)


        queryset = queryset.exclude(id__in=following_ids)


        suggested_users = queryset[:10]




        suggested_users_list = list(suggested_users)


    else:
        print("User is NOT authenticated.")
        suggested_users_list = []


    context = {
        'posts': posts,
        'comment_form': CommentForm(),
        'stories': stories,
        'suggested_users': suggested_users_list,
        'recommended_posts': recommended_posts,
        'current_year': current_year,
    }


    return render(request, 'social_app/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def messages_view(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'social_app/messages.html', {'messages': messages})

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('messages')
    else:
        form = MessageForm()
    return render(request, 'social_app/send_message.html', {'form': form, 'receiver': receiver})

@login_required
def forums_view(request):
    forums = Forum.objects.all()
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.created_by = request.user
            forum.save()
            return redirect('forums')
    else:
        form = ForumForm()
    return render(request, 'social_app/forums.html', {'forums': forums, 'form': form})

@login_required
def forum_detail(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    posts = forum.posts.all()
    form = ForumPostForm()

    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.forum = forum
            post.user = request.user
            post.save()
            return redirect('social_app:forum_detail', forum_id=forum.id)

    return render(request, 'social_app/forum_detail.html', {'forum': forum, 'posts': posts, 'form': form})
@login_required
def friends(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    # Get the current user's profile and get all users they are following
    friends = request.user.profile.following.all()

    return render(request, 'social_app/friends.html', {
        'pending_requests': pending_requests,
        'friends': friends
    })

@login_required
def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    context = {
        'profile_user': profile_user,
    }
    return render(request, 'social_app/user_profile.html', context)


@login_required
def media(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.user = request.user
            media.save()
            return redirect('media')
    else:
        form = MediaUploadForm()
    
    user_media = Media.objects.filter(user=request.user)
    return render(request, 'social_app/media.html', {'form': form, 'media': user_media})


@login_required
def settings_view(request):
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    account_form = AccountForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if 'profile_submit' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile changes saved successfully!')
            return redirect('settings')

        if 'account_submit' in request.POST and account_form.is_valid():
            account_form.save() # Now save() in AccountForm handles password logic
            messages.success(request, 'Account changes saved successfully!')
            return redirect('settings')

    context = {
        'profile_form': profile_form,
        'account_form': account_form,
    }
    return render(request, 'social_app/settings.html', context)


@login_required
@require_POST
def like_post(request, post_id):
    print(f"like_post view called for post_id: {post_id}, user: {request.user}") # Debugging print
    post = get_object_or_404(Post, id=post_id)
    liked = False

    if request.user in post.likes.all():
        print(f"User {request.user} already liked post {post_id}, removing like") # Debugging print
        post.likes.remove(request.user)
    else:
        print(f"User {request.user} liking post {post_id}, adding like") # Debugging print
        post.likes.add(request.user)
        liked = True

    print(f"Returning JsonResponse: {{'liked': {liked}, 'likes_count': {post.likes.count()}}}") # Debugging print
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return JsonResponse({
                'status': 'success',
                'comment_id': comment.id,
                'username': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%b %d, %Y %H:%M')
            })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@require_POST
def follow_user(request):
    user_id = request.POST.get('user_id')
    if not user_id:
        return HttpResponseBadRequest("User ID is required.")

    try:
        user_id = int(user_id)
    except ValueError:
        return HttpResponseBadRequest("Invalid User ID.")

    user_to_follow = get_object_or_404(User, id=user_id)
    profile = request.user.profile

    if user_to_follow == request.user:
        return HttpResponseBadRequest("You cannot follow yourself.")

    if not hasattr(user_to_follow, 'profile'):
        return HttpResponseBadRequest("Target user does not have a profile.")

    if user_to_follow in profile.following.all():
        profile.following.remove(user_to_follow)
        user_to_follow.profile.followers.remove(request.user)
    else:
        profile.following.add(user_to_follow)
        user_to_follow.profile.followers.add(request.user)

    return redirect('home')


def toggle_follow(user, user_to_follow):
    profile = user.profile

    if user_to_follow in profile.following.all():
        profile.following.remove(user_to_follow)
    else:
        profile.following.add(user_to_follow)

def get_file_preview(file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'post_files', file_name)
    preview_text = "No preview available for this file type."

    try:
        file_extension = os.path.splitext(file_name)[1].lower()

        if file_extension in ['.txt', '.csv', '.log', '.html', '.css', '.js', '.py', '.md', '.ini', '.conf', '.sh']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    preview_text = f.read(500)
                    if len(preview_text) >= 500:
                        preview_text += " ... (truncated)"
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        preview_text = f.read(500)
                        if len(preview_text) >= 500:
                            preview_text += " ... (truncated)"
                except Exception:
                    preview_text = "Text preview unavailable (encoding error)."

        elif file_extension in ['.pdf']:
            preview_text = "PDF file - Preview not directly supported (click 'View File')"
        elif file_extension in ['.docx', '.doc']:
            preview_text = "Word Document (.docx, .doc) - Preview not directly supported (click 'View File')"
        elif file_extension in ['.xlsx', '.xls', '.ods']:
            preview_text = "Spreadsheet (.xlsx, .xls, .ods) - Preview not directly supported (click 'View File')"
        elif file_extension in ['.pptx', '.ppt', '.odp']:
            preview_text = "Presentation (.pptx, .ppt, .odp) - Preview not directly supported (click 'View File')"
        elif file_extension in ['.zip', '.rar', '.7z']:
            preview_text = "Archive (.zip, .rar, .7z) - Preview not directly supported (click 'View File')"


    except FileNotFoundError:
        preview_text = "File not found for preview."
    except Exception as e:
        preview_text = f"Error generating preview: {e}"

    return preview_text

@login_required
def upload_media(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for file in files:
            Media.objects.create(
                user=request.user,
                file=file,
                title=file.name
            )
        return JsonResponse({'message': 'Upload successful'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user not in post.views.all():
        post.views.add(request.user)
    return redirect('home')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print("Post Form is VALID!")
            post = form.save(commit=False)
            post.user = request.user
            print("Form cleaned data:", form.cleaned_data)
            if form.cleaned_data['image']:
                print("Image data detected in cleaned_data")
            else:
                print("No image data found in cleaned_data")

            post.save()
            print("Post saved successfully to database. Post ID:", post.id)
            return redirect('home')
        else:
            print("Post Form Errors:", form.errors)
    else:
        form = PostForm()
    return render(request, 'social_app/home.html', {'form': form})

class FollowUnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Validate input data
        serializer = FollowUnfollowSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'status': 'error', 'message': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


        user_to_follow_id = serializer.validated_data['user_id']
        user_to_follow = get_object_or_404(User, id=user_to_follow_id)

        try:

            followed, followers_count = toggle_follow(request.user, user_to_follow)
        except ValueError as e:
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Return success response
        return Response({
            'status': 'success',
            'followed': followed,
            'followers_count': followers_count,
        }, status=status.HTTP_200_OK)

def api_stories(request):
    stories = Story.objects.all()
    data = [
        {
            'user': {
                'profile_pic': story.user.profile.profile_pic.url,
                'get_full_name': story.user.get_full_name
            }
        } for story in stories
    ]
    return JsonResponse(data, safe=False)

from django.http import JsonResponse
from django.contrib.auth.models import User

def api_suggestions(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

    user = request.user
    profile = user.profile


    following_users = profile.following.all()


    suggested_users = User.objects.exclude(
        id=user.id
    ).exclude(
        id__in=following_users.values_list('id', flat=True)
    )[:10]

    data = [
        {
            'id': suggested_user.id,
            'user': {
                'profile_pic': suggested_user.profile.profile_pic.url if suggested_user.profile.profile_pic else '',  # Handle missing profile_pic
                'get_full_name': suggested_user.get_full_name(),
                'username': suggested_user.username,
            }
        } for suggested_user in suggested_users
    ]
    return JsonResponse(data, safe=False)

def about(request):
    return render(request, 'social_app/about.html')

def terms_of_service(request):
    return render(request, 'social_app/terms_of_service.html')

def privacy_policy(request):
    return render(request, 'social_app/privacy_policy.html')

def contact(request):
    return render(request, 'social_app/contact.html')

def api_recommendations(request):
    recommendations = Recommendation.objects.all()
    data = [
        {
            'image': recommendation.image.url,
            'title': recommendation.title
        } for recommendation in recommendations
    ]
    return JsonResponse(data, safe=False)

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ForumListAPIView(generics.ListAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ForumDetailAPIView(generics.RetrieveAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ForumPostListAPIView(generics.ListAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ForumPostDetailAPIView(generics.RetrieveAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MediaListAPIView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MediaDetailAPIView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]