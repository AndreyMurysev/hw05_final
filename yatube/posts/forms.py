from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Текст записи',
            'group': 'Название группы, где размещена запись',
            'image': 'Добавить изобажение'}

    def save(self, user):
        obj = super(PostForm, self).save(commit=False)
        obj.author = user
        return obj.save()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def save(self, user, post):
        obj = super(CommentForm, self).save(commit=False)
        obj.author = user
        obj.post = post
        return obj.save()
