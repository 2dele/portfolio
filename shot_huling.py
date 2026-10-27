# -*- coding: utf-8 -*-
"""截取护铃迹安各页面（静态渲染）。"""
import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899/templates"
OUT = r"C:\Users\tuo\Desktop\简历\portfolio\shots\huling"
os.makedirs(OUT, exist_ok=True)

PAGES = [
    ("login.html", 1366, 850, "login"),
    ("index2.html", 1366, 850, "index"),
    ("map.html", 1366, 850, "map"),
    ("lujingguihua2.html", 1366, 850, "route"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for f, w, h, name in PAGES:
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1.5)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        try:
            page.goto(f"{BASE}/{f}", wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(3500)
            page.screenshot(path=os.path.join(OUT, f"{name}.png"), full_page=False)
            print("shot:", name, "| js errors:", len(errors))
        except Exception as e:
            print("FAIL", name, e)
        page.close()
    browser.close()
print("Done")
