# 2D Racing Car Game

This 2D racing car game features 10 progressively challenging levels where you compete against a bot opponent. The bot's speed increases by 0.2 times with each level, making each race more difficult than the last. In the final level, both you and the bot reach the same maximum velocity; however, the bot starts at maximum speed while you must accelerate from a standstill. Mastering your controls and strategy is key to overtaking the bot and achieving victory!

## How to Run the Game

1. **Install Pygame**: Ensure you have Python installed on your computer. Open your terminal or command prompt and install Pygame using:
   ```bash
   pip install pygame
   ```
2. **Run the Game**:
   - Unzip the game files.
   - Navigate to the `car demo > tp0` directory.
   - Open the terminal in this directory and run the game script:
     ```bash
     python racinggame.py
     ```

Once executed, the game window should open, and you're ready to play!

## Controls and Gameplay

- **W** - Move forward
- **A** - Turn left
- **S** - Move backward
- **D** - Turn right
- **B** - Speed boost (instantly increases velocity to 12)

### Gameplay Details

- **Normal Map**: Press `Space` to start the game against the AI. Progress through 10 levels. Winning all levels displays a "Win" message, while losing to the bot results in a "Loss" message, and the game resets.
- **Alternative Map**: At any level, you can choose to switch to the second map (referred to as "the cowards' way out"). Once switched, you cannot return to the original map, and you will resume the level with a mark of "shame" for not completing the normal map.

### Tips for Success

- Use your speed boost (`B`) wisely to gain a temporary advantage over the bot.
- Plan your acceleration and movements to maintain control and avoid collisions.

### Video Demonstration

[![Watch the demo](https://img.youtube.com/vi/SMv9HHqWIUM/0.jpg)](https://www.youtube.com/watch?v=SMv9HHqWIUM)

