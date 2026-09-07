# -*- coding: utf-8 -*-
import base64, os
base = r'c:\Users\helight\Desktop\坦克'
# 用户明确要求:
#   彩蛋关卡背景 = PNG (黄衣+来来我敬你)
#   主关卡背景   = JPG (咖啡馆+泰迪熊)
egg_img = os.path.join(base, 'fde39df515689ea09822c814f75e7676.png')
main_img = os.path.join(base, '242d5a9862c9d458e550b6187c7262a9.jpg')

with open(egg_img, 'rb') as f:
    egg_b64 = base64.b64encode(f.read()).decode()
with open(main_img, 'rb') as f:
    main_b64 = base64.b64encode(f.read()).decode()

with open(os.path.join(base, 'bg_egg.b64'), 'w', encoding='utf-8') as f:
    f.write('data:image/png;base64,' + egg_b64)   # PNG 对应彩蛋
with open(os.path.join(base, 'bg_main.b64'), 'w', encoding='utf-8') as f:
    f.write('data:image/jpeg;base64,' + main_b64) # JPEG 对应主关卡

print(f'[OK] EGG  (彩蛋 PNG) B64 LEN: {len(egg_b64)}')
print(f'[OK] MAIN (主关 JPG) B64 LEN: {len(main_b64)}')
