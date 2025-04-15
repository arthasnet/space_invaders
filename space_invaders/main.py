    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Create simple sound effects directory and files if needed
    sounds_dir = os.path.join('assets', 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    # Create simple wav files for sound effects if they don't exist
    def create_simple_sound_file(filename, duration=0.3, frequency=440):
        """Create a simple beep sound file if it doesn't exist"""
        import wave
        import struct
        import math
        
        filepath = os.path.join(sounds_dir, filename)
        
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
            print(f"Error creating sound file {filename}: {e}")
            return None
    
    # Create different sound effects with different frequencies
    shoot_sound_file = create_simple_sound_file('shoot.wav', 0.1, 880)
    explosion_sound_file = create_simple_sound_file('explosion.wav', 0.3, 220)
    player_hit_sound_file = create_simple_sound_file('hit.wav', 0.2, 330)
    game_over_sound_file = create_simple_sound_file('gameover.wav', 0.5, 150)
    
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
