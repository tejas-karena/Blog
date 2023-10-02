from django.test import TestCase, Client
from blogpost.models import User, Post, Comment
from django.utils import timezone
from blogpost.forms import SignUpForm
from django.urls import reverse


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email="sim@gmail.com",
            first_name="Sima",
            last_name="Sen",
            country="india",
            birth_date="2022-12-12",
        )

    def test_email_label(self):
        author = User.objects.get(id=1)
        field_label = author._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email address")
        

    def test_first_name_max_length(self):
        author = User.objects.get(id=1)
        max_length = author._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 250)


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "sim@gmail.com",
            "first_name": "Sima",
            "last_name": "Sen",
            "country": "india",
            "birth_date": timezone.now().date(),
        }
        cls.user = User.objects.create(**cls.user_data)

    def test_create_post(self):
        post_data = {
            "title": "Test Post",
            "blog": "This is a test post.",
            "author": self.user,
        }
        post = Post.objects.create(**post_data)
        self.assertEqual(post.title, post_data["title"])
        self.assertEqual(post.blog, post_data["blog"])
        self.assertEqual(post.author, self.user)

    def test_post_ordering(self):
        post_data = {
            "title": "Test Post",
            "blog": "This is a test post.",
            "author": self.user,
        }
        post1 = Post.objects.create(**post_data)
        post2 = Post.objects.create(**post_data)

        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], post1)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "sim@gmail.com",
            "first_name": "Sima",
            "last_name": "Sen",
            "country": "india",
            "birth_date": timezone.now().date(),
        }
        cls.user = User.objects.create(**cls.user_data)

        cls.post_data = {
            "title": "Test Post",
            "blog": "This is a test post.",
            "author": cls.user,
        }
        cls.post = Post.objects.create(**cls.post_data)

    def test_create_comment(self):
        comment_data = {
            "username": self.user,
            "commentblog": self.post,
            "comment": "This is a my comment.",
        }
        comment = Comment.objects.create(**comment_data)
        self.assertEqual(comment.username, self.user)
        self.assertEqual(comment.commentblog, self.post)
        self.assertEqual(comment.comment, comment_data["comment"])

    def test_comment_date(self):
        comment_data = {
            "username": self.user,
            "commentblog": self.post,
            "comment": "This is a test comment.",
        }
        comment = Comment.objects.create(**comment_data)
        self.assertIsNotNone(comment.comment_date)

    def test_comment_string_represent(self):
        long_comment = (
            "This is a very long comment that has more than 75 characters. " * 3
        )
        comment_data = {
            "username": self.user,
            "commentblog": self.post,
            "comment": long_comment,
        }
        comment = Comment.objects.create(**comment_data)
        self.assertEqual(str(comment), long_comment[:75])


class SignUpFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email="sim@gmail.com",
            first_name="Sima",
            last_name="Sen",
            country="india",
            birth_date="2022-12-12",
        )

    def test_signup_form_date_field(self):
        form = SignUpForm()
        self.assertTrue(
            form.fields["birth_date"].label is None
            or form.fields["birth_date"].label == "Birthdate"
        )


class BlogListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 15

        for author_id in range(number_of_authors):
            User.objects.create(
                email=f"sim{author_id}@gmail.com",
                first_name=f"Sima {author_id}",
                last_name=f"Sen {author_id}",
                country=f" {author_id}'s india",
                birth_date=f"2022-12-{author_id}",
            )


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("home")

    def test_home_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blogpost/home.html")


class TestBlogListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("blog-list")

    def test_blog_list_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blogpost/blog_list.html")


class TestAuthorListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("author-list")

    def test_author_list_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_author_list_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blogpost/author_list.html")


class TestBlogAddView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sim@gmail.com",
            password="simpassword",
            first_name="Sim",
            last_name="Sen",
        )

    def test_blog_add_view_status_code(self):
        self.client = Client()
        self.client.login(email="sim@gmail.com", password="simpassword")
        response = self.client.get(reverse("blog-add", kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_blog_add_view_status_code(self):
        self.client = Client()
        self.client.login(email="ram@gmail.com",password="myPassword")
        response = self.client.get(reverse("blog-add",))    

    def test_blog_add_view_template(self):
        self.client = Client()
        self.client.login(email="sim@gmail.com", password="simpassword")
        response = self.client.get(reverse("blog-add", kwargs={"pk": self.user.id}))
        self.assertTemplateUsed(response, "blogpost/blog_add.html")


class TestCommentFunView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sim@gmail.com",
            password="simpassword",
            first_name="Sim",
            last_name="Sen",
        )
        self.post = Post.objects.create(
            title="Test Post", blog="This is my content", author=self.user
        )

    def test_comment_fun_view_post(self):
        self.client = Client()
        self.client.login(email="sim@gmail.com", password="simpassword")
        response = self.client.post(
            reverse("comment", kwargs={"pk": self.post.pk}), {"comment": "Test comment"}
        )
        self.assertRedirects(
            response, reverse("blog-detail", kwargs={"pk": self.post.pk})
        )


class TestSearchFunView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("blog-search")

    def test_search_fun_view_post_form(self):
        data = {"search": "Test"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
