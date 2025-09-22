from django.contrib.auth import get_user_model
from django.db import models
from slugify import slugify

UserModel = get_user_model()

class BlogPost(models.Model):
    MAX_TITLE_LENGTH = 200

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name='Заглавие на пост',
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=MAX_TITLE_LENGTH,
    )

    content = models.TextField(
        verbose_name='Съдържание на поста',
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    excerpt = models.TextField(
        blank=True,
        null=True,
        verbose_name='извадка',
        help_text='Откъс от целия текст за кратко представяне'

    )

    created_at = models.DateTimeField(auto_now_add=True)

    published = models.BooleanField(
        default=False,
        verbose_name='Публикуван',
    )

    def save(self, *args, **kwargs):
        if not self.slug or slugify(self.title) != self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блог пост'
        verbose_name_plural = 'Блог постове'
        ordering = ['-created_at']

    def create_excerpt(self):
        if not self.excerpt:
            self.excerpt = self.content[:250]

    def __str__(self):
        return f'{self.title} ({self.created_at.strftime("%d.%m.%Y")})'


class BlogImage(models.Model):
    MAX_CAPTION_LENGTH = 255

    post = models.ForeignKey(
        BlogPost,
        verbose_name='Блог',
        on_delete=models.CASCADE,
        related_name='images',
    )

    image = models.ImageField(
        upload_to='blog_images/',
        verbose_name='Изображение',
    )

    alt_text = models.CharField(
        max_length=MAX_CAPTION_LENGTH,
        null=True,
        blank=True,
        verbose_name='Описание на изображението',
        help_text="Кратко описание на изображението (alt текст)",
    )

    def __str__(self):
        return f'Изображение за пост: {self.post.title}'
