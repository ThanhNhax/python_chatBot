# logic.py — LÕI của chatbot, không phụ thuộc Django.
# Có thể chạy thử thẳng trong terminal: python logic.py
import json
import re
import unicodedata
from pathlib import Path

# Đường dẫn tới knowledge.json, tính từ vị trí file này nên chạy ở đâu cũng không lỗi
DUONG_DAN_DU_LIEU = Path(__file__).parent / "data" / "knowledge.json"

CAU_TRA_LOI_MAC_DINH = (
    "Xin lỗi, mình chưa hiểu câu hỏi này. "
    "Bạn thử hỏi về: ngành học, học phí, điểm chuẩn, học bổng, ký túc xá nhé!"
)


def bo_dau(text):
    """Chuẩn hóa câu: chữ thường, bỏ dấu tiếng Việt, bỏ dấu câu.

    VD: "Học phí bao nhiêu?!" -> "hoc phi bao nhieu"
    Nhờ vậy người dùng gõ có dấu hay không dấu đều khớp được với từ khóa.
    """
    text = text.lower()
    # NFD tách chữ và dấu ra riêng: "ọ" -> "o" + dấu nặng
    text = unicodedata.normalize("NFD", text)
    # Mn là nhóm ký tự "dấu", bỏ hết đi chỉ còn chữ gốc
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    # "đ" không tách được bằng NFD nên phải đổi riêng
    text = text.replace("đ", "d")
    # Dấu câu và ký tự lạ đổi thành khoảng trắng: "hoc phi?!" -> "hoc phi  "
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # Gộp nhiều khoảng trắng liền nhau thành 1
    return re.sub(r"\s+", " ", text).strip()


def nap_du_lieu(duong_dan=DUONG_DAN_DU_LIEU):
    """Đọc knowledge.json, trả về danh sách intent.

    Từ khóa được chuẩn hóa 1 lần ở đây, đỡ phải chuẩn hóa lại mỗi lần có người hỏi.
    """
    with open(duong_dan, encoding="utf-8") as f:
        intents = json.load(f)["intents"]
    for intent in intents:
        intent["keywords"] = [bo_dau(kw) for kw in intent["keywords"]]
    return intents


def tinh_diem(cau_hoi_sach, intent):
    """Chấm điểm 1 intent: mỗi từ khóa xuất hiện được cộng số TỪ của nó.

    VD: câu "diem chuan nganh cntt"
        - intent diem_chuan: "diem chuan" khớp -> 2 điểm
        - intent nganh_hoc:  "nganh" khớp      -> 1 điểm
    => chọn diem_chuan, vì cụm từ dài thường cụ thể hơn từ đơn.
    """
    # Thêm khoảng trắng 2 đầu để khớp theo TỪ NGUYÊN VẸN:
    # từ khóa "hi" chỉ khớp " hi ", không khớp bên trong "hoc phi" hay "chi phi"
    cau_dem = f" {cau_hoi_sach} "
    diem = 0
    for kw in intent["keywords"]:
        if f" {kw} " in cau_dem:
            diem += len(kw.split())
    return diem


def tra_loi(cau_hoi, intents):
    """Nhận câu hỏi, trả về câu trả lời của intent có điểm cao nhất."""
    cau_sach = bo_dau(cau_hoi)
    if not cau_sach:
        return "Bạn chưa nhập câu hỏi nào, thử gõ 'học phí' hoặc 'ngành học' nhé!"

    intent_tot_nhat, diem_cao_nhat = None, 0
    for intent in intents:
        diem = tinh_diem(cau_sach, intent)
        # Dùng ">" chứ không phải ">=": nếu hòa điểm thì giữ intent đứng trước trong file
        if diem > diem_cao_nhat:
            intent_tot_nhat, diem_cao_nhat = intent, diem

    if intent_tot_nhat is None:   # không từ khóa nào khớp
        return CAU_TRA_LOI_MAC_DINH
    return intent_tot_nhat["answer"]


def chay_terminal():
    """Chạy thử chatbot ngay trong terminal (giai đoạn 1, chưa cần web)."""
    intents = nap_du_lieu()
    print("Chatbot tuyển sinh PTIT (demo). Gõ 'thoat' để dừng.")
    while True:
        cau_hoi = input("Bạn: ").strip()
        if bo_dau(cau_hoi) in ("thoat", "exit", "quit"):
            print("Bot: Tạm biệt!")
            break
        print("Bot:", tra_loi(cau_hoi, intents))


if __name__ == "__main__":
    chay_terminal()
