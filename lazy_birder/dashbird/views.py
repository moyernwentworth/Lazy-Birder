from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os, shutil, sys
from django.contrib.auth.decorators import login_required
from google.cloud import storage
import pymysql


# this is a function based view, have to render the request
# ensure user is logged in
@login_required
def bird_posts(request):
    ############################
    yearlst = ["_21"]
    year = yearlst[0]
    monthlst=["Mar","Apr","May"]
    month = monthlst[1]
    daylst = datetime.today().day
    day = str(daylst)

    # input NORTHERN_FLICKER~nick_21Apr06_12_57_38.jpg
    def downloadPics():
        client = storage.Client.from_service_account_json(json_credentials_path=r'/Users/wil/Code/gcp_key.json')
        # get bucket 
        bucket = client.get_bucket('processed-birds')
        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        # https://googleapis.dev/python/storage/latest/client.html 
        # https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/storage_download_file.py
        #source_blob_name = pic
        #print (source_blob_name)
        #'Users/wil/Code/Lazy-Birder/lazy_birder/media/wil/new'
        destination_file_name = r'/Users/wil/Code/Lazy-Birder/lazy_birder/media/wil/new/' #+pic
        old_file_name = r'/Users/wil/Code/Lazy-Birder/lazy_birder/media/wil/old/'
        #blob = bucket.blob(source_blob_name)
        #bucket = storage_client.get_bucket(bucket_name=bucket_name)
        blobs = bucket.list_blobs()
        for blobOrig in blobs:
            blob = str(blobOrig.name).split("~")
            print (blob[0])
            blob = blob[1]

            if blob[:4] == "nick":
                if blob[:7] == "nick" + year:
                    if blob[:10] == "nick" + year + month:
                        if blob[:12] == "nick" + year + month + day:
                            filename = blobOrig.name.replace(':', '-')
                            if os.path.exists(old_file_name + filename) == False:
                                blobOrig.download_to_filename(destination_file_name + filename)  # Download
        
        #blob.download_to_filename(destination_file_name)

        #print(
        #    "Blob {} downloaded to {}.".format(
        #        source_blob_name, destination_file_name
        #    )
        #)

    def main():
        print("start")
        downloadPics()
        os.environ['CONNECTION_NAME'] = 'utility-range-305718:us-central1:lazybirderdb'
        os.environ['DB_USER'] = 'user'
        os.environ['DB_PASSWORD'] = 'LazyPassword01'
        os.environ['DB_NAME'] = 'ProcImages'
        #getSQL()

    main()
    ######################################
    # get current logged in user
    current_user = request.user
    # create paths for user's folders that will hold images
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'media', str(current_user))
    old_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'media', str(current_user), 'old')
    new_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'media', str(current_user), 'new')
    if not os.path.isdir(base_path):
        os.mkdir(base_path) 
    if not os.path.isdir(old_path):
        os.mkdir(old_path)
    if not os.path.isdir(new_path):
        os.mkdir(new_path)
    # see what pics have been added to new_dir in each user's
    new_pic_list = [pic for pic in os.listdir(new_path)]
    # create post for each new image
    for pic in new_pic_list:
        string_list = pic.replace('.jpg','').replace('~','_').split('_')
        species = ''
        if (len(string_list) == 7 ):
            species = str(string_list[0]) + ' ' + str(string_list[1])
        else:
            species = str(string_list[0])
        # resize pic
        resized_pic = Image.open(os.path.join(new_path, pic))
        resized_pic = resized_pic.resize((400, 300))
        resized_pic.save(os.path.join(new_path, pic))
        # move new photo to old folder where it will be served
        shutil.move(os.path.join(new_path, pic), old_path)
        # Create post
        automated_post = Post(
                title = species,
                author = current_user,
                content = 'A ' + species + ' visited your feeder!',
                date_posted = datetime.now(),
                bird_photo = os.path.join('..', 'media', str(current_user), 'old', pic)
        )
        automated_post.save()
    # ensure list is empty next time through
    new_pic_list = []

    post_list =  Post.objects.filter(author=current_user).order_by('-date_posted')
    # if we want to show all users posts
    # post_list = Post.objects.all().order_by('-date_posted')
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 5)
    try: 
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # context = {
    #     'posts': Post.objects.all()
    # }
    return render(request, 'dashbird/bird_posts.html', {'posts': posts})


def home(request):
    return render(request, 'dashbird/home.html')


# this is a class based view
class PostListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    template_name = 'dashbird/home.html'
    context_object_name = 'posts'
    # posts go from most recent on the top
    ordering = ['-date_posted']
    # set number of posts per page
    paginate_by = 5

    def automate_posts(self, request):
        automated_post = Post(
            title = 'Test Post',
            author = self.request.user,
            content = 'This is an example post',
            date_posted = datetime.now(),
            bird_photo = 'media/test1.jpeg'
        )
        automated_post.save()



class UserPostListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    template_name = 'dashbird/user_posts.html'
    context_object_name = 'posts'
    # set number of posts per page
    paginate_by = 5


    def get_queryset(self):
        """filter posts by user, show them reverse chronologically"""
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

        

class PostDetailView(DetailView):
    model = Post
    fields = ['title', 'content', 'bird_photo']



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'bird_photo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        return True if self.request.user == post.author else False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'


    def test_func(self):
        """ensures the logged in user is editing their own post, no one elses"""
        post = self.get_object()
        return True if self.request.user == post.author else False

