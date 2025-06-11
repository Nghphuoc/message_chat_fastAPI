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