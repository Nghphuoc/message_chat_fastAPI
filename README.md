✅ 1. Đăng ký / Đăng nhập
Người dùng tạo tài khoản → thêm bản ghi vào tb_users với các thông tin như username, password, email, phone, role_id,...

Đăng nhập thành công → cập nhật trạng thái trong tb_user_status (is_online = 1, last_seen = NOW()).

✅ 2. Tạo phòng chat
Người dùng tạo phòng → thêm bản ghi vào tb_chat_rooms (có thể là nhóm is_group = 1 hoặc cá nhân is_group = 0).

Hệ thống thêm người dùng vào phòng thông qua bảng tb_user_room (user_id, room_id, joined_at).

✅ 3. Mời hoặc thêm người vào phòng chat
Thêm người dùng vào tb_user_room với room_id tương ứng.

✅ 4. Gửi tin nhắn
Người dùng gửi tin nhắn → thêm bản ghi vào tb_messages:

user_id: người gửi

room_id: phòng chat

content, file_url, created_at, message_id...

✅ 5. Phản ứng với tin nhắn (Reaction)
Người dùng phản ứng với tin nhắn → thêm vào tb_reaction:

user_id, message_id, emoji, created_at

✅ 6. Xem trạng thái người dùng (online / offline)
Trạng thái lưu ở tb_user_status:

is_online, last_seen, user_id

✅ 7. Kết bạn
Người dùng gửi lời mời kết bạn → thêm vào tb_friendships:

user_id, friend_id, status = 'pending'

Người nhận chấp nhận → cập nhật status = 'accepted'

Có thể chặn (blocked) hoặc hủy kết bạn.

✅ 8. Phân quyền người dùng
Vai trò của người dùng lưu trong tb_roles (admin, moderator,...) thông qua role_id trong tb_users.

✅ 9. Rời khỏi phòng chat
Người dùng rời phòng → xóa bản ghi tương ứng trong tb_user_room.

✅ 10. Xóa hoặc vô hiệu hóa tài khoản
Cập nhật flagDelete trong tb_users:

'not_active', 'active', 'delete'


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


## user_room

| Trường         | Ý nghĩa                             | Cần điền gì                          |
| -------------- | ----------------------------------- | ------------------------------------ |
| `user_room_id` | ID duy nhất của quan hệ user - room | UUID hoặc auto-gen                   |
| `user_id`      | ID của từng người dùng              | Ghi **2 dòng**, 1 dòng cho mỗi người |
| `room_id`      | ID của phòng vừa tạo                | Trùng nhau cho cả 2 người            |
| `joined_at`    | Thời điểm người đó tham gia         | `NOW()` hoặc thời điểm accept        |
