import pygame
import sys
import os
import json
import random
import wave
import struct
import math
from constants import *
from player import Player
from projectile import Projectile
from enemy import Enemy, EnemyFormation

def load_high_score():
    """Load high score from file, or return 0 if file doesn't exist"""
    try:
        if os.path.exists('highscore.json'):
            with open('highscore.json', 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
    except Exception as e:
        print(f"Error loading high score: {e}")
    return 0

def save_high_score(score):
    """Save high score to file"""
    try:
        with open('highscore.json', 'w') as f:
            json.dump({'high_score': score}, f)
    except Exception as e:
        print(f"Error saving high score: {e}")

def draw_text(surface, text, size, x, y, color=WHITE, align="topleft"):
    """Helper function to draw text on a surface"""
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "topleft":
        text_rect.topleft = (x, y)
    elif align == "center":
        text_rect.center = (x, y)
    
    surface.blit(text_surface, text_rect)
    return text_rect

# Function to create a simple beep sound file
def create_simple_sound_file(filepath, duration=0.3, frequency=440):
    """Create a simple beep sound file if it doesn't exist"""
    # Skip if file already exists
    if os.path.exists(filepath):
        return filepath
        
    try:
        # Sound parameters
        sample_rate = 44100
        num_samples = int(duration * sample_rate)
        
        # Create a simple sine wave
        wave_file = wave.open(filepath, 'w')
        wave_file.setnchannels(1)  # Mono
        wave_file.setsampwidth(2)  # 16-bit
        wave_file.setframerate(sample_rate)
        
        # Generate simple waveform
        for i in range(num_samples):
            value = int(32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
            data = struct.pack('<h', value)
            wave_file.writeframes(data)
            
        wave_file.close()
        return filepath
    except Exception as e:
        print(f"Error creating sound file {filepath}: {e}")
        return None

def main():
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Create simple sound effects directory and files if needed
    sounds_dir = os.path.join('assets', 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    # Create different sound effects with different frequencies
    shoot_sound_file = create_simple_sound_file(os.path.join(sounds_dir, 'shoot.wav'), 0.1, 880)
    explosion_sound_file = create_simple_sound_file(os.path.join(sounds_dir, 'explosion.wav'), 0.3, 220)
    player_hit_sound_file = create_simple_sound_file(os.path.join(sounds_dir, 'hit.wav'), 0.2, 330)
    game_over_sound_file = create_simple_sound_file(os.path.join(sounds_dir, 'gameover.wav'), 0.5, 150)
    
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()  # Initialize sound mixer
    
    # Create the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    
    # Set up the game clock
    clock = pygame.time.Clock()
    
    # Game state variables
    
    # Load sound effects
    try:
        shoot_sound = pygame.mixer.Sound(shoot_sound_file) if shoot_sound_file else None
        explosion_sound = pygame.mixer.Sound(explosion_sound_file) if explosion_sound_file else None
        player_hit_sound = pygame.mixer.Sound(player_hit_sound_file) if player_hit_sound_file else None
        game_over_sound = pygame.mixer.Sound(game_over_sound_file) if game_over_sound_file else None
        
        # Set default volumes
        if shoot_sound: shoot_sound.set_volume(0.5)
        if explosion_sound: explosion_sound.set_volume(0.5)
        if player_hit_sound: player_hit_sound.set_volume(0.5)
        if game_over_sound: game_over_sound.set_volume(0.5)
        
        print("Sound effects loaded successfully")
    except Exception as e:
        # Fallback if the sound loading doesn't work
        shoot_sound = None
        explosion_sound = None
        player_hit_sound = None
        game_over_sound = None
        print(f"Warning: Sound effects could not be loaded: {e}")
    
    # Set default volume
    volume = 0.5
    pygame.mixer.music.set_volume(volume)
    
    # Game state variables
    running = True
    score = 0
    high_score = load_high_score()
    lives = PLAYER_LIVES
    game_over = False
    game_started = False  # Track if the game has started
    game_over_time = 0  # Track when game over occurred for restart delay
    player_hit_time = 0  # Track when player was hit for flash effect
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    
    # Create player
    player = Player()
    all_sprites.add(player)
    
    # Create enemy formation
    enemy_formation = EnemyFormation()
    for enemy in enemy_formation.enemies:
        all_sprites.add(enemy)
    # Main game loop
    # Function to reset the game
    def reset_game():
        nonlocal score, lives, game_over, game_started, player_hit_time, player, enemy_formation
        score = 0
        lives = PLAYER_LIVES
        game_over = False
        game_started = True
        player_hit_time = 0
        
        # Clear all sprite groups
        all_sprites.empty()
        player_bullets.empty()
        enemy_bullets.empty()
        
        # Create new player
        player = Player()
        all_sprites.add(player)
        
        # Create new enemy formation
        enemy_formation = EnemyFormation()
        for enemy in enemy_formation.enemies:
            all_sprites.add(enemy)
    
    # Main game loop
    while running:
        current_time = pygame.time.get_ticks()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and not game_started and not game_over:
                    # Start the game when SPACE is pressed on start screen
                    game_started = True
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    # Increase volume
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                    if shoot_sound:
                        shoot_sound.set_volume(volume)
                        explosion_sound.set_volume(volume)
                        player_hit_sound.set_volume(volume)
                        game_over_sound.set_volume(volume)
                elif event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE):
                    # Decrease volume
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                    if shoot_sound:
                        shoot_sound.set_volume(volume)
                        explosion_sound.set_volume(volume)
                        player_hit_sound.set_volume(volume)
                        game_over_sound.set_volume(volume)
                elif game_started and not game_over:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()
                    elif event.key == pygame.K_SPACE:
                        bullet_pos = player.shoot()
                        if bullet_pos:
                            # Create new bullet and add it to sprite groups
                            new_bullet = Projectile(bullet_pos[0], bullet_pos[1])
                            player_bullets.add(new_bullet)
                            all_sprites.add(new_bullet)
                            # Play shooting sound
                            if shoot_sound:
                                shoot_sound.play()
                elif game_over and event.key == pygame.K_r:
                    # Reset the game if R is pressed on game over screen, after a delay
                    if current_time - game_over_time > 1000:  # 1 second delay
                        reset_game()
            elif event.type == pygame.KEYUP and game_started and not game_over:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.stop()
        
        # Game logic update (only if game has started and not game over)
        if game_started and not game_over:
            # Update player and bullets
            player.update()
            player_bullets.update()
            enemy_bullets.update()
            
            # Update enemy formation
            enemy_formation.update(current_time)
            
            # Check if any enemies should shoot
            enemy_shooting_positions = enemy_formation.check_enemies_shooting()
            for pos in enemy_shooting_positions:
                new_bullet = Projectile(pos[0], pos[1], is_player_bullet=False)
                enemy_bullets.add(new_bullet)
                all_sprites.add(new_bullet)
            
            # Check for collisions between player bullets and enemies
            hits = pygame.sprite.groupcollide(enemy_formation.enemies, player_bullets, True, True)
            for enemy, bullets in hits.items():
                score += SCORE_PER_HIT
                # Update high score if needed
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                # Remove the enemy from all sprite groups
                enemy.kill()
                # Play explosion sound
                if explosion_sound:
                    explosion_sound.play()
            # Check for collisions between enemy bullets and player
            if pygame.sprite.spritecollide(player, enemy_bullets, True):
                lives -= 1
                # Set player hit time for flash effect
                player_hit_time = current_time
                # Play player hit sound
                if player_hit_sound:
                    player_hit_sound.play()
                
                if lives <= 0:
                    game_over = True
                    game_over_time = current_time
                    # Play game over sound
                    if game_over_sound:
                        game_over_sound.play()
            # Check for collisions between enemies and player
            # Check for collisions between enemies and player
            if pygame.sprite.spritecollide(player, enemy_formation.enemies, False):
                lives = 0
                game_over = True
                game_over_time = current_time
                # Play game over sound
                if game_over_sound:
                    game_over_sound.play()
            # Check if enemies have reached the bottom
            if enemy_formation.get_lowest_enemy_position() >= player.rect.top:
                game_over = True
                game_over_time = current_time
                # Play game over sound
                if game_over_sound:
                    game_over_sound.play()
            # Check if all enemies are destroyed
            if not enemy_formation.any_enemies_left():
                # Create new wave of enemies
                enemy_formation = EnemyFormation()
                for enemy in enemy_formation.enemies:
                    all_sprites.add(enemy)
        # Drawing
        screen.fill(BLACK)
        
        if not game_started:
            # Draw start screen
            # Title
            title_text = "SPACE INVADERS"
            draw_text(screen, title_text, 72, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, color=GREEN, align="center")
            
            # Instructions
            instructions = [
                "Arrow Keys: Move Left/Right",
                "Space: Shoot",
                "Escape: Quit Game",
                "+/-: Volume Up/Down",
                "",
                "Press SPACE to Start"
            ]
            
            for i, line in enumerate(instructions):
                draw_text(screen, line, 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40, align="center")
            
            # Display high score
            draw_text(screen, f"High Score: {high_score}", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, 
                      color=(255, 215, 0), align="center")  # Gold color for high score
            
            # Draw some enemy examples
            enemy_example = Enemy(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 50, 0, 0)
            enemy_example.update(0, False)
            screen.blit(enemy_example.image, enemy_example.rect)
            
            enemy_example2 = Enemy(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 50, 2, 0)
            enemy_example2.update(0, False)
            screen.blit(enemy_example2.image, enemy_example2.rect)
            
        else:
            # Draw all game objects
            all_sprites.draw(screen)
            enemy_formation.enemies.draw(screen)
            
            # Apply flash effect if player was recently hit
            if player_hit_time > 0 and current_time - player_hit_time < 500:  # Flash for 500ms
                if (current_time - player_hit_time) % 100 < 50:  # Alternate flash every 50ms
                    # Create a red flash overlay on the player
                    flash_surface = pygame.Surface((player.rect.width, player.rect.height), pygame.SRCALPHA)
                    flash_surface.fill((255, 0, 0, 128))  # Semi-transparent red
                    screen.blit(flash_surface, player.rect)
            
            # Display score, high score and lives
            draw_text(screen, f"Score: {score}", 36, 10, 10)
            draw_text(screen, f"High Score: {high_score}", 36, SCREEN_WIDTH // 2, 10, align="center")
            draw_text(screen, f"Lives: {lives}", 36, SCREEN_WIDTH - 150, 10)
            
            # Display game over screen if necessary
            if game_over:
                # Semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill(BLACK)
                screen.blit(overlay, (0, 0))
                
                # Game over text
                draw_text(screen, "GAME OVER", 72, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100, 
                         color=RED, align="center")
                
                # Final score, high score and restart instructions
                draw_text(screen, f"Final Score: {score}", 36, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 
                         align="center")
                draw_text(screen, f"High Score: {high_score}", 36, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50, 
                         color=(255, 215, 0), align="center")
                
                # Only show restart prompt after a delay
                if current_time - game_over_time > 1000:  # 1 second delay
                    draw_text(screen, "Press R to restart", 36, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100, 
                             align="center")
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

