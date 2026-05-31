---
theme: default
title: Ứng dụng Hybrid Machine Learning trong CTI
info: |
  ## Ứng dụng Hybrid Machine Learning trong CTI
  An toàn và Đảm bảo Thông tin — Thuyết trình Nghiên cứu

  Khung học máy hỗn hợp cho phát hiện URL độc hại,
  phân loại xâm nhập mạng và phân tích hành vi bất thường.
class: text-center
drawings:
  persist: false
transition: slide-left
fonts:
  sans: Inter
  mono: Fira Code
---

# Ứng dụng Hybrid Machine Learning trong Cyber Threat Intelligence

<div class="text-xl text-gray-400 mt-4 font-normal">
Môn học: An toàn và Đảm bảo Thông tin
</div>

<div class="abs-bl mx-14 my-12 flex flex-col gap-1 text-left text-sm text-gray-500">
  <div>Tháng 5, 2026</div>
</div>

<style>
h1 {
  background: linear-gradient(135deg, #1E3A5F 0%, #3B82F6 50%, #60A5FA 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 3.2rem !important;
  font-weight: 800;
  line-height: 1.2;
}

/* Tối ưu hóa kích thước bảng biểu và code block */
table {
  width: 100% !important;
  margin: 0.15rem 0 !important;
  border-collapse: collapse !important;
}
th {
  padding: 2px 4px !important;
  font-size: 10.5px !important;
  font-weight: 700 !important;
  background-color: rgba(148, 163, 184, 0.15) !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.3) !important;
}
td {
  padding: 1.5px 4px !important;
  font-size: 10px !important;
  line-height: 1.15 !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1) !important;
}
code {
  padding: 0px 2px !important;
  font-size: 9.5px !important;
}

/* Tắt hoàn toàn menu Goto / Danh sách slide (Agenda) */
#slidev-goto-dialog,
.autocomplete-list,
[id^="slidev-goto"] {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
</style>

---
transition: fade-out
---

# Nội dung Chương trình

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-2 gap-4">

<div class="space-y-2 text-sm">

### Cơ sở Lý thuyết
1. Tổng quan về Cyber Threat Intelligence (CTI - Tình báo mối đe dọa an ninh mạng)
2. Xu hướng áp dụng Machine Learning (ML - Học máy)
3. Sự hạn chế của Signature-based Detection (Phát hiện dựa trên chữ ký)
4. Phân biệt Supervised Learning (Học có giám sát) & Unsupervised Learning (Học không giám sát)

</div>

<div class="space-y-2 text-sm">

### Các ứng dụng thực nghiệm
5. Network Intrusion Classification (Phân loại xâm nhập mạng) <span class="inline-block text-xs bg-red-500 text-white px-2 py-0.5 rounded-full align-middle">DEMO</span>
6. User and Entity Behavior Analytics (UEBA - Phân tích hành vi người dùng và thực thể) <span class="inline-block text-xs bg-red-500 text-white px-2 py-0.5 rounded-full align-middle">DEMO</span>
7. Dự báo khai thác lỗ hổng bảo mật
8. Phishing URL Detection (Phát hiện URL lừa đảo) <span class="inline-block text-xs bg-red-500 text-white px-2 py-0.5 rounded-full align-middle">DEMO</span>
9. AI-based Antivirus (Trình diệt mã độc thông minh)
10. Adversarial Machine Learning (Adversarial ML - Học máy đối kháng)

</div>

</div>

<div class="mt-4 p-3 rounded-lg bg-blue-500 bg-opacity-10 border border-blue-500 border-opacity-20">
  <div class="text-xs text-blue-300">
    Hệ thống tích hợp 3 mô hình thực nghiệm được huấn luyện trên <strong>651K mẫu URL</strong> + <strong>125K luồng mạng (NSL-KDD)</strong>.
  </div>
</div>

</div>

---
layout: two-cols
---

# Tổng quan về CTI

<div class="flex flex-col justify-center mt-2">

<div class="text-lg font-medium text-blue-400 mb-4 pr-4">
"Thu thập, tinh lọc và phân tích dữ liệu đe dọa một cách hệ thống nhằm hỗ trợ đưa ra các quyết định phòng thủ hiệu quả."
</div>

<div class="space-y-2 text-sm pr-4">

**Ba cấp độ vận hành của CTI trong doanh nghiệp:**

| Cấp độ | Đối tượng | Ví dụ áp dụng |
|---|---|---|
| **Strategic (Chiến lược)** | Ban giám đốc, CISO | Đánh giá rủi ro từ nhóm APT đối với ngành |
| **Operational (Vận hành)** | Nhóm Blue Team | Phân tích kỹ thuật TTPs, MITRE ATT&CK |
| **Tactical (Kỹ thuật)** | Chuyên viên SOC | Cập nhật các chỉ số IoC (IP, hash, URL) |

</div>

<div class="mt-3 p-2.5 rounded bg-yellow-500 bg-opacity-10 border border-yellow-500 border-opacity-20 text-xs text-yellow-300 pr-4">
ML tối ưu hóa giai đoạn <strong>Processing</strong> và <strong>Analysis</strong> khi khối lượng telemetry vượt quá giới hạn xử lý của con người.
</div>

</div>

::right::

<div class="flex flex-col justify-center items-center h-full pl-4">
  <img src="/media/image3.png" class="rounded-lg border border-gray-700 shadow-lg max-h-70 object-contain" />
  <div class="text-center text-xs text-gray-400 mt-2">
    Sơ đồ Chu trình CTI (Cyber Threat Intelligence Cycle) chuyên nghiệp
  </div>
</div>

---

# Tại sao cần Machine Learning hiện nay?

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-3 gap-4">

<div class="p-4 rounded-xl bg-blue-500 bg-opacity-10 border border-blue-500 border-opacity-20 text-center">
  <div class="font-bold text-sm text-blue-400 mb-1">Năng lực Tính toán (Compute)</div>
  <div class="text-xs text-gray-400">Hạ tầng GPU/TPU trở nên phổ biến và giá thành hợp lý. Các nền tảng MLOps đám mây cho phép tối ưu thời gian huấn luyện.</div>
</div>

<div class="p-4 rounded-xl bg-green-500 bg-opacity-10 border border-green-500 border-opacity-20 text-center">
  <div class="font-bold text-sm text-green-400 mb-1">Khối lượng Dữ liệu (Data)</div>
  <div class="text-xs text-gray-400">Sự phát triển của telemetry doanh nghiệp từ hệ thống SIEM, EDR và tường lửa thế hệ mới tạo ra nguồn dữ liệu khổng lồ.</div>
</div>

<div class="p-4 rounded-xl bg-red-500 bg-opacity-10 border border-red-500 border-opacity-20 text-center">
  <div class="font-bold text-sm text-red-400 mb-1">Mức độ Phức tạp (Threats)</div>
  <div class="text-xs text-gray-400">Các cuộc tấn công Zero-day (Mối đe dọa chưa công bố), Polymorphic Malware (Mã độc đa hình), phishing ứng dụng AI phát triển nhanh chóng.</div>
</div>

</div>

<div class="mt-4 text-center font-mono text-xs">

```
10 năm trước:  Thuật toán ✓   Dữ liệu thô ✗   Năng lực xử lý ✗
Hiện tại:      Thuật toán ✓   Dữ liệu thô ✓   Năng lực xử lý ✓  → Hội tụ công nghệ
```

</div>

</div>

---

# Sự thất bại hệ thống của phương pháp truyền thống

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-2 gap-4">

<div class="p-4 rounded-xl border border-red-500 border-opacity-30 bg-red-500 bg-opacity-5">
  <div class="font-bold text-sm text-red-400 mb-1">Signature-based Detection</div>
  <div class="text-xs text-gray-400">
    Kẻ tấn công chỉ cần sửa đổi 1 byte trong mã nguồn → mã hash thay đổi → vượt qua AV truyền thống.
    <br/>Bất lực trước các cuộc tấn công <strong>Zero-day</strong> và <strong>Polymorphic Malware</strong>.
  </div>
</div>

<div class="p-4 rounded-xl border border-red-500 border-opacity-30 bg-red-500 bg-opacity-5">
  <div class="font-bold text-sm text-red-400 mb-1">Quy tắc lọc tĩnh (Static Firewalls)</div>
  <div class="text-xs text-gray-400">
    Không có khả năng mô hình hóa hoặc nhận biết sự bất thường trong hành vi người dùng.<br/>
    Ví dụ: Đăng nhập từ VPN lúc 3 giờ sáng từ một châu lục khác? <strong>Không có quy tắc tĩnh nào bắt được nếu tài khoản hợp lệ.</strong>
  </div>
</div>

<div class="p-4 rounded-xl border border-red-500 border-opacity-30 bg-red-500 bg-opacity-5">
  <div class="font-bold text-sm text-red-400 mb-1">Phân tích Nhật ký Thủ công</div>
  <div class="text-xs text-gray-400">
    Các doanh nghiệp lớn tạo ra hàng <strong>Terabyte logs</strong> mỗi ngày.<br/>
    Chuyên viên SOC bị quá tải → dẫn tới hiện tượng <strong>alert fatigue (mệt mỏi vì cảnh báo)</strong>.
  </div>
</div>

<div class="p-4 rounded-xl border border-red-500 border-opacity-30 bg-red-500 bg-opacity-5">
  <div class="font-bold text-sm text-red-400 mb-1">Blocklist IoC Tĩnh</div>
  <div class="text-xs text-gray-400">
    Kẻ tấn công tự động xoay vòng IP/Domain liên tục theo giờ.<br/>
    Danh sách blocklist luôn đi sau và trở nên lỗi thời trước khi kịp cập nhật vào hệ thống.
  </div>
</div>

</div>

</div>

---

# ML trong Đảm bảo An ninh mạng

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-2 gap-4">

<!-- Cột bên trái: Supervised Learning -->
<div class="p-3 rounded-xl border border-blue-200 bg-blue-50/50 dark:border-blue-900/50 dark:bg-blue-950/20 flex flex-col justify-between">
  <div>
    <div class="text-md font-bold text-blue-700 dark:text-blue-400 mb-0.5">Supervised Learning</div>
    <div class="text-[11px] text-slate-600 dark:text-slate-300 mb-1">
      Huấn luyện trên <strong>dữ liệu đã được gán nhãn</strong>.<br/>
      Mô hình học sự khác biệt giữa mẫu độc hại và mẫu lành tính.
    </div>

<!-- Gorgeous Light/Dark Adaptive Flow Diagram -->
<div class="flex flex-col gap-1.5 my-1.5 bg-slate-100/70 dark:bg-slate-900/50 p-2 rounded-lg border border-slate-200 dark:border-slate-800 shadow-inner">
  <div class="flex items-center justify-between text-[10px] font-mono">
    <span class="px-1.5 py-0.5 rounded bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-900/40 dark:text-blue-300 dark:border-blue-800 font-bold">Dữ liệu nhãn</span>
    <span class="text-slate-400 dark:text-slate-600 font-bold">➔</span>
    <span class="px-1.5 py-0.5 rounded bg-purple-100 text-purple-800 border border-purple-200 dark:bg-purple-900/40 dark:text-purple-300 dark:border-purple-800 font-bold">Random Forest</span>
    <span class="text-slate-400 dark:text-slate-600 font-bold">➔</span>
    <span class="px-1.5 py-0.5 rounded bg-green-100 text-green-800 border border-green-200 dark:bg-green-900/40 dark:text-green-300 dark:border-green-800 font-bold">Dự đoán</span>
  </div>
  <div class="border-t border-slate-200 dark:border-slate-800 my-0.5"></div>
  <div class="space-y-1 text-[10px] font-mono text-slate-600 dark:text-slate-300">
    <div class="flex justify-between items-center bg-slate-200/50 dark:bg-slate-800/50 px-1.5 py-0.5 rounded">
      <span class="text-slate-500 dark:text-slate-400">URL nghi vấn</span>
      <span class="text-slate-400 dark:text-slate-600">➔</span>
      <span class="text-red-600 dark:text-red-400 font-semibold">Lừa đảo / An toàn</span>
    </div>
    <div class="flex justify-between items-center bg-slate-200/50 dark:bg-slate-800/50 px-1.5 py-0.5 rounded">
      <span class="text-slate-500 dark:text-slate-400">Luồng mạng</span>
      <span class="text-slate-400 dark:text-slate-600">➔</span>
      <span class="text-red-600 dark:text-red-400 font-semibold">DoS / Probe / Normal</span>
    </div>
  </div>
</div>
  </div>

  <div class="mt-1 text-[10px] text-blue-600 dark:text-blue-400 font-semibold">
    Ứng dụng thực nghiệm: Phishing URL Detection, Network Intrusion Classification
  </div>
</div>

<!-- Cột bên phải: Unsupervised Learning -->
<div class="p-3 rounded-xl border border-green-200 bg-green-50/50 dark:border-green-900/50 dark:bg-green-950/20 flex flex-col justify-between">
  <div>
    <div class="text-md font-bold text-green-700 dark:text-green-400 mb-0.5">Unsupervised Learning</div>
    <div class="text-[11px] text-slate-600 dark:text-slate-300 mb-1">
      <strong>Không cần dữ liệu nhãn</strong>. Mô hình tự học phân phối hành vi bình thường.<br/>
      Mọi điểm nằm ngoài phân phối này sẽ bị đánh giá bất thường.
    </div>

<!-- Gorgeous Light/Dark Adaptive Flow Diagram -->
<div class="flex flex-col gap-1.5 my-1.5 bg-slate-100/70 dark:bg-slate-900/50 p-2 rounded-lg border border-slate-200 dark:border-slate-800 shadow-inner">
  <div class="flex items-center justify-between text-[10px] font-mono">
    <span class="px-1.5 py-0.5 rounded bg-green-100 text-green-800 border border-green-200 dark:bg-green-900/40 dark:text-green-300 dark:border-green-800 font-bold">Dữ liệu thô</span>
    <span class="text-slate-400 dark:text-slate-600 font-bold">➔</span>
    <span class="px-1.5 py-0.5 rounded bg-purple-100 text-purple-800 border border-purple-200 dark:bg-purple-900/40 dark:text-purple-300 dark:border-purple-800 font-bold">Isolation Forest</span>
    <span class="text-slate-400 dark:text-slate-600 font-bold">➔</span>
    <span class="px-1.5 py-0.5 rounded bg-yellow-100 text-yellow-800 border border-yellow-200 dark:bg-yellow-900/40 dark:text-yellow-300 dark:border-yellow-800 font-bold">Kiểm tra</span>
  </div>
  <div class="border-t border-slate-200 dark:border-slate-800 my-0.5"></div>
  <div class="space-y-1 text-[10px] font-mono text-slate-600 dark:text-slate-300">
    <div class="flex justify-between items-center bg-slate-200/50 dark:bg-slate-800/50 px-1.5 py-0.5 rounded">
      <span class="text-slate-500 dark:text-slate-400">Nhật ký đăng nhập</span>
      <span class="text-slate-400 dark:text-slate-600">➔</span>
      <span class="text-yellow-600 dark:text-yellow-400 font-semibold">Điểm bất thường</span>
    </div>
    <div class="flex justify-between items-center bg-slate-200/50 dark:bg-slate-800/50 px-1.5 py-0.5 rounded">
      <span class="text-slate-500 dark:text-slate-400">Telemetry mạng thô</span>
      <span class="text-slate-400 dark:text-slate-600">➔</span>
      <span class="text-yellow-600 dark:text-yellow-400 font-semibold">Vạch trần dị biệt</span>
    </div>
  </div>
</div>
  </div>

  <div class="mt-1 text-[10px] text-green-600 dark:text-green-400 font-semibold">
    Ứng dụng thực nghiệm: UEBA (Phát hiện hành vi đăng nhập bất thường)
  </div>
</div>

</div>

<div class="mt-2 text-center text-[10px] text-slate-500 dark:text-slate-400">
  CTI hiện đại kết hợp cả hai: Supervised cho mối đe dọa đã biết, Unsupervised cho Zero-day.
</div>

</div>

---
layout: center
class: text-center
---

# Sáu Bề mặt Ứng dụng ML trong Phòng thủ Chủ động

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-3 gap-4 max-w-3xl mx-auto">

<div class="p-4 rounded-lg border border-blue-500 border-opacity-30 bg-blue-500 bg-opacity-10 relative">
  <div class="absolute -top-2 -right-2 text-xs bg-red-500 text-white px-2 py-0.5 rounded-full">DEMO</div>
  <div class="text-sm font-bold">1. Network Intrusion Classification</div>
</div>

<div class="p-4 rounded-lg border border-blue-500 border-opacity-30 bg-blue-500 bg-opacity-10 relative">
  <div class="absolute -top-2 -right-2 text-xs bg-red-500 text-white px-2 py-0.5 rounded-full">DEMO</div>
  <div class="text-sm font-bold">2. UEBA Anomaly Detection</div>
</div>

<div class="p-4 rounded-lg border border-gray-600 border-opacity-30 bg-gray-600 bg-opacity-10">
  <div class="text-sm font-bold">3. Exploit Prediction Modeling</div>
</div>

<div class="p-4 rounded-lg border border-blue-500 border-opacity-30 bg-blue-500 bg-opacity-10 relative">
  <div class="absolute -top-2 -right-2 text-xs bg-red-500 text-white px-2 py-0.5 rounded-full">DEMO</div>
  <div class="text-sm font-bold">4. Phishing URL Detection</div>
</div>

<div class="p-4 rounded-lg border border-gray-600 border-opacity-30 bg-gray-600 bg-opacity-10">
  <div class="text-sm font-bold">5. AI-based Antivirus</div>
</div>

<div class="p-4 rounded-lg border border-gray-600 border-opacity-30 bg-gray-600 bg-opacity-10">
  <div class="text-sm font-bold">6. Adversarial ML Defense</div>
</div>

</div>

</div>

---

# 1 · Network Intrusion Classification

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-2 gap-4">

<div>

### 5 lớp trạng thái luồng mạng (KDD)

<div class="text-xs space-y-1 mt-1">

| Lớp | Ý nghĩa kỹ thuật |
|---|---|
| **Normal** | Lưu lượng mạng hợp lệ |
| **DoS** | Tấn công từ chối dịch vụ (Flood) |
| **Probe** | Dò quét cổng, thu thập thông tin mạng (Scan) |
| **R2L** | Truy cập từ xa trái phép (Remote-to-Local) |
| **U2R** | Leo thang đặc quyền (User-to-Root) |

</div>

<div class="mt-2 p-2 rounded bg-blue-500 bg-opacity-10 text-xs">
  <strong>Thuật toán: Random Forest (300 cây)</strong><br/>
  Huấn luyện trên <strong>125.973 luồng mạng NSL-KDD</strong><br/>
  Độ chính xác thực nghiệm: <strong class="text-green-400">98.8%</strong>
</div>

</div>

<div>

### Trích xuất 15 đặc trưng luồng mạng

```
duration        → thời lượng kết nối
src_bytes       → số byte gửi đi từ nguồn
dst_bytes       → số byte nhận về tại đích
wrong_fragment  → lỗi phân mảnh TCP/IP
diff_srv_rate   → tỷ lệ dịch vụ khác nhau
count           → số kết nối trong 2 giây gần nhất
```

<div class="mt-2 text-xs text-gray-400">

**Nhận diện đặc trưng tấn công:**
- **DoS**: duration ≈ 0, serror_rate (lỗi SYN) cao.
- **Probe**: diff_srv_rate tăng vọt do quét nhiều cổng.
- **U2R**: thời lượng dài, lượng bytes thấp, xuất hiện cờ khẩn cấp (urgent flags).

</div>

</div>

</div>

<div class="text-xs text-gray-500 mt-1">
  Tài liệu tham khảo: Tavallaee et al. (2009) — NSL-KDD dataset · Breiman (2001) — Random Forests
</div>

</div>

---

# 1 · Thực nghiệm — Phân loại Xâm nhập Mạng

<div class="flex flex-col justify-center h-[400px]">

<div class="mt-1">
  <iframe
    src="http://127.0.0.1:8000/?embed=true&tab=intrusion"
    class="w-full rounded-lg border border-gray-700"
    style="height: 380px;"
    allow="clipboard-write"
  />
</div>


</div>

---

# 2 · UEBA Anomaly Detection — Đặc trưng Đầu vào

<div class="grid grid-cols-2 gap-4 mt-2">

<div>

<div class="text-xl font-bold mb-2 text-blue-300">Vectơ hóa 9 đặc trưng đăng nhập</div>

<div class="text-[15px] compact-table">

| Đặc trưng | Ý nghĩa giám sát an ninh |
|---|---|
| `hour_of_day` | Thời gian đăng nhập trong ngày |
| `is_weekend` | Cờ nhận diện ngày cuối tuần |
| `country_distance_km` | Khoảng cách địa lý di chuyển |
| `device_change` | Sự thay đổi vân tay thiết bị |
| `failed_attempts` | Tần suất đăng nhập thất bại |
| `session_duration_min` | Thời lượng phiên tương tác |
| `bytes_downloaded_mb` | Dung lượng tải xuống |
| `unusual_hour` | Cờ đăng nhập ngoài giờ làm việc |
| `vpn_used` | Cờ sử dụng kết nối VPN |

</div>

</div>

<div class="flex flex-col justify-center p-4 border border-blue-500/25 bg-blue-500/5 rounded-xl h-fit my-auto">
  <div class="text-sm font-bold text-blue-400 mb-2">Mục tiêu Giám sát UEBA</div>
  <div class="text-xs text-gray-300 space-y-2">
    <div>• <strong>Dấu vân tay hành vi</strong>: Xây dựng hồ sơ hoạt động duy nhất cho từng tài khoản người dùng thực tế.</div>
    <div>• <strong>Phát hiện tinh vi</strong>: Nhận diện các bất thường về thời gian, khoảng cách địa lý (đăng nhập bất khả thi) và đột biến tải tài nguyên.</div>
    <div>• <strong>Bảo vệ nâng cao</strong>: Ngăn chặn triệt để hành vi lạm dụng tài khoản hợp pháp (Compromised credentials) - nơi các chữ ký tĩnh bất lực.</div>
  </div>
</div>

</div>

<div class="text-xs text-gray-500 mt-4">
  Tài liệu tham khảo: Liu, Ting, Zhou (2008) — Isolation Forest · Chandola et al. (2009)
</div>

<style scoped>
.compact-table th, .compact-table td {
  padding-top: 1px !important;
  padding-bottom: 1px !important;
  line-height: 1.4 !important;
}
</style>

---

# 2 · UEBA Anomaly Detection — Thuật toán Cô lập

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-2 gap-4">

<div class="space-y-3">

<div class="p-3.5 rounded-lg border border-gray-600 border-opacity-30 bg-gray-800 bg-opacity-30">
  <div class="font-bold text-sm text-gray-400 mb-1">Cơ chế hoạt động của Isolation Forest</div>
  <div class="text-xs text-gray-300">Tập trung cô lập các điểm dữ liệu bất thường thay vì vẽ biên phân lớp thông thường. Điểm dữ liệu khác biệt sẽ dễ bị cô lập bằng các nhát cắt ngẫu nhiên → đường dẫn tới lá ngắn → điểm bất thường cao.</div>
</div>

<div class="p-3.5 rounded-lg border border-green-500 border-opacity-30 bg-green-500 bg-opacity-5">
  <div class="font-bold text-sm text-green-400 mb-1">Phương thức huấn luyện tối ưu</div>
  <div class="text-xs text-gray-300">Huấn luyện hoàn toàn không giám sát (Unsupervised) trên <strong>5.000 mẫu đăng nhập lành tính</strong>. Mô hình tự học phân phối bình thường mà không cần gán nhãn trước.</div>
</div>

</div>

<div class="flex flex-col justify-center items-center h-full pl-4">
  <div class="p-4 rounded-xl border border-blue-500 border-opacity-30 bg-blue-500 bg-opacity-5 w-full">
    <div class="text-sm font-bold text-blue-400 mb-2">Đánh giá Mô hình Thực nghiệm</div>
    <div class="text-xs text-gray-300 space-y-1">
      <strong>Thuật toán: Isolation Forest (200 cây quyết định)</strong><br/>
      Khả năng nhận diện: độ phủ <strong class="text-green-400">80%</strong> trên các kịch bản giả lập tấn công (Mass exfiltration, Unusual hour login).
    </div>
  </div>
</div>

</div>

<div class="text-xs text-gray-500 mt-2">
  Tài liệu tham khảo: Liu, Ting, Zhou (2008) — Isolation Forest · Chandola et al. (2009)
</div>

</div>

---

# 2 · Thực nghiệm — UEBA Anomaly Detection

<div class="flex flex-col justify-center h-[400px]">

<div class="mt-1">
  <iframe
    src="http://127.0.0.1:8000/?embed=true&tab=behavior"
    class="w-full rounded-lg border border-gray-700"
    style="height: 380px;"
    allow="clipboard-write"
  />
</div>


</div>

---

# 3 · Quản lý Lỗ hổng Bảo mật & Dự báo Khai thác

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-2 gap-4">

<div class="space-y-3">

<div class="p-3.5 rounded-lg border border-gray-600 border-opacity-30 bg-gray-800 bg-opacity-30">
  <div class="font-bold text-sm text-gray-400 mb-1">Thang điểm CVSS truyền thống (Tĩnh)</div>
  <div class="text-xs text-gray-300">Điểm mức độ nghiêm trọng được cố định khi công bố. Không phản ánh sự thay đổi thực tế trên internet, không trả lời được câu hỏi lỗ hổng nào đang thực sự bị khai thác ngoài đời thực.</div>
</div>

<div class="p-3.5 rounded-lg border border-blue-500 border-opacity-30 bg-blue-500 bg-opacity-5">
  <div class="font-bold text-sm text-blue-400 mb-1">Mô hình Học máy Dự báo (Động)</div>
  <div class="text-xs text-gray-300">Liên tục cập nhật xác suất dựa trên thông tin thời gian thực. Giúp doanh nghiệp tối ưu hóa nguồn lực bằng cách ưu tiên vá các lỗ hổng có khả năng bị tấn công cao nhất trước.</div>
</div>

</div>

<div class="flex flex-col justify-center items-center h-full pl-4">
  <img src="/media/image10.png" class="rounded-lg border border-gray-700 shadow-lg max-h-70 object-contain" />
  <div class="text-center text-xs text-gray-400 mt-2">
    Quy trình phân tích động và dự báo mã khai thác CVE
  </div>
</div>

</div>

</div>

---

# 4 · Phishing URL Detection

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-2 gap-4">

<div>

### Phân tích cú pháp URL thành 11 đặc trưng

<div class="p-2.5 rounded-lg bg-gray-800 font-mono text-xs mt-1">
<span class="text-red-400">http</span>://<span class="text-yellow-400">paypal-secure-login</span>.<span class="text-red-400">xyz</span>/verify?id=abc
</div>

<div class="text-xs space-y-0.5 mt-1.5">

| Tín hiệu nhận dạng | Tên đặc trưng | Giá trị |
|---|---|---|
| Không dùng HTTPS | `has_https` | 0 |
| Xuất hiện ký tự `-` | `num_hyphens` | 2 |
| Tên miền phụ đáng ngờ | `tld_suspicious` | 1 |
| Chứa từ khóa nhạy cảm | `suspicious_kw_count` | 3 |
| Ký tự truy vấn dữ liệu | `num_equals` | 1 |

</div>

<div class="mt-2 text-xs text-gray-400">
<strong>Đặc điểm nổi bật:</strong> Mô hình chỉ phân tích đặc trưng từ vựng của chuỗi URL thô mà không cần gửi yêu cầu HTTP truy cập trực tiếp. Thời gian phản hồi <strong>&lt;1ms</strong>, an toàn cho tích hợp inline.
</div>

</div>

<div class="flex flex-col justify-center items-center h-full pl-4">
  <img src="/media/image11.png" class="rounded-lg border border-gray-700 shadow-lg max-h-70 object-contain" />
  <div class="text-center text-xs text-gray-400 mt-2">
    Kiến trúc trích xuất đặc trưng từ vựng và phân loại Phishing
  </div>
</div>

</div>

</div>

---

# 4 · Thực nghiệm — Phishing URL Detection

<div class="flex flex-col justify-center h-[400px]">

<div class="mt-1">
  <iframe
    src="http://127.0.0.1:8000/?embed=true&tab=phishing"
    class="w-full rounded-lg border border-gray-700"
    style="height: 380px;"
    allow="clipboard-write"
  />
</div>


</div>

---

# 5 · AI-based Antivirus

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-2 gap-4">

<div class="space-y-3">

<div class="p-3 rounded-xl border border-gray-600 border-opacity-30">
  <div class="text-sm font-bold text-gray-400 mb-1">Hệ thống AV truyền thống</div>
  <div class="space-y-0.5 text-xs text-gray-300">
    <div>• Đối sánh mã hash và chuỗi nhị phân tĩnh</div>
    <div>• Chỉ nhận biết được các biến thể độc hại đã biết</div>
    <div>• <span class="text-red-400">Thất bại trước mã độc Zero-day</span></div>
    <div>• <span class="text-red-400">Dễ bị vượt qua bằng cách đổi bytes ngẫu nhiên</span></div>
  </div>
</div>

<div class="p-3 rounded-xl border border-blue-500 border-opacity-30 bg-blue-500 bg-opacity-5">
  <div class="text-sm font-bold text-blue-400 mb-1">AI-based Antivirus</div>
  <div class="space-y-0.5 text-xs text-gray-300">
    <div>• <strong>Phân tích Tĩnh (Static)</strong>: PE features (PE header) → Random Forest</div>
    <div>• <strong>Phân tích Động (Dynamic)</strong>: API-call sequences → LSTM</div>
    <div>• <span class="text-green-400">Nhận diện mã độc chưa từng công bố</span></div>
    <div>• <span class="text-green-400">Khả năng khái quát hóa cực kỳ cao</span></div>
  </div>
</div>

</div>

<div class="flex flex-col justify-center items-center h-full pl-4">
  <img src="/media/image12.png" class="rounded-lg border border-gray-700 shadow-lg max-h-70 object-contain" />
  <div class="text-center text-xs text-gray-400 mt-2">
    Mô hình lai kết hợp phân tích PE tĩnh và LSTM động
  </div>
</div>

</div>

</div>

---

# 6 · Adversarial ML & Cuộc đua Vũ trang CTI

<div class="flex flex-col justify-center h-[380px]">

<div class="grid grid-cols-2 gap-4">

<div class="space-y-3">

<div class="p-3 rounded-xl border border-red-500 border-opacity-30 bg-red-500 bg-opacity-5">
  <div class="text-sm font-bold text-red-400 mb-1">Kẻ tấn công lạm dụng AI</div>
  <div class="space-y-0.5 text-xs text-gray-300">
    <div>🤖 Dùng LLM tự động hóa viết email lừa đảo tinh vi</div>
    <div>🔄 Công cụ tạo mã độc đa hình tự biến đổi liên tục</div>
    <div>🎯 Thiết kế các mẫu đối kháng đánh lừa bộ phân loại</div>
  </div>
</div>

<div class="p-3 rounded-xl border border-green-500 border-opacity-30 bg-green-500 bg-opacity-5">
  <div class="text-sm font-bold text-green-400 mb-1">Defenders Use AI</div>
  <div class="space-y-0.5 text-xs text-gray-300">
    <div>🔍 Phát hiện hành vi bất thường lọc các biến thể mới</div>
    <div>🛡 Huấn luyện đối kháng (Adversarial training) bền bỉ</div>
    <div>🧩 Triển khai mô hình hỗn hợp (Ensembles) giảm thiểu rủi ro</div>
  </div>
</div>

</div>

<div class="flex flex-col justify-center items-center h-full pl-4">
  <img src="/media/image13.png" class="rounded-lg border border-gray-700 shadow-lg max-h-70 object-contain" />
  <div class="text-center text-xs text-gray-400 mt-2">
    Phương thức tấn công đối kháng phá hủy mô hình Học máy phòng thủ
  </div>
</div>

</div>

</div>

---
layout: center
---

# Kết luận & Định hướng Tương lai

<div class="flex flex-col justify-center h-[380px] max-w-4xl">

<div class="grid grid-cols-3 gap-4">

<div class="p-3 rounded-xl border border-blue-500 border-opacity-30 bg-blue-500 bg-opacity-5 text-center">
  <div class="text-2xl mb-1">🎣</div>
  <div class="font-bold text-sm text-blue-400">Phishing URL Detection</div>
  <div class="text-xs text-gray-400 mt-1">Random Forest</div>
  <div class="text-xs">651K URLs thực tế</div>
  <div class="text-xl font-bold text-green-400 mt-1">96.5%</div>
  <div class="text-[10px] text-gray-500">Độ chính xác (Accuracy)</div>
</div>

<div class="p-3 rounded-xl border border-blue-500 border-opacity-30 bg-blue-500 bg-opacity-5 text-center">
  <div class="text-2xl mb-1">🛡</div>
  <div class="font-bold text-sm text-blue-400">Intrusion Classification</div>
  <div class="text-xs text-gray-400 mt-1">Random Forest (5 lớp)</div>
  <div class="text-xs">125K luồng mạng</div>
  <div class="text-xl font-bold text-green-400 mt-1">98.8%</div>
  <div class="text-[10px] text-gray-500">Độ chính xác (Accuracy)</div>
</div>

<div class="p-3 rounded-xl border border-green-500 border-opacity-30 bg-green-500 bg-opacity-5 text-center">
  <div class="text-2xl mb-1">👤</div>
  <div class="font-bold text-sm text-green-400">UEBA Anomaly</div>
  <div class="text-xs text-gray-400 mt-1">Isolation Forest</div>
  <div class="text-xs">5K logins giả lập</div>
  <div class="text-xl font-bold text-green-400 mt-1">80%</div>
  <div class="text-[10px] text-gray-500">Độ phủ (Recall)</div>
</div>

</div>

<div class="mt-4 max-w-3xl">

### Định hướng Phát triển Nghiên cứu

<div class="grid grid-cols-2 gap-3 mt-2 text-xs">
  <div>→ Sử dụng học sâu trên chuỗi ký tự URL thô (URLNet)</div>
  <div>→ Áp dụng mô hình chuỗi thời gian (LSTM/Transformer) cho luồng mạng</div>
  <div>→ Vòng lặp phản hồi của phân tích viên (Active learning - AI²)</div>
  <div>→ Triển khai dữ liệu đo lường hành vi thực tế từ SIEM doanh nghiệp</div>
</div>

</div>

</div>

---
layout: center
class: text-center
---

# Lời cảm ơn

<div class="flex flex-col justify-center h-[380px]">

<div class="text-gray-400 mt-4 text-xl font-light">
Học máy không được thiết kế để thay thế chuyên viên phân tích an ninh.<br/>
Nó là một <strong class="text-blue-400">công cụ nhân bội sức mạnh bảo mật</strong>.
</div>

<div class="mt-6 text-sm text-gray-600">

**Tài liệu tham khảo chính:**
Breiman (2001) · Liu, Ting & Zhou (2008) · Tavallaee et al. (2009) · Sahingoz et al. (2019) · Goodfellow et al. (2014)

</div>

</div>
