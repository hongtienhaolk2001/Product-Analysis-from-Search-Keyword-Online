# useful lib
import os
import csv
import pandas as pd
# translate lib
from googletrans import Translator as Tran_gg
from translate import Translator

#data
dict_catgories = {'thời trang': {'thời trang nam': {'quần', 'áo', 'sơmi',
                                                    'kaki', 'sơ mi', 'khoác',
                                                    'jean', 'quần dài', 'tay dài',
                                                    'tay ngắn', 'thun', 'áo thun',
                                                    'thể thao', 'hoodie', 'áo polo',
                                                    'sweater', 'khoác dù', 'quần ngắn'},

                                 'thời trang nữ': {'đầm', 'váy', 'khoác',
                                                   'áo thun', 'áo polo', 'quần jean',
                                                   'quần thun', 'quần ngắn', 'áo kiểu',
                                                   'áo croptop', 'áo sweater', 'bomber',
                                                   'khoác dù', 'sơ mi', 'ngắn tay', 'dài tay', },

                                 'trẻ em': {'tã', 'bỉm', 'bỉm vải',
                                            'tã vải', 'bỉm hữu cơ', 'yếm sơ sinh',
                                            'tấm lót chống thấm', 'khăn xô', 'tả dán',
                                            'mũ bo', 'khăn sữa'},

                                 'đồng hồ': {'nhựa', 'sapphire', 'kính khoáng',
                                             'đồng hồ kim', 'đồng hồ điện tử', 'da tổng hợp',
                                             'thép không gỉ', 'dây cao su ', 'dây vải',
                                             'atm', 'chronograph', 'kim dạ quang', 'Bấm giờ thể thao',
                                             'cơ lộ máy', 'cơ tự động', 'năng lượng mặt trời', 'đồng hồ'},

                                 'túi xách': {'túi bao tử', 'túi chống thấm', 'túi da',
                                              'da sáp', 'túi vải', 'túi đeo chéo', 'túi xách'},

                                 'giày dép': {'dép kẹp', 'quai ngang', 'đế cao su', 'giày dép',
                                              'xăng đan', 'sneaker', 'cao cổ', 'sandal',
                                              'giày da', 'dép da', 'dép cao su'},

                                 'phụ kiện': {'móc khóa', 'kính', 'kính mát', 'kính thể thao',
                                              'gọng kính', 'tròng kính', 'kính râm',
                                              'kính vận', 'ví', 'ví da', 'mũ len',
                                              'ví cầm tay', 'ví da bò sáp', 'ví vải',
                                              'mũ ', 'nón', 'mũ lưỡi trai', 'snapback', },

                                 'trang sức': {'bông tai', 'nhẫn', 'mặt dây chuyền',
                                               'lắc', 'vòng', 'dây cổ', 'dây chuyền',
                                               'cài áo', 'kiềng', 'móc khóa', 'kara'},

                                 'balo': {'daypack', 'balo laptop', 'balo quân sự', 'balo du lịch',
                                          'balo quai chéo', 'dây rút', 'balo chống nước', 'vali'},
                                 'thời trang khác': []
                                 },

                  'mỹ phẩm': {'chăm sóc da': {'sửa rửa mặt', 'lotion', 'kem dưỡng ẩm',
                                              'mặt nạ', 'toner', 'nước hoa hồng',
                                              'bông tẩy trang', 'nước tẩy trang', 'mụn',
                                              'trị mụn', 'kem trị mụn', 'thâm',
                                              'trị thâm', 'kem trị thâm', 'bỏng',
                                              'phỏng', 'sẹo', 'kem trị sẹo', 'vitamic c',
                                              'cấp ẩm', 'xịt khoáng', 'lột mụn', 'son dưỡng', },

                              'chăm sóc tóc': {'dầu gội', 'dầu gội bưởi', 'kích mọc tóc',
                                               'kích thích mọc tóc', 'hair tonic',
                                               'pomelo', 'dầu xả'},

                              'làm đẹp': {'mascara', 'son', 'son bóng',
                                          'chuốt mi', 'kem nền', 'kem lót',
                                          'kem che khuyết điểm', 'chải mi', 'phấn mắt',
                                          'bút chì kẻ mắt', 'kẻ mắt', 'bút kẻ mắt',
                                          'chì trượt kẻ mày', 'kẻ mày',
                                          'phấn phủ', 'bảng phấn mắt', 'miếng dán mun',
                                          'son kem', 'son môi nhung', 'son lì',
                                          'phấn', 'bảng phấn', 'cọ trang điểm',
                                          'kem bắt sáng', 'bọt biển trang điểm',
                                          'phấn tạo khối', 'bông tẩy trang'},

                              'son': {'son dưỡng', ' son lì', '3ce', 'mac', 'ysl',
                                      'son môi', 'son bóng', 'son tint', 'son kem lì',
                                      'son kem', 'son dưỡng ẩm', 'son nước', 'son thỏi',
                                      'black rouge', 'tone', 'vaseline', 'tom ford',
                                      'son mịn', 'son bút chì', 'nội địa trung',
                                      'son gương', 'son chống thấm', 'dior', 'gucci',
                                      'ofelia', 'siêu lì', 'handmade', 'không chì',
                                      'velvet', 'son bút', 'son gió', 'son lót', 'son lụa'
                                      },

                              'nước hoa': {'tinh dầu', 'dầu thơm', 'xịt thơm', 'nước hoa mini',
                                           'nước hoa nữ', 'chanel', 'toàn thân', 'nước hoa nam',
                                           'nước hoa khô', 'body mist', 'ysl', 'dior', 'replica',
                                           'luxury', 'gucci', 'chanel'},

                              'phấn': {'phấn nền', 'phấn lót', 'phấn thơm', 'phấn nước',
                                       'phấn phủ', 'kiềm dầu', 'phấn bắt sáng', 'phấn mắt',
                                       'phấn da', 'phấn bột', 'che khuyết điểm', 'phấn má hồng',
                                       'gel', 'phấn rôm', 'chất lì', 'phấn nén', 'mắt nhũ',
                                       'phấn lạnh', 'seurum', 'phấn mịn', 'nâng tone',
                                       'cusion', 'phấn tạo khối', 'phủ khoáng', 'chống lão hoá',
                                       'siêu mịn'},
                              'mỹ phẩm khác': []
                              },

                  'công nghệ': {'điện thoại': {'iPhone', 'Android', 'iOS', 'samsung',
                                               'xiaomi', 'redmi', 'note', 'helio', 'snapdragon',
                                               'vivo', 'realme', 'nokia', 'oppo', 'ram',
                                               'pisen', 'hoco', '128GB', '256GB', '512GB',
                                               'galaxy', 'huawei', 'viettel', 'pro',
                                               'flag chip', 'lg', 'sony', 'ultra', 'ss', 'thoại'},

                                'phụ kiện điện thoại': {'sim', 'thẻ nhớ', 'sạc', 'dự phòng',
                                                        'bút cảm ứng', 'que chọc sim', 'dây quấn',
                                                        'ốp lưng', 'kính cường lực', 'giá đỡ',
                                                        'cáp sạc', 'tai nghe', 'loa', 'pin',
                                                        'túi đựng', 'củ sạc nhanh', 'led usb',
                                                        'kẹp điện thoại', 'bao da'},

                                'laptop': {'msi', 'dell', 'lenovo', 'acer', 'asus', 'vostro',
                                           'hp', 'pavilion', 'apple', 'macbook', 'latitude',
                                           'panasonic', 'thinkpad', 'core I', 'AMD', 'card rời',
                                           'vaio', 'intel', 'laptop'},

                                'máy tính': {'case', 'desktop', 'máy bộ', 'máy ráp',
                                             'vga', 'gtx', 'pc', 'thùng máy', 'tản nước',
                                             'server', 'máy tính nhúng', 'máy tính mini',
                                             'workstation', 'máy đồng bộ', 'máy văn phòng', 'máy tính'},

                                'camera': {'full hd', '4k', '60fps', 'độ phân giải', 'camera',
                                           'hikvision', 'camera wifi', 'webcame',
                                           'camera hành trình', 'camera 360', 'kinect',
                                           'camera ban đêm', 'camera râu', 'smart camera',
                                           'camera ngoài trời', 'camera giám sát',
                                           'mini camera', 'camera oto', 'camera nội soi', 'flycam'},

                                'điện tử': {'đèn led', 'mic karaoke', 'ổ cắm thông minh',
                                            'sạc bình', 'chuyển nguồn', 'sạc đa năng',
                                            'loa điện tử'},
                                'công nghệ khác': []

                                },

                  'gia dụng': {'thiết bị điện gia đình': {'quạt điện', 'nồi cơm điện', 'bếp từ',
                                                          'bếp hồng ngoại', 'ấm siêu tốc',
                                                          'tivi', 'tủ lạnh', 'máy giặt',
                                                          'máy sấy', 'lò nướng', 'lò vi sóng',
                                                          'đèn', 'máy hút bụi', 'máy ép'},

                               'dụng cụ bếp': {'nồi', 'niêu', 'xoong', 'chảo',
                                               'dĩa', 'muỗng', 'đũa', 'thìa',
                                               'môi', 'chén', 'bát', 'tô', 'dao',
                                               'thớt', 'bếp gas', 'máy xay thịt',
                                               'bào rau củ', 'kệ treo tường', 'hộp đựng dao',
                                               'máy đánh trứng', 'móc treo', 'bếp nướng than'},

                               'bột giặt': {'omo', 'tide', 'downy', 'viso', 'suft',
                                            'nước giặt', 'bột giặt máy', 'lix',
                                            'bột tẩy', 'omo matic', 'attack',
                                            'aba', 'joins', 'ariel', 'viên giặt',
                                            'comfort', 'pao', 'bột giặt'},

                               'nước lau sàn': {'gif', 'sunlight', 'nước lau sàn chanh sả',
                                                'nước lau sàn hữu cơ', 'gabi đậm đặc',
                                                'sinh học', 'swat', 'lifeboy', 'nước lau sàn'},
                               'gia dụng khác': []

                               },

                  'bách hoá': {'thực phẩm': {'thực phẩm chức năng', 'thực phẩm bảo vệ sức khoẻ',
                                             'màu thực phẩm', 'đồ ăn vặt', 'khô', 'bánh tráng',
                                             'sữa', 'trứng', 'khô cá', 'khô bò', 'ruốc',
                                             'xúc xích', 'cơm cháy', 'khô mực', 'sấy',
                                             'rong biển', 'snack', 'chà bông', 'hạt dẻ',
                                             'hạt điều', 'thịt heo', 'khô rim', 'khô gà',
                                             'đậu', 'thịt xông khói', 'tai heo', 'khô cá',
                                             'thực phẩm chay', 'thực phẩm'},

                               'gia vị': {'đường', 'muối', 'hạt nêm', 'bột ngọt', 'nước mắm',
                                          'nước tương', 'hành', 'tỏi', 'ớt', 'hạt dổi', 'gia vị',
                                          'mắc khén', 'chanh', 'sả', 'gừng', 'quế', 'hồi',
                                          'bột gia vị', 'nước nêm', 'nước gia vị',
                                          'nước lẩu', 'nước nêm cô đặc', 'ngũ vị hương',
                                          'tiêu', 'hành', 'nghệ', 'xốt mayonnaise',
                                          'xốt chua ngọt', 'mắc mật', 'gia vị cà ri',
                                          'gia vị lẩu', 'gia vị nấu phở', 'tương trộn',
                                          'muối hồng', 'thảo quả', 'xốt ướp nướng',
                                          'xốt gia vị hoàn chỉnh'},

                               'bánh kẹo': {'kẹo dẻo', 'kẹo sấy', 'thạch dừa', 'bánh ống', 'bánh kẹo',
                                            'biscotti', 'mứt sấy', 'sấy dẻo', 'trái cây sấy',
                                            'bánh quy bơ', 'bánh tráng', 'socola', 'marshmallow',
                                            'bánh quy', 'mentos', 'bánh rế', 'bánh khoai tây',
                                            'bánh gấu', 'kẹo bi', 'thạch', 'bánh pía', 'kẹo bạc hà',
                                            'bim bim', 'kitkat', 'kẹo dứa', 'phô mai', 'kẹo sữa bò',
                                            'bánh hạnh nhân', 'mứt dâu tây', 'sing gum',
                                            'bánh đa', 'kẹo nougat', 'mè xửng'},
                               'bách hoá khác': []

                               },

                  'phương tiện': {
                      'oto': {'lưới tản nhiệt', 'cản xe ô tô', 'nắp ca-pô', 'đèn pha ô tô',
                              'kính chắn gió xe ô tô', 'gương chiếu hậu', 'cản trước',
                              'đèn pha', 'đèn chạy ban ngày', 'phanh bánh trước',
                              'mâm', 'bánh trước', 'bảng điều khiển trung tâm',
                              'khung ghế', 'vô lăng', 'cabin', 'phanh bánh sau',
                              'bộ nạp phụ', 'nắp cốp sau', 'ăng ten', 'túi khí',
                              'màn oled', 'táp lô', 'bàn đạp phanh', 'ly hợp',
                              'bàn đạp ga', 'chân phanh', 'cần số', 'ghế ngồi',
                              'khung liền vỏ', 'khung rời vỏ', 'dây đai an toàn',
                              'gioăng cao su', 'trần xe', 'cửa gió điều hoà',
                              'phuộc trước', 'phuộc sau', 'mâm ép', 'bố ly hợp', 'bố thắng trước',
                              'bố thắng sau', 'cao su chân máy', 'rotuyn lái trong', 'đồng hồ taplo',
                              'cảm biến abs', 'ốc lạnh', 'quạt dàn lạnh', 'dàn lạnh',
                              'dàn lạnh sau', 'dàn nóng', 'van tiết lưu', 'đèn pha', 'đèn lái',
                              'đèn cản', 'cản trước', 'cửa xe', 'kính chiếu hậu', 'đuôi cá',
                              'sét gạt mưa', 'lọc gió động cơ', 'lọc gió', 'lọc nhiên liệu',
                              'láp ngang cầu sau', 'láp dọc đồng bộ', 'cao su chân máy trước',
                              'mâm ép', 'búp sen thắng sau', 'honda', 'Hyundai', 'Ford', 'Toyota',
                              'Suzuki', 'Isuzu', 'KIA', 'Mercedes Benz', 'Cooper', 'Audi', 'BMW', 'Lamborghini',
                              'Jaguar', 'Aston Martin', 'Vinfast', 'Mitsubishi', 'Chevrolet', 'Lexus',
                              'Mazda', 'Nissan', 'Peugeot', 'Porsche', 'Ferrari', 'ôtô', 'oto', 'ô tô'
                              },

                      'xe máy': {'công tắc máy', 'song song khoá cổ', 'chìa khoá yên', 'xe máy',
                                 'cụm công tắc cốt', 'pha', 'công tắc kèn', 'công tắc quẹo',
                                 'công tơ mét', 'cụm công tắc đèn chính', 'nút đề', 'tay ga',
                                 'tay thắng trước', 'bửng', 'vít ráp móc treo', 'bàn đạp thắng sau',
                                 'chổ để chân', 'công tắc đèn stop', 'giò đạp', 'gác chân', 'dè sau',
                                 'khung giữ khi dựng hay đẩy xe', 'baga trước', 'chỗ đựng đồ nghề',
                                 'khoá yên', 'khung gắn gát chân', 'chân chống đứng',
                                 'chỗ để chân', 'cần sang số', 'khoá xăng', 'lọc xăng', 'kính chiếu hậu',
                                 'yên xe', 'cao su giảm chấn yên xe', 'nắp xăng',
                                 'các chi tiết cố định và di động', 'các chi tiết của nền tảng cung cấp khí',
                                 'bộ phận làm trơn, sử dụng mát', 'hệ thống nhiên liệu',
                                 'bộ phận đánh lửa', 'bánh sau', 'bánh trước', 'vành bánh xe',
                                 'tay phanh/phanh tay', 'phanh chân', 'xích xe', 'chân chống',
                                 'côn xe', 'phanh đĩa', 'phanh tang trống', 'động cơ', 'chắn bùn',
                                 'bình xăng', 'cần số', 'ghi-đông', 'tay cầm', 'đèn pha trước',
                                 'đèn cảnh báo', 'săm xe', 'bộ phận giảm thanh', 'gương chiếu hậu',
                                 'kính chắn gió', 'yên xe', 'giảm xóc', 'phuộc', 'bảng đồng hồ',
                                 'công tơ mét', 'đồng hồ tốc độ', 'đồng hồ đo',
                                 'đồng hồ chỉ giờ', 'đồng hồ nhiên liệu', 'căm', 'nan hoa',
                                 'đèn chiếu hậu', 'đèn xi nhan', 'phuộc trước', 'phuộc sau',
                                 'phanh trước', 'phanh sau', 'ống pô', 'chỗ để chân trước',
                                 'gác chân sau', 'khung sườn', 'công tắc đề', 'bình ắc quy',
                                 'pít tông', 'bạc pít tông', 'lọc gió', 'khoá xăng', 'bình xăng con',
                                 'van', 'van nạp', 'van xả', 'tay dên', 'bánh răng trục cam', 'trục cam',
                                 'tay quay', 'bánh đà', 'buồng xi-lanh', 'bugi', 'hộp số', 'bộ ly hợp', 'bộ nồi',
                                 'phân khối', 'loại động cơ', 'công suất tối đa', 'tỉ số nén',
                                 'mô-men xoắn cực đại', 'đường kính x hành trình piston',
                                 'giới hạn vòng tua máy', 'tốc độ tối đa', 'van trên mỗi xi-lanh',
                                 'hệ thống phun xăng', 'hệ thống điều khiển khí', 'hệ thống bơm nhớt',
                                 'hệ thống làm mát', 'hệ thống bướm ga', 'độ nghiêng chảng ba',
                                 'trọng lượng khô', 'trọng lượng ướt', 'chiều cao tổng thể',
                                 'chiều dài tổng thể', 'chiều rộng tổng thể', 'khoảng sáng gầm xe',
                                 'chiều cao yên', 'chiều dài trục cơ sở', 'khoảng cách hai bánh',
                                 'dung tích bình xăng', 'dung tích nhớt máy', 'hệ thống khởi động'
                                 },

                      'xe đạp': {'hệ thống truyền lực', 'bàn đạp', 'đùi', 'trục giữa', 'đĩa',
                                 'xích', 'líp', 'hệ thống chuyển động', 'bánh xe', ' hệ thống lái',
                                 'tay lái ', 'ghi - đông', 'cổ phuốc', 'hệ thống phanh', 'tay phanh',
                                 'dây phanh', 'khung chịu lực', 'yên', 'bánh xe', 'nan hoa', 'căm',
                                 'đũa', 'moay – ơ', 'vành', 'săm và lốp', 'líp xe'
                                 },

                      'máy bay': {'bồn nhiên liệu trước', 'bồn nhiên liệu giữa', 'cửa khoang hàng hoá',
                                  'phần làm thon cánh', 'động cơ GE', 'bộ phận hạ cánh',
                                  'hộp cánh giữa', 'bộ phận hạ cánh chính', 'cánh ổn định ngang',
                                  'đuôi máy bay', 'cửa vào hành khách', 'phần lái di chuyển',
                                  'đầu cánh', 'phần lái cố định', 'vỏ động cơ', 'cánh lái'
                                  },
                      'tàu thuỷ': {'neo', 'xích neo', 'máy neo', 'hãm xích', 'vỏ tàu',
                                   'buồng lái', 'hộp số tàu thuỷ', 'động cơ', 'li hợp',
                                   'hệ trục', 'chân vịt', 'bánh lái', 'trục thượng', 'cột buồm',
                                   'lá buồm', 'dây chằng', 'lèo mũi', 'trục hạ', 'mũi tàu',
                                   'cabin', 'nạng', 'dây bạt', 'máy lái tự động', 'con quay',
                                   'PID', 'LQG', 'cuốn chiếu', 'định vị động', 'ăng ten'
                                   },

                      'tàu hoả': {'đầu máy', 'đường ray', 'tà vẹt', 'ray', 'khổ đường ray',
                                  'toa xe lửa', 'bánh xe lửa', 'đầu máy hơi nước',
                                  'đầu máy diesel', 'bộ tản nhiệt',
                                  'quạt tản nhiệt', 'động cơ diesel', 'đai tản nhiệt',
                                  'khớp nối', 'máy nén khí', 'đai truyền động',
                                  'hộp số tàu hoả', 'hãm phanh toa'
                                  },
                      'phương tiện khác': []

},

    'giải trí': {'đồ chơi': {'siêu nhân', 'rubik', 'gương nam châm',
                             'mô hình', 'thú nhồi bông', 'kính vạn hoa',
                             'lắp ráp', 'lego', 'đồ chơi nhựa dẻo',
                             'tranh cát', 'mô hình hoạt hình', 'dây cót',
                             'xếp hình', 'bộ đồ chơi nấu ăn', 'bộ đồ chơi khoa học',
                             'con vật nhựa', 'gỗ xếp chồng', 'đồ chơi bằng giấy',
                             'bóng bay', 'đèn pin', 'bút vẽ 3D', 'squid game',
                             'origami', 'đồ chơi em bé', 'đồ chơi sáng tạo',
                             'búp bê', 'barbie', 'tranh ghép hình', 'đồ chơi'
                             },

                 'sách': {'sách tiếng anh', 'văn học', 'cổ điển',
                          'trinh thám', 'viễn tưởng', 'hiện đại',
                                        'đời thường', 'truyện', 'sách giáo dục',
                                        'sách hướng nghiệp', 'self-help', 'kinh điển',
                                        'thiếu nhi', 'người lớn', 'manga', 'sách kinh tế',
                                        'sách kinh doanh', 'sách ngoại ngữ', 'phong thuỷ',
                                        'tiểu thuyết', 'ngôn tình', 'truyện ngắn',
                                        'truyện dài', ' tình cảm', 'kinh dị', 'tản văn',
                                        'tuỳ bút', 'hồi ký', 'hiện thực', 'phụ nữ', 'tuổi trẻ'
                          },

                 'thể thao': {'thể thao nam', 'thể thao nữ', 'băng keo thể thao',
                              'tai nghe thể thao', 'giày thể thao', 'vớ thể thao',
                              'đồ bộ thể thao', 'quần thể thao', 'áo thể thao',
                              'áo bóng đá', 'băng quấn chân', 'dây nhảy',
                                            'đồ tập gym', 'yoga', 'băng bảo vệ đầu gối',
                                            'quần sooc thể thao', 'quần giữ nhiệt', 'bra thể thao',
                                            'jogger', 'bình nước thể thao', 'túi đeo thể thao'
                              },

                 'du lịch': {'vali du lịch', 'túi du lịch', 'hộp đồ du lịch',
                             'balo dã ngoại', 'balo du lịch', 'võng xếp',
                             'lều cắm trại', 'gối chữ U', 'dây đai', 'máy hút chân không',
                             'dàn phơi tiện dụng', 'bếp nướng ngoài trời'
                             },
                 'giải trí khác': []

                 },

    'shop': {'giao hàng': {'giao hàng nhanh', 'giao hàng tiết kiệm',
                           'giao hàng hoả tốc', 'giao hàng bảo mật',
                           'giao hàng kín đáo', 'giao hàng siêu tốc'},

             'dịch vụ': {'dịch vụ in 3D', 'dịch vụ gói quà', 'dịch vụ nạp thẻ',
                         'dịch vụ cắt laser', 'dịch vụ in áo', 'dịch vụ viết thiệp',
                         'dịch vụ chuyển phát', 'dịch vụ in ảnh', 'dịch vụ khách hàng'},
             'shop khác': []

             },
}

if not os.path.isdir('contentss'):
    os.mkdir('contentss')
try:
    rows = []
    with open("contentss/data.csv", encoding="utf-8") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    for i in dict_catgories.keys():
        for j in range(8):
            dict_other = list(dict_catgories[i])[-1]
            if dict_other == rows[j][0]:
                dict_catgories[i][i + ' khác'].append(rows[j][j + 1])
except:
    df = pd.DataFrame(list())
    df.to_csv('contentss/data.csv')

temp = {}
for i in range(8):
    temp[list(dict_catgories)[i]] = {}
    temp[list(dict_catgories)[i]][list(dict_catgories)[i] + ' khác'] = []


def dict_to_list(dict_item):
    '''
    Thêm key (từ dictionary vào list)
    '''
    lists = []
    for key in dict_item:
        lists.append(key)
    return lists


def most_frequent(List):
    '''
    Trả về value có frequent nhiều nhất
    '''
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if curr_frequency >= counter:
            counter = curr_frequency
            num = i
    return num

    # if key_sen == 'None':
    #     print('Không có mặt hàng này')
    #     print("Các mặt hàng hiện có: ", list(dict_catgories))
    #     count = 0
    #     n = input("Nhập vào category tương ứng : ")
    #     while (n not in list(dict_catgories)):
    #         n = input('Nhập lại category tương ứng: ')
    #     dict_catgories[n][n + ' khác'].append(sen)
    #     temp[n][n + ' khác'].append(sen)
    #     df = pd.DataFrame(temp)
    #     df.to_csv('contentss/data.csv', index=True)

    # elif key_sen == 'not null':
    #     return most_frequent(key_list)

    # else:
    #     return key_sen


def content_sen_ca(sens):
    '''
    '''
    key_list = []
    keys_1 = []
    key_sen = 'None'
    model = []
    for sen in sens:
        for key1 in dict_catgories:
            keys_1.append(key1)
        for key2 in keys_1:
            a = dict_catgories.get(key2).keys()
            a = dict_to_list(a)
            for key3 in a:
                b = dict_catgories.get(key2).get(key3)
                b = dict_to_list(b)
                for sp in b:
                    if len(sen.split()) >= 2:
                        if sen in sp:
                            key_sen = key2.lower()
                        else:
                            for x in sen.split():
                                if x in sp:
                                    key_sen = 'not null'
                                    key_list.append(key2)
                    else:
                        if sen in sp:
                            key_sen = 'not null'
                            key_list.append(key2)
        if key_sen == 'not null':
            model.append(most_frequent(key_list))

        else:
            model.append(key_sen)
    
    cate = most_frequent(model)
    if cate == 'None':
        print('Không có mặt hàng này')
        print("Các mặt hàng hiện có: ", list(dict_catgories))
        count = 0
        n = input('Nhập category tương ứng: ')
        while (n not in list(dict_catgories)):
            n = input('Nhập lại category tương ứng: ')
        dict_catgories[n][n + ' khác'].append(sen)
        temp[n][n + ' khác'].append(sen)
        df = pd.DataFrame(temp)
        df.to_csv('contentss/data.csv', index=True)
        cate = n
    for mod in model:
        if mod == 'None':
            # print('Không có mặt hàng này')
            # print("Các mặt hàng hiện có: ", list(dict_catgories))
            count = 0
            n = cate
            dict_catgories[n][n + ' khác'].append(sen)
            temp[n][n + ' khác'].append(sen)
            df = pd.DataFrame(temp)
            df.to_csv('contentss/data.csv', index=True)
        else:
            pass
    return cate


#input_val = input("Nhập từ khóa: ").lower()
def model_detect(input_val):
    # Google
    translator_gg = Tran_gg()
    trans_gg_eng = translator_gg.translate(input_val, dest='en')
    trans_gg_vie = translator_gg.translate(input_val, dest='vi')
    #print('trans1_eng: ', trans_gg_eng.text)
    #print('trans1_vi: ', trans_gg_vie.text)

    # Translate
    translator = Translator(from_lang='en', to_lang="vi")
    translation = translator.translate(input_val)
    list_tran = translation.split(',')
    list_inp = []
    for inp in list_tran:
        list_inp.append(inp.strip().lower())
    #print('trans2: ', list_inp)

    list_n = ['son']
    for name in list_n:
        if name in input_val.lower():
            select_model = content_sen_ca([input_val])
            break
        elif trans_gg_eng.text.lower() == input_val.lower():
            select_model = content_sen_ca(list_inp)
        elif trans_gg_vie.text.lower() == input_val.lower():
            select_model = content_sen_ca([input_val])

    return select_model

# print(model_detect(input_val))
