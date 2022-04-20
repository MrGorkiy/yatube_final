from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F, CheckConstraint

User = get_user_model()


class Group(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Ссылка", unique=True)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField("Текст", help_text="Текст поста")
    pub_date = models.DateTimeField("Дата создания", auto_now_add=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        max_length=200,
        blank=True,
        null=True,
        related_name="posts",
        verbose_name="Группа",
        help_text="Добавить пост в группу",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    image = models.ImageField("Картинка", upload_to="posts/", blank=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField("Комментарий", help_text="Текст комментария")
    created = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        related_name="following",
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name="follower",
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Подписку"
        verbose_name_plural = "Подписки"
        unique_together = ('author', 'user')
        constraints = [
            CheckConstraint(check=~Q(author=F('user')), name='author_not_user')
        ]