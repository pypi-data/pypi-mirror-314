from duowen_agent.nlp.checker import Checker
from duowen_agent.nlp.extractor import Extractor
from duowen_agent.nlp.split_sentence import SplitSentence

extractor = Extractor()

# 去除文本中的异常字符、冗余字符、HTML标签、括号信息、URL、E-mail、电话号码，全角字母数字转换为半角
clean_text = extractor.clean_text

# 抽取出文本中的所有中文字符串
extract_chinese = extractor.extract_chinese

# 提取文本中的 E-mail
extract_email = extractor.extract_email

# 提取文本中的url链接
extract_url = extractor.extract_url

# 从文本中抽取出电话号码
extract_phone_number = extractor.extract_phone_number

# 提取文本中的 IP 地址
extract_ip_address = extractor.extract_ip_address

# 提取文本中的 ID 身份证号
extract_id_card = extractor.extract_id_card

# 从文本中抽取出 QQ 号码
extract_qq = extractor.extract_qq

# 从文本中抽取出 微信号 号码
extract_wechat_id = extractor.extract_wechat_id

# 提取文本中的括号及括号内内容，当有括号嵌套时，提取每一对  成对的括号的内容
extract_parentheses = extractor.extract_parentheses

# 提取文本中的机动车牌号
extract_motor_vehicle_licence_plate = extractor.extract_motor_vehicle_licence_plate

# 删除文本中的 email
remove_email = extractor.remove_email

# 删除文本中的 url 链接
remove_url = extractor.remove_url

# 删除文本中的电话号码
remove_phone_number = extractor.remove_phone_number

# 删除文本中的 ip 地址
remove_ip_address = extractor.remove_ip_address

# 删除文本中的身份证号
remove_id_card = extractor.remove_id_card

# 删除文本中的电 QQ 号
remove_qq = extractor.remove_qq

# 删除文本中的括号及括号内内容
remove_parentheses = extractor.remove_parentheses

# 删除文本中的 html 标签
remove_html_tag = extractor.remove_html_tag

# 删除文本中的异常字符
remove_exception_char = extractor.remove_exception_char

# 去除冗余字符
remove_redundant_char = extractor.remove_redundant_char

# 替换文本中的 email 为归一化标签
replace_email = extractor.replace_email

# 将文本中的 url 链接归一化
replace_url = extractor.replace_url

# 替换文本中的电话号码为归一化标签 token
replace_phone_number = extractor.replace_phone_number

# 替换文本中的 ip 地址为归一化标签
replace_ip_address = extractor.replace_ip_address

# 替换文本中的身份证号为归一化标签
replace_id_card = extractor.replace_id_card

# 替换文本中的电 QQ 号为归一化标签
replace_qq = extractor.replace_qq

# 替换文本中的所有中文字符串为空格，默认为空格，可以自定义指定目标字符。
replace_chinese = extractor.replace_chinese

checker = Checker()

# 检查文本中是否包含中文字符，若至少包含一个，则返回 True，否则返回 False
check_any_chinese_char = checker.check_any_chinese_char

# 检查文本中是否全部为中文字符，若全部都是，则返回 True
check_all_chinese_char = checker.check_all_chinese_char

# 检查文本中是否包含阿拉伯数字字符，若至少包含一个，则返回 True，否则返回 False。
check_any_arabic_num = checker.check_any_arabic_num

# 检查文本中是否全部为阿拉伯数字字符，若全部都是，则返回 True
check_all_arabic_num = checker.check_all_arabic_num

split_sentence = SplitSentence()
