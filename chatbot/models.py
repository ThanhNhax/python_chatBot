from django.db import models

class Intent(models.Model):
    tag = models.CharField(max_length=100, unique=True, verbose_name="Chủ đề")
    keywords = models.TextField(verbose_name="Từ khóa (cách nhau bởi dấu phẩy)", help_text="Nhập các từ khóa, phân cách nhau bởi dấu phẩy (,)")
    answer = models.TextField(verbose_name="Câu trả lời")

    def __str__(self):
        return self.tag
    
    def get_keywords_list(self):
        return [kw.strip() for kw in self.keywords.split(',') if kw.strip()]

class UnresolvedQuestion(models.Model):
    question = models.CharField(max_length=500, verbose_name="Câu hỏi chưa hiểu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian hỏi")

    class Meta:
        verbose_name = "Câu hỏi chưa hiểu"
        verbose_name_plural = "Các câu hỏi chưa hiểu"

    def __str__(self):
        return self.question
