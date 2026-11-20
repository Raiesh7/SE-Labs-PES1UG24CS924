import random
import pygame
from game.text_box import TextBox

class GameEngine:
    MAX_ATTEMPTS = 10

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False
        self.search_min = 1
        self.search_max = 100
        self.guess_history = []

        self.input_box = TextBox(width // 2 - 110, 150, 120, 48)
        self.submit_btn = pygame.Rect(width // 2 + 25, 150, 100, 48)

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_btn = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 22)

    def submit_guess(self):
        if self.game_won or self.game_over:
            return

        if not self.input_box.text.strip():
            self.feedback_msg = "Enter a number before submitting."
            self.feedback_color = (255, 200, 80)
            return

        try:
            guess = int(self.input_box.text)
        except ValueError:
            self.feedback_msg = "Enter a valid whole number."
            self.feedback_color = (255, 200, 80)
            return

        if guess < 1 or guess > 100:
            self.feedback_msg = "Guess must be between 1 and 100."
            self.feedback_color = (255, 200, 80)
            return
        
        self.attempts += 1
        self.input_box.clear()

        if guess < self.secret_number:
            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)
            self.search_min = max(self.search_min, guess + 1)
            self.guess_history.insert(0, (guess, "LOW", (80, 160, 240)))
        elif guess > self.secret_number:
            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)
            self.search_max = min(self.search_max, guess - 1)
            self.guess_history.insert(0, (guess, "HIGH", (240, 100, 80)))
        else:
            self.feedback_msg = f"CORRECT! Found in {self.attempts} attempts."
            self.feedback_color = (80, 220, 90)
            self.guess_history.insert(0, (guess, "CORRECT", (80, 220, 90)))
            self.game_won = True
            return

        self.guess_history = self.guess_history[:6]
        if self.attempts >= self.MAX_ATTEMPTS:
            self.game_over = True
            self.feedback_msg = f"GAME OVER! The number was {self.secret_number}"
            self.feedback_color = (255, 80, 80)

    def reset(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False
        self.search_min = 1
        self.search_max = 100
        self.guess_history = []
        self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()
            elif event.key == pygame.K_r and (self.game_won or self.game_over):
                self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((30, 34, 42))

        title_surf = self.font_title.render("Number Guessing Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 35))

        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts}/{self.MAX_ATTEMPTS}",
            True,
            (180, 185, 195),
        )
        screen.blit(attempts_surf, (self.width // 2 - attempts_surf.get_width() // 2, 95))

        range_surf = self.font_medium.render(
            f"Search range: {self.search_min} - {self.search_max}",
            True,
            (255, 220, 80),
        )
        screen.blit(range_surf, (self.width // 2 - range_surf.get_width() // 2, 118))
        self.input_box.render(screen)

        pygame.draw.rect(screen, (50, 150, 80), self.submit_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.submit_btn, width=2, border_radius=6)
        btn_text = self.font_btn.render("SUBMIT", True, (255, 255, 255))
        screen.blit(
            btn_text,
            (self.submit_btn.centerx - btn_text.get_width() // 2, self.submit_btn.centery - btn_text.get_height() // 2),
        )

        feedback_surf = self.font_medium.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (self.width // 2 - feedback_surf.get_width() // 2, 235))

        history_title = self.font_small.render("Recent guesses", True, (220, 220, 220))
        screen.blit(history_title, (20, 145))
        for index, (guess, direction, color) in enumerate(self.guess_history[:6]):
            history_surf = self.font_small.render(f"{guess}  {direction}", True, color)
            screen.blit(history_surf, (20, 170 + index * 24))

        if self.game_won or self.game_over:
            restart_surf = self.font_medium.render("Press [R] to Start a New Game", True, (255, 220, 80))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, 295))
