import re
import unicodedata
import google.generativeai as genai
from chatbot.models import Intent, UnresolvedQuestion

# Cấu hình API Key của bạn
import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

CAU_TRA_LOI_MAC_DINH = (
    "Xin lỗi, mình chưa hiểu câu hỏi này. "
    "Bạn thử hỏi về: ngành học, học phí, điểm chuẩn, học bổng, ký túc xá nhé!"
)

def bo_dau(text):
    """Chuẩn hóa câu: chữ thường, bỏ dấu tiếng Việt, bỏ dấu câu."""
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def tinh_diem(cau_hoi_sach, intent):
    """Chấm điểm 1 intent: dựa trên số từ khóa khớp."""
    cau_dem = f" {cau_hoi_sach} "
    diem = 0
    # Lấy danh sách từ khóa từ Database, sau đó chuẩn hóa không dấu
    for kw in intent.get_keywords_list():
        kw_sach = bo_dau(kw)
        if f" {kw_sach} " in cau_dem:
            diem += len(kw_sach.split())
    return diem

def tra_loi(cau_hoi):
    """Nhận câu hỏi, truy vấn Database và trả về câu trả lời bằng Hybrid (Intent -> Gemini)."""
    cau_sach = bo_dau(cau_hoi)
    if not cau_sach:
        return "Bạn chưa nhập câu hỏi nào, thử gõ 'học phí' hoặc 'ngành học' nhé!"

    # ==========================================
    # BƯỚC 1: KIỂM TRA TỪ KHÓA TỐC ĐỘ CAO (0.1s)
    # ==========================================
    intent_tot_nhat, diem_cao_nhat = None, 0
    intents = Intent.objects.all()
    
    for intent in intents:
        diem = tinh_diem(cau_sach, intent)
        if diem > diem_cao_nhat:
            intent_tot_nhat, diem_cao_nhat = intent, diem

    # NẾU TÌM THẤY TỪ KHÓA -> Trả lời ngay lập tức
    if intent_tot_nhat is not None and diem_cao_nhat > 0:
        return intent_tot_nhat.answer

    # ==========================================
    # BƯỚC 2: GỌI GEMINI AI NẾU KHÔNG TÌM THẤY TỪ KHÓA
    # ==========================================
    try:
        # Gom tất cả kiến thức từ các Intent để dạy cho AI
        context_text = "THÔNG TIN CƠ SỞ ĐỂ TRẢ LỜI KHÁCH HÀNG:\n"
        for intent in intents:
            context_text += f"- {intent.answer}\n"
            
        system_instruction = (
            "Bạn là trợ lý ảo tư vấn tuyển sinh PTIT. "
            "Hãy trả lời khách hàng một cách lịch sự, tự nhiên, và ngắn gọn. "
            "TUYỆT ĐỐI CHỈ trả lời dựa trên thông tin được cung cấp dưới đây. "
            "KHÔNG ĐƯỢC bịa đặt, tự sáng tác hoặc tìm kiếm thông tin bên ngoài. "
            "Nếu khách hỏi thông tin KHÔNG CÓ trong tài liệu, hãy trả lời chính xác chữ: 'UNRESOLVED'."
        )
        
        model = genai.GenerativeModel(
            model_name="gemini-3.5-flash",
            system_instruction=system_instruction
        )
        
        prompt = f"{context_text}\n\nCâu hỏi của khách: {cau_hoi}"
        response = model.generate_content(prompt)
        answer = response.text.strip()
        
        # Nếu AI không biết câu trả lời
        if "UNRESOLVED" in answer:
            UnresolvedQuestion.objects.create(question=cau_hoi)
            return CAU_TRA_LOI_MAC_DINH
            
        return answer
        
    except Exception as e:
        print("Lỗi Gemini:", e)
        UnresolvedQuestion.objects.create(question=cau_hoi)
        return "Hệ thống AI đang bận xử lý, vui lòng thử lại sau."
