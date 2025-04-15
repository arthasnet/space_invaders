import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Create a simple rectangle for the player ship
        # Create a surface for the player ship with transparency
        self.image = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        
        # Draw a triangular spaceship using polygon
        width, height = PLAYER_SIZE
        
        # Define the points for the triangle (spaceship)
        points = [
            (width // 2, 0),  # Top center
            (0, height),      # Bottom left
            (width, height)   # Bottom right
        ]
        
        # Draw the ship body (green triangle)
        pygame.draw.polygon(self.image, GREEN, points)
        
        # Add some details to the ship
        pygame.draw.polygon(self.image, WHITE, points, 2)  # White outline
        
        # Add an engine glow at the bottom
        pygame.draw.rect(self.image, BLUE, 
                         (width // 3, height - 8, width // 3, 8))
        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        
        # Set initial position
        self.rect.centerx = PLAYER_START_X
        self.rect.bottom = PLAYER_START_Y
        
        # Movement speed
        self.speed = PLAYER_SPEED
        
        # Direction of movement (0 = stationary)
        self.direction_x = 0
        
        # Shooting cooldown
        self.last_shot_time = 0
        self.shoot_cooldown = 500  # milliseconds
    
    def update(self):
        """Update the player's position based on movement direction"""
        # Move the player horizontally
        self.rect.x += self.direction_x * self.speed
        
        # Keep the player within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def move_left(self):
        """Set direction to move left"""
        self.direction_x = -1
    
    def move_right(self):
        """Set direction to move right"""
        self.direction_x = 1
    
    def stop(self):
        """Stop horizontal movement"""
        self.direction_x = 0
    
    def can_shoot(self):
        """Check if player can shoot based on cooldown"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_cooldown:
            self.last_shot_time = current_time
            return True
        return False
    
    def shoot(self):
        """Create a projectile if cooldown allows"""
        if self.can_shoot():
            # This will return the position where the bullet should be created
            bullet_x = self.rect.centerx
            bullet_y = self.rect.top
            return (bullet_x, bullet_y)
        return None

