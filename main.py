from maix import touchscreen, app, time, display, image, camera
import requests
from PIL import Image
import time

image.load_font("sourcehansans", "/maixapp/share/font/SourceHanSansCN-Regular.otf", size = 32)
print("fonts:", image.fonts())
image.set_default_font("sourcehansans")



ts = touchscreen.TouchScreen()
disp = display.Display()

img = image.Image(disp.width(), disp.height())
# draw exit button
exit_label = "< Exit"
size = image.string_size(exit_label)
exit_btn_pos = [0, 0, 8*2 + size.width(), 12 * 2 + size.height()]
img.draw_string(8, 12, exit_label, image.Color.from_rgb(255, 0, 0))
img.draw_rect(exit_btn_pos[0], exit_btn_pos[1], exit_btn_pos[2], exit_btn_pos[3],  image.Color.from_rgb(255, 0, 0), 2)

# draw scan button
scan_label = "scan"
size = image.string_size(scan_label)
scan_btn_pos = [0, 50, 8*2 + size.width(), 12 * 2 + size.height()]
img.draw_string(8, 72, scan_label, image.Color.from_rgb(255, 0, 0))
img.draw_rect(scan_btn_pos[0], scan_btn_pos[1], scan_btn_pos[2], scan_btn_pos[3],  image.Color.from_rgb(255, 0, 0), 2)

def ws(ce_str):  # 网页
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    response = requests.get(
        f'https://s0.wp.com/mshots/v1/{ce_str}/?w=552&h=368', headers=headers)
    #print(response.status_code)
    try:
        file = open("a.png", "wb")
        file.write(response.content)
        file.close()
    except:
        print(response.status_code)
def is_in_button(x, y, btn_pos):
    return x > btn_pos[0] and x < btn_pos[0] + btn_pos[2] and y > btn_pos[1] and y < btn_pos[1] + btn_pos[3]
def find_url():
    cam = camera.Camera(320, 240)

    while 1:
        img = cam.read()
        qrcodes = img.find_qrcodes()
        for qr in qrcodes:
            corners = qr.corners()
            for i in range(4):
                img.draw_line(corners[i][0], corners[i][1], corners[(i + 1) % 4][0], corners[(i + 1) % 4][1], image.COLOR_RED)
            img.draw_string(qr.x(), qr.y() - 15, qr.payload(), image.COLOR_RED)
            url=qr.payload()
            try:
                if url.split('/') [0] == 'http:' or url.split('/') [0] == 'https:':
                    return(url)
            except:
                pass
        disp.show(img)
  
    return(url)
def draw_button ():
    global img,exit_btn_pos,scan_btn_pos
    # draw exit button
    exit_label = "< Exit"
    size = image.string_size(exit_label)
    exit_btn_pos = [0, 0, 8*2 + size.width(), 12 * 2 + size.height()]
    img.draw_string(8, 12, exit_label, image.Color.from_rgb(255, 0, 0))
    img.draw_rect(exit_btn_pos[0], exit_btn_pos[1], exit_btn_pos[2], exit_btn_pos[3],  image.Color.from_rgb(255, 0, 0), 2)

    # draw scan button
    scan_label = "scan"
    size = image.string_size(scan_label)
    scan_btn_pos = [0, 50, 8*2 + size.width(), 12 * 2 + size.height()]
    img.draw_string(8, 72, scan_label, image.Color.from_rgb(255, 0, 0))
    img.draw_rect(scan_btn_pos[0], scan_btn_pos[1], scan_btn_pos[2], scan_btn_pos[3],  image.Color.from_rgb(255, 0, 0), 2)
    
def get_web(url):
    global img
    ws(url)
    while not Image.open('a.png').size == (552, 368):
        img = image.Image(552, 368)
        img.draw_rect(0, 0, disp.width(), disp.height(), color=image.Color.from_rgb(255, 0, 0), thickness=-1)
        img.draw_rect(10, 10, 100, 100, color=image.Color.from_rgb(255, 0, 0))
        img.draw_string(10, 10, "加载中", color=image.Color.from_rgb(255, 255, 255))
        disp.show(img)
        time.sleep(1)
        ws(url)
    img = image.Image(552, 368)
    img = image.load("./a.png").resize(disp.width(), disp.height())
    print('ok')
    if img is None:
        raise Exception(f"load image failed")
    draw_button ()
    disp.show(img)
    x, y, pressed = ts.read()
    while is_in_button(x, y, exit_btn_pos) or is_in_button(x, y, scan_btn_pos):
        x, y, pressed = ts.read()
while not app.need_exit():
    x, y, pressed = ts.read()
    if is_in_button(x, y, exit_btn_pos):
        app.set_exit_flag(True)
    if is_in_button(x, y, scan_btn_pos): 
        get_web(find_url())
        draw_button ()
    disp.show(img)
