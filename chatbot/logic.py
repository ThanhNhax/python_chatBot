import re
import unicodedata

from chatbot.models import Intent

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
    """Nhận câu hỏi, truy vấn Database và trả về câu trả lời."""
    cau_sach = bo_dau(cau_hoi)
    if not cau_sach:
        return "Bạn chưa nhập câu hỏi nào, thử gõ 'học phí' hoặc 'ngành học' nhé!"

    intent_tot_nhat, diem_cao_nhat = None, 0
    # Lấy toàn bộ chủ đề từ Database
    intents = Intent.objects.all()
    
    for intent in intents:
        diem = tinh_diem(cau_sach, intent)
        if diem > diem_cao_nhat:
            intent_tot_nhat, diem_cao_nhat = intent, diem

    if intent_tot_nhat is None:
        return CAU_TRA_LOI_MAC_DINH
    return intent_tot_nhat.answer
