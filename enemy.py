import pygame
import random
import math
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, row, col):
        super().__init__()
        
        # Create a surface for the enemy with transparency
        self.image = pygame.Surface(ENEMY_SIZE, pygame.SRCALPHA)
        self.original_image = pygame.Surface(ENEMY_SIZE, pygame.SRCALPHA)
        
        # Different enemy types based on row
        self.row = row
        self.col = col
        
        width, height = ENEMY_SIZE
        
        # Different shapes and colors based on row
        if row == 0:
            # Top row: UFO-like enemies (red)
            color = RED
            # Draw oval-like UFO
            pygame.draw.ellipse(self.original_image, color, (0, height//4, width, height//2))
            # Draw cockpit
            pygame.draw.ellipse(self.original_image, (200, 200, 255), (width//3, height//3, width//3, height//3))
            # Draw lights
            pygame.draw.circle(self.original_image, BLUE, (width//4, height//2), height//8)
            pygame.draw.circle(self.original_image, GREEN, (3*width//4, height//2), height//8)
            
        elif row == 1 or row == 2:
            # Middle rows: crab-like enemies (blue)
            color = BLUE
            # Draw body
            pygame.draw.rect(self.original_image, color, (width//4, height//4, width//2, height//2))
            # Draw eyes
            pygame.draw.circle(self.original_image, WHITE, (width//3, height//3), height//8)
            pygame.draw.circle(self.original_image, WHITE, (2*width//3, height//3), height//8)
            pygame.draw.circle(self.original_image, BLACK, (width//3, height//3), height//16)
            pygame.draw.circle(self.original_image, BLACK, (2*width//3, height//3), height//16)
            # Draw claws
            pygame.draw.rect(self.original_image, color, (0, height//2, width//5, height//4))
            pygame.draw.rect(self.original_image, color, (4*width//5, height//2, width//5, height//4))
            
        else:
            # Bottom rows: octopus-like enemies (green)
            color = GREEN
            # Draw head
            pygame.draw.circle(self.original_image, color, (width//2, height//3), height//3)
            # Draw eyes
            pygame.draw.circle(self.original_image, WHITE, (width//3, height//3), height//10)
            pygame.draw.circle(self.original_image, WHITE, (2*width//3, height//3), height//10)
            pygame.draw.circle(self.original_image, BLACK, (width//3, height//3), height//20)
            pygame.draw.circle(self.original_image, BLACK, (2*width//3, height//3), height//20)
            # Draw tentacles
            for i in range(4):
                offset = i * (width//3)
                pygame.draw.line(self.original_image, color, 
                                (width//6 + offset, 2*height//3), 
                                (width//6 + offset, height), 
                                width//10)
        
        # Add white outline
        if row == 0:
            pygame.draw.ellipse(self.original_image, WHITE, (0, height//4, width, height//2), 1)
        elif row == 1 or row == 2:
            pygame.draw.rect(self.original_image, WHITE, (width//4, height//4, width//2, height//2), 1)
        else:
            pygame.draw.circle(self.original_image, WHITE, (width//2, height//3), height//3, 1)
        
        # Copy the original image to the display image
        self.image = self.original_image.copy()
        
        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        
        # Set initial position
        self.rect.x = x
        self.rect.y = y
        
        # Store row and column for formation tracking
        # Direction is shared among all enemies and managed by EnemyFormation
        
        # Animation values
        self.animation_timer = random.randint(0, 100)  # Randomize starting phase
        self.pulse_amount = 0
        self.growing = True
        
        # Shooting variables
        self.shoot_chance = 0.001  # 0.1% chance to shoot per frame
        self.preparing_to_shoot = False
        self.shoot_prep_timer = 0
        
    def update(self, direction, drop):
        """Update enemy position based on formation movement"""
        if drop:
            self.rect.y += ENEMY_DROP_SPEED
        else:
            self.rect.x += ENEMY_SPEED * direction
            
        # Animation: pulse effect
        self.animation_timer += 1
        
        # Pulse the size every 30 frames
        if self.animation_timer % 30 == 0:
            self.growing = not self.growing
            
        # Determine pulse amount (0 to 0.2)
        if self.growing:
            self.pulse_amount = 0.05 + 0.15 * math.sin(self.animation_timer * 0.1)
        else:
            self.pulse_amount = 0.05 + 0.15 * math.sin(self.animation_timer * 0.1 + math.pi)
            
        # Apply the pulse to create a subtle animation
        pulse_factor = 1.0 + self.pulse_amount
        width, height = ENEMY_SIZE
        scaled_width = int(width * pulse_factor)
        scaled_height = int(height * pulse_factor)
        
        # Center the scaled image
        x_offset = (scaled_width - width) // 2
        y_offset = (scaled_height - height) // 2
        
        # Reset the image and scale it
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        
        # Handle shoot preparation visual
        if self.preparing_to_shoot:
            self.shoot_prep_timer += 1
            # Flash the enemy white when about to shoot
            if self.shoot_prep_timer % 10 < 5:
                # Create a white overlay
                overlay = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 100))  # Semi-transparent white
                self.image.blit(overlay, (0, 0))
                
            if self.shoot_prep_timer >= 30:
                self.preparing_to_shoot = False
                self.shoot_prep_timer = 0
    
    def can_shoot(self):
        """Determine if this enemy will shoot on this frame"""
        if not self.preparing_to_shoot and random.random() < self.shoot_chance:
            self.preparing_to_shoot = True
            self.shoot_prep_timer = 0
            return False  # Don't shoot immediately, wait for visual cue
        
        # Only return True if we've been preparing to shoot and timer is at a certain value
        if self.preparing_to_shoot and self.shoot_prep_timer == 25:  # Shoot after 25 frames of preparation
            self.preparing_to_shoot = False
            return True
            
        return False

class EnemyFormation:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.direction = 1  # 1 for right, -1 for left
        self.should_drop = False
        self.time_since_last_drop = 0
        
        # Create the enemy formation
        self.create_formation()
    
    def create_formation(self):
        """Create a grid of enemies"""
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                # Calculate the position of each enemy in the grid
                x = 50 + col * (ENEMY_SIZE[0] + ENEMY_SPACING)
                y = 50 + row * (ENEMY_SIZE[1] + ENEMY_SPACING)
                
                # Create a new enemy and add it to the group
                enemy = Enemy(x, y, row, col)
                self.enemies.add(enemy)
    
    def update(self, current_time):
        """Update the entire enemy formation"""
        # Check if any enemy has reached the edge of the screen
        if self.should_change_direction():
            self.direction *= -1  # Reverse direction
            self.should_drop = True
        else:
            self.should_drop = False
        
        # Update all enemies with the new direction
        for enemy in self.enemies:
            enemy.update(self.direction, self.should_drop)
    
    def should_change_direction(self):
        """Check if any enemy has reached the screen edge"""
        for enemy in self.enemies:
            if (self.direction == 1 and enemy.rect.right >= SCREEN_WIDTH) or \
               (self.direction == -1 and enemy.rect.left <= 0):
                return True
        return False
    
    def check_enemies_shooting(self):
        """Check which enemies will shoot this frame"""
        shooting_positions = []
        
        # Only bottom-most enemies in each column can shoot
        # Create a dictionary to track the bottom-most enemy in each column
        bottom_enemies = {}
        
        for enemy in self.enemies:
            # If this enemy is lower than the current bottom enemy in this column, update
            if enemy.col not in bottom_enemies or enemy.rect.y > bottom_enemies[enemy.col].rect.y:
                bottom_enemies[enemy.col] = enemy
        
        # Now check if any of the bottom enemies will shoot
        for col, enemy in bottom_enemies.items():
            if enemy.can_shoot():
                shooting_positions.append((enemy.rect.centerx, enemy.rect.bottom))
        
        return shooting_positions
    
    def any_enemies_left(self):
        """Check if there are any enemies left"""
        return len(self.enemies) > 0
    
    def get_lowest_enemy_position(self):
        """Get the y position of the lowest enemy"""
        if not self.enemies:
            return 0
        
        return max(enemy.rect.bottom for enemy in self.enemies)

