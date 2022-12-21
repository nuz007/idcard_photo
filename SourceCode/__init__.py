#import pyi_splash
import os,sys,time
import tkinter as tk
from tkinter import ttk,messagebox,filedialog

from PIL import ImageFont, ImageDraw, Image, ImageTk

#time.sleep(2)
#pyi_splash.close()

def basepath():
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        # 单个exe解药后的路径
        base_path = sys._MEIPASS
    else:
        # 不打包，正常执行的路径
        base_path = os.path.abspath(".")
    return base_path

weights = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]  #权重
M_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  #除以11的余数对应的校验码


def check():
    total = 0
    for j in range(17):
        total += int(idbox.get()[j])* weights[j]#计算验证码
    return M_codes[total % 11]

def sex():return("男" if int(idbox.get()[16])%2 else "女" )


#设置需要显示的字体
namefont = ImageFont.truetype(os.path.join(basepath(),"datas/hei.ttf"), 72)
otherfont = ImageFont.truetype(os.path.join(basepath(),'datas/hei.ttf'), 64)
birthdayfont = ImageFont.truetype(os.path.join(basepath(),'datas/birthday.ttf'), 60)
idfont = ImageFont.truetype(os.path.join(basepath(),'datas/idnum.ttf'), 90)

def get_len(txt):
    len_txt = len(txt)
    len_txt_utf8 = len(txt.encode('utf-8'))
    # 中文字符多算1位
    size = int((len_txt_utf8 - len_txt) / 2 + len_txt)
    return size


def get_txt(txtxt):
    tmp=[]
    tmpx=""
    tmpy=0
    tmpz=0
    for i in txtxt:
        tmpx=tmpx+i
        tmpy+=1
        if get_len(tmpx)>=22:
            tmp.append(txtxt[tmpz:tmpy])
            tmpz=tmpy
            tmpx=""
        if get_len(txtxt[tmpz:])<22:
            tmp.append(txtxt[tmpz:])
            break
    return tmp

xximg=None

def Make(select=0):
    global xximg,img_pil


    if not(namebox.get().replace(" ","")) or not(ethnicbox.get().replace(" ","")) or not(addressbox.get().replace(" ","")):
        messagebox.showerror("错误","未输入信息")
        return
    if len(idbox.get())!=18:
        messagebox.showerror("错误","无效的身份证号位数")
        return
    try:int(idbox.get()[:17])
    except:
        messagebox.showerror("错误","身份证号前17位不能包含字母")
        return

    img_pil = Image.open(os.path.join(basepath(),"datas/demo.png"))
    draw = ImageDraw.Draw(img_pil)

    #绘制文字信息
    draw.text((360,240), namebox.get(), font = namefont, fill = (0,0,0))#姓名(630, 690)
    draw.text((360, 390), sex(), fill=(0, 0, 0), font=otherfont)#性别(630, 840)
    draw.text((800, 390), ethnicbox.get(), fill=(0, 0, 0), font=otherfont)#民族(1030, 840)
    draw.text((360, 525), str(int(idbox.get()[6:10])), fill=(0, 0, 0), font=birthdayfont)#出生年(630, 975)
    draw.text((680, 525), str(int(idbox.get()[10:12])), fill=(0, 0, 0), font=birthdayfont)#出生月(950, 975)
    draw.text((880, 525), str(int(idbox.get()[12:14])), fill=(0, 0, 0), font=birthdayfont)#出生日(1150, 975)


    addr_loc_y = 660#1115
    addr_lines = get_txt(addressbox.get())#地址
    for addr_line in addr_lines:
        draw.text((360, addr_loc_y), addr_line, fill=(0, 0, 0), font=otherfont)#630
        addr_loc_y += 100

    draw.text((610, 1015), idbox.get()[:17]+check(), fill=(0, 0, 0), font=idfont)#身份证号(900, 1475)


    draw.text((800, 2110), policebox.get(), fill=(0, 0, 0), font=otherfont)#公安局(1050, 2750)
    draw.text((800, 2255), validbox.get(), fill=(0, 0, 0), font=otherfont)#有效期(1050, 2895)


    if select:
        imgpath=filedialog.askopenfilename(initialdir=os.getcwd(),title="选择身份证头像")
        avatar=Image.open(imgpath)
        if not imgpath.replace(" ","").replace("/",""):
            messagebox.showerror("错误","未选择头像无法生成")
            return
    elif sex()=="男":avatar = Image.open(os.path.join(basepath(),"datas/man.png"))#头像
    else:avatar = Image.open(os.path.join(basepath(),"datas/woman.png"))#头像
    avatar = avatar.resize((500, 670))
    avatar = avatar.convert('RGBA')
    img_pil.paste(avatar, (1230, 160), mask=avatar)#(1500, 690)

    tmp=img_pil.resize((325,413))
    xximg=ImageTk.PhotoImage(tmp)
    imgshow.config(image=xximg)

    if not os.path.exists(os.path.join(os.path.expanduser('~'),"Desktop","身份证照片生成器")):os.makedirs(os.path.join(os.path.expanduser('~'),"Desktop","身份证照片生成器"))
    img_pil.save(os.path.join(os.path.expanduser('~'),"Desktop","身份证照片生成器",f"{namebox.get()}_身份证照片.png"))
    messagebox.showinfo("信息",f"已保存身份证照片在桌面/身份证照片生成器/{namebox.get()}_身份证照片.png")

helptxt="""使用教程:\n\n1. 请先同意用户协议(不同意代表你是犯罪分子)\n\n2. 输入姓名，民族等信息\n\n3. 保存头像(如果可行)\n\n4. 生成，会在桌面生成一个文件名为姓名_身份证.png的文件。
马化腾
汉
广东省深圳市福田区福中路315号黄埔雅苑乐悠园3座12D
440301197110292910
深圳市公安局
2018.1.1-2038.1.1"""
abouttxt="身份证照片生成器1.0Alpha\n\n2022.12"

    
q=tk.Tk()

q.iconbitmap(os.path.join(basepath(),"datas/icon.ico"))
q.resizable(0,0)
q.title("身份证照片生成器")
ttk.Label(q,text="姓　　名:").grid(row=0,column=0)
namebox=ttk.Entry(q,width=35)
namebox.grid(row=0,column=1)
ttk.Label(q,text="民　　族:").grid(row=1,column=0)
ethnicbox=ttk.Entry(q,width=35)
ethnicbox.grid(row=1,column=1)
ttk.Label(q,text="详细住址:").grid(row=2,column=0)
addressbox=ttk.Entry(q,width=35)
addressbox.grid(row=2,column=1)
ttk.Label(q,text="身份证号:").grid(row=3,column=0)
idbox=ttk.Entry(q,width=35)
idbox.grid(row=3,column=1)
ttk.Label(q,text="签发机关:").grid(row=4,column=0)
policebox=ttk.Entry(q,width=35)
policebox.grid(row=4,column=1)
ttk.Label(q,text="有效期限:").grid(row=5,column=0)
validbox=ttk.Entry(q,width=35)
validbox.grid(row=5,column=1)


imgshow=ttk.Label(q)
imgshow.grid(row=6,column=0,columnspan=2)


Menu=tk.Menu(q)
xMenu=tk.Menu(Menu,tearoff=False)
Menu.add_cascade(label="文件",menu=xMenu)
xMenu.add_command(label="选择头像生成并保存",command=lambda: Make(select=1))
xMenu.add_command(label="直接生成并保存",command=Make)
zMenu=tk.Menu(Menu,tearoff=False)
Menu.add_cascade(label="帮助",menu=zMenu)
zMenu.add_command(label="帮助",command=lambda: messagebox.showinfo("帮助",helptxt))
zMenu.add_cascade(label="关于",command=lambda: messagebox.showinfo("关于",abouttxt))
q.config(menu=Menu)
if os.path.exists(os.path.join(os.path.expanduser('~'),"AppData\\Roaming\\Microsoft\\InputMethod\\Chs\\ChsPinyinConfig.dat")):
    messagebox.showinfo("用户协议","由于您不同意用户协议，本程序不再为您服务。")
    os._exit(1)

if messagebox.askyesno("用户协议","是否同意此用户协议？\n\n请勿使用此程序作为任何违法犯罪行为！后果自负！后果自负！后果自负！\n本程序采用GPLv3开源协议，许可证链接: https://www.gnu.org/licenses/quick-guide-gplv3.zh-cn.html\n"):q.mainloop()
else:
    try:os.makedirs(os.path.join(os.path.expanduser('~'),"AppData\\Roaming\\Microsoft\\InputMethod\\Chs"))
    except:pass
    with open(os.path.join(os.path.expanduser('~'),"AppData\\Roaming\\Microsoft\\InputMethod\\Chs\\ChsPinyinConfig.dat"),"w") as xxx:
        xxx.write("""{
    "Name":"微软拼音",
    "Name_en-US":"Microsoft Pinyin",
    "Version":"21.0.0",
    "OS":"Microsoft Windows"
}""")

    messagebox.showerror("用户协议","由于您不同意用户协议，本程序不再为您服务。")