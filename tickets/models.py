from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', '📋 Открыт'),
        ('in_progress', '⚙️ В работе'),
        ('resolved', '✅ Решен'),
        ('closed', '🔒 Закрыт'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '🟢 Низкий'),
        ('medium', '🟡 Средний'),
        ('high', '🟠 Высокий'),
        ('critical', '🔴 Критический'),
    ]
    
    title = models.CharField('Тема', max_length=200)
    description = models.TextField('Описание')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField('Приоритет', max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Тикет'
        verbose_name_plural = 'Тикеты'
    
    def __str__(self):
        return self.title

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('Комментарий')
    created_at = models.DateTimeField('Добавлен', auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    def __str__(self):
        return f'Комментарий к #{self.ticket.id}'