import pygame
import numpy as np
import math
import random

# --- GLOBAL DIMENSIONS ---
WIDTH, HEIGHT = 1400, 900
SIDEBAR_WIDTH = 340 
LOG_HEIGHT = 200
VIEW_W = WIDTH - SIDEBAR_WIDTH
VIEW_H = HEIGHT - LOG_HEIGHT
FOV = 400

CONFIG = {
    'mass': 1.0, 'arm': 0.25, 'g': 9.81, 'drag': 0.08, 'thrust': 1.0,
    'fps': 60, 'tilt_limit': 45.0, 'yaw_speed': 2.0,
    'box_map': True, 'fpv_mode': False
}

# --- PRO THEME COLORS (Matched to Reference) ---
C_BG_MAIN = (20, 20, 20)       
C_SIDEBAR = (10, 10, 10)       # Pitch black sidebar
C_LOG_BG = (5, 5, 5)           

C_ACCENT = (50, 255, 50)       # Bright Terminal Green
C_ACCENT_DIM = (20, 100, 20)   # Dim Green
C_TEXT_MAIN = (200, 255, 200)  # Pale Green Text
C_TEXT_SUB = (100, 150, 100)   # Darker Green Text

C_INPUT_BG = (20, 20, 20)      
C_INPUT_BORDER = (40, 60, 40)  

# 3D World Colors
C_SKY = (135, 206, 235)        # Sky Blue for contrast vs UI
C_CHECKER_1 = (30, 30, 30)     # Dark floor
C_CHECKER_2 = (25, 25, 25)
C_GRID = (0, 100, 0)           # Dark Green Grid
C_HUD = (50, 255, 50)          # HUD Green
C_HUD_BG = (0, 20, 0, 100)
C_WALL = (100, 100, 110)

PALETTE = [
    (200, 60, 60), (60, 150, 200), (60, 200, 100),
    (200, 200, 50), (150, 80, 180), (200, 120, 50)
]

# --- HELPER ---
def normalize_angle(rad):
    deg = math.degrees(rad)
    return (deg + 180) % 360 - 180

# --- PHYSICS ---
class QuadPhysics:
    def __init__(self):
        self.state = np.zeros(12); self.state[2] = 1.0
        self.time = 0.0
        self.I = np.array([0.01, 0.01, 0.02])
        self.history = []

    def step(self, motors, dt):
        x, y, z, phi, theta, psi, vx, vy, vz, p, q, r = self.state
        m, g, d = CONFIG['mass'], CONFIG['g'], CONFIG['drag']
        k_t, k_m = 0.01 * CONFIG['thrust'], 0.001
        L = CONFIG['arm'] / 1.4142

        w_sq = np.clip(motors, 0, None)
        thrust = k_t * np.sum(w_sq)
        tau = np.array([
            L * k_t * (w_sq[1] + w_sq[3] - w_sq[0] - w_sq[2]),
            L * k_t * (w_sq[0] + w_sq[1] - w_sq[2] - w_sq[3]),
            k_m * (w_sq[0] - w_sq[1] - w_sq[2] + w_sq[3])
        ])

        cph, sph = math.cos(phi), math.sin(phi)
        cth, sth = math.cos(theta), math.sin(theta)
        cps, sps = math.cos(psi), math.sin(psi)

        a_x = ((cps*sth*cph + sps*sph)*thrust/m) - d*vx
        a_y = ((sps*sth*cph - cps*sph)*thrust/m) - d*vy
        a_z = (-g + (cth*cph)*thrust/m) - d*vz

        p_dot, q_dot, r_dot = np.linalg.inv(np.diag(self.I)) @ (tau - np.cross([p,q,r], np.diag(self.I)@[p,q,r]))

        self.state += dt * np.array([vx, vy, vz, p, q, r, a_x, a_y, a_z, p_dot, q_dot, r_dot])
        self.time += dt
        
        if self.state[2] < 0: self.state[2] = 0; self.state[8] = 0; self.state[9:12] = 0
        self.history.append([self.time] + list(self.state))
        if len(self.history) > 20: self.history.pop(0)

class Map:
    def __init__(self):
        self.obstacles = []
        limit = 60.0
        for _ in range(30):
            x = random.uniform(-limit+5, limit-5)
            y = random.uniform(-limit+5, limit-5)
            if abs(x) < 5 and abs(y) < 5: continue 
            self.obstacles.append({'x':x, 'y':y, 'w':random.uniform(2,5), 'h':random.uniform(4,15), 'c':random.choice(PALETTE)})
        
        step = 10.0
        for i in np.arange(-limit, limit+step, step):
            self.obstacles.append({'x': i, 'y': limit, 'w': 2, 'h': 10, 'c': C_WALL})
            self.obstacles.append({'x': i, 'y': -limit, 'w': 2, 'h': 10, 'c': C_WALL})
            self.obstacles.append({'x': limit, 'y': i, 'w': 2, 'h': 10, 'c': C_WALL})
            self.obstacles.append({'x': -limit, 'y': i, 'w': 2, 'h': 10, 'c': C_WALL})

class Camera:
    def project(self, p, pos, ang):
        x, y, z = p
        cx, cy, cz = pos
        dx, dy, dz = x-cx, y-cy, z-cz
        c, s = math.cos(-ang), math.sin(-ang)
        rx, ry = dx*c - dy*s, dx*s + dy*c
        if ry <= 0.1: return None
        current_fov = FOV * (VIEW_W / 1100.0) 
        scale = current_fov / ry
        return (int(SIDEBAR_WIDTH + VIEW_W/2 + rx*scale), int(VIEW_H/2 - dz*scale))

# --- RENDERER ---
def draw_world(screen, phys, cam, map_obj):
    # --- IMPORTANT: CLIP TO 3D VIEW ONLY ---
    # This prevents 3D objects from drawing over the Sidebar or Log
    view_rect = pygame.Rect(SIDEBAR_WIDTH, 0, VIEW_W, VIEW_H)
    screen.set_clip(view_rect)

    x, y, z, phi, theta, psi = phys.state[:6]
    
    if CONFIG['fpv_mode']:
        cam_pos = (x, y, z + 0.1)
        horizon_y = int(VIEW_H/2 - (theta * FOV))
    else:
        dist = 5.0
        cam_pos = (x - dist*math.cos(psi), y - dist*math.sin(psi), z + 2.5)
        horizon_y = VIEW_H//2

    # Draw Sky
    pygame.draw.rect(screen, C_SKY, (SIDEBAR_WIDTH, 0, VIEW_W, max(0, horizon_y)))

    # Draw Ground (Checkerboard)
    # Clip strictly to ground area to prevent sky overwrite
    ground_rect = pygame.Rect(SIDEBAR_WIDTH, horizon_y, VIEW_W, max(0, VIEW_H - horizon_y))
    screen.set_clip(ground_rect) 
    screen.fill(C_CHECKER_2) 

    tile_sz = 5.0
    radius = 20
    sx, sy = int(x // tile_sz), int(y // tile_sz)
    cam_ang = psi - 1.57

    for i in range(-radius, radius):
        for j in range(-radius, radius):
            wx1 = (sx + i) * tile_sz
            wy1 = (sy + j) * tile_sz
            wx2 = wx1 + tile_sz; wy2 = wy1 + tile_sz
            
            p1 = cam.project((wx1, wy1, 0), cam_pos, cam_ang)
            p2 = cam.project((wx2, wy1, 0), cam_pos, cam_ang)
            p3 = cam.project((wx2, wy2, 0), cam_pos, cam_ang)
            p4 = cam.project((wx1, wy2, 0), cam_pos, cam_ang)
            
            if p1 and p2 and p3 and p4:
                color = C_CHECKER_1 if (sx + i + sy + j) % 2 == 0 else C_CHECKER_2
                pygame.draw.polygon(screen, color, [p1, p2, p3, p4])

    # Restore Clip to full 3D view for objects
    screen.set_clip(view_rect)

    # Grid Lines
    def line(p1, p2, col):
        s1 = cam.project(p1, cam_pos, psi-1.57)
        s2 = cam.project(p2, cam_pos, psi-1.57)
        if s1 and s2: 
            pygame.draw.line(screen, col, s1, s2, 1)

    grid_sz = 2.0
    gsx, gsy = int(x//grid_sz), int(y//grid_sz)
    for i in range(-20, 20):
        wx = (gsx + i) * grid_sz
        line((wx, y-40, 0), (wx, y+40, 0), C_GRID)
        wy = (gsy + i) * grid_sz
        line((x-40, wy, 0), (x+40, wy, 0), C_GRID)

    # Obstacles
    render_list = []
    for o in map_obj.obstacles:
        if not CONFIG['box_map'] and abs(o['x']) > 55: continue 
        d = math.sqrt((o['x']-cam_pos[0])**2 + (o['y']-cam_pos[1])**2)
        render_list.append((d, o))
    render_list.sort(key=lambda k: k[0], reverse=True)

    for _, o in render_list:
        w, h, c = o['w']/2, o['h'], o['c']
        pts = [(o['x']-w, o['y']-w, 0), (o['x']+w, o['y']-w, 0), (o['x']+w, o['y']+w, 0), (o['x']-w, o['y']+w, 0),
               (o['x']-w, o['y']-w, h), (o['x']+w, o['y']-w, h), (o['x']+w, o['y']+w, h), (o['x']-w, o['y']+w, h)]
        scr = [cam.project(p, cam_pos, psi-1.57) for p in pts]
        if not any(pt is None for pt in scr):
            faces = [
                (scr[4], scr[5], scr[6], scr[7], (min(c[0]+40,255), min(c[1]+40,255), min(c[2]+40,255))),
                (scr[0], scr[1], scr[5], scr[4], (c[0]*0.8, c[1]*0.8, c[2]*0.8)),
                (scr[1], scr[2], scr[6], scr[5], (c[0]*0.6, c[1]*0.6, c[2]*0.6)),
                (scr[2], scr[3], scr[7], scr[6], (c[0]*0.8, c[1]*0.8, c[2]*0.8)),
                (scr[3], scr[0], scr[4], scr[7], (c[0]*0.6, c[1]*0.6, c[2]*0.6))
            ]
            for f in faces: 
                pygame.draw.polygon(screen, f[4], f[:4])

    # Drone Body
    if not CONFIG['fpv_mode']:
        arm = CONFIG['arm']
        d_pts = [(0,0,0), (arm,arm,0), (arm,-arm,0), (-arm,arm,0), (-arm,-arm,0)]
        R_z = np.array([[math.cos(psi), -math.sin(psi), 0], [math.sin(psi), math.cos(psi), 0], [0,0,1]])
        R_y = np.array([[math.cos(theta), 0, math.sin(theta)], [0,1,0], [-math.sin(theta), 0, math.cos(theta)]])
        R_x = np.array([[1,0,0], [0, math.cos(phi), -math.sin(phi)], [0, math.sin(phi), math.cos(phi)]])
        R = R_z @ R_y @ R_x
        w_pts = [np.array([x,y,z]) + R @ np.array(p) for p in d_pts]
        s_pts = [cam.project(p, cam_pos, psi-1.57) for p in w_pts]
        if all(s_pts):
            c, fr, fl, rr, rl = s_pts
            pygame.draw.line(screen, (255,50,50), c, fr, 4)
            pygame.draw.line(screen, (255,50,50), c, fl, 4)
            pygame.draw.line(screen, (200,200,200), c, rr, 4)
            pygame.draw.line(screen, (200,200,200), c, rl, 4)
            
    # Reset Clip for UI
    screen.set_clip(None)

def rotate_point(x, y, angle_rad):
    """ Rotates a point (x,y) by angle_rad """
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return (x * c - y * s, x * s + y * c)

# --- HUD ---
def draw_pitch_ladder(screen, phys, font):
    x, y, z, phi, theta, psi = phys.state[:6]
    cx, cy = SIDEBAR_WIDTH + VIEW_W // 2, VIEW_H // 2
    
    # Clip to view area so lines don't bleed into sidebar
    screen.set_clip(pygame.Rect(SIDEBAR_WIDTH, 0, VIEW_W, VIEW_H))
    
    # Draw Fixed Boresight (The "W" or Crosshair in the center)
    # This represents YOUR aircraft, so it stays fixed to the screen
    pygame.draw.line(screen, C_ACCENT, (cx-20, cy), (cx-5, cy), 2)
    pygame.draw.line(screen, C_ACCENT, (cx+5, cy), (cx+20, cy), 2)
    pygame.draw.line(screen, C_ACCENT, (cx, cy-15), (cx, cy-5), 2)
    pygame.draw.circle(screen, C_ACCENT, (cx, cy), 2)

    # Scale: 1 degree of pitch = 15 pixels on screen
    pitch_scale = 15.0
    
    # Range of pitch lines to draw
    # We draw lines for every 10 degrees, from -90 to +90
    for i in range(-9, 10):
        pitch_line_deg = i * 10
        
        # 1. Calculate the vertical offset relative to the horizon
        # If we pitch up (theta > 0), the ladder lines move DOWN
        diff_deg = pitch_line_deg - math.degrees(theta)
        
        # Optimization: Don't do math for lines far off screen
        if abs(diff_deg * pitch_scale) > VIEW_H: continue

        # 2. Define the line in "Unrotated" coordinates relative to screen center
        # The center of the line is at (0, -diff * scale)
        line_y = -diff_deg * pitch_scale
        width = 120 if pitch_line_deg == 0 else (80 - abs(i)*4) # Horizon is wider
        
        p1_raw = (-width/2, line_y)
        p2_raw = (width/2, line_y)
        
        # 3. Rotate the points by the Roll angle (-phi)
        # We rotate by negative phi because if we roll right, world tilts left
        r1 = rotate_point(p1_raw[0], p1_raw[1], -phi)
        r2 = rotate_point(p2_raw[0], p2_raw[1], -phi)
        
        # 4. Translate to screen coordinates
        p1 = (cx + r1[0], cy + r1[1])
        p2 = (cx + r2[0], cy + r2[1])
        
        # 5. Draw
        # Horizon (0 deg) is usually a solid long line
        if pitch_line_deg == 0:
            pygame.draw.line(screen, C_ACCENT, p1, p2, 1)
        else:
            # Positive pitch = Solid, Negative pitch = Dashed (Simulated with gaps)
            color = C_ACCENT if pitch_line_deg > 0 else C_ACCENT_DIM
            
            # Draw the main line
            pygame.draw.line(screen, color, p1, p2, 1)
            
            # Draw the "Feet" (vertical ticks at ends of lines)
            # We need to rotate the feet vectors too
            foot_len = 5 if pitch_line_deg > 0 else -5
            
            f1_raw = (p1_raw[0], p1_raw[1] + foot_len)
            f2_raw = (p2_raw[0], p2_raw[1] + foot_len)
            
            rf1 = rotate_point(f1_raw[0], f1_raw[1], -phi)
            rf2 = rotate_point(f2_raw[0], f2_raw[1], -phi)
            
            pf1 = (cx + rf1[0], cy + rf1[1])
            pf2 = (cx + rf2[0], cy + rf2[1])
            
            pygame.draw.line(screen, color, p1, pf1, 1)
            pygame.draw.line(screen, color, p2, pf2, 1)

            # Draw Numbers (Text follows the line)
            # Rotating text in pygame every frame is expensive/ugly, 
            # so we just position it at the rotated end of the line
            if i != 0:
                label = font.render(str(pitch_line_deg), True, color)
                # Position text slightly outside the line
                screen.blit(label, (p2[0] + 5, p2[1] - 7))
    # Reset clip
    screen.set_clip(None)

def draw_hud_tapes(screen, phys, font):
    x, y, z, phi, theta, psi, vx, vy, vz = phys.state[:9]
    spd = math.sqrt(vx**2 + vy**2)
    cy = VIEW_H // 2
    
    # Speed Tape (Left)
    lx = SIDEBAR_WIDTH + 50
    pygame.draw.rect(screen, C_HUD_BG, (lx, 50, 60, VIEW_H-100))
    pygame.draw.rect(screen, C_HUD, (lx, 50, 60, VIEW_H-100), 2)
    screen.blit(font.render("SPD", True, C_HUD), (lx+15, 30))
    
    screen.set_clip(pygame.Rect(lx, 50, 60, VIEW_H-100))
    for s in range(int(spd)-8, int(spd)+9):
        dy = (s - spd) * 30
        line_y = cy - dy
        if 0 < line_y < VIEW_H:
            pygame.draw.line(screen, C_HUD, (lx, line_y), (lx+10, line_y), 2)
            if s % 5 == 0: 
                screen.blit(font.render(str(s), True, C_HUD), (lx+15, line_y-8))
                pygame.draw.line(screen, C_HUD, (lx, line_y), (lx+18, line_y), 2)
    screen.set_clip(None)
    
    val_rect = pygame.Rect(lx-10, cy-15, 50, 30)
    pygame.draw.rect(screen, C_LOG_BG, val_rect)
    pygame.draw.rect(screen, C_HUD, val_rect, 2)
    screen.blit(font.render(f"{spd:.1f}", True, C_HUD), (lx+5, cy-9))
    
    # Altitude Tape (Right)
    rx = WIDTH - 80
    pygame.draw.rect(screen, C_HUD_BG, (rx, 50, 60, VIEW_H-100))
    pygame.draw.rect(screen, C_HUD, (rx, 50, 60, VIEW_H-100), 2)
    screen.blit(font.render("ALT", True, C_HUD), (rx+15, 30))
    
    screen.set_clip(pygame.Rect(rx, 50, 60, VIEW_H-100))
    for a in range(int(z)-8, int(z)+9):
        dy = (a - z) * 30
        line_y = cy - dy
        if 0 < line_y < VIEW_H:
            pygame.draw.line(screen, C_HUD, (rx+50, line_y), (rx+60, line_y), 2)
            if a % 5 == 0: 
                screen.blit(font.render(str(a), True, C_HUD), (rx+15, line_y-8))
                pygame.draw.line(screen, C_HUD, (rx+42, line_y), (rx+60, line_y), 2)
    screen.set_clip(None)

    val_rect = pygame.Rect(rx+20, cy-15, 50, 30)
    pygame.draw.rect(screen, C_LOG_BG, val_rect)
    pygame.draw.rect(screen, C_HUD, val_rect, 2)
    screen.blit(font.render(f"{z:.1f}", True, C_HUD), (rx+25, cy-9))

    # Heading (Top)
    cx_scr = SIDEBAR_WIDTH + VIEW_W//2
    deg = math.degrees(psi) % 360
    tape_y = 40
    pygame.draw.rect(screen, C_HUD_BG, (cx_scr-150, tape_y, 300, 35))
    pygame.draw.rect(screen, C_HUD, (cx_scr-150, tape_y, 300, 35), 2)
    screen.blit(font.render("HDG", True, C_HUD), (cx_scr-15, 15))
    
    screen.set_clip(pygame.Rect(cx_scr-150, tape_y, 300, 35))
    for h in range(int(deg)-45, int(deg)+46):
        if h % 15 == 0:
            dx = (h - deg) * 4
            if -150 < dx < 150:
                l = str(h%360)
                if h%360==0: l="N"; 
                if h%360==90: l="E"; 
                if h%360==180: l="S"; 
                if h%360==270: l="W"
                pygame.draw.line(screen, C_HUD, (cx_scr+dx, tape_y+20), (cx_scr+dx, tape_y+35))
                t = font.render(l, True, C_HUD)
                screen.blit(t, (cx_scr+dx-t.get_width()/2, tape_y+2))
    screen.set_clip(None)
    
    val_rect = pygame.Rect(cx_scr-25, tape_y+40, 50, 25)
    pygame.draw.rect(screen, C_LOG_BG, val_rect)
    pygame.draw.rect(screen, C_HUD, val_rect, 2)
    screen.blit(font.render(f"{int(deg)}", True, C_HUD), (cx_scr-10, tape_y+42))

# --- MODERN UI ---
class InputBox:
    def __init__(self, x, y, w, label, key):
        self.rect = pygame.Rect(x, y, w, 32)
        self.label = label
        self.key = key
        self.text = str(CONFIG[key])
        self.active = False
        self.hover = False
        
        self.step = 0.1
        if key == 'fps': self.step = 5
        elif key == 'arm': self.step = 0.01
        elif key == 'tilt_limit': self.step = 1.0
        elif key == 'mass': self.step = 0.1
    
    def handle(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN: 
            self.active = self.hover
        
        if event.type == pygame.MOUSEWHEEL and self.hover:
            val = CONFIG[self.key]
            val += event.y * self.step
            if val < 0.01: val = 0.01
            if self.step >= 1: val = int(val)
            else: val = round(val, 2)
            CONFIG[self.key] = val
            self.text = str(val)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            else: self.text += event.unicode
            try: CONFIG[self.key] = float(self.text)
            except: pass
    
    def update_text(self): self.text = str(CONFIG[self.key])
            
    def draw(self, screen, font, font_label):
        screen.blit(font_label.render(self.label, True, C_TEXT_SUB), (self.rect.x, self.rect.y-16))
        
        bg_col = (40, 40, 40) if self.hover else C_INPUT_BG
        pygame.draw.rect(screen, bg_col, self.rect, border_radius=3)
        
        border_col = C_ACCENT if self.active else C_INPUT_BORDER
        pygame.draw.rect(screen, border_col, self.rect, 1, border_radius=3)
        
        screen.blit(font.render(self.text, True, C_TEXT_MAIN), (self.rect.x+10, self.rect.y+6))

class ToggleBox:
    def __init__(self, x, y, label, key):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.label = label
        self.key = key
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            CONFIG[self.key] = not CONFIG[self.key]
    def draw(self, screen, font):
        pygame.draw.rect(screen, C_INPUT_BG, self.rect, border_radius=3)
        if CONFIG[self.key]:
            pygame.draw.rect(screen, C_ACCENT, (self.rect.x+4, self.rect.y+4, 12, 12), border_radius=2)
        pygame.draw.rect(screen, C_INPUT_BORDER, self.rect, 1, border_radius=3)
        screen.blit(font.render(self.label, True, C_TEXT_MAIN), (self.rect.right+12, self.rect.y+2))

def draw_sidebar(screen, inputs, toggles, font_L, font_M, font_S):
    # Sidebar Background (Full Height)
    pygame.draw.rect(screen, C_SIDEBAR, (0, 0, SIDEBAR_WIDTH, HEIGHT))
    pygame.draw.line(screen, (30, 30, 30), (SIDEBAR_WIDTH, 0), (SIDEBAR_WIDTH, HEIGHT), 1)
    
    # Title
    screen.blit(font_L.render("QUAD SIMULATOR", True, C_ACCENT), (20, 25))

    # --- BUTTONS (Visual Only) ---
    btn_y = 70
    pygame.draw.rect(screen, (20, 60, 20), (20, btn_y, SIDEBAR_WIDTH-40, 35), border_radius=4)
    pygame.draw.rect(screen, C_ACCENT_DIM, (20, btn_y, SIDEBAR_WIDTH-40, 35), 1, border_radius=4)
    t = font_M.render("RESTART SIMULATION (R)", True, C_TEXT_MAIN)
    screen.blit(t, (SIDEBAR_WIDTH//2 - t.get_width()//2, btn_y+8))
    
    # --- SECTIONS ---
    y_cursor = 140
    screen.blit(font_M.render("DRONE PHYSICS", True, C_ACCENT), (20, y_cursor))
    pygame.draw.line(screen, C_ACCENT_DIM, (20, y_cursor+22), (SIDEBAR_WIDTH-20, y_cursor+22), 1)
    
    inputs[0].rect.y = y_cursor + 45
    inputs[1].rect.y = y_cursor + 100
    inputs[2].rect.y = y_cursor + 155
    
    y_cursor = 340
    screen.blit(font_M.render("SIMULATION SETTINGS", True, C_ACCENT), (20, y_cursor))
    pygame.draw.line(screen, C_ACCENT_DIM, (20, y_cursor+22), (SIDEBAR_WIDTH-20, y_cursor+22), 1)
    
    inputs[3].rect.y = y_cursor + 45
    inputs[4].rect.y = y_cursor + 100
    inputs[5].rect.y = y_cursor + 155
    
    for inp in inputs: inp.draw(screen, font_M, font_S)
    
    toggles[0].rect.y = 560; toggles[0].rect.x = 20
    toggles[1].rect.y = 560; toggles[1].rect.x = 160
    for tog in toggles: tog.draw(screen, font_M)

    # Info Box
    y_info = HEIGHT - 120
    # pygame.draw.rect(screen, (15, 15, 15), (15, y_info, SIDEBAR_WIDTH-30, 100), border_radius=5)
    
    lines = ["WASD: Pitch/Roll", "Arrows: Alt/Yaw", "Scroll to Edit Values"]
    for i, l in enumerate(lines):
        screen.blit(font_S.render(l, True, (100, 100, 100)), (25, y_info + i*20))

def draw_log_terminal(screen, phys, font_Mono):
    log_y = HEIGHT - LOG_HEIGHT
    
    # Terminal Header
    pygame.draw.rect(screen, (10, 10, 10), (SIDEBAR_WIDTH, log_y, VIEW_W, 30))
    screen.blit(font_Mono.render("DATA TERMINAL >_ 10Hz Sample Rate", True, C_ACCENT), (SIDEBAR_WIDTH+10, log_y+8))
    
    # Terminal Body
    pygame.draw.rect(screen, C_LOG_BG, (SIDEBAR_WIDTH, log_y+30, VIEW_W, LOG_HEIGHT-30))
    pygame.draw.line(screen, (30, 30, 30), (SIDEBAR_WIDTH, log_y), (WIDTH, log_y), 1)
    
    headers = ["T(s)", "Pos.X", "Pos.Y", "Pos.Z", "Vel.X", "Vel.Y", "Vel.Z", "Roll", "Pitch", "Yaw"]
    col_width = VIEW_W / len(headers)
    
    for i, h in enumerate(headers):
        screen.blit(font_Mono.render(h, True, C_TEXT_SUB), (SIDEBAR_WIDTH + i*col_width + 10, log_y + 40))
    
    for r_idx, row in enumerate(reversed(phys.history)):
        if r_idx > 5: break
        y_pos = log_y + 65 + r_idx * 20
        
        t, px, py, pz, phi, theta, psi, vx, vy, vz, p, q, r = row
        d_row = [t, px, py, pz, vx, vy, vz, normalize_angle(phi), normalize_angle(theta), normalize_angle(psi)]
        
        for c_idx, val in enumerate(d_row):
            col = C_TEXT_MAIN if r_idx == 0 else (80, 80, 80)
            screen.blit(font_Mono.render(f"{val:.2f}", True, col), (SIDEBAR_WIDTH + c_idx*col_width + 10, y_pos))

# --- MAIN ---
def main():
    global WIDTH, HEIGHT, VIEW_W, VIEW_H 
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Pro Quadcopter HUD v2.1")
    clock = pygame.time.Clock()
    
    # Font Setup for the "Pro" Look
    font_L = pygame.font.SysFont("Verdana", 24, bold=True)
    font_M = pygame.font.SysFont("Consolas", 14) 
    font_S = pygame.font.SysFont("Verdana", 11) 
    font_Mono = pygame.font.SysFont("Consolas", 13) 
    font_HUD = pygame.font.SysFont("Consolas", 14, bold=True)

    phys = QuadPhysics()
    map_obj = Map()
    cam = Camera()
    
    inputs = [
        InputBox(25, 0, 290, "Mass (kg)", 'mass'),
        InputBox(25, 0, 290, "Arm Length (m)", 'arm'),
        InputBox(25, 0, 290, "Thrust Mult", 'thrust'),
        InputBox(25, 0, 290, "Target FPS", 'fps'),
        InputBox(25, 0, 290, "Max Tilt (deg)", 'tilt_limit'),
        InputBox(25, 0, 290, "Yaw Speed", 'yaw_speed')
    ]
    toggles = [
        ToggleBox(0, 0, "FPV Mode", 'fpv_mode'),
        ToggleBox(0, 0, "Box Map", 'box_map')
    ]
    
    tp, tr, ty, tvz = 0, 0, 0, 0
    paused = False
    
    running = True
    while running:
        fps = CONFIG['fps']
        dt = 1.0/fps
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            
            if e.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = e.w, e.h
                VIEW_W = WIDTH - SIDEBAR_WIDTH
                VIEW_H = HEIGHT - LOG_HEIGHT
                if WIDTH < 800: WIDTH = 800
                if HEIGHT < 600: HEIGHT = 600
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            for i in inputs: i.handle(e)
            for t in toggles: t.handle(e)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: phys.state = np.zeros(12); phys.state[2] = 1.0; tp=0; tr=0
                if e.key == pygame.K_ESCAPE: paused = not paused 
                
        if not paused:
            keys = pygame.key.get_pressed()
            ramp = 0.05 * (60/fps)
            if keys[pygame.K_w]: tp += ramp
            elif keys[pygame.K_s]: tp -= ramp
            else: tp *= 0.9
            if keys[pygame.K_a]: tr -= ramp
            elif keys[pygame.K_d]: tr += ramp
            else: tr *= 0.9
            lim = math.radians(CONFIG['tilt_limit'])
            tp = np.clip(tp, -lim, lim); tr = np.clip(tr, -lim, lim)
            tvz = 2.0 if keys[pygame.K_UP] else (-2.0 if keys[pygame.K_DOWN] else 0)
            ys = CONFIG['yaw_speed']
            ty = ys if keys[pygame.K_LEFT] else (-ys if keys[pygame.K_RIGHT] else 0)
            
            st = phys.state
            phi, theta, psi, vz, p, q, r = st[3], st[4], st[5], st[8], st[9], st[10], st[11]
            kp, kd = 4.0, 2.5
            req_p = kp*(tp - theta) - kd*q
            req_r = kp*(tr - phi) - kd*p
            req_y = 4.0*(ty - r)
            hover = (CONFIG['mass'] * CONFIG['g']) / (max(math.cos(theta)*math.cos(phi), 0.1)) / 4.0 / 0.01
            th_adj = 5.0 * (tvz - vz)
            base = hover + th_adj
            phys.step(np.array([base+req_p-req_r+req_y, base+req_p+req_r-req_y, base-req_p-req_r-req_y, base-req_p+req_r+req_y]), dt)

        # --- DRAWING ORDER (Fixes Clipping) ---
        # 1. Draw World (with internal clipping)
        draw_world(screen, phys, cam, map_obj)
        
        # 2. Draw Pitch Ladder (The PFD replacement)
        draw_pitch_ladder(screen, phys, font_HUD)

        # 3. Draw HUD Tapes
        draw_hud_tapes(screen, phys, font_HUD)
        
        # 4. Draw UI Layers (Sidebar & Log) LAST to ensure they are on top
        draw_sidebar(screen, inputs, toggles, font_L, font_M, font_S)
        draw_log_terminal(screen, phys, font_Mono)
        
        if paused:
            ov = pygame.Surface((VIEW_W, VIEW_H)); ov.set_alpha(180); ov.fill((0,0,0))
            screen.blit(ov, (SIDEBAR_WIDTH, 0))
            t = font_L.render("SIMULATION PAUSED", True, C_TEXT_MAIN)
            screen.blit(t, (SIDEBAR_WIDTH + VIEW_W//2 - t.get_width()//2, VIEW_H//2))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()