
| Bảng             | Mô tả chức năng               |
| ---------------- | ----------------------------- |
| `tb_users`       | Thông tin người dùng          |
| `tb_chat_rooms`  | Danh sách phòng chat          |
| `tb_user_room`   | Người dùng tham gia phòng nào |
| `tb_messages`    | Tin nhắn trong phòng          |
| `tb_reaction`    | Phản ứng emoji với tin nhắn   |
| `tb_user_status` | Trạng thái online/offline     |
| `tb_friendships` | Danh sách bạn bè, trạng thái  |
| `tb_roles`       | Phân quyền người dùng         |


## detail more about work-flow

✅ 1. Đăng ký và Đăng nhập
🔹 Đăng ký
Khi người dùng đăng ký:

Hệ thống ghi vào tb_users:

username, password, email, phone, img_url, display_name

role_id: phân quyền mặc định (ví dụ: user)

flagDelete = 'active'

created_at = NOW()

user_id: UUID

🎯 Quan trọng: user_id là khoá chính và là điểm liên kết đến tất cả bảng khác liên quan đến người dùng.

🔹 Đăng nhập
Hệ thống kiểm tra username và password khớp trong tb_users và flagDelete = 'active'

Nếu đúng, cập nhật bảng tb_user_status:

user_id: ID người dùng

is_online = 1

last_seen = NOW()

✅ 2. Tạo phòng chat (room)
🔹 Khi người dùng tạo phòng:
Hệ thống thêm vào bảng tb_chat_rooms:

chat_room_id: UUID

name: tên phòng (nếu là group)

is_group: 1 (group chat) hoặc 0 (private chat)

created_by: user_id người tạo

created_at: thời gian tạo

Sau đó, hệ thống thêm người tạo vào bảng tb_user_room:

user_id: người tạo

room_id: chat_room_id

joined_at = NOW()

user_room_id: UUID

✅ 3. Mời thêm người vào phòng
Khi mời thêm người vào phòng:

Thêm bản ghi mới vào tb_user_room với user_id và room_id.

✅ 4. Gửi tin nhắn
🔹 Khi người dùng gửi tin nhắn:
Thêm vào bảng tb_messages:

message_id: UUID

user_id: người gửi

room_id: phòng đang chat

content: nội dung text

file_url: nếu gửi ảnh/file

created_at = NOW()

🔗 Mối liên hệ:

Tin nhắn → biết ai gửi (user_id) và thuộc phòng nào (room_id)

✅ 5. Phản ứng với tin nhắn (emoji)
🔹 Khi người dùng bấm emoji:
Thêm vào bảng tb_reaction:

reaction_id: UUID

user_id: ai gửi emoji

message_id: tin nhắn nào

emoji: ví dụ 👍, ❤️,...

created_at = NOW()

✅ 6. Xem trạng thái online
🔹 Bảng tb_user_status hoạt động như sau:
Khi người dùng đăng nhập:

is_online = 1

last_seen = NOW()

Khi thoát ứng dụng:

is_online = 0

last_seen = NOW()

✅ 7. Kết bạn
🔹 Khi gửi yêu cầu kết bạn:
Thêm vào tb_friendships:

user_id: người gửi

friend_id: người nhận

status = 'pending'

created_at = NOW()

🔹 Khi người nhận đồng ý:
Cập nhật status = 'accepted'

🔹 Khi bị chặn:
Cập nhật status = 'blocked'

⚠️ Có thể lấy danh sách bạn bè qua WHERE status = 'accepted' AND (user_id = ? OR friend_id = ?)

✅ 8. Vai trò người dùng
🔹 Khi tạo người dùng:
Gán role_id (liên kết tới tb_roles)

🔹 Trong tb_roles:
role_id liên kết với role_enum: 'admin', 'moderator', 'user'

Hệ thống có thể kiểm tra quyền khi thực hiện các thao tác nhạy cảm.

✅ 9. Xóa hoặc vô hiệu hóa người dùng
Thay vì xóa bản ghi, hệ thống cập nhật:

flagDelete = 'delete' (khóa)

flagDelete = 'not_active' (tạm thời)

Tránh mất dữ liệu và giúp khôi phục dễ dàng.

✅ 10. Rời khỏi phòng chat
Xóa bản ghi trong tb_user_room tương ứng với user_id và room_id


## WEB SOCKET

🔁 1. Pub/Sub (Publish/Subscribe) – Giao tiếp giữa các client
👉 Mục đích:
Giúp các client nhận tin nhắn theo thời gian thực mà không cần polling (hỏi liên tục).

🔧 Cách hoạt động:
Khi người dùng gửi tin nhắn, ứng dụng publish tin đó lên một channel Redis tương ứng với room_id.

Tất cả các WebSocket client đang subscribe vào channel đó sẽ nhận được tin nhắn ngay lập tức.

💬 Ví dụ:
python
Copy
Edit
await redis.publish("room_123", "hello world")
Tất cả client đang subscribe vào "room_123" sẽ nhận "hello world" tức thì.

📦 2. Lưu trữ trạng thái tạm thời (optional)
🔒 Dùng cho:
Trạng thái online/offline của người dùng

Danh sách phòng đang hoạt động

Tạm lưu message (nếu không dùng database)

Ví dụ:
python
Copy
Edit
redis.set("user:123:online", True, ex=300)  # hết hạn sau 5 phút
🧠 3. Message Queue (nâng cao)
Redis có thể kết hợp với Redis Streams hoặc Redis Lists để:

Lưu tin nhắn chưa được đọc

Làm hệ thống phân phối tin nhắn có độ bền tạm thời

⚡ Tổng Quan Vai Trò Redis Trong Chat App
Vai trò	Redis tính năng	Ghi chú
Giao tiếp real-time	Pub/Sub	Gửi tin nhắn đến nhiều client
Lưu trạng thái tạm thời	Key-Value store	Trạng thái online/offline
Hàng đợi tin nhắn (optional)	Lists/Streams	Tin nhắn chưa xử lý
Session cache (optional)	Key-Value store	Cho auth/token/session

📌 So sánh:
Cách	Ưu điểm	Nhược điểm
Redis Pub/Sub	Siêu nhanh, đơn giản	Không lưu lại message cũ
Redis Stream	Lưu tin nhắn, hỗ trợ nhiều consumer	Cấu hình phức tạp hơn
WebSocket không Redis	Dễ cho app nhỏ	Không scale được giữa servers

🌐 Khi nào dùng Redis trong WebSocket app?
Khi bạn cần nhiều client / nhiều instance server giao tiếp với nhau (scale out).

Khi cần phản hồi real-time, không delay.

Khi muốn tách logic gửi/nhận tin nhắn khỏi WebSocket.


## websocket.py
@router.websocket("/ws/{room_id}/{user_id}")
async def chat_ws(ws: WebSocket, room_id: str, user_id: str):
    # 1. Chấp nhận kết nối WebSocket
    await ws.accept()

    # 2. Đăng ký kết nối người dùng vào bộ nhớ để broadcast sau
    register(ws, room_id, user_id)

    # 3. Lặp để nhận tin nhắn liên tục từ client
    while True:
        # 4. Nhận dữ liệu dạng JSON text từ client
        raw = await ws.receive_text()
        payload = json.loads(raw)  # JSON -> dict

        # 5. Tách ra các phần: type và data
        type_ = payload["type"]
        data = payload["data"]

        # 6. Xử lý theo loại tin nhắn gửi tới
        if type_ == "send_message":
            # Gửi tin nhắn: lưu vào database, rồi publish Redis để sync
            save_to_db(data)
            await redis.publish(f"room:{room_id}", json.dumps(payload))

        elif type_ == "reaction":
            # Thả emoji: lưu vào DB và publish để các client cùng phòng nhận được
            save_reaction(data)
            await redis.publish(f"room:{room_id}", json.dumps(payload))

        elif type_ == "typing":
            # Trạng thái đang gõ: broadcast trực tiếp, không cần lưu DB hay Redis
            await broadcast(room_id, payload)


const socket = new WebSocket("ws://localhost:8000/ws/r1/u1");

socket.onmessage = (e) => {
  const { type, data } = JSON.parse(e.data);
  if (type === "new_message") showMessage(data);
  if (type === "reaction") updateReaction(data);
  if (type === "typing") showTyping(data.user_id);
};

