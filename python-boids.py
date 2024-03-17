import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 512, 512
NUM_FISH = 50
MAX_SPEED = 2
NEIGHBOR_RADIUS = 50
SEPARATION_RADIUS = 30
SEPARATION_FORCE = 0.8
ALIGNMENT_FORCE = 0.1
COHESION_FORCE = 0.05
SCREEN_CENTER = (WIDTH // 2, HEIGHT // 2)
BG_COLOR = (15, 10, 15)
FISH_COLOR = (255, 100, 200)


class Fish:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self, flock):
        # Rule 1: Separation
        separation = self.separate(flock)
        # Rule 2: Alignment
        alignment = self.align(flock)
        # Rule 3: Cohesion
        cohesion = self.cohere(flock)

        # Update velocity
        self.vx += separation[0] * SEPARATION_FORCE + alignment[0] * ALIGNMENT_FORCE + cohesion[0] * COHESION_FORCE
        self.vy += separation[1] * SEPARATION_FORCE + alignment[1] * ALIGNMENT_FORCE + cohesion[1] * COHESION_FORCE

        # Limit speed
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > MAX_SPEED:
            scale_factor = MAX_SPEED / speed
            self.vx *= scale_factor
            self.vy *= scale_factor

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Wrap around screen
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0

    def separate(self, flock):
        separation_vector = [0, 0]
        for other_fish in flock:
            if other_fish != self:
                distance = math.sqrt((self.x - other_fish.x) ** 2 + (self.y - other_fish.y) ** 2)
                if distance == 0: # To avoid division by zero
                    distance = 0.001
                if distance < SEPARATION_RADIUS:
                    separation_vector[0] += (self.x - other_fish.x) / distance
                    separation_vector[1] += (self.y - other_fish.y) / distance
        return separation_vector

    def align(self, flock):
        avg_velocity = [0, 0]
        num_neighbors = 0
        for other_fish in flock:
            if other_fish != self:
                distance = math.sqrt((self.x - other_fish.x) ** 2 + (self.y - other_fish.y) ** 2)
                if distance < NEIGHBOR_RADIUS:
                    avg_velocity[0] += other_fish.vx
                    avg_velocity[1] += other_fish.vy
                    num_neighbors += 1
        if num_neighbors > 0:
            avg_velocity[0] /= num_neighbors
            avg_velocity[1] /= num_neighbors
        return avg_velocity

    def cohere(self, flock):
        center_of_mass = [0, 0]
        num_neighbors = 0
        for other_fish in flock:
            if other_fish != self:
                distance = math.sqrt((self.x - other_fish.x) ** 2 + (self.y - other_fish.y) ** 2)
                if distance < NEIGHBOR_RADIUS:
                    center_of_mass[0] += other_fish.x
                    center_of_mass[1] += other_fish.y
                    num_neighbors += 1
        if num_neighbors > 0:
            center_of_mass[0] /= num_neighbors
            center_of_mass[1] /= num_neighbors
            return [center_of_mass[0] - self.x, center_of_mass[1] - self.y]
        else:
            return [0, 0]

    def draw(self, screen):
        # Draw fish as an arrow shape
        angle = math.atan2(self.vy, self.vx)
        pygame.draw.polygon(screen, FISH_COLOR, [(self.x + math.cos(angle) * 10, self.y + math.sin(angle) * 10),
                                                  (self.x + math.cos(angle + 5 * math.pi / 6) * 10, self.y + math.sin(angle + 5 * math.pi / 6) * 10),
                                                  (self.x + math.cos(angle - 5 * math.pi / 6) * 10, self.y + math.sin(angle - 5 * math.pi / 6) * 10)])
        

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()

    # Create fish
    fish = [Fish(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(-1, 1), random.uniform(-1, 1))
            for _ in range(NUM_FISH)]

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update fish
        for fishy in fish:
            fishy.update(fish)

        # Draw
        screen.fill(BG_COLOR)
        for fishy in fish:
            fishy.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
