# -*- coding: utf-8 -*-
"""
WQ · 坦克大战 · 游戏生成器
根据设计文档生成单文件 HTML 游戏 (tank-battle.html)
技术栈: Python (生成器) -> HTML5 Canvas + 原生 JavaScript
"""

import os

# ============ 游戏配置数据 (WQ 全主题) ============
GAME_CONFIG = {
    "title": "WQ · 坦克大战",
    "version": "v1.1",
    "slogan": "王者无敌 · 奇迹永存",
}

# 7 款 WQ 坦克
WQ_TANKS = [
    {"id": "WQ-01", "name": "WQ-01 先锋", "color": "#3DDC84", "hp": 100, "speed": 2.2, "fireRate": 380, "dmg": 25, "price": 0, "unlock": "init", "passive": "regen", "ult": "bombard"},
    {"id": "WQ-02", "name": "WQ-02 风暴", "color": "#4FC3F7", "hp": 80,  "speed": 3.0, "fireRate": 240, "dmg": 14, "price": 3000, "unlock": "gold", "passive": "drift", "ult": "dash"},
    {"id": "WQ-03", "name": "WQ-03 铁锤", "color": "#FF5252", "hp": 180, "speed": 1.6, "fireRate": 520, "dmg": 40, "price": 8000, "unlock": "gold", "passive": "reflect", "ult": "quake"},
    {"id": "WQ-04", "name": "WQ-04 幻影", "color": "#FFD600", "hp": 70,  "speed": 2.6, "fireRate": 360, "dmg": 22, "price": 15000, "unlock": "gold", "passive": "stealth", "ult": "clone"},
    {"id": "WQ-05", "name": "WQ-05 霸王", "color": "#9E9E9E", "hp": 150, "speed": 1.8, "fireRate": 460, "dmg": 55, "price": 30000, "unlock": "gold", "passive": "bosskiller", "ult": "railgun"},
    {"id": "WQ-06", "name": "WQ-06 量子", "color": "#B388FF", "hp": 110, "speed": 2.4, "fireRate": 340, "dmg": 28, "price": 0, "unlock": "clear", "passive": "cooldown", "ult": "slow"},
    {"id": "WQ-07", "name": "WQ-07 菁英", "color": "#00E5FF", "hp": 143, "speed": 2.8, "fireRate": 300, "dmg": 36, "price": 0, "unlock": "egg", "passive": "lifesteal", "ult": "tsunami"},
]

# 6 种 WQ 武器
WQ_WEAPONS = [
    {"id": "WQ-穿甲弹", "type": "single", "dmg": 25, "cd": 0,   "price": 0,     "speed": 7, "color": "#FFD600"},
    {"id": "WQ-加特林", "type": "rapid",  "dmg": 8,  "cd": 60,  "price": 2000,  "speed": 8, "color": "#FF9100"},
    {"id": "WQ-激光炮", "type": "laser",  "dmg": 4,  "cd": 200, "price": 6000,  "speed": 12,"color": "#00F0FF"},
    {"id": "WQ-散射炮", "type": "shotgun","dmg": 12, "cd": 500, "price": 9000,  "speed": 6, "color": "#FF2D95"},
    {"id": "WQ-追踪弹", "type": "homing", "dmg": 30, "cd": 700, "price": 18000, "speed": 5, "color": "#76FF03"},
    {"id": "WQ-黑洞炮", "type": "blackhole","dmg":80,"cd":1500,"price": 50000, "speed": 4, "color": "#AA00FF"},
    # WQ 彩蛋专属隐藏武器：通关彩蛋地图后解锁
    {"id": "WQ-浪尖炮", "type": "laser",  "dmg": 20, "cd": 300, "price": 0,     "speed": 16,"color": "#00E5FF", "unlock": "egg"},
]

# 4 种 WQ 普通敌人
WQ_ENEMIES = {
    "scout":  {"name": "WQ-侦察车",   "hp": 40,  "dmg": 10, "speed": 1.8, "color": "#A1887F", "fireRate": 1200, "score": 50},
    "tank":   {"name": "WQ-步兵坦克", "hp": 80,  "dmg": 18, "speed": 1.0, "color": "#FF8A65", "fireRate": 1500, "score": 100},
    "artillery":{"name":"WQ-自行火炮","hp": 120, "dmg": 30, "speed": 0.7, "color": "#BA68C8", "fireRate": 2200, "score": 180},
    "drone":  {"name": "WQ-无人机群", "hp": 20,  "dmg": 8,  "speed": 2.4, "color": "#64B5F6", "fireRate": 900,  "score": 40},
}

# 3 只 WQ Boss + 1 只 WQ 彩蛋 Boss
WQ_BOSSES = {
    "WQ-钢铁蜈蚣": {"hp": 3000, "dmg": 25, "color": "#D32F2F", "chapter": 1, "phases": 3},
    "WQ-量子守卫":  {"hp": 5000, "dmg": 35, "color": "#00B0FF", "chapter": 2, "phases": 3},
    "WQ-机械君主":  {"hp": 8000, "dmg": 45, "color": "#FFD600", "chapter": 3, "phases": 3},
    "WQ-浪尖霸主":  {"hp": 6000, "dmg": 30, "color": "#00E5FF", "chapter": 0, "phases": 3},  # 彩蛋 Boss
}

# 3 大 WQ 章节
WQ_CHAPTERS = [
    {"id": 1, "name": "WQ 荒漠边境", "filter": "sepia(0.4) saturate(1.3) brightness(1.05)", "levels": 10},
    {"id": 2, "name": "WQ 赛博都市", "filter": "hue-rotate(180deg) saturate(1.5) contrast(1.2)", "levels": 10},
    {"id": 3, "name": "WQ 太空基地", "filter": "brightness(0.8) contrast(1.3) saturate(0.6) hue-rotate(60deg)", "levels": 10},
]


def build_game(output_path="tank-battle.html"):
    """生成完整的单文件 HTML 游戏"""
    # 读取背景图 base64 (内联到 HTML, 避免外部文件依赖)
    bg_egg_b64 = ""
    bg_main_b64 = ""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, "bg_egg.b64"), "r", encoding="utf-8") as f:
            bg_egg_b64 = f.read().strip()
        with open(os.path.join(base_dir, "bg_main.b64"), "r", encoding="utf-8") as f:
            bg_main_b64 = f.read().strip()
    except Exception as e:
        print(f"[WARN] 背景图加载失败: {e}")

    # 注入背景图常量到 JS 代码头部
    js_with_bg = (
        "// ===== WQ 背景图 (内联 base64, 避免外部依赖) =====\n"
        f'const WQ_BG_EGG = "{bg_egg_b64}";\n'
        f'const WQ_BG_MAIN = "{bg_main_b64}";\n'
        + JS_CODE
    )

    html = TEMPLATE_HTML.format(
        title=GAME_CONFIG["title"],
        version=GAME_CONFIG["version"],
        slogan=GAME_CONFIG["slogan"],
        css=CSS_STYLE,
        js=js_with_bg,
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] 已生成: {output_path}  ({len(html)} 字节)")
    return output_path


# ============ HTML 骨架 ============
TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;500;700&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<!-- ============ WQ 主菜单 ============ -->
<div id="mainMenu" class="scene active">
  <div class="menu-bg"></div>
  <h1 class="game-title">WQ · TANK BATTLE</h1>
  <p class="game-slogan">— {slogan} —</p>
  <div class="menu-buttons">
    <button class="wq-btn" onclick="SceneManager.goto('arsenal')">▶ WQ 开始战斗</button>
    <button class="wq-btn" onclick="SceneManager.goto('arsenal')">🛡 WQ 武器库</button>
    <button class="wq-btn" onclick="SceneManager.goto('levelSelect')">📊 WQ 关卡选择</button>
    <button class="wq-btn" onclick="toggleSettings()">⚙ WQ 设置</button>
  </div>
  <div class="menu-footer">
    <span id="eggTrigger" class="egg-text" ondblclick="enterEggMap()">WQ 浪尖菁英</span>
    <span class="menu-info">WQ金币 <span id="menuGold">0</span>  ·  {version}</span>
  </div>
  <div id="settingsPanel" class="settings-panel hidden">
    <h3>WQ 设置</h3>
    <label>WQ 音效音量 <input type="range" id="sfxVol" min="0" max="100" value="70" oninput="Save.settings.sfxVolume=this.value/100"></label>
    <label>WQ 背景音量 <input type="range" id="bgmVol" min="0" max="100" value="50" oninput="Save.settings.bgmVolume=this.value/100"></label>
    <label><input type="checkbox" id="shakeToggle" checked oninput="Save.settings.screenShake=this.checked"> WQ 屏幕震动</label>
    <button class="wq-btn small" onclick="toggleSettings()">WQ 关闭</button>
    <button class="wq-btn small danger" onclick="resetSave()">WQ 重置存档</button>
  </div>
</div>

<!-- ============ WQ 武器库 ============ -->
<div id="arsenal" class="scene">
  <h2 class="scene-title">★ WQ ARSENAL ★ <span class="gold-display">WQ金币: <span id="arsenalGold">0</span></span></h2>
  <div class="arsenal-layout">
    <div class="tank-list" id="tankList"></div>
    <div class="tank-preview">
      <canvas id="tankPreviewCanvas" width="240" height="240"></canvas>
      <div class="tank-stats" id="tankStats"></div>
    </div>
    <div class="weapon-list" id="weaponList"></div>
  </div>
  <div class="arsenal-actions">
    <button class="wq-btn" onclick="SceneManager.goto('mainMenu')">◀ WQ 返回</button>
    <button class="wq-btn primary" onclick="startBattle()">▶ WQ 开始战斗</button>
    <button class="wq-btn" onclick="SceneManager.goto('levelSelect')">WQ 关卡选择</button>
  </div>
</div>

<!-- ============ WQ 关卡选择 ============ -->
<div id="levelSelect" class="scene">
  <h2 class="scene-title">★ WQ 关卡选择 ★</h2>
  <div class="chapter-tabs">
    <button class="tab-btn active" onclick="switchChapter(0)">🏜 WQ 荒漠边境</button>
    <button class="tab-btn" onclick="switchChapter(1)">🏙 WQ 赛博都市</button>
    <button class="tab-btn" onclick="switchChapter(2)">🚀 WQ 太空基地</button>
  </div>
  <div class="level-grid" id="levelGrid"></div>
  <div class="mode-select">
    <button class="wq-btn primary" onclick="startEndless()">∞ WQ 无尽模式</button>
    <button class="wq-btn" onclick="SceneManager.goto('mainMenu')">◀ WQ 返回</button>
  </div>
</div>

<!-- ============ WQ 游戏画面 ============ -->
<div id="gameScene" class="scene">
  <div id="hud" class="hud">
    <div class="hud-top">
      <span id="hudLevel">WQ 关卡 1-1</span>
      <span id="hudWave">WQ 敌人 0/0</span>
      <span id="hudScore">WQ 得分 0</span>
    </div>
    <div class="hud-bars">
      <div class="bar-row"><span class="bar-label">WQ血量</span><div class="bar"><div id="hpBar" class="bar-fill hp"></div></div><span id="hpText">100/100</span></div>
      <div class="bar-row"><span class="bar-label">WQ能量</span><div class="bar"><div id="mpBar" class="bar-fill mp"></div></div><span id="mpText">0/100</span></div>
      <div class="bar-row"><span class="bar-label">WQ护盾</span><div class="bar"><div id="shieldBar" class="bar-fill shield"></div></div><span id="shieldText">0</span></div>
      <div class="bar-row"><span class="bar-label">WQ金币</span><span id="goldText">0</span></div>
    </div>
    <div id="bossBarWrap" class="boss-bar hidden">
      <span id="bossName">WQ BOSS</span>
      <div class="bar"><div id="bossBar" class="bar-fill boss"></div></div>
    </div>
    <div class="hud-bottom">
      <div class="weapon-slots" id="weaponSlots"></div>
      <div class="bar-row"><span class="bar-label">WQ大招(K)</span><div class="bar"><div id="ultBar" class="bar-fill ult"></div></div></div>
      <button class="wq-btn small" onclick="pauseGame()">⏸ WQ 暂停</button>
    </div>
    <canvas id="minimap" width="120" height="120"></canvas>
  </div>
  <canvas id="game"></canvas>
</div>

<!-- ============ WQ 弹窗 ============ -->
<div id="modal" class="modal hidden">
  <div class="modal-content" id="modalContent"></div>
</div>

<!-- ============ WQ 商店(无尽模式) ============ -->
<div id="shop" class="modal hidden">
  <div class="modal-content shop-content">
    <h2>🛒 WQ 商店 - 波次 <span id="shopWave">5</span></h2>
    <div id="shopItems" class="shop-items"></div>
    <button class="wq-btn" onclick="rerollShop()">🔄 WQ 刷新 (100WQ金币)</button>
    <button class="wq-btn primary" onclick="closeShop()">▶ WQ 继续</button>
  </div>
</div>

<script>
{js}
</script>
</body>
</html>
"""


# ============ CSS 样式 (科幻赛博风 + WQ 主题) ============
CSS_STYLE = """
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{background:#0A0E27;color:#E0E8FF;font-family:'Exo 2',sans-serif;overflow:hidden;height:100vh;width:100vw}
canvas{display:block}
.hidden{display:none!important}

/* 场景 */
.scene{position:fixed;inset:0;display:none;flex-direction:column;align-items:center;justify-content:center}
.scene.active{display:flex}

/* 主菜单 */
#mainMenu{background:radial-gradient(ellipse at center,#1A1F4E 0%,#0A0E27 70%)}
.menu-bg{position:absolute;inset:0;background:linear-gradient(135deg,transparent 40%,rgba(0,240,255,0.05) 50%,transparent 60%);background-size:200% 200%;animation:scan 8s linear infinite}
@keyframes scan{0%{background-position:0 0}100%{background-position:200% 200%}}
.game-title{font-family:'Orbitron',monospace;font-size:56px;font-weight:900;color:#00F0FF;text-shadow:0 0 20px #00F0FF,0 0 40px rgba(0,240,255,0.5);letter-spacing:4px;margin-bottom:8px}
.game-slogan{color:#FF2D95;font-size:18px;letter-spacing:6px;margin-bottom:40px;text-shadow:0 0 10px rgba(255,45,149,0.6)}
.menu-buttons{display:flex;flex-direction:column;gap:14px;z-index:1}
.menu-footer{position:absolute;bottom:20px;left:0;right:0;display:flex;justify-content:space-between;padding:0 28px;font-size:13px;color:#4A5A8C;font-family:'Orbitron',monospace}
.egg-text{cursor:pointer;opacity:0.4;transition:all 0.3s;padding:4px 8px}
.egg-text:hover{opacity:0.7;text-shadow:0 0 8px #00F0FF}
.egg-text.cleared{color:#00E5FF;opacity:1;text-shadow:0 0 10px #00E5FF}
.menu-info{color:#4A5A8C}

/* WQ 按钮 */
.wq-btn{font-family:'Orbitron',monospace;font-size:16px;font-weight:700;color:#00F0FF;background:rgba(0,240,255,0.08);border:2px solid #00F0FF;padding:12px 32px;cursor:pointer;letter-spacing:2px;transition:all 0.2s;min-width:240px;border-radius:2px;position:relative;overflow:hidden}
.wq-btn:hover{background:rgba(0,240,255,0.2);box-shadow:0 0 20px rgba(0,240,255,0.5);transform:translateY(-2px)}
.wq-btn:active{transform:translateY(0)}
.wq-btn.primary{color:#FF2D95;border-color:#FF2D95;background:rgba(255,45,149,0.1)}
.wq-btn.primary:hover{background:rgba(255,45,149,0.2);box-shadow:0 0 20px rgba(255,45,149,0.5)}
.wq-btn.small{min-width:auto;padding:6px 16px;font-size:13px}
.wq-btn.danger{color:#FF4444;border-color:#FF4444;background:rgba(255,68,68,0.1)}

/* 设置面板 */
.settings-panel{position:absolute;top:80px;right:40px;background:rgba(10,14,39,0.95);border:1px solid #00F0FF;padding:20px;border-radius:4px;display:flex;flex-direction:column;gap:12px;z-index:10}
.settings-panel label{display:flex;align-items:center;gap:10px;font-size:13px;color:#E0E8FF}
.settings-panel input[type=range]{width:140px}

/* 武器库 */
.scene-title{font-family:'Orbitron',monospace;font-size:28px;color:#00F0FF;margin-bottom:20px;text-shadow:0 0 10px rgba(0,240,255,0.5);display:flex;gap:30px;align-items:center}
.gold-display{color:#FFB800;font-size:16px}
.arsenal-layout{display:grid;grid-template-columns:240px 1fr 280px;gap:20px;width:90%;max-width:1100px;height:60vh}
.tank-list,.weapon-list{background:rgba(0,240,255,0.04);border:1px solid rgba(0,240,255,0.3);border-radius:4px;padding:12px;overflow-y:auto}
.tank-preview{display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(0,240,255,0.04);border:1px solid rgba(0,240,255,0.3);border-radius:4px;padding:16px}
.tank-card{background:rgba(10,14,39,0.6);border:1px solid #2A3A6C;padding:10px;margin-bottom:8px;cursor:pointer;transition:all 0.2s;border-radius:3px}
.tank-card:hover{border-color:#00F0FF;background:rgba(0,240,255,0.1)}
.tank-card.equipped{border-color:#FFB800;box-shadow:0 0 10px rgba(255,184,0,0.4)}
.tank-card.locked{opacity:0.5;cursor:not-allowed}
.tank-card.egg{border-color:#00E5FF}
.tank-name{font-family:'Orbitron',monospace;font-size:13px;font-weight:700}
.tank-info{font-size:11px;color:#7A8ABF;margin-top:4px}
.tank-stats{margin-top:12px;font-size:12px;color:#E0E8FF;text-align:center;line-height:1.8}
.stat-bar{display:inline-block;width:80px;height:6px;background:#1A2050;border-radius:3px;margin:0 4px;vertical-align:middle}
.stat-bar>div{height:100%;background:#00F0FF;border-radius:3px}
.weapon-card{background:rgba(10,14,39,0.6);border:1px solid #2A3A6C;padding:10px;margin-bottom:8px;cursor:pointer;transition:all 0.2s;border-radius:3px}
.weapon-card:hover{border-color:#FF2D95}
.weapon-card.equipped{border-color:#FFB800;box-shadow:0 0 10px rgba(255,184,0,0.4)}
.weapon-card.locked{opacity:0.5}
.weapon-name{font-family:'Orbitron',monospace;font-size:12px;font-weight:700}
.weapon-info{font-size:11px;color:#7A8ABF;margin-top:4px}
.arsenal-actions{display:flex;gap:14px;margin-top:20px}

/* 关卡选择 */
.chapter-tabs{display:flex;gap:10px;margin-bottom:20px}
.tab-btn{font-family:'Orbitron',monospace;font-size:14px;color:#7A8ABF;background:transparent;border:1px solid #2A3A6C;padding:8px 20px;cursor:pointer;border-radius:2px}
.tab-btn.active{color:#00F0FF;border-color:#00F0FF;background:rgba(0,240,255,0.1)}
.level-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;width:80%;max-width:800px}
.level-card{aspect-ratio:1;background:rgba(0,240,255,0.06);border:2px solid #2A3A6C;border-radius:4px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:all 0.2s;font-family:'Orbitron',monospace}
.level-card:hover{border-color:#00F0FF;box-shadow:0 0 15px rgba(0,240,255,0.4);transform:scale(1.05)}
.level-card.locked{opacity:0.4;cursor:not-allowed}
.level-card.boss{border-color:#FF4444}
.level-card.boss:hover{box-shadow:0 0 15px rgba(255,68,68,0.5)}
.level-num{font-size:22px;font-weight:900;color:#00F0FF}
.level-stars{font-size:12px;color:#FFB800;margin-top:4px}
.mode-select{display:flex;gap:14px;margin-top:24px}

/* 游戏画面 */
#gameScene{background:#000}
#game{position:absolute;inset:0;width:100%;height:100%}

/* HUD */
.hud{position:absolute;inset:0;pointer-events:none;z-index:5;font-family:'Orbitron',monospace}
.hud-top{position:absolute;top:10px;left:50%;transform:translateX(-50%);display:flex;gap:30px;font-size:13px;color:#00F0FF;background:rgba(10,14,39,0.6);padding:6px 18px;border-radius:3px;border:1px solid rgba(0,240,255,0.3)}
.hud-bars{position:absolute;top:50px;left:14px;display:flex;flex-direction:column;gap:6px;font-size:11px;min-width:240px}
.bar-row{display:flex;align-items:center;gap:8px}
.bar-label{color:#7A8ABF;width:70px;text-align:right}
.bar{flex:1;height:14px;background:#1A2050;border:1px solid #2A3A6C;border-radius:2px;overflow:hidden;min-width:120px}
.bar-fill{height:100%;transition:width 0.2s}
.bar-fill.hp{background:linear-gradient(90deg,#FF5252,#FF8A80)}
.bar-fill.mp{background:linear-gradient(90deg,#4FC3F7,#81D4FA)}
.bar-fill.shield{background:linear-gradient(90deg,#00E5FF,#18FFFF)}
.bar-fill.boss{background:linear-gradient(90deg,#FF4444,#FF8A80)}
.bar-fill.ult{background:linear-gradient(90deg,#FFB800,#FFD600)}
.boss-bar{position:absolute;top:40px;left:50%;transform:translateX(-50%);width:60%;max-width:600px;text-align:center}
.boss-bar span{color:#FF4444;font-size:14px;font-weight:700}
.boss-bar .bar{height:18px}
.hud-bottom{position:absolute;bottom:14px;left:14px;right:14px;display:flex;align-items:center;gap:14px;pointer-events:auto}
.weapon-slots{display:flex;gap:8px;flex:1}
.weapon-slot{background:rgba(10,14,39,0.7);border:1px solid #2A3A6C;padding:6px 12px;border-radius:3px;font-size:11px;cursor:pointer;transition:all 0.2s;min-width:90px}
.weapon-slot.active{border-color:#FFB800;box-shadow:0 0 10px rgba(255,184,0,0.5);color:#FFB800}
.weapon-slot .cd{display:block;height:3px;background:#1A2050;margin-top:4px;border-radius:2px;overflow:hidden}
.weapon-slot .cd>div{height:100%;background:#00F0FF;width:100%;transition:width 0.1s}
#minimap{position:absolute;bottom:60px;right:14px;border:1px solid rgba(0,240,255,0.3);background:rgba(10,14,39,0.7);border-radius:3px}

/* 弹窗 */
.modal{position:fixed;inset:0;background:rgba(0,0,0,0.8);display:flex;align-items:center;justify-content:center;z-index:100}
.modal-content{background:linear-gradient(135deg,#0F1535,#1A2050);border:2px solid #00F0FF;padding:32px;border-radius:6px;text-align:center;max-width:500px;box-shadow:0 0 40px rgba(0,240,255,0.3)}
.modal-content h2{font-family:'Orbitron',monospace;color:#00F0FF;margin-bottom:16px;font-size:24px}
.modal-content p{color:#E0E8FF;margin-bottom:8px;line-height:1.6}
.modal-content .stars{font-size:32px;color:#FFB800;margin:16px 0}
.modal-buttons{display:flex;gap:12px;justify-content:center;margin-top:20px}
.shop-content{max-width:600px}
.shop-items{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:16px 0}
.shop-item{background:rgba(0,240,255,0.06);border:1px solid #2A3A6C;padding:12px;border-radius:3px;cursor:pointer;transition:all 0.2s;text-align:left}
.shop-item:hover{border-color:#FFB800}
.shop-item h4{color:#FFB800;font-family:'Orbitron',monospace;font-size:13px}
.shop-item p{font-size:11px;color:#7A8ABF;margin-top:4px}

/* 通用动画 */
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
.pulse{animation:pulse 1s infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.toast{position:fixed;top:20px;left:50%;transform:translateX(-50%);background:rgba(10,14,39,0.95);border:1px solid #00F0FF;color:#00F0FF;padding:10px 24px;border-radius:3px;font-family:'Orbitron',monospace;font-size:14px;z-index:200;animation:toastIn 0.3s}
@keyframes toastIn{from{opacity:0;transform:translate(-50%,-20px)}to{opacity:1;transform:translate(-50%,0)}}
"""


# ============ JavaScript 游戏代码 ============
JS_CODE = r"""
// ==================== WQ · 坦克大战 · 游戏引擎 ====================
// 全 WQ 主题 · 单文件 HTML5 Canvas 游戏

// ----- 游戏配置 (WQ 全主题) -----
const WQ_TANKS = """ + repr(WQ_TANKS).replace("'", '"') + r""";
const WQ_WEAPONS = """ + repr(WQ_WEAPONS).replace("'", '"') + r""";
const WQ_ENEMIES = """ + repr(WQ_ENEMIES).replace("'", '"') + r""";
const WQ_BOSSES = """ + repr(WQ_BOSSES).replace("'", '"') + r""";
const WQ_CHAPTERS = """ + repr(WQ_CHAPTERS).replace("'", '"') + r""";

// ----- WQ 存档系统 -----
const Save = {
  data: null,
  defaults: {
    version: 2,
    wqGold: 0,
    wqUnlockedTanks: ["WQ-01"],
    wqEquippedTank: "WQ-01",
    wqUnlockedWeapons: ["WQ-穿甲弹"],
    wqEquippedWeapons: ["WQ-穿甲弹","WQ-穿甲弹","WQ-穿甲弹"],
    wqLevelProgress: { maxChapter:1, maxLevel:1, stars:{} },
    wqEndlessBest: { wave:0, score:0, date:"" },
    wqEndlessLeaderboard: [],
    wqSettings: { sfxVolume:0.7, bgmVolume:0.5, screenShake:true },
    easterEgg: { foundEggMap:false, eggMapCleared:false, eggMapClearCount:0, eggMapBestTime:null, achievements:[] }
  },
  load(){ try{ const s=localStorage.getItem("wq_tank_save"); this.data = s?JSON.parse(s):JSON.parse(JSON.stringify(this.defaults)); }catch(e){ this.data=JSON.parse(JSON.stringify(this.defaults)); } this.migrate(); },
  migrate(){ const d=this.data; for(const k in this.defaults){ if(d[k]===undefined) d[k]=this.defaults[k]; } },
  save(){ try{ localStorage.setItem("wq_tank_save", JSON.stringify(this.data)); }catch(e){} },
  reset(){ this.data=JSON.parse(JSON.stringify(this.defaults)); this.save(); location.reload(); },
  get settings(){ return this.data.wqSettings; },
  get gold(){ return this.data.wqGold; },
  addGold(n){ this.data.wqGold=Math.max(0,this.data.wqGold+n); this.save(); this.updateGoldUI(); },
  updateGoldUI(){ const g=this.gold; document.getElementById('menuGold').textContent=g; document.getElementById('arsenalGold').textContent=g; const gt=document.getElementById('goldText'); if(gt) gt.textContent=g; }
};
window.Save = Save;

// ----- WQ 场景管理 -----
const SceneManager = {
  current: 'mainMenu',
  goto(id){
    document.querySelectorAll('.scene').forEach(s=>s.classList.remove('active'));
    const el=document.getElementById(id);
    if(el){ el.classList.add('active'); this.current=id; }
    // 自动隐藏所有弹窗 (修复: 返回后弹窗不消失的 bug)
    document.getElementById('modal').classList.add('hidden');
    document.getElementById('shop').classList.add('hidden');
    // 停止游戏循环
    if(Game.running){ Game.running=false; Game.paused=false; }
    if(id==='mainMenu') Save.updateGoldUI();
    if(id==='arsenal') Arsenal.render();
    if(id==='levelSelect') LevelSelect.render();
  }
};
window.SceneManager = SceneManager;

// ----- WQ 音频系统 (Web Audio 合成) -----
const Audio = {
  ctx: null,
  init(){ if(!this.ctx){ try{ this.ctx=new (window.AudioContext||window.webkitAudioContext)(); }catch(e){} } },
  beep(freq, dur, type='square', vol=0.3){
    this.init(); if(!this.ctx) return;
    const o=this.ctx.createOscillator(), g=this.ctx.createGain();
    o.type=type; o.frequency.value=freq; g.gain.value=vol*Save.settings.sfxVolume;
    o.connect(g); g.connect(this.ctx.destination);
    o.start(); g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime+dur);
    o.stop(this.ctx.currentTime+dur);
  },
  fire(){ this.beep(800,0.08,'square',0.15); setTimeout(()=>this.beep(400,0.05,'square',0.1),30); },
  explosion(){ this.init(); if(!this.ctx) return; const b=this.ctx.createBufferSource(),sr=this.ctx.sampleRate,bf=this.ctx.createBuffer(1,sr*0.3,sr),dt=bf.getChannelData(0); for(let i=0;i<dt.length;i++) dt[i]=(Math.random()*2-1)*Math.pow(1-i/dt.length,2); const f=this.ctx.createBiquadFilter(); f.type='lowpass'; f.frequency.value=800; const g=this.ctx.createGain(); g.gain.value=0.3*Save.settings.sfxVolume; b.buffer=bf; b.connect(f); f.connect(g); g.connect(this.ctx.destination); b.start(); },
  coin(){ this.beep(880,0.05,'sine',0.2); setTimeout(()=>this.beep(1320,0.08,'sine',0.15),50); },
  hurt(){ this.beep(200,0.15,'sawtooth',0.2); },
  bossWarn(){ this.beep(60,0.5,'pulse',0.3); setTimeout(()=>this.beep(120,0.3,'sawtooth',0.2),200); },
  ult(){ this.beep(200,0.6,'sawtooth',0.25); setTimeout(()=>this.beep(800,0.3,'square',0.2),300); }
};
window.Audio = Audio;

// ----- WQ 输入系统 -----
const Input = {
  keys: {},
  mouse: {x:0,y:0,down:false},
  init(){
    window.addEventListener('keydown', e=>{ this.keys[e.key.toLowerCase()]=true; if(e.key===' ') e.preventDefault(); });
    window.addEventListener('keyup', e=>{ this.keys[e.key.toLowerCase()]=false; });
    const c=document.getElementById('game');
    c.addEventListener('mousemove', e=>{ const r=c.getBoundingClientRect(); this.mouse.x=e.clientX-r.left; this.mouse.y=e.clientY-r.top; });
    c.addEventListener('mousedown', e=>{ this.mouse.down=true; });
    c.addEventListener('mouseup', e=>{ this.mouse.down=false; });
  },
  isDown(k){ return !!this.keys[k.toLowerCase()]; }
};
window.Input = Input;

// ----- WQ Toast 提示 -----
function toast(msg, dur=2000){
  const t=document.createElement('div'); t.className='toast'; t.textContent=msg;
  document.body.appendChild(t);
  setTimeout(()=>{ t.style.opacity='0'; t.style.transition='opacity 0.3s'; setTimeout(()=>t.remove(),300); }, dur);
}
window.toast = toast;

// ----- WQ 设置 -----
function toggleSettings(){ document.getElementById('settingsPanel').classList.toggle('hidden'); }
window.toggleSettings = toggleSettings;
function resetSave(){ if(confirm('WQ 警告：确定重置所有存档？')){ Save.reset(); } }
window.resetSave = resetSave;

// ==================== WQ 武器库 ====================
const Arsenal = {
  selectedTank: 0,
  render(){
    Save.updateGoldUI();
    this.renderTanks();
    this.renderWeapons();
    this.renderPreview();
  },
  renderTanks(){
    const list=document.getElementById('tankList'); list.innerHTML='<h3 style="color:#00F0FF;font-family:Orbitron;margin-bottom:10px;font-size:14px">WQ 坦克</h3>';
    WQ_TANKS.forEach((t,i)=>{
      const unlocked=this.isUnlocked(t);
      const equipped=Save.data.wqEquippedTank===t.id;
      const card=document.createElement('div');
      card.className='tank-card'+(equipped?' equipped':'')+(unlocked?'':' locked')+(t.unlock==='egg'?' egg':'');
      card.innerHTML=`<div class="tank-name" style="color:${t.color}">${t.name}</div><div class="tank-info">${unlocked?(equipped?'✓ 已装备':'点击装备'):(t.unlock==='gold'?t.price+' WQ金币':t.unlock==='clear'?'通关解锁':t.unlock==='egg'?'WQ彩蛋解锁':'未解锁')}</div>`;
      if(unlocked) card.onclick=()=>{ Save.data.wqEquippedTank=t.id; Save.save(); this.render(); };
      list.appendChild(card);
    });
  },
  isUnlocked(t){
    if(t.unlock==='init') return true;
    if(t.unlock==='gold') return Save.data.wqUnlockedTanks.includes(t.id) || Save.gold>=t.price;
    if(t.unlock==='clear') return Save.data.wqUnlockedTanks.includes(t.id);
    if(t.unlock==='egg') return Save.data.wqUnlockedTanks.includes(t.id);
    return Save.data.wqUnlockedTanks.includes(t.id);
  },
  renderWeapons(){
    const list=document.getElementById('weaponList'); list.innerHTML='<h3 style="color:#FF2D95;font-family:Orbitron;margin-bottom:10px;font-size:14px">WQ 武器 (装备3个)</h3>';
    WQ_WEAPONS.forEach(w=>{
      const unlocked=Save.data.wqUnlockedWeapons.includes(w.id);
      const equipped=Save.data.wqEquippedWeapons.includes(w.id);
      const card=document.createElement('div');
      card.className='weapon-card'+(equipped?' equipped':'')+(unlocked?'':' locked')+(w.unlock==='egg'?' egg':'');
      // WQ 修复：彩蛋武器显示"WQ彩蛋解锁"，不能用金币买
      let infoText;
      if(unlocked){ infoText = equipped ? '✓ 已装备' : '点击装备'; }
      else if(w.unlock==='egg'){ infoText = 'WQ彩蛋解锁'; }
      else { infoText = w.price+' WQ金币'; }
      card.innerHTML=`<div class="weapon-name" style="color:${w.color}">${w.id}</div><div class="weapon-info">${infoText}</div>`;
      if(unlocked){
        card.onclick=()=>{
          const eq=Save.data.wqEquippedWeapons;
          if(eq.includes(w.id)){ const idx=eq.indexOf(w.id); if(eq.filter(x=>x===w.id).length>1||eq.length>1) eq[idx]=eq[eq.length-1]; eq.pop(); }
          else if(eq.length<3) eq.push(w.id);
          else { eq[2]=w.id; toast('WQ: 已替换第3槽位'); }
          Save.save(); this.renderWeapons();
        };
      } else if(w.unlock==='egg'){
        // WQ 彩蛋武器：未通关彩蛋前不能购买
        card.onclick=()=>{ toast('WQ 需通关彩蛋地图才能解锁!'); };
      } else {
        card.onclick=()=>{
          if(Save.gold>=w.price){ Save.addGold(-w.price); Save.data.wqUnlockedWeapons.push(w.id); Save.save(); toast('WQ 解锁: '+w.id); this.renderWeapons(); }
          else toast('WQ金币不足!');
        };
      }
      list.appendChild(card);
    });
  },
  renderPreview(){
    const t=WQ_TANKS.find(x=>x.id===Save.data.wqEquippedTank)||WQ_TANKS[0];
    const cv=document.getElementById('tankPreviewCanvas'), ctx=cv.getContext('2d');
    ctx.clearRect(0,0,240,240);
    ctx.save(); ctx.translate(120,120); ctx.rotate(Date.now()*0.0005);
    // 绘制 WQ 坦克预览
    ctx.fillStyle=t.color; ctx.shadowBlur=20; ctx.shadowColor=t.color;
    ctx.fillRect(-30,-20,60,40);
    ctx.fillStyle='#1A2050'; ctx.fillRect(-20,-14,40,28);
    // 炮塔
    ctx.fillStyle=t.color; ctx.beginPath(); ctx.arc(0,0,14,0,Math.PI*2); ctx.fill();
    ctx.fillRect(0,-4,36,8);
    ctx.restore();
    // WQ 标记
    ctx.fillStyle='#00F0FF'; ctx.font='bold 12px Orbitron'; ctx.textAlign='center';
    ctx.fillText('WQ', 120, 220);
    // 属性
    const stats=document.getElementById('tankStats');
    stats.innerHTML=`<div style="color:${t.color};font-weight:700;margin-bottom:8px">${t.name}</div>`+
      `WQ生命: ${t.hp} <span class="stat-bar"><div style="width:${t.hp/180*100}%"></div></span><br>`+
      `WQ速度: ${t.speed.toFixed(1)} <span class="stat-bar"><div style="width:${t.speed/3*100}%"></div></span><br>`+
      `WQ火力: ${t.dmg} <span class="stat-bar"><div style="width:${t.dmg/55*100}%"></div></span><br>`+
      `<div style="margin-top:6px;color:#FF2D95;font-size:11px">WQ大招: ${this.getUltName(t.ult)}</div>`;
    setTimeout(()=>{ if(SceneManager.current==='arsenal') this.renderPreview(); }, 50);
  },
  getUltName(u){ return {bombard:'WQ全屏轰炸',dash:'WQ超新星冲刺',quake:'WQ震地冲击波',clone:'WQ量子分身',railgun:'WQ轨道炮',slow:'WQ时间减速',tsunami:'WQ海啸怒涛'}[u]||u; }
};
window.Arsenal = Arsenal;

// ==================== WQ 关卡选择 ====================
const LevelSelect = {
  chapter: 0,
  render(){
    const grid=document.getElementById('levelGrid'); grid.innerHTML='';
    const ch=WQ_CHAPTERS[this.chapter];
    for(let i=1;i<=10;i++){
      const lvNum=this.chapter*10+i;
      const isBoss=i===10;
      const unlocked=this.isUnlocked(lvNum);
      const stars=this.getStars(lvNum);
      const card=document.createElement('div');
      card.className='level-card'+(unlocked?'':' locked')+(isBoss?' boss':'');
      card.innerHTML=`<div class="level-num">${this.chapter+1}-${i}</div>${isBoss?'<div style="color:#FF4444;font-size:10px">WQ BOSS</div>':''}<div class="level-stars">${'★'.repeat(stars)}${'☆'.repeat(3-stars)}</div>`;
      if(unlocked) card.onclick=()=>startLevel(this.chapter+1, i);
      grid.appendChild(card);
    }
  },
  isUnlocked(lvNum){
    if(lvNum===1) return true;
    const p=Save.data.wqLevelProgress;
    if(lvNum<=p.maxLevel+1) return true;
    if(this.chapter+1<p.maxChapter) return true;
    if(this.chapter+1===p.maxChapter && lvNum<=p.maxLevel+1) return true;
    return lvNum<=p.maxLevel+1;
  },
  getStars(lvNum){ return Save.data.wqLevelProgress.stars[lvNum]||0; },
  switchChapter(idx){ this.chapter=idx; document.querySelectorAll('.tab-btn').forEach((b,i)=>b.classList.toggle('active',i===idx)); this.render(); }
};
window.LevelSelect = LevelSelect;
function switchChapter(i){ LevelSelect.switchChapter(i); }
window.switchChapter = switchChapter;

// ==================== WQ 游戏核心 ====================
const Game = {
  canvas: null, ctx: null,
  W: 0, H: 0,
  running: false, paused: false,
  lastTime: 0, dt: 0,
  player: null, enemies: [], bullets: [], particles: [], drops: [], walls: [],
  boss: null,
  level: {chapter:1, level:1, mode:'level'}, // mode: 'level'|'endless'|'egg'
  wave: 0, enemiesKilled: 0, enemiesTotal: 0, score: 0, goldEarned: 0,
  startTime: 0, timeLimit: 180,
  screenShake: 0, slowMo: 0,
  bgImage: null, bgFilter: '',
  spawnQueue: [],
  
  init(){
    this.canvas=document.getElementById('game');
    this.ctx=this.canvas.getContext('2d');
    this.resize(); window.addEventListener('resize',()=>this.resize());
    Input.init();
  },
  resize(){ this.W=this.canvas.width=window.innerWidth; this.H=this.canvas.height=window.innerHeight; },
  
  startLevel(chapter, level){
    this.level={chapter,level,mode:'level'};
    this.timeLimit=180;
    this.setupBattle();
  },
  startEndless(){
    this.level={chapter:1,level:1,mode:'endless'};
    this.wave=0; this.score=0; this.goldEarned=0;
    this.setupBattle();
  },
  startEgg(){
    this.level={chapter:0,level:0,mode:'egg'};
    Save.data.easterEgg.foundEggMap=true; Save.save();
    this.setupBattle();
  },
  
  setupBattle(){
    SceneManager.goto('gameScene');
    this.enemies=[]; this.bullets=[]; this.particles=[]; this.drops=[]; this.walls=[];
    this.boss=null; this.enemiesKilled=0; this.score=0; this.goldEarned=0;
    this.startTime=Date.now(); this.screenShake=0; this.slowMo=0;
    this.eggPhase = (this.level.mode==='egg') ? 1 : null;  // 彩蛋阶段控制
    this.eggBossDefeated = false;  // WQ 修复：重置 Boss 击败标志
    
    // 创建玩家
    const tankData=WQ_TANKS.find(t=>t.id===Save.data.wqEquippedTank)||WQ_TANKS[0];
    this.player=new Tank(this.W/2, this.H/2, tankData, true);
    
    // 加载背景图
    this.loadBackground();
    
    // 生成地图墙块 (含 WQ 墙块)
    this.generateWalls();
    
    // 生成敌人
    this.generateEnemies();
    
    this.updateHUD();
    this.running=true; this.paused=false;
    this.lastTime=performance.now();
    requestAnimationFrame(t=>this.loop(t));
  },
  
  loadBackground(){
    const img=new Image();
    // 使用内联 base64 图片 (避免 assets/*.jpg 外部文件依赖)
    if(this.level.mode==='egg'){
      img.src = WQ_BG_EGG || '';
      this.bgFilter='none';
    } else {
      img.src = WQ_BG_MAIN || '';
      const ch=WQ_CHAPTERS[(this.level.chapter-1)||0];
      this.bgFilter=ch?ch.filter:'none';
    }
    img.onload=()=>{ this.bgImage=img; };
    img.onerror=()=>{ this.bgImage=null; };
  },
  
  generateWalls(){
    // 边界墙
    const ts=32;
    // 生成 WQ 墙块 (每关3-5组)
    const wqCount=4;
    for(let i=0;i<wqCount;i++){
      const x=100+Math.random()*(this.W-300);
      const y=100+Math.random()*(this.H-300);
      this.walls.push({type:'wq',x,y,w:ts*2,h:ts,solid:true});
    }
    // 砖墙
    for(let i=0;i<8;i++){
      this.walls.push({type:'brick',x:Math.random()*this.W,y:Math.random()*this.H,w:ts,h:ts,solid:true,hp:30});
    }
    // 钢墙
    for(let i=0;i<3;i++){
      this.walls.push({type:'steel',x:Math.random()*this.W,y:Math.random()*this.H,w:ts,h:ts,solid:true});
    }
  },
  // WQ 工具：清除指定点周围半径 r 范围内的墙（用于 Boss 出生点清场）
  clearWallsAround(cx, cy, r){
    if(!this.walls) return;
    const before = this.walls.length;
    this.walls = this.walls.filter(w => {
      // 墙矩形中心
      const wx = w.x + w.w/2, wy = w.y + w.h/2;
      const d = Math.hypot(wx-cx, wy-cy);
      return d > r;  // 距离 > r 的保留
    });
  },
  generateEnemies(){
    if(this.level.mode==='endless'){
      this.wave++;
      const count=3+Math.floor(this.wave/3);
      this.enemiesTotal=count; this.enemiesKilled=0;
      const types=Object.keys(WQ_ENEMIES);
      for(let i=0;i<count;i++){
        const t=types[Math.floor(Math.random()*types.length)];
        const x=Math.random()<0.5?50:this.W-50;
        const y=50+Math.random()*(this.H-100);
        this.enemies.push(new Enemy(x,y,WQ_ENEMIES[t]));
      }
      // 每10波 Mini-Boss
      if(this.wave%10===0){ this.spawnBoss(Math.floor(this.wave/10)); }
      // 每5波商店
      if(this.wave%5===0 && this.wave>0){ setTimeout(()=>this.openShop(),100); }
    } else if(this.level.mode==='egg'){
      // ===== 彩蛋地图: 三阶段推进 (小怪 -> 更多小怪 -> 彩蛋Boss) =====
      this.eggPhase = this.eggPhase || 1;
      if(this.eggPhase===1){
        // 第一阶段: 6 只侦察车
        this.enemiesTotal=6; this.enemiesKilled=0;
        for(let i=0;i<6;i++){
          const x=Math.random()*this.W, y=Math.random()*this.H;
          this.enemies.push(new Enemy(x,y,WQ_ENEMIES.scout));
        }
        toast('WQ 彩蛋阶段 1/3: 清除侦察兵!',2000);
      } else if(this.eggPhase===2){
        // 第二阶段: 4 只精英敌人
        this.enemiesTotal=4; this.enemiesKilled=0;
        const mix=['tank','artillery','drone','tank'];
        mix.forEach((t,i)=>{
          const x=Math.random()*this.W, y=Math.random()*this.H;
          this.enemies.push(new Enemy(x,y,WQ_ENEMIES[t]));
        });
        toast('WQ 彩蛋阶段 2/3: 精英部队来袭!',2000);
      } else if(this.eggPhase===3){
        // 第三阶段: 彩蛋 Boss 登场
        this.enemiesTotal=0; this.enemiesKilled=0;
        this.spawnEggBoss();
      }
    } else {
      // 关卡模式
      const lvNum=this.level.chapter*10+this.level.level-10;
      const count=3+Math.floor(lvNum/2);
      this.enemiesTotal=count; this.enemiesKilled=0;
      const types=Object.keys(WQ_ENEMIES);
      for(let i=0;i<count;i++){
        const t=types[Math.min(types.length-1, Math.floor(i/3))];
        const x=Math.random()<0.5?50:this.W-50;
        const y=50+Math.random()*(this.H-100);
        this.enemies.push(new Enemy(x,y,WQ_ENEMIES[t]));
      }
      // Boss 关
      if(this.level.level===10){
        const bossKey=Object.keys(WQ_BOSSES)[this.level.chapter-1];
        this.spawnBoss(this.level.chapter);
      }
    }
    this.updateHUD();
  },
  
  spawnBoss(chapter){
    const bossKey=Object.keys(WQ_BOSSES)[chapter-1];
    const bd=WQ_BOSSES[bossKey];
    // WQ 修复：清除 Boss 出生点附近的墙，避免一出生就嵌墙里永久卡死
    this.clearWallsAround(this.W/2, 100, 80);
    this.boss=new Boss(this.W/2, 100, bd, bossKey, chapter);
    document.getElementById('bossBarWrap').classList.remove('hidden');
    document.getElementById('bossName').textContent=bossKey;
    Audio.bossWarn();
    this.screenShake=20;
  },

  spawnEggBoss(){
    // 彩蛋专属 Boss: WQ-浪尖霸主 (chapter=0)
    const bossKey = "WQ-浪尖霸主";
    const bd=WQ_BOSSES[bossKey];
    // WQ 修复：清除彩蛋 Boss 出生点附近的墙
    this.clearWallsAround(this.W/2, 100, 80);
    this.boss=new Boss(this.W/2, 100, bd, bossKey, 0);
    document.getElementById('bossBarWrap').classList.remove('hidden');
    document.getElementById('bossName').textContent=bossKey+' ★彩蛋BOSS★';
    Audio.bossWarn();
    this.screenShake=25;
    toast('⚠ WQ 浪尖霸主降临!',2500);
  },
  
  loop(t){
    if(!this.running) return;
    this.dt=Math.min(50, t-this.lastTime)/16.67;
    this.lastTime=t;
    if(this.slowMo>0){ this.slowMo-=this.dt*16.67; this.dt*=0.2; }
    if(!this.paused){ this.update(); }
    this.render();
    requestAnimationFrame(t=>this.loop(t));
  },
  
  update(){
    // 玩家
    if(this.player) this.player.update(this.dt);
    // 敌人
    this.enemies.forEach(e=>e.update(this.dt));
    // Boss
    if(this.boss) this.boss.update(this.dt);
    // 子弹
    this.bullets=this.bullets.filter(b=>{ b.update(this.dt); return b.alive; });
    // 粒子
    this.particles=this.particles.filter(p=>{ p.update(this.dt); return p.life>0; });
    // 道具
    this.drops.forEach(d=>d.update(this.dt));
    // 碰撞
    this.checkCollisions();
    // 屏幕震动衰减
    if(this.screenShake>0) this.screenShake*=0.9;
    // 清理死亡敌人
    this.enemies=this.enemies.filter(e=>{
      if(e.hp<=0){
        this.onEnemyKilled(e); return false;
      } return true;
    });
    if(this.boss && this.boss.hp<=0){ this.onBossKilled(); }
    // 检查胜利
    this.checkVictory();
    this.updateHUD();
  },
  
  checkCollisions(){
    // 子弹 vs 墙/坦克
    for(const b of this.bullets){
      if(!b.alive) continue;
      // vs 墙
      for(const w of this.walls){
        if(b.x>w.x&&b.x<w.x+w.w&&b.y>w.y&&b.y<w.y+w.h){
          b.alive=false;
          this.spawnExplosion(b.x,b.y,8,b.color);
          if(w.type==='brick'){ w.hp-=b.dmg; if(w.hp<=0) this.walls=this.walls.filter(x=>x!==w); }
          break;
        }
      }
      // vs 敌人
      if(b.fromPlayer){
        for(const e of this.enemies){
          if(e.contains(b.x,b.y)){ e.takeDamage(b.dmg); b.alive=false; this.spawnExplosion(b.x,b.y,10,b.color); Audio.hurt(); break; }
        }
        if(this.boss && this.boss.contains(b.x,b.y)){ this.boss.takeDamage(b.dmg); b.alive=false; this.spawnExplosion(b.x,b.y,12,b.color); }
      } else {
        // 敌人子弹 vs 玩家
        if(this.player && this.player.contains(b.x,b.y)){
          this.player.takeDamage(b.dmg); b.alive=false; this.spawnExplosion(b.x,b.y,10,b.color); Audio.hurt();
          this.screenShake=Math.max(this.screenShake,8);
        }
      }
    }
    // 道具拾取（放宽为距离检测：道具会阻挡坦克前进，所以接触边缘即可拾取）
    for(const d of this.drops){
      if(this.player && !d.collected){
        const dd = Math.hypot(this.player.x-d.x, this.player.y-d.y);
        if(dd < this.player.size + 12){ d.collect(); } // 道具半径约10，+2容错
      }
    }
    this.drops=this.drops.filter(d=>!d.collected);
  },
  
  onEnemyKilled(e){
    this.enemiesKilled++; this.score+=e.data.score||50;
    const gold=Math.floor(20+Math.random()*30); this.goldEarned+=gold;
    this.spawnExplosion(e.x,e.y,25,e.data.color);
    Audio.explosion();
    // 能量
    if(this.player){ this.player.mp=Math.min(100,this.player.mp+5); }
    // 道具掉落
    if(Math.random()<0.2){ this.drops.push(new Drop(e.x,e.y)); }
  },
  
  onBossKilled(){
    this.spawnExplosion(this.boss.x,this.boss.y,60,this.boss.data.color);
    Audio.explosion();
    this.screenShake=30; this.slowMo=1500;
    const goldReward=500+this.boss.chapter*500;
    this.goldEarned+=goldReward; this.score+=2000;
    document.getElementById('bossBarWrap').classList.add('hidden');
    // 彩蛋地图 Boss
    if(this.level.mode==='egg'){
      this.eggBossDefeated = true;  // WQ 修复：标记 Boss 已击败，checkVictory 才会显示胜利
      Save.data.easterEgg.eggMapCleared=true;
      Save.data.easterEgg.eggMapClearCount++;
      if(!Save.data.wqUnlockedTanks.includes('WQ-07')){
        Save.data.wqUnlockedTanks.push('WQ-07');
        Save.addGold(10000);
        Save.data.easterEgg.achievements.push('浪尖之上');
        toast('WQ 成就: 浪尖之上! 解锁 WQ-07 菁英!',4000);
      } else { Save.addGold(1000); }
      // WQ 修复：解锁彩蛋专属隐藏武器 WQ-浪尖炮
      if(!Save.data.wqUnlockedWeapons.includes('WQ-浪尖炮')){
        Save.data.wqUnlockedWeapons.push('WQ-浪尖炮');
        toast('WQ 解锁隐藏武器: WQ-浪尖炮!',4000);
      }
      Save.save();
      document.getElementById('eggTrigger').classList.add('cleared');
    }
    this.boss=null;
  },
  
  checkVictory(){
    if(this.boss) return;
    if(this.enemies.length===0){
      if(this.level.mode==='level'){
        // 通关 (key统一: 0-based chapter*10 + 1-based level)
        const lvKey = (this.level.chapter-1)*10 + this.level.level;
        const stars=this.calcStars();
        Save.data.wqLevelProgress.stars[lvKey]=stars;
        if(this.level.level<10){ Save.data.wqLevelProgress.maxLevel=Math.max(Save.data.wqLevelProgress.maxLevel,this.level.level+1); }
        else { Save.data.wqLevelProgress.maxChapter=Math.max(Save.data.wqLevelProgress.maxChapter,this.level.chapter+1); Save.data.wqLevelProgress.maxLevel=1; }
        Save.addGold(this.goldEarned+stars*100);
        Save.save();
        this.showVictory(stars);
        this.running=false;
      } else if(this.level.mode==='endless'){
        // 继续下一波
        setTimeout(()=>{ if(this.running) this.generateEnemies(); },2000);
      } else if(this.level.mode==='egg'){
        // 彩蛋地图: 阶段推进
        if(this.eggPhase===1){
          this.eggPhase=2;
          setTimeout(()=>{ if(this.running) this.generateEnemies(); },1500);
        } else if(this.eggPhase===2){
          this.eggPhase=3;
          setTimeout(()=>{ if(this.running) this.generateEnemies(); },1500);
        } else if(this.eggPhase===3 && this.eggBossDefeated){
          // WQ 修复：只有 Boss 真正被击败后才显示胜利
          // （之前 Bug：阶段2清空后 setTimeout 还没生成 Boss，下一帧 checkVictory 就误判胜利）
          this.showEggVictory();
          this.running=false;
        }
        // eggPhase===3 但 eggBossDefeated=false 时：Boss 还在战斗或等待生成，什么都不做
      }
    }
  },
  
  calcStars(){
    let stars=1;
    if(this.player && this.player.hp>this.player.maxHp*0.5) stars=2;
    const time=(Date.now()-this.startTime)/1000;
    if(time<this.timeLimit) stars=3;
    return stars;
  },
  
  showVictory(stars){
    const c=document.getElementById('modalContent');
    c.innerHTML=`<h2 style="color:#FFB800">WQ 胜利!</h2><p>WQ关卡 ${this.level.chapter}-${this.level.level}</p><div class="stars">${'★'.repeat(stars)}${'☆'.repeat(3-stars)}</div><p>WQ得分: ${this.score}</p><p>WQ金币: +${this.goldEarned+stars*100}</p><div class="modal-buttons"><button class="wq-btn primary" onclick="SceneManager.goto('levelSelect')">WQ 继续</button><button class="wq-btn" onclick="SceneManager.goto('mainMenu')">WQ 返回</button></div>`;
    document.getElementById('modal').classList.remove('hidden');
  },
  
  showEggVictory(){
    const c=document.getElementById('modalContent');
    c.innerHTML=`<h2 style="color:#00E5FF">WQ 浪尖之上 · 菁英永存!</h2><p>🥚 WQ 彩蛋地图通关!</p><p>已解锁隐藏坦克: <b style="color:#00E5FF">WQ-07 菁英</b></p><p>WQ金币: +10000</p><div class="modal-buttons"><button class="wq-btn primary" onclick="SceneManager.goto('arsenal')">WQ 查看武器库</button><button class="wq-btn" onclick="SceneManager.goto('mainMenu')">WQ 返回</button></div>`;
    document.getElementById('modal').classList.remove('hidden');
  },
  
  gameOver(){
    this.running=false;
    if(this.level.mode==='endless'){
      const best=Save.data.wqEndlessBest;
      if(this.wave>best.wave){ Save.data.wqEndlessBest={wave:this.wave,score:this.score,date:new Date().toLocaleDateString()}; }
      Save.data.wqEndlessLeaderboard.push({name:'WQ玩家',wave:this.wave,score:this.score,date:new Date().toLocaleDateString()});
      Save.data.wqEndlessLeaderboard.sort((a,b)=>b.wave-a.wave);
      Save.data.wqEndlessLeaderboard=Save.data.wqEndlessLeaderboard.slice(0,10);
      Save.addGold(this.goldEarned);
      Save.save();
    }
    const c=document.getElementById('modalContent');
    c.innerHTML=`<h2 style="color:#FF4444">WQ GAME OVER</h2>${this.level.mode==='endless'?`<p>WQ 波次: ${this.wave}</p><p>WQ 得分: ${this.score}</p>`:`<p>WQ 关卡 ${this.level.chapter}-${this.level.level}</p>`}<p>WQ 得分: ${this.score}</p><div class="modal-buttons"><button class="wq-btn primary" onclick="document.getElementById('modal').classList.add('hidden');Game.setupBattle()">WQ 重试</button><button class="wq-btn" onclick="SceneManager.goto('mainMenu');document.getElementById('modal').classList.add('hidden')">WQ 返回</button></div>`;
    document.getElementById('modal').classList.remove('hidden');
  },
  
  spawnExplosion(x,y,count,color){
    for(let i=0;i<count;i++){
      this.particles.push(new Particle(x,y,color));
    }
  },
  
  updateHUD(){
    if(!this.player) return;
    const p=this.player;
    document.getElementById('hpBar').style.width=(p.hp/p.maxHp*100)+'%';
    document.getElementById('hpText').textContent=`${Math.ceil(p.hp)}/${p.maxHp}`;
    document.getElementById('mpBar').style.width=p.mp+'%';
    document.getElementById('mpText').textContent=`${Math.floor(p.mp)}/100`;
    document.getElementById('shieldBar').style.width=Math.min(100,p.shield)+'%';
    document.getElementById('shieldText').textContent=Math.floor(p.shield);
    document.getElementById('goldText').textContent=this.goldEarned;
    document.getElementById('ultBar').style.width=p.mp+'%';
    document.getElementById('hudLevel').textContent=this.level.mode==='endless'?`WQ 无尽 · 波次 ${this.wave}`:this.level.mode==='egg'?'WQ 彩蛋地图':`WQ 关卡 ${this.level.chapter}-${this.level.level}`;
    document.getElementById('hudWave').textContent=`WQ 敌人 ${this.enemiesKilled}/${this.enemiesTotal}`;
    document.getElementById('hudScore').textContent=`WQ 得分 ${this.score}`;
    // Boss 血条
    if(this.boss){
      document.getElementById('bossBar').style.width=(this.boss.hp/this.boss.maxHp*100)+'%';
    }
    // 武器槽
    this.renderWeaponSlots();
    // 小地图
    this.renderMinimap();
  },
  
  renderWeaponSlots(){
    const slots=document.getElementById('weaponSlots'); 
    if(slots.children.length!==3){
      slots.innerHTML='';
      for(let i=0;i<3;i++){
        const d=document.createElement('div'); d.className='weapon-slot'; d.onclick=()=>{ this.player.weaponIdx=i; };
        slots.appendChild(d);
      }
    }
    if(this.player){
      Save.data.wqEquippedWeapons.forEach((wid,i)=>{
        const w=WQ_WEAPONS.find(x=>x.id===wid); if(!w) return;
        const slot=slots.children[i];
        slot.innerHTML=`<div>[${i+1}] ${w.id}</div><div class="cd"><div style="width:${this.player.weaponCooldowns[i]>0?(1-this.player.weaponCooldowns[i]/(w.cd||300))*100:100}%"></div></div>`;
        slot.classList.toggle('active', this.player.weaponIdx===i);
      });
    }
  },
  
  renderMinimap(){
    const cv=document.getElementById('minimap'), ctx=cv.getContext('2d');
    ctx.clearRect(0,0,120,120);
    ctx.fillStyle='rgba(10,14,39,0.7)'; ctx.fillRect(0,0,120,120);
    const sx=120/this.W, sy=120/this.H;
    // 玩家
    if(this.player){ ctx.fillStyle='#3DDC84'; ctx.fillRect(this.player.x*sx-2,this.player.y*sy-2,4,4); }
    // 敌人
    ctx.fillStyle='#FF4444';
    this.enemies.forEach(e=>ctx.fillRect(e.x*sx-1,e.y*sy-1,2,2));
    if(this.boss){ ctx.fillStyle='#FFD600'; ctx.fillRect(this.boss.x*sx-3,this.boss.y*sy-3,6,6); }
  },
  
  render(){
    const ctx=this.ctx;
    ctx.save();
    // 屏幕震动
    if(this.screenShake>0.5 && Save.settings.screenShake){
      ctx.translate((Math.random()-0.5)*this.screenShake,(Math.random()-0.5)*this.screenShake);
    }
    // 背景
    ctx.fillStyle='#0A0E27'; ctx.fillRect(0,0,this.W,this.H);
    if(this.bgImage){
      ctx.save();
      ctx.filter=this.bgFilter||'none';
      ctx.drawImage(this.bgImage,0,0,this.W,this.H);
      ctx.restore();
      // 暗色叠加
      ctx.fillStyle=this.level.mode==='egg'?'rgba(10,14,39,0.55)':'rgba(10,14,39,0.6)';
      ctx.fillRect(0,0,this.W,this.H);
    } else {
      // 无图时的渐变背景
      const grad=ctx.createRadialGradient(this.W/2,this.H/2,0,this.W/2,this.H/2,this.W/2);
      grad.addColorStop(0,'#1A1F4E'); grad.addColorStop(1,'#0A0E27');
      ctx.fillStyle=grad; ctx.fillRect(0,0,this.W,this.H);
    }
    // 墙块
    this.renderWalls(ctx);
    // 道具
    this.drops.forEach(d=>d.render(ctx));
    // 子弹
    this.bullets.forEach(b=>b.render(ctx));
    // 敌人
    this.enemies.forEach(e=>e.render(ctx));
    // Boss
    if(this.boss) this.boss.render(ctx);
    // 玩家
    if(this.player) this.player.render(ctx);
    // 粒子
    this.particles.forEach(p=>p.render(ctx));
    ctx.restore();
  },
  
  renderWalls(ctx){
    for(const w of this.walls){
      if(w.type==='wq'){
        this.drawWQWall(ctx,w.x,w.y,w.w,w.h);
      } else if(w.type==='brick'){
        ctx.fillStyle='#8B4513'; ctx.fillRect(w.x,w.y,w.w,w.h);
        ctx.strokeStyle='#5D2E0A'; ctx.strokeRect(w.x,w.y,w.w,w.h);
      } else if(w.type==='steel'){
        ctx.fillStyle='#9E9E9E'; ctx.fillRect(w.x,w.y,w.w,w.h);
        ctx.strokeStyle='#616161'; ctx.strokeRect(w.x,w.y,w.w,w.h);
        ctx.fillStyle='#E0E0E0'; ctx.fillRect(w.x+4,w.y+4,w.w-8,4);
      }
    }
  },
  
  drawWQWall(ctx,x,y,w,h){
    // WQ 字符墙块
    const cols=Math.floor(w/16), rows=Math.floor(h/16);
    const colors = this.level.mode==='egg' ? ['#8B5A2B','#F5E6D3'] : 
                   this.level.chapter===1 ? ['#D4A04A','#8B6B2A'] :
                   this.level.chapter===2 ? ['#00F0FF','#FF2D95'] : ['#E0E8FF','#4A3A8C'];
    ctx.font='bold 11px Orbitron'; ctx.textAlign='center'; ctx.textBaseline='middle';
    for(let r=0;r<rows;r++){
      for(let c=0;c<cols;c++){
        const ch=((r+c)%2===0)?'W':'Q';
        ctx.fillStyle=ch==='W'?colors[0]:colors[1];
        ctx.shadowBlur=4; ctx.shadowColor=colors[0];
        ctx.fillText(ch, x+c*16+8, y+r*16+8);
      }
    }
    ctx.shadowBlur=0;
  },
  
  pause(){ this.paused=!this.paused; if(this.paused){ toast('WQ 已暂停 - 按P继续'); } },
  
  openShop(){
    this.paused=true;
    document.getElementById('shopWave').textContent=this.wave;
    const items=document.getElementById('shopItems'); items.innerHTML='';
    const shopItems=[
      {name:'WQ 医疗包',desc:'回复 50 WQ血量',price:200,act:()=>{ this.player.hp=Math.min(this.player.maxHp,this.player.hp+50); }},
      {name:'WQ 护盾',desc:'+50 WQ护盾',price:300,act:()=>{ this.player.shield+=50; }},
      {name:'WQ 能量',desc:'WQ大招满槽',price:150,act:()=>{ this.player.mp=100; }},
      {name:'WQ 火力强化',desc:'+10 WQ伤害(本局)',price:500,act:()=>{ this.player.dmgBonus+=10; }}
    ];
    shopItems.forEach(it=>{
      const d=document.createElement('div'); d.className='shop-item';
      d.innerHTML=`<h4>${it.name}</h4><p>${it.desc}</p><p style="color:#FFB800;margin-top:6px">${it.price} WQ金币</p>`;
      d.onclick=()=>{
        if(this.goldEarned>=it.price){ this.goldEarned-=it.price; it.act(); toast('WQ 购买: '+it.name); d.style.opacity='0.4'; }
        else toast('WQ金币不足!');
      };
      items.appendChild(d);
    });
    document.getElementById('shop').classList.remove('hidden');
  }
};
window.Game = Game;

function pauseGame(){ Game.pause(); }
window.pauseGame = pauseGame;
function startBattle(){ startLevel(1,1); }
window.startBattle = startBattle;
function startLevel(c,l){ Game.startLevel(c,l); document.getElementById('modal').classList.add('hidden'); }
window.startLevel = startLevel;
function startEndless(){ Game.startEndless(); document.getElementById('modal').classList.add('hidden'); }
window.startEndless = startEndless;
function closeShop(){ document.getElementById('shop').classList.add('hidden'); Game.paused=false; }
window.closeShop = closeShop;
function rerollShop(){ if(Game.goldEarned>=100){ Game.goldEarned-=100; Game.openShop(); } else toast('WQ金币不足!'); }
window.rerollShop = rerollShop;

// ----- 彩蛋入口 -----
function enterEggMap(){
  if(confirm('⚠ WQ 检测到隐藏信号，是否前往 WQ 浪尖菁英秘密基地？')){
    Game.startEgg();
  }
}
window.enterEggMap = enterEggMap;

// ==================== WQ 实体类 ====================
// ===== WQ 碰撞辅助：实体(正方形) AABB 检测 =====
function WQ_AABB(x1,y1,s1,x2,y2,s2){ return Math.abs(x1-x2)<(s1+s2) && Math.abs(y1-y2)<(s1+s2); }
function WQ_AABB_Wall(x,y,s,w){ return (x+s)>w.x && (x-s)<(w.x+w.w) && (y+s)>w.y && (y-s)<(w.y+w.h); }
// 检查实体在新坐标 (nx,ny) 处是否被任何障碍物阻挡
//   self: 实体自身；options 可临时跳过某类碰撞
function WQ_isBlocked(self, nx, ny, options={}){
  const s = self.size;
  // 边界
  if(nx-s < 0 || nx+s > Game.W || ny-s < 0 || ny+s > Game.H) return true;
  if(!options.ignoreWalls){
    for(const w of Game.walls){ if(w.solid && WQ_AABB_Wall(nx,ny,s,w)) return true; }
  }
  if(!options.ignoreDrops){
    for(const d of Game.drops){ if(!d.collected && WQ_AABB(nx,ny,s, d.x,d.y, 10)) return true; }
  }
  if(!options.ignoreBoss){
    if(Game.boss && Game.boss!==self && WQ_AABB(nx,ny,s, Game.boss.x,Game.boss.y,Game.boss.size)) return true;
  }
  if(!options.ignorePlayer){
    if(Game.player && Game.player!==self && WQ_AABB(nx,ny,s, Game.player.x,Game.player.y,Game.player.size)) return true;
  }
  if(!options.ignoreEnemies){
    for(const e of Game.enemies){
      if(e===self) continue;
      // 玩家坦克 ↔ 克隆坦克：友军互不阻挡（克隆坦克 isPlayer=true）
      if(self.isPlayer && e.isPlayer) continue;
      const es = e.size || 16;
      if(WQ_AABB(nx,ny,s, e.x,e.y,es)) return true;
    }
  }
  return false;
}

class Tank {
  constructor(x,y,data,isPlayer){
    this.x=x; this.y=y; this.data=data; this.isPlayer=isPlayer;
    this.angle=0; this.turretAngle=0;
    this.hp=data.hp; this.maxHp=data.hp;
    this.shield=0; this.mp=0;
    this.speed=data.speed; this.fireRate=data.fireRate;
    this.lastFire=0; this.size=18;
    this.weaponIdx=0; this.weaponCooldowns=[0,0,0];
    this.dmgBonus=0;
    this.stealthTimer=0; this.invuln=0;
    this.trail=[];
  }
  update(dt){
    if(this.invuln>0) this.invuln-=dt*16.67;
    // —— WQ 分轴碰撞移动：先X后Y，被阻挡则回退该轴 ——
    const oldX=this.x, oldY=this.y;
    let mv=false;
    let dx=0, dy=0;
    if(Input.isDown('w')||Input.isDown('arrowup')){ dy-=this.speed*dt; this.angle=-Math.PI/2; mv=true; }
    if(Input.isDown('s')||Input.isDown('arrowdown')){ dy+=this.speed*dt; this.angle=Math.PI/2; mv=true; }
    if(Input.isDown('a')||Input.isDown('arrowleft')){ dx-=this.speed*dt; this.angle=Math.PI; mv=true; }
    if(Input.isDown('d')||Input.isDown('arrowright')){ dx+=this.speed*dt; this.angle=0; mv=true; }
    // 先试 X 轴
    const tryX = oldX + dx;
    if(!WQ_isBlocked(this, tryX, oldY)){ this.x = tryX; }
    // 再试 Y 轴（基于更新后的 X）
    const tryY = oldY + dy;
    if(!WQ_isBlocked(this, this.x, tryY)){ this.y = tryY; }
    // 拖尾
    if(mv){ this.trail.push({x:this.x,y:this.y,a:0.5}); if(this.trail.length>10) this.trail.shift(); }
    this.trail.forEach(t=>t.a-=0.05*dt); this.trail=this.trail.filter(t=>t.a>0);
    // 炮塔朝向鼠标
    this.turretAngle=Math.atan2(Input.mouse.y-this.y, Input.mouse.x-this.x);
    // 开火
    if(Input.isDown('j')||Input.isDown(' ')||Input.mouse.down){ this.fire(); }
    // 切换武器
    if(Input.isDown('1')) this.weaponIdx=0;
    if(Input.isDown('2')) this.weaponIdx=1;
    if(Input.isDown('3')) this.weaponIdx=2;
    // 大招
    if((Input.isDown('k')||Input.isDown('shift'))&&this.mp>=100){ this.ultimate(); this.mp=0; }
    // 武器冷却
    for(let i=0;i<3;i++){ if(this.weaponCooldowns[i]>0) this.weaponCooldowns[i]-=dt*16.67; }
    // 被动: 回血
    if(this.data.passive==='regen' && Date.now()%10000<16) this.hp=Math.min(this.maxHp,this.hp+5);
    // 被动: 隐身
    if(this.data.passive==='stealth'){ this.stealthTimer+=dt*16.67; if(this.stealthTimer>15000) this.stealthTimer=0; }
  }
  fire(){
    if(Date.now()-this.lastFire<this.fireRate) return;
    const wid=Save.data.wqEquippedWeapons[this.weaponIdx]||'WQ-穿甲弹';
    const w=WQ_WEAPONS.find(x=>x.id===wid); if(!w) return;
    if(this.weaponCooldowns[this.weaponIdx]>0) return;
    this.lastFire=Date.now();
    if(w.cd) this.weaponCooldowns[this.weaponIdx]=w.cd;
    const dmg=w.dmg+this.dmgBonus;
    const spd=w.speed;
    const col=w.color;
    Audio.fire();
    // 不同武器类型
    if(w.type==='single'||w.type==='rapid'){
      Game.bullets.push(new Bullet(this.x+Math.cos(this.turretAngle)*25, this.y+Math.sin(this.turretAngle)*25, this.turretAngle, spd, dmg, col, true));
    } else if(w.type==='shotgun'){
      for(let i=-2;i<=2;i++){ Game.bullets.push(new Bullet(this.x,this.y,this.turretAngle+i*0.15,spd,dmg,col,true)); }
    } else if(w.type==='laser'){
      Game.bullets.push(new Bullet(this.x,this.y,this.turretAngle,spd*1.5,dmg,col,true,'laser'));
    } else if(w.type==='homing'){
      Game.bullets.push(new Bullet(this.x,this.y,this.turretAngle,spd,dmg,col,true,'homing'));
    } else if(w.type==='blackhole'){
      Game.bullets.push(new Bullet(this.x,this.y,this.turretAngle,spd,dmg*2,col,true,'blackhole'));
    }
  }
  ultimate(){
    Audio.ult();
    Game.screenShake=15;
    const u=this.data.ult;
    if(u==='bombard'){ Game.enemies.forEach(e=>e.takeDamage(e.hp*0.5)); if(Game.boss) Game.boss.takeDamage(Game.boss.maxHp*0.1); }
    else if(u==='dash'){ this.invuln=3000; this.speed*=2; setTimeout(()=>this.speed=this.data.speed,3000); }
    else if(u==='quake'){ Game.enemies.forEach(e=>{ e.stunned=2000; }); this.shield=100; }
    else if(u==='clone'){ for(let i=0;i<2;i++){ const c=new Tank(this.x+30*(i+1),this.y,this.data,true); c.invuln=10000; Game.enemies.push(c); } }
    else if(u==='railgun'){ Game.enemies=Game.enemies.filter(e=>{ if(e.hp<100){ Game.spawnExplosion(e.x,e.y,15,e.data.color); return false; } e.takeDamage(50); return true; }); }
    else if(u==='slow'){ Game.slowMo=8000; }
    else if(u==='tsunami'){ Game.enemies.forEach(e=>{ e.takeDamage(40); e.y+=20; }); Game.screenShake=25; }
    toast('WQ 大招: '+Arsenal.getUltName(u)+'!',1500);
  }
  takeDamage(dmg){
    if(this.invuln>0) return;
    if(this.shield>0){ this.shield-=dmg; if(this.shield<0){ this.hp-=Math.abs(this.shield); this.shield=0; } }
    else this.hp-=dmg;
    if(this.data.passive==='lifesteal'){} // 已在击杀时处理
    if(this.hp<=0){ Game.gameOver(); }
  }
  contains(x,y){ return Math.abs(x-this.x)<this.size && Math.abs(y-this.y)<this.size; }
  collidesWall(w){ return this.x+this.size>w.x && this.x-this.size<w.x+w.w && this.y+this.size>w.y && this.y-this.size<w.y+w.h; }
  render(ctx){
    // 拖尾
    this.trail.forEach(t=>{ ctx.fillStyle=this.data.color; ctx.globalAlpha=t.a*0.3; ctx.fillRect(t.x-6,t.y-6,12,12); });
    ctx.globalAlpha=1;
    // 隐身
    if(this.data.passive==='stealth' && this.stealthTimer>10000 && this.stealthTimer<15000) ctx.globalAlpha=0.3;
    ctx.save();
    ctx.translate(this.x,this.y);
    // 车身
    ctx.fillStyle=this.data.color; ctx.shadowBlur=15; ctx.shadowColor=this.data.color;
    ctx.fillRect(-this.size,-this.size+2,this.size*2,this.size*2-4);
    ctx.fillStyle='#1A2050'; ctx.fillRect(-this.size+3,-this.size+5,this.size*2-6,this.size*2-10);
    // 炮塔
    ctx.rotate(this.turretAngle);
    ctx.fillStyle=this.data.color;
    ctx.fillRect(0,-4,30,8);
    ctx.beginPath(); ctx.arc(0,0,10,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#1A2050'; ctx.beginPath(); ctx.arc(0,0,6,0,Math.PI*2); ctx.fill();
    ctx.restore();
    ctx.globalAlpha=1;
    // HP 条
    if(this.hp<this.maxHp){
      ctx.fillStyle='#FF4444'; ctx.fillRect(this.x-20,this.y-this.size-8,40,3);
      ctx.fillStyle='#3DDC84'; ctx.fillRect(this.x-20,this.y-this.size-8,40*this.hp/this.maxHp,3);
    }
  }
}

class Enemy {
  constructor(x,y,data){
    this.x=x; this.y=y; this.data=data;
    this.hp=data.hp; this.maxHp=data.hp;
    this.angle=0; this.size=16;
    this.lastFire=Date.now()+Math.random()*1000;
    this.stunned=0; this.alive=true;
  }
  update(dt){
    if(this.stunned>0){ this.stunned-=dt*16.67; return; }
    // AI: 朝玩家移动 + 保持距离
    if(!Game.player) return;
    const oldX=this.x, oldY=this.y;
    const dxVec=Game.player.x-this.x, dyVec=Game.player.y-this.y;
    const dist=Math.sqrt(dxVec*dxVec+dyVec*dyVec) || 1;
    this.angle=Math.atan2(dyVec,dxVec);
    let dir = 0; // +1 前进, -1 后退, 0 停留
    if(dist>200) dir = 1;
    else if(dist<150) dir = -1;
    const step = dir * this.data.speed * dt;
    const mx = dxVec/dist * step;  // 期望的 X 增量
    const my = dyVec/dist * step;  // 期望的 Y 增量
    // 先试 X 轴
    const tryX = oldX + mx;
    if(!WQ_isBlocked(this, tryX, oldY)){ this.x = tryX; }
    // 再试 Y 轴（基于更新后的 X）
    const tryY = oldY + my;
    if(!WQ_isBlocked(this, this.x, tryY)){ this.y = tryY; }
    // 开火
    if(Date.now()-this.lastFire>this.data.fireRate){
      this.lastFire=Date.now();
      Game.bullets.push(new Bullet(this.x,this.y,this.angle,4,this.data.dmg,this.data.color,false));
    }
  }
  takeDamage(dmg){ this.hp-=dmg; }
  contains(x,y){ return Math.abs(x-this.x)<this.size && Math.abs(y-this.y)<this.size; }
  render(ctx){
    ctx.save(); ctx.translate(this.x,this.y); ctx.rotate(this.angle);
    ctx.fillStyle=this.data.color; ctx.shadowBlur=8; ctx.shadowColor=this.data.color;
    ctx.fillRect(-this.size,-this.size+2,this.size*2,this.size*2-4);
    ctx.fillStyle='#1A2050'; ctx.fillRect(-this.size+3,-this.size+5,this.size*2-6,this.size*2-10);
    ctx.fillStyle=this.data.color; ctx.fillRect(0,-3,24,6);
    ctx.restore();
    // HP
    if(this.hp<this.maxHp){
      ctx.fillStyle='#FF4444'; ctx.fillRect(this.x-16,this.y-this.size-6,32,2);
      ctx.fillStyle='#FF8A80'; ctx.fillRect(this.x-16,this.y-this.size-6,32*this.hp/this.maxHp,2);
    }
  }
}

class Boss {
  constructor(x,y,data,name,chapter){
    this.x=x; this.y=y; this.data=data; this.name=name; this.chapter=chapter;
    this.hp=data.hp; this.maxHp=data.hp;
    this.phase=1; this.size=40;
    this.angle=0; this.lastFire=Date.now();
    this.moveT=0;
    // WQ 修复：方向系数，撞墙后主动反向，避免卡死等 sin 反转
    this.dirX = 1;
    this.dirY = 1;
    // WQ 修复：Y 轴基准点（出生 Y），巡逻围绕此点上下漂移
    this.baseY = y;
  }
  update(dt){
    this.moveT+=dt;
    // —— WQ 修复：分轴碰撞 + 撞墙主动反向 + Y轴增量式 ——
    const oldX=this.x, oldY=this.y;
    // X 方向：sin 提供基础速度波形，乘以 dirX 实现撞墙反向
    const dx = Math.sin(this.moveT*0.02) * 2 * dt * this.dirX;
    // Y 方向：增量式（不再用 targetY - oldY），围绕 baseY 漂移
    const dy = Math.sin(this.moveT*0.015) * 0.8 * dt * this.dirY;
    // 先试 X 轴
    const tryX = oldX + dx;
    if(!WQ_isBlocked(this, tryX, oldY)){
      this.x = tryX;
    } else {
      // X 轴撞墙：立即反向，下一帧就会朝相反方向移动
      this.dirX *= -1;
    }
    // 再试 Y 轴（基于更新后的 X）
    const tryY = oldY + dy;
    if(!WQ_isBlocked(this, this.x, tryY)){
      this.y = tryY;
    } else {
      // Y 轴撞墙：立即反向
      this.dirY *= -1;
    }
    // WQ 安全网：Y 不能漂移太远（baseY ± 50），防止累积漂移到屏幕中部
    if(this.y < this.baseY - 50){ this.y = this.baseY - 50; this.dirY = 1; }
    if(this.y > this.baseY + 50){ this.y = this.baseY + 50; this.dirY = -1; }
    // 阶段
    const hpRatio=this.hp/this.maxHp;
    if(hpRatio<0.6 && this.phase<2){ this.phase=2; Game.screenShake=15; toast('WQ '+this.name+' 阶段2!',1500); }
    if(hpRatio<0.3 && this.phase<3){ this.phase=3; Game.screenShake=20; toast('WQ '+this.name+' 狂暴模式!',1500); }
    // 开火
    if(Date.now()-this.lastFire>800-this.phase*200){
      this.lastFire=Date.now();
      // 弹幕
      const count=this.phase+2;
      for(let i=0;i<count;i++){
        const a=this.angle+(i-count/2)*0.3;
        Game.bullets.push(new Bullet(this.x,this.y,a,3.5,this.data.dmg,this.data.color,false));
      }
      // 朝玩家
      if(Game.player){
        const pa=Math.atan2(Game.player.y-this.y,Game.player.x-this.x);
        Game.bullets.push(new Bullet(this.x,this.y,pa,4,this.data.dmg,this.data.color,false));
      }
    }
    this.angle+=0.02*dt;
  }
  takeDamage(dmg){
    this.hp-=dmg;
    // WQ-05 霸王被动
    if(Game.player && Game.player.data.passive==='bosskiller') this.hp-=dmg*0.5;
  }
  contains(x,y){ return Math.abs(x-this.x)<this.size && Math.abs(y-this.y)<this.size; }
  render(ctx){
    ctx.save(); ctx.translate(this.x,this.y); ctx.rotate(this.angle);
    ctx.fillStyle=this.data.color; ctx.shadowBlur=25; ctx.shadowColor=this.data.color;
    // 多边形 Boss
    ctx.beginPath();
    const sides=6+this.phase;
    for(let i=0;i<sides;i++){
      const a=i/sides*Math.PI*2, r=this.size*(i%2?0.7:1);
      ctx.lineTo(Math.cos(a)*r,Math.sin(a)*r);
    }
    ctx.closePath(); ctx.fill();
    ctx.fillStyle='#1A2050'; ctx.beginPath(); ctx.arc(0,0,this.size*0.5,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=this.data.color; ctx.beginPath(); ctx.arc(0,0,this.size*0.3,0,Math.PI*2); ctx.fill();
    ctx.restore();
    // WQ 标记
    ctx.fillStyle='#FFF'; ctx.font='bold 14px Orbitron'; ctx.textAlign='center';
    ctx.fillText('WQ', this.x, this.y+5);
  }
}

class Bullet {
  constructor(x,y,angle,speed,dmg,color,fromPlayer,special){
    this.x=x; this.y=y; this.vx=Math.cos(angle)*speed; this.vy=Math.sin(angle)*speed;
    this.dmg=dmg; this.color=color; this.fromPlayer=fromPlayer;
    this.special=special; this.alive=true; this.size=special==='laser'?4:3;
    this.life=200; this.target=null;
  }
  update(dt){
    // 追踪
    if(this.special==='homing' && Game.enemies.length>0){
      if(!this.target || this.target.hp<=0) this.target=Game.enemies[0];
      const dx=this.target.x-this.x, dy=this.target.y-this.y, d=Math.sqrt(dx*dx+dy*dy);
      this.vx+=dx/d*0.3*dt; this.vy+=dy/d*0.3*dt;
      const s=Math.sqrt(this.vx*this.vx+this.vy*this.vy); this.vx=this.vx/s*5; this.vy=this.vy/s*5;
    }
    this.x+=this.vx*dt; this.y+=this.vy*dt;
    this.life-=dt;
    if(this.x<0||this.x>Game.W||this.y<0||this.y>Game.H||this.life<0) this.alive=false;
    // 黑洞: 吸附敌人
    if(this.special==='blackhole'){
      Game.enemies.forEach(e=>{
        const dx=this.x-e.x, dy=this.y-e.y, d=Math.sqrt(dx*dx+dy*dy);
        if(d<80){ e.x+=dx/d*2*dt; e.y+=dy/d*2*dt; }
      });
    }
  }
  render(ctx){
    ctx.fillStyle=this.color; ctx.shadowBlur=10; ctx.shadowColor=this.color;
    if(this.special==='laser'){ ctx.fillRect(this.x-2,this.y-8,4,16); }
    else if(this.special==='blackhole'){ ctx.beginPath(); ctx.arc(this.x,this.y,8,0,Math.PI*2); ctx.fill(); ctx.strokeStyle=this.color; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(this.x,this.y,12,0,Math.PI*2); ctx.stroke(); }
    else { ctx.beginPath(); ctx.arc(this.x,this.y,this.size,0,Math.PI*2); ctx.fill(); }
    ctx.shadowBlur=0;
  }
}

class Particle {
  constructor(x,y,color){
    this.x=x; this.y=y; this.color=color;
    const a=Math.random()*Math.PI*2, s=1+Math.random()*4;
    this.vx=Math.cos(a)*s; this.vy=Math.sin(a)*s;
    this.life=30+Math.random()*30; this.maxLife=this.life;
    this.size=2+Math.random()*3;
  }
  update(dt){ this.x+=this.vx*dt; this.y+=this.vy*dt; this.vx*=0.95; this.vy*=0.95; this.life-=dt; }
  render(ctx){
    ctx.globalAlpha=this.life/this.maxLife;
    ctx.fillStyle=this.color; ctx.shadowBlur=8; ctx.shadowColor=this.color;
    ctx.beginPath(); ctx.arc(this.x,this.y,this.size,0,Math.PI*2); ctx.fill();
    ctx.globalAlpha=1; ctx.shadowBlur=0;
  }
}

class Drop {
  constructor(x,y){
    this.x=x; this.y=y; this.collected=false;
    const types=['medkit','shield','energy','gold'];
    this.type=types[Math.floor(Math.random()*types.length)];
    this.t=0;
  }
  update(dt){ this.t+=dt; }
  collect(){
    this.collected=true;
    if(this.type==='medkit'){ Game.player.hp=Math.min(Game.player.maxHp,Game.player.hp+30); toast('WQ: +30 HP'); }
    else if(this.type==='shield'){ Game.player.shield+=40; toast('WQ: +40 护盾'); }
    else if(this.type==='energy'){ Game.player.mp=Math.min(100,Game.player.mp+30); toast('WQ: +30 能量'); }
    else { Game.goldEarned+=50; toast('WQ: +50 金币'); }
    Audio.coin();
  }
  render(ctx){
    const colors={medkit:'#FF5252',shield:'#00E5FF',energy:'#FFD600',gold:'#FFB800'};
    const icons={medkit:'+',shield:'S',energy:'E',gold:'$'};
    ctx.fillStyle=colors[this.type]; ctx.shadowBlur=12; ctx.shadowColor=colors[this.type];
    ctx.beginPath(); ctx.arc(this.x,this.y+Math.sin(this.t*0.1)*3,10,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#FFF'; ctx.font='bold 12px Orbitron'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(icons[this.type],this.x,this.y+Math.sin(this.t*0.1)*3);
    ctx.shadowBlur=0;
  }
}

// ==================== WQ 初始化 ====================
window.addEventListener('DOMContentLoaded', ()=>{
  Save.load();
  Game.init();
  Save.updateGoldUI();
  // 彩蛋状态
  if(Save.data.easterEgg.eggMapCleared){ document.getElementById('eggTrigger').classList.add('cleared'); }
  // 设置
  document.getElementById('sfxVol').value=Save.settings.sfxVolume*100;
  document.getElementById('bgmVol').value=Save.settings.bgmVolume*100;
  document.getElementById('shakeToggle').checked=Save.settings.screenShake;
  // 按键
  window.addEventListener('keydown', e=>{
    if(e.key.toLowerCase()==='p'||e.key==='Escape'){ if(Game.running) Game.pause(); }
  });
  toast('WQ · 坦克大战 · 就绪! 王者无敌 · 奇迹永存', 3000);
});
"""


if __name__ == "__main__":
    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tank-battle.html")
    build_game(output)
