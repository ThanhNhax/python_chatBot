# views.py — lớp "vỏ" web: nhận request từ trình duyệt, gọi lõi logic.py, trả kết quả.
from django.http import JsonResponse
from django.shortcuts import render

from .logic import nap_du_lieu, tra_loi

# Đọc knowledge.json 1 LẦN khi server khởi động, không đọc lại mỗi lần có người hỏi
INTENTS = nap_du_lieu()


def trang_chat(request):
    """Trả về trang HTML chứa khung chat (đường dẫn: /)."""
    return render(request, "chatbot/index.html")


def chat_api(request):
    """Nhận câu hỏi, trả câu trả lời dạng JSON (đường dẫn: /chat/).

    VD: trình duyệt gọi /chat/?q=hoc phi  ->  {"answer": "Học phí năm học ..."}
    Dùng GET cho đơn giản, tránh phải xử lý CSRF token của POST khi mới học Django.
    """
    cau_hoi = request.GET.get("q", "")
    return JsonResponse(
        {"answer": tra_loi(cau_hoi, INTENTS)},
        json_dumps_params={"ensure_ascii": False},  # giữ nguyên tiếng Việt có dấu
    )
