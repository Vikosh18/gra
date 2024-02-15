import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1300, 800
FPS = 60
FIGURE_SIZE = 50
FIGURE_SPEED = 0.5
WHITE = (255, 255, 255)
SCORE_PER_FIGURE = 10
NUM_FIGURES = 5
ACCELERATION_INTERVAL = 10000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Клацай на фігурки!")

clock = pygame.time.Clock()

class Figure:
    def __init__(self, global_speed):
        self.x = random.randint(0, WIDTH - FIGURE_SIZE)
        self.y = 0
        self.speed = global_speed
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self, figures):
        self.y += self.speed

        for figure in figures:
            if self is not figure and self.collide(figure):
                self.y = figure.y - FIGURE_SIZE

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, FIGURE_SIZE, FIGURE_SIZE))

    def collide(self, other_figure):
        if (self.x < other_figure.x + FIGURE_SIZE and
            self.x + FIGURE_SIZE > other_figure.x and
            self.y < other_figure.y + FIGURE_SIZE and
            self.y + FIGURE_SIZE > other_figure.y):
            return True
        return False

def draw_play_button():
    font = pygame.font.SysFont(None, 100)
    play_button = font.render("Play", True, (255, 0, 0))
    play_button_rect = play_button.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(play_button, play_button_rect)
    return play_button_rect

def start_game():
    figures = []
    score = 0
    misses = 0
    figures_to_remove = []

    global_speed = FIGURE_SPEED
    acceleration_timer = pygame.time.get_ticks()

    for _ in range(NUM_FIGURES):
        new_figure = Figure(global_speed)
        figures.append(new_figure)

    play_button_rect = draw_play_button()
    pygame.display.flip()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    waiting_for_start = False

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                hit = False  # Змінна, що вказує, чи було попадання по фігурці
                for figure in figures:
                    if figure.x < mouse_pos[0] < figure.x + FIGURE_SIZE and figure.y < mouse_pos[1] < figure.y + FIGURE_SIZE:
                        score += SCORE_PER_FIGURE
                        figures_to_remove.append(figure)
                        hit = True  # Якщо було попадання, змінити значення на True
                if not hit:
                    misses += 1  # Якщо не було попадання, збільшити лічильник промахів

        for figure in figures_to_remove:
            figures.remove(figure)
        figures_to_remove.clear()

        if random.randint(1, 100) < 5:
            new_figure = Figure(global_speed)
            new_figure.update(figures)
            figures.append(new_figure)

        current_time = pygame.time.get_ticks()
        if current_time - acceleration_timer > ACCELERATION_INTERVAL:
            global_speed += 0.4
            acceleration_timer = current_time

        for figure in figures:
            figure.update(figures)
            figure.draw()

            if figure.y >= HEIGHT:
                font = pygame.font.SysFont(None, 72)
                game_over_text = font.render("Game Over! Score: " + str(score), True, (0, 0, 0))
                screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 30))

                misses_text = font.render("Misses: " + str(misses), True, (0, 0, 0))
                screen.blit(misses_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

                play_again_button = font.render("Play Again(Click)", True, (0, 0, 0))
                play_again_rect = play_again_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
                screen.blit(play_again_button, play_again_rect)

                pygame.display.flip()

                waiting_for_restart = True
                while waiting_for_restart:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if play_again_rect.collidepoint(mouse_pos):
                                waiting_for_restart = False
                                return score, misses

        font = pygame.font.SysFont(None, 36)
        text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def main():
    while True:
        score, misses = start_game()
        print("You scored:", score)
        print("ПРОМАХІВ:", misses)

if __name__ == "__main__":
    main()
