# Telegram Music Bot - Project Overview

## Description

A fully-featured Telegram music bot with voice chat capabilities, speech recognition, and multi-platform streaming support. The bot uses an assistant account to join groups and play music in voice chats.

## Key Features

### Core Functionality
- **Voice Chat Integration**: Assistant account joins voice chats to play music
- **Multi-Platform Support**: YouTube, Spotify, SoundCloud, and more
- **Speech Recognition**: Speak your requests, bot recognizes and plays
- **Auto-Join**: Assistant automatically joins groups when bot is added
- **Comprehensive Logging**: All activities logged to a dedicated logger group
- **Statistics Tracking**: MongoDB-powered analytics and usage stats

### Commands
- `/start` - Welcome message and bot introduction
- `/help` - Comprehensive help documentation
- `/stats` - Bot statistics (uptime, plays, commands)
- `/ping` - Check bot latency
- `/assiststart` - Start assistant in voice chat
- `/assistclose` - Stop assistant from voice chat
- `/play [song]` - Play music (text command)
- Voice messages - Speak to play music

## Technical Stack

### Languages & Frameworks
- **Python 3.11+**
- **Pyrogram** - Telegram MTProto API framework
- **Py-TgCalls** - Voice chat integration
- **Motor** - Async MongoDB driver

### Key Libraries
- `yt-dlp` - Universal video/audio downloader
- `spotipy` - Spotify API integration
- `speech_recognition` - Voice to text conversion
- `pydub` - Audio processing
- `ffmpeg` - Audio/video manipulation

### Database
- **MongoDB** - Document database for stats, chat info, and play history

## Architecture

### Bot Structure
```
bot.py                  # Main entry point, initializes bot and assistant
├── config.py          # Configuration management
├── database/
│   └── mongodb.py     # Database operations
├── handlers/
│   ├── commands.py    # Basic command handlers
│   ├── voice_chat.py  # Voice chat management
│   └── music.py       # Music playback handlers
└── utils/
    ├── logger.py      # Logging utilities
    ├── downloader.py  # Music download and search
    └── speech.py      # Speech recognition
```

### Data Flow

1. **User Command** → Bot receives command
2. **Command Handler** → Routes to appropriate handler
3. **Music Search** → Searches platform (YouTube/Spotify)
4. **Download** → Downloads audio using yt-dlp
5. **Voice Chat** → Assistant joins and streams audio
6. **Logging** → Logs activity to logger group
7. **Database** → Updates statistics

### Voice Recognition Flow

1. User sends voice message
2. Bot downloads voice file
3. Converts to WAV format
4. Google Speech Recognition processes audio
5. Extracts song request
6. Plays requested song

## Deployment Options

### Heroku (Recommended for beginners)
- One-click deploy via button
- Automatic buildpacks for Python and FFmpeg
- Easy environment variable management
- Free tier available

### VPS (Recommended for production)
- Full control over resources
- Better performance
- No usage limits
- Systemd service for auto-restart

### Docker
- Containerized deployment
- Easy updates
- Consistent environment
- Docker Compose for easy management

## Configuration

### Required Environment Variables
```
API_ID              # Telegram API ID
API_HASH            # Telegram API Hash
BOT_TOKEN           # Bot token from BotFather
STRING_SESSION      # Assistant account session
LOGGER_GROUP_ID     # Logger group ID
MONGODB_URI         # MongoDB connection string
OWNER_ID            # Owner Telegram user ID
```

### Optional Variables
```
YOUTUBE_API_KEY         # YouTube Data API (for advanced features)
YOUTUBE_COOKIES_PATH    # For age-restricted content
SPOTIFY_CLIENT_ID       # Spotify integration
SPOTIFY_CLIENT_SECRET   # Spotify integration
```

## Security Features

- String session for assistant account (no password storage)
- Environment variables for sensitive data
- MongoDB connection with authentication
- No hardcoded credentials
- Secure cookie handling for YouTube

## Performance Optimizations

- Async/await throughout for non-blocking operations
- Efficient caching of downloaded music
- Connection pooling for database
- Lazy loading of music platforms
- Automatic cleanup of cache files

## Error Handling

- Comprehensive try-catch blocks
- Logging of all errors
- Graceful degradation
- User-friendly error messages
- Automatic reconnection on network issues

## Monitoring & Logging

### Bot Logs
- Startup information
- System resource usage
- Error tracking
- Performance metrics

### Logger Group
- Bot start/stop events
- Assistant join/leave events
- Song play history
- Command usage
- Error notifications

### Database Tracking
- Total plays
- Command statistics
- Active chats
- Play history with timestamps

## Future Enhancement Ideas

- Queue system for multiple songs
- Playlist support
- User preferences
- Admin controls
- DJ mode (user voting)
- Lyrics display
- Now playing with album art
- Multiple voice chat support
- Audio effects (bass boost, etc.)
- User permissions system

## Development

### Local Development
```bash
./setup.sh              # Initial setup
python generate_session.py  # Generate session
./start.sh              # Run bot
```

### Testing
- Test in a private group
- Verify all commands
- Test voice recognition
- Check error handling
- Validate logging

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Support & Documentation

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation**: [README.md](README.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **License**: [LICENSE](LICENSE)

## Credits & Acknowledgments

Built with love using open-source technologies:
- Pyrogram Team
- Py-TgCalls Team
- yt-dlp Contributors
- SpeechRecognition Library
- MongoDB
- All open-source contributors

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Note**: This bot is for educational purposes. Always comply with Telegram's Terms of Service and respect content platforms' policies.
