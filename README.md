# spellcheck-vn
Spellcheck for vietnamese or a custom dictionary.

# Install dependencies
```bash
pip3 install -r requirements.txt
```

# Usage
## Init dictionary from vocab file
```bash
python3 --infile="a_vocab_file" \
	--update-dict=True \
	--odfile="your_dict_file.json" \
	--ovfile="o_vocab_file"
```	

## Update dicitonary
```bash
python3 --infile="a_vocab_file" \
	--dict-file="i_dict_file.json" \
	--update-dict=True \
	--odfile="o_dict_file.json" \
	--ovfile="o_vocab_file"
```
Example output logging:
```log
INFO:__main__:Adding `bênh` to dict
INFO:__main__:`bệnh` not in dictionary
INFO:__main__:Adding `bệnh` to dict
INFO:__main__:`béo` not in dictionary
INFO:__main__:Adding `béo` to dict
INFO:__main__:`bèo` not in dictionary
INFO:__main__:Adding `bèo` to dict
INFO:__main__:`bếp` not in dictionary
INFO:__main__:Adding `bếp` to dict
INFO:__main__:`bẹp` not in dictionary
INFO:__main__:Adding `bẹp` to dict
```

## Spell checking
```bash
python3 --infile="a_vocab_file" \
	--dict-file="i_dict_file.json" \
	--odfile="o_dict_file.json" \
	--ovfile="o_vocab_file"
```
Example results:
```log
INFO:__main__:xu_dong_duong.txt:41 -- Tá c giả: Paul Doumer
INFO:__main__:`c` not found, but maybe cằn|cúi|cúng|cúc|cút|cựu|cực|cài|cày|cà|cào|cành|càng|cãi|còi|còn|còng|cò|còm|cợt|cõi|cõng|cổng|cổ|cuộn|cuộc|cuối|cuốn|cuống|cuốc|cung|cuồn|cuồng|cua|cùng|cù|cùm|cũi|cũng|cũ|cội|cộng|cộ|cộc|cột|cải|cảnh|cảng|cả|cảo|cảm|cớ|câu|cây|cân|câm|cậu|cận|cập|cậy|cật|cứu|cứng|cứ|cồn|cồng|chằng|chúa|chúng|chú|chút|chúi|chúc|chen|che|chìa|chì|chìm|chỉnh|chỉn|chỉ|chãi|chã|chão|chòi|chòng|chợn|chợ|chợt|chõng|chổng|chua|chuồn|chuồng|chung|chu|chuẩn|chuỗi|chuộng|chuộc|chuột|chuối|chuốc|chuốt|chuyên|chuyển|chuyến|chuyện|chuông|chính|chín|chí|chích|chùa|chùng|chùm|chiêu|chiêng|chiêm|chia|chinh|chi|chiểu|chiều|chiền|chiếu|chiến|chiếc|chiếm|chim|chế|chếch|chết|chực|chội|chộp|chẳng|chới|chớp|chớ|chớm|chề|châu|chân|châm|chệch|chậu|chập|chậm|chật|chứa|chứng|chứ|chức|chồng|chồm|chênh|chê|chặn|chặng|chặt|chấp|chấn|chấm|chất|chạ|chạp|chạy|chạm|chạnh|chối|chốn|chống|chốc|chốt|chở|chởm|chửa|chửi|chừa|chừng|chẩy|chéo|chép|chén|chém|chọi|chọn|chọc|chảo|chảy|chải|chèo|chè|chào|chày|chàng|chài|chàm|chủng|chủ|choáng|chong|cho|choàng|chĩa|chụp|chục|chụm|cháu|cháy|chánh|chán|chác|chẻ|chểnh|chắp|chắn|chắc|chịu|chị|chịt|chau|chao|chan|cha|chai|chay|chóng|chó|chóp|chói|chót|chóc|chữa|chững|chữ|chỗ|chôn|chông|chơi|chơ|chầu|chầy|chầm|chẽn|chẽ|chưởng|chướng|chước|chư|chương|chưa|chỏm|chăn|chăng|chăm|chờn|chờ|cạo|cạnh|cạn|cạm|cối|cống|cố|cốc|cốt|cởi|cừ|cẩu|cẩn|cẩm|cặp|cặn|cửu|cửa|của|củng|coi|con|cong|co|com|cụ|cục|cụm|cụt|cáu|cáo|cánh|cá|cám|cáp|cái|cát|cách|các|cấu|cấp|cấy|cấm|cất|cao|canh|can|ca|cai|cay|cam|cỡ|cắp|cắn|cắm|cắt|cữ|cỗi|côn|công|cô|cơn|cơ|cơm|cói|cóng|có|cầu|cầy|cần|cầm|cọng|cọp|cọ|cọc|cọt|cưa|cưỡi|cưỡng|cưng|cưới|cướp|cước|cưu|cược|cương|cười|cường|cỏi|cỏn|cỏ|căn|căng|căm|cờ !
INFO:__main__:`paul` not in dictionary
INFO:__main__:`doumer` not in dictionary
```
