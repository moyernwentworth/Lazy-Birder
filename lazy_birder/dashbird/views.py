from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os, shutil
from django.contrib.auth.decorators import login_required
from google.cloud import storage


# ensure user is logged in
@login_required
def bird_posts(request):
    # variables that are used for google cloud platform purposes
    yearlst = ["_21"]
    year = yearlst[0]
    monthlst=["Mar","Apr","May"]
    month = monthlst[1]
    daylst = datetime.today().day
    day = str(daylst)

    def downloadPics():
        """Using a gcp key as described in the readme, download images from your 
        bucket which are the bird photos from your feeder"""

        # see readme for setting up client variable
        client = storage.Client.from_service_account_json(json_credentials_path=r'/Users/wil/Code/gcp_key.json')

        # get bucket 
        bucket = client.get_bucket('processed-birds')
        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        # https://googleapis.dev/python/storage/latest/client.html 
        # https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/storage_download_file.py
    
        destination_file_name = r'/Users/wil/Code/Lazy-Birder/lazy_birder/media/wil/new/' #+pic
        blobs = bucket.list_blobs()
        # for all images in your google bucket, save with a predetermined naming convention
        for blobOrig in blobs:
            blob = str(blobOrig.name).split("~")
            print (blob[0])
            blob = blob[1]
            filename = blobOrig.name.replace(':', '-')
            if os.path.exists(destination_file_name + filename) == False:
                blobOrig.download_to_filename(destination_file_name + filename)  # Download

    def main():
        # download pictures from bucket and set local environment variables
        print("start")
        downloadPics()
        os.environ['CONNECTION_NAME'] = 'utility-range-305718:us-central1:lazybirderdb'
        os.environ['DB_USER'] = 'user'
        os.environ['DB_PASSWORD'] = 'LazyPassword01'
        os.environ['DB_NAME'] = 'ProcImages'

    main()
    # get current logged in user
    current_user = request.user

    # the followinf blocks take in downloaded images, gathers info from its name, resizes
    # the images, and then saves image and metadata to a post object which is then displayed to the user

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

        # Create post object using the post model
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

    # show logged in users posts 
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 5)

    # account for not enough post objects to fill a paginated page
    try: 
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'dashbird/bird_posts.html', {'posts': posts})


def home(request):
    return render(request, 'dashbird/home.html')


class UserPostListView(ListView):
    """Can filter to see only a selected user's posts"""
    model = Post
    template_name = 'dashbird/user_posts.html'
    context_object_name = 'posts'
    # set number of posts per page
    paginate_by = 5


    def get_queryset(self):
        """filter posts by user, show them reverse chronologically"""
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

        

class PostDetailView(DetailView):
    """Shows a full page of details of a selected post"""
    model = Post
    fields = ['title', 'content', 'bird_photo']



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows users to change the title and content of their posts"""
    model = Post
    fields = ['title', 'content', 'bird_photo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        return True if self.request.user == post.author else False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows uers to delete there own posts"""
    model = Post
    success_url = '/'


    def test_func(self):
        """ensures the logged in user is editing their own post, no one elses"""
        post = self.get_object()
        return True if self.request.user == post.author else False

