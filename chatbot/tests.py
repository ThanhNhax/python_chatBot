# tests.py — kiểm thử tự động. Chạy: python manage.py test
from django.test import SimpleTestCase

from .logic import bo_dau, nap_du_lieu, tra_loi


class LogicTest(SimpleTestCase):
    def setUp(self):
        self.intents = nap_du_lieu()

    def test_bo_dau(self):
        self.assertEqual(bo_dau("Học phí bao nhiêu?!"), "hoc phi bao nhieu")
        self.assertEqual(bo_dau("Đại học"), "dai hoc")

    def test_hoi_co_dau_va_khong_dau_nhu_nhau(self):
        self.assertEqual(tra_loi("học phí", self.intents), tra_loi("hoc phi", self.intents))

    def test_cum_tu_dai_thang_tu_don(self):
        # "điểm chuẩn ngành CNTT" chứa cả "diem chuan" và "nganh" -> phải ra điểm chuẩn
        self.assertIn("Điểm chuẩn", tra_loi("điểm chuẩn ngành CNTT", self.intents))

    def test_khop_theo_tu_nguyen_ven(self):
        # "hi" (chào hỏi) không được khớp bên trong "học phí"
        self.assertIn("Học phí", tra_loi("học phí", self.intents))

    def test_ktx(self):
        self.assertIn("Ký túc xá", tra_loi("KTX ở đâu", self.intents))

    def test_khong_hieu_va_rong(self):
        self.assertIn("chưa hiểu", tra_loi("asdfgh", self.intents))
        self.assertIn("chưa nhập", tra_loi("   ", self.intents))


class WebTest(SimpleTestCase):
    def test_trang_chu(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'id="khung"')

    def test_chat_api(self):
        r = self.client.get("/chat/", {"q": "học bổng"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("Học bổng", r.json()["answer"])
