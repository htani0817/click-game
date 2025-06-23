import pygame
import random
import time
import json
import os

# 初期化
pygame.init()

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ゲーム状態
TITLE_SCREEN = 0
DIFFICULTY_SELECT = 1
TIME_SELECT = 2
PLAYING = 3
GAME_OVER = 4

# 難易度設定
DIFFICULTIES = {
    "Easy": {"grid": 3, "cell_size": 120},
    "Normal": {"grid": 6, "cell_size": 80},
    "Hard": {"grid": 9, "cell_size": 60}
}

TIME_OPTIONS = [10, 20, 30]

class ClickGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Click Game Ver.1.0.0")
        self.clock = pygame.time.Clock()
        
        # フォント設定
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 28)
        
        # ゲーム状態
        self.state = TITLE_SCREEN
        self.selected_difficulty = None
        self.selected_time = None
        self.grid_size = 3
        self.cell_size = 120
        self.game_time = 10
        
        # ゲーム変数
        self.grid = []
        self.target_row = -1
        self.target_col = -1
        self.score = 0
        self.start_time = 0
        self.game_over_flag = False
        
        # ハイスコア
        self.high_scores = self.load_high_scores()
        
        # ボタン設定
        self.buttons = []
        self.setup_buttons()
    
    def load_high_scores(self):
        """ハイスコアを読み込み"""
        try:
            if os.path.exists("high_scores.json"):
                with open("high_scores.json", "r") as f:
                    return json.load(f)
        except:
            pass
        
        # デフォルトハイスコア
        return {
            "Easy": {"10": 0, "20": 0, "30": 0},
            "Normal": {"10": 0, "20": 0, "30": 0},
            "Hard": {"10": 0, "20": 0, "30": 0}
        }
    
    def save_high_scores(self):
        """ハイスコアを保存"""
        try:
            with open("high_scores.json", "w") as f:
                json.dump(self.high_scores, f)
        except:
            pass
    
    def update_high_score(self):
        """ハイスコアを更新"""
        difficulty_name = self.get_difficulty_name()
        time_key = str(self.game_time)
        
        if difficulty_name and time_key in self.high_scores[difficulty_name]:
            if self.score > self.high_scores[difficulty_name][time_key]:
                self.high_scores[difficulty_name][time_key] = self.score
                self.save_high_scores()
                return True
        return False
    
    def get_difficulty_name(self):
        """現在の難易度名を取得"""
        for name, config in DIFFICULTIES.items():
            if config["grid"] == self.grid_size:
                return name
        return None
    
    def setup_buttons(self):
        """ボタンを設定"""
        self.buttons = []
        
        if self.state == TITLE_SCREEN:
            self.buttons = [
                {"text": "START GAME", "rect": pygame.Rect(300, 250, 200, 60), "action": "start"},
                {"text": "HIGH SCORES", "rect": pygame.Rect(300, 330, 200, 60), "action": "scores"},
                {"text": "QUIT", "rect": pygame.Rect(300, 410, 200, 60), "action": "quit"}
            ]
        
        elif self.state == DIFFICULTY_SELECT:
            y_pos = 200
            for difficulty in DIFFICULTIES.keys():
                self.buttons.append({
                    "text": f"{difficulty} ({DIFFICULTIES[difficulty]['grid']}x{DIFFICULTIES[difficulty]['grid']})",
                    "rect": pygame.Rect(250, y_pos, 300, 60),
                    "action": f"difficulty_{difficulty}"
                })
                y_pos += 80
            
            self.buttons.append({"text": "BACK", "rect": pygame.Rect(50, 500, 100, 50), "action": "back"})
        
        elif self.state == TIME_SELECT:
            y_pos = 200
            for time_option in TIME_OPTIONS:
                self.buttons.append({
                    "text": f"{time_option} seconds",
                    "rect": pygame.Rect(300, y_pos, 200, 60),
                    "action": f"time_{time_option}"
                })
                y_pos += 80
            
            self.buttons.append({"text": "BACK", "rect": pygame.Rect(50, 500, 100, 50), "action": "back"})
    
    def handle_button_click(self, pos):
        """ボタンクリックを処理"""
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                action = button["action"]
                
                if action == "start":
                    self.state = DIFFICULTY_SELECT
                elif action == "scores":
                    self.show_high_scores()
                elif action == "quit":
                    return False
                elif action == "back":
                    if self.state == DIFFICULTY_SELECT:
                        self.state = TITLE_SCREEN
                    elif self.state == TIME_SELECT:
                        self.state = DIFFICULTY_SELECT
                elif action.startswith("difficulty_"):
                    difficulty = action.split("_")[1]
                    self.selected_difficulty = difficulty
                    self.grid_size = DIFFICULTIES[difficulty]["grid"]
                    self.cell_size = DIFFICULTIES[difficulty]["cell_size"]
                    self.state = TIME_SELECT
                elif action.startswith("time_"):
                    time_value = int(action.split("_")[1])
                    self.selected_time = time_value
                    self.game_time = time_value
                    self.start_game()
                
                self.setup_buttons()
                break
        
        return True
    
    def show_high_scores(self):
        """ハイスコア画面を表示"""
        self.screen.fill(WHITE)
        
        title = self.title_font.render("HIGH SCORES", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        y_pos = 120
        for difficulty in DIFFICULTIES.keys():
            diff_text = self.subtitle_font.render(f"{difficulty}:", True, BLACK)
            self.screen.blit(diff_text, (100, y_pos))
            y_pos += 40
            
            for time_key in ["10", "20", "30"]:
                score = self.high_scores[difficulty][time_key]
                score_text = self.text_font.render(f"{time_key}s: {score} points", True, DARK_GRAY)
                self.screen.blit(score_text, (150, y_pos))
                y_pos += 30
            y_pos += 20
        
        # 戻るボタン
        back_button = pygame.Rect(50, 500, 100, 50)
        pygame.draw.rect(self.screen, LIGHT_GRAY, back_button)
        pygame.draw.rect(self.screen, BLACK, back_button, 2)
        back_text = self.button_font.render("BACK", True, BLACK)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
        
        pygame.display.flip()
        
        # 戻るボタンの待機
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        waiting = False
        
        return True
    
    def start_game(self):
        """ゲームを開始"""
        self.state = PLAYING
        self.grid = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.start_time = time.time()
        self.game_over_flag = False
        self.set_new_target()
    
    def set_new_target(self):
        """新しいターゲットマスを設定"""
        if self.target_row >= 0 and self.target_col >= 0:
            self.grid[self.target_row][self.target_col] = False
        
        self.target_row = random.randint(0, self.grid_size - 1)
        self.target_col = random.randint(0, self.grid_size - 1)
        self.grid[self.target_row][self.target_col] = True
    
    def get_cell_rect(self, row, col):
        """指定されたマスの矩形を取得"""
        margin = 10
        total_width = self.grid_size * self.cell_size + (self.grid_size - 1) * margin
        total_height = self.grid_size * self.cell_size + (self.grid_size - 1) * margin
        
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = 150
        
        x = start_x + col * (self.cell_size + margin)
        y = start_y + row * (self.cell_size + margin)
        
        return pygame.Rect(x, y, self.cell_size, self.cell_size)
    
    def handle_game_click(self, pos):
        """ゲーム中のクリック処理"""
        if self.game_over_flag:
            return
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = self.get_cell_rect(row, col)
                if rect.collidepoint(pos):
                    if row == self.target_row and col == self.target_col:
                        self.score += 1
                        self.set_new_target()
                    return
    
    def update_game(self):
        """ゲーム状態の更新"""
        if self.state == PLAYING and not self.game_over_flag:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.game_time:
                self.game_over_flag = True
                self.state = GAME_OVER
                self.is_new_high_score = self.update_high_score()
    
    def draw_title_screen(self):
        """タイトル画面を描画"""
        # グラデーション背景
        for y in range(SCREEN_HEIGHT):
            color_value = int(255 * (1 - y / SCREEN_HEIGHT))
            color = (color_value, color_value + 50, 255)
            if color[1] > 255:
                color = (color[0], 255, color[2])
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # タイトル
        title = self.title_font.render("CLICK GAME", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # バージョン表示（右下）
        version_text = self.text_font.render("Ver.1.0.0", True, WHITE)
        version_rect = version_text.get_rect()
        version_rect.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)
        self.screen.blit(version_text, version_rect)
    
    def draw_buttons(self):
        """ボタンを描画"""
        for button in self.buttons:
            # ボタンの影
            shadow_rect = button["rect"].copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(self.screen, DARK_GRAY, shadow_rect)
            
            # ボタン本体
            pygame.draw.rect(self.screen, LIGHT_BLUE, button["rect"])
            pygame.draw.rect(self.screen, BLUE, button["rect"], 3)
            
            # ボタンテキスト
            text = self.button_font.render(button["text"], True, BLACK)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
    
    def draw_game(self):
        """ゲーム画面を描画"""
        self.screen.fill(WHITE)
        
        # タイトル
        difficulty_name = self.get_difficulty_name()
        title = self.subtitle_font.render(f"{difficulty_name} - {self.game_time}s", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # グリッドを描画
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = self.get_cell_rect(row, col)
                
                if self.grid[row][col]:
                    # ターゲットマス（アニメーション効果）
                    pulse = int(50 * (1 + 0.5 * pygame.math.Vector2(1, 0).rotate(time.time() * 360).x))
                    color = (255 - pulse, 0, 0)
                else:
                    color = LIGHT_GRAY
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)
        
        # スコアと時間を表示
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.game_time - elapsed_time)
        
        score_text = self.text_font.render(f"Score: {self.score}", True, BLACK)
        time_text = self.text_font.render(f"Time: {remaining_time:.1f}s", True, BLACK)
        
        self.screen.blit(score_text, (50, 100))
        self.screen.blit(time_text, (SCREEN_WIDTH - 150, 100))
        
        # 現在のハイスコア表示
        current_high = self.high_scores[difficulty_name][str(self.game_time)]
        high_text = self.text_font.render(f"High Score: {current_high}", True, PURPLE)
        self.screen.blit(high_text, (50, 120))
    
    def draw_game_over(self):
        """ゲームオーバー画面を描画"""
        # 半透明オーバーレイ
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # ゲームオーバーテキスト
        game_over_text = self.title_font.render("GAME OVER!", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        # スコア表示
        score_text = self.subtitle_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(score_text, score_rect)
        
        # 新記録の場合
        if hasattr(self, 'is_new_high_score') and self.is_new_high_score:
            new_record_text = self.button_font.render("NEW HIGH SCORE!", True, YELLOW)
            new_record_rect = new_record_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
            self.screen.blit(new_record_text, new_record_rect)
        
        # 操作説明
        restart_text = self.text_font.render("Press R to Restart or ESC to Menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        """画面描画"""
        if self.state == TITLE_SCREEN:
            self.draw_title_screen()
            self.draw_buttons()
        
        elif self.state == DIFFICULTY_SELECT:
            self.screen.fill(WHITE)
            title = self.title_font.render("SELECT DIFFICULTY", True, BLUE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)
            self.draw_buttons()
        
        elif self.state == TIME_SELECT:
            self.screen.fill(WHITE)
            title = self.title_font.render("SELECT TIME", True, BLUE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)
            
            difficulty_text = self.subtitle_font.render(f"Difficulty: {self.selected_difficulty}", True, BLACK)
            difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            self.screen.blit(difficulty_text, difficulty_rect)
            
            self.draw_buttons()
        
        elif self.state == PLAYING:
            self.draw_game()
        
        elif self.state == GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """メインゲームループ"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左クリック
                        if self.state in [TITLE_SCREEN, DIFFICULTY_SELECT, TIME_SELECT]:
                            if not self.handle_button_click(event.pos):
                                running = False
                        elif self.state == PLAYING:
                            self.handle_game_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if self.state == GAME_OVER:
                        if event.key == pygame.K_r:
                            self.start_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = TITLE_SCREEN
                            self.setup_buttons()
            
            self.update_game()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = ClickGame()
    game.run()
