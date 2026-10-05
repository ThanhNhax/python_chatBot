from django.http import JsonResponse
from django.shortcuts import render
from .logic import tra_loi

def trang_chat(request):
    """Trả về trang HTML chứa khung chat."""
    return render(request, "chatbot/index.html")

def chat_api(request):
    """API gọi hàm tra_loi() để lấy kết quả từ DB."""
    cau_hoi = request.GET.get("q", "")
    return JsonResponse(
        {"answer": tra_loi(cau_hoi)},
        json_dumps_params={"ensure_ascii": False},  # Giữ tiếng Việt có dấu
    )
