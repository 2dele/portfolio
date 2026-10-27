# -*- coding: utf-8 -*-
"""截取乡途各页面真实界面。"""
import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:4173"
OUT = r"C:\Users\tuo\Desktop\简历\portfolio\shots\xiangtu"
os.makedirs(OUT, exist_ok=True)

VIEWS = [
    ("u_pass", "home", "home"),
    ("u_pass", "schedules", "schedules"),
    ("u_pass", "orders", "orders"),
    ("u_pass", "profile", "profile"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 430, "height": 880},
                            device_scale_factor=2)
    page.goto(BASE, wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(1500)

    def get_state():
        return page.evaluate("async () => (await fetch('/api/state').then(r=>r.json()))")

    def put_state(payload):
        page.evaluate(
            "(p) => fetch('/api/state', {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(p)}).then(r=>r.json())",
            payload)

    for user_id, view, name in VIEWS:
        s = get_state()
        s["currentUser"] = {"id": user_id}
        s["view"] = {"name": view, "params": {}}
        s["viewStack"] = []
        put_state(s)
        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(1800)
        page.screenshot(path=os.path.join(OUT, f"{name}.png"))
        print("shot:", name)

    # 管理后台（桌面尺寸）
    page2 = browser.new_page(viewport={"width": 1366, "height": 850},
                             device_scale_factor=1.5)
    page2.goto(BASE, wait_until="domcontentloaded", timeout=15000)
    page2.wait_for_timeout(1500)
    s = page2.evaluate("async () => (await fetch('/api/state').then(r=>r.json()))")
    s["currentUser"] = {"id": "u_manager"}
    s["view"] = {"name": "dashboard", "params": {}}
    s["viewStack"] = []
    page2.evaluate(
        "(p) => fetch('/api/state', {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(p)}).then(r=>r.json())", s)
    page2.reload(wait_until="domcontentloaded")
    page2.wait_for_timeout(1800)
    page2.screenshot(path=os.path.join(OUT, "admin.png"))
    print("shot: admin")

    browser.close()
print("Done")
