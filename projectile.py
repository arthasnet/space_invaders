import pygame
import random
import math
from constants import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, is_player_bullet=True):
        super().__init__()
        # Create the bullet surface with transparency
        self.image = pygame.Surface(BULLET_SIZE, pygame.SRCALPHA)
        self.original_image = pygame.Surface(BULLET_SIZE, pygame.SRCALPHA)
        
        # Store if this is a player bullet
        self.is_player_bullet = is_player_bullet
        
        # Animation timer and properties
        self.animation_timer = 0
        self.trail_positions = []  # Store previous positions for trail effect
        
        # Different visuals for player vs enemy projectiles
        width, height = BULLET_SIZE
        
        if is_player_bullet:
            # Player bullet: laser beam style
            # Main beam (bright center)
            pygame.draw.rect(self.original_image, (100, 255, 100), (width//3, 0, width//3, height))
            
            # Glow effect around the beam
            pygame.draw.rect(self.original_image, (200, 255, 200, 150), (0, 0, width, height))
            
            # Create a gradient effect (brighter at the top)
            for i in range(5):
                alpha = 150 - i * 30
                y_pos = i * height // 5
                glow_height = height // 5
                glow_surface = pygame.Surface((width, glow_height), pygame.SRCALPHA)
                glow_surface.fill((255, 255, 255, alpha))
                self.original_image.blit(glow_surface, (0, y_pos))
                
        else:
            # Enemy bullet: plasma ball style
            # Core of the plasma
            pygame.draw.circle(self.original_image, (255, 100, 100), (width//2, height//2), width//2)
            
            # Outer glow
            for radius in range(width//2, 0, -1):
                alpha = 150 - radius * 20
                if alpha > 0:
                    pygame.draw.circle(self.original_image, (255, 200, 100, alpha), 
                                      (width//2, height//2), radius)
        
        # Copy to the display image
        self.image = self.original_image.copy()
        self.image.fill(BULLET_COLOR)
        
        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        
        # Set initial position
        self.rect.centerx = x
        self.rect.bottom = y if is_player_bullet else y + 5
        # Set bullet speed (negative for upward movement, positive for downward)
        self.speed = -BULLET_SPEED if is_player_bullet else BULLET_SPEED
        
        # Store previous positions for trail effect (only last few positions)
        self.max_trail_length = 5 if is_player_bullet else 3
        self.is_player_bullet = is_player_bullet
    
    def update(self):
        """Update the bullet's position and animation"""
        # Store current position for trail effect before moving
        if len(self.trail_positions) >= self.max_trail_length:
            self.trail_positions.pop(0)  # Remove oldest position
        self.trail_positions.append((self.rect.centerx, self.rect.centery))
        
        # Move the bullet vertically
        self.rect.y += self.speed
        
        # Animate the bullet
        self.animation_timer += 1
        
        if self.is_player_bullet:
            # Player bullet: Trailing effect
            self.update_player_bullet_visuals()
        else:
            # Enemy bullet: Pulsing effect
            self.update_enemy_bullet_visuals()
        
        # Remove the bullet if it goes off screen
        if (self.is_player_bullet and self.rect.bottom < 0) or \
           (not self.is_player_bullet and self.rect.top > SCREEN_HEIGHT):
            self.kill()  # Remove this bullet from all sprite groups
    
    def update_player_bullet_visuals(self):
        """Update the visual appearance of player bullets"""
        # Reset the image
        self.image = self.original_image.copy()
        
        # Add slight pulsing glow effect
        pulse = math.sin(self.animation_timer * 0.2) * 0.2 + 0.8  # 0.6 to 1.0 range
        
        # Apply a slight scale effect based on pulse
        width, height = BULLET_SIZE
        scaled_width = max(int(width * pulse), 1)
        
        # Ensure we maintain the height but vary the width slightly
        if scaled_width != width:
            temp_image = pygame.transform.scale(self.image, (scaled_width, height))
            # Create a new image to blit the scaled image centered
            self.image = pygame.Surface(BULLET_SIZE, pygame.SRCALPHA)
            x_offset = (width - scaled_width) // 2
            self.image.blit(temp_image, (x_offset, 0))
    
    def update_enemy_bullet_visuals(self):
        """Update the visual appearance of enemy bullets"""
        # Reset the image
        self.image = self.original_image.copy()
        
        # Pulsing effect for enemy projectiles
        pulse = math.sin(self.animation_timer * 0.3) * 0.3 + 0.7  # 0.4 to 1.0 range
        
        # Apply color pulsing effect
        width, height = BULLET_SIZE
        
        # Apply a color overlay that pulses
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        alpha = int(100 * pulse)  # Pulsing alpha
        overlay.fill((255, 255, 0, alpha))  # Yellow-ish glow
        self.image.blit(overlay, (0, 0))
        
        # Also apply rotation for plasma ball effect
        angle = self.animation_timer * 5 % 360
        self.image = pygame.transform.rotate(self.image, angle)
        
        # Ensure the rotated image is still centered on the bullet rect
        new_rect = self.image.get_rect(center=self.rect.center)
        self.rect = new_rect

