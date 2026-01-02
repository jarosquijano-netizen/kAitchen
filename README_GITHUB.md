# 🍳 k[AI]tchen

AI-powered family meal planning system with personalized menu generation and TV kitchen display.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## 🌟 Features

- **👨‍👩‍👧‍👦 Family Profile Management**: Detailed profiles for adults and children with dietary preferences
- **🤖 AI Menu Generation**: Personalized weekly menus using Claude AI (Anthropic)
- **📖 Recipe Extraction**: Automatic extraction from web URLs
- **📺 TV Kitchen Display**: Large, readable interface for your kitchen
- **🛒 Shopping Lists**: Auto-generated from weekly menus
- **🌍 Multi-language**: Spanish interface (easily adaptable)

## 🚀 Quick Deploy to Railway

### One-Click Deploy

1. Click the "Deploy on Railway" button above
2. Add PostgreSQL database in Railway dashboard
3. Set environment variables:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
4. Deploy! 🎉

### Manual Railway Deployment

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project
railway init

# 4. Add PostgreSQL
railway add --plugin postgresql

# 5. Set environment variables
railway variables set ANTHROPIC_API_KEY=your-key-here
railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# 6. Deploy
railway up

# 7. Open your app
railway open
```

## 💻 Local Development

### Prerequisites

- Python 3.8+
- pip
- (Optional) PostgreSQL for local testing

### Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/family-kitchen-menu.git
cd family-kitchen-menu

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template
cp .env.example .env

# 5. Edit .env with your keys
# Add your ANTHROPIC_API_KEY

# 6. Initialize database
python init.py

# 7. Run application
python app.py

# 8. Open browser
# Admin: http://localhost:5000
# TV Display: http://localhost:5000/tv
```

## 🔑 Required API Keys

### Anthropic Claude (Required)

1. Go to https://console.anthropic.com/
2. Create account or login
3. Navigate to "API Keys"
4. Create new key
5. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

**Cost**: ~$0.10-0.30 per menu generation (~$1-2/month)

### Clerk Authentication (Optional)

For multi-user/household support:

1. Go to https://clerk.com/
2. Create application
3. Get API keys
4. Add to `.env`:
   ```
   CLERK_SECRET_KEY=sk_test_...
   CLERK_PUBLISHABLE_KEY=pk_test_...
   ```

### Resend Email (Optional)

For weekly menu emails:

1. Go to https://resend.com/
2. Create account
3. Get API key
4. Add to `.env`: `RESEND_API_KEY=re_...`

## 📁 Project Structure

```
family-kitchen-menu/
├── app.py                    # Flask application & API
├── database.py               # Database operations (SQLite/PostgreSQL)
├── recipe_extractor.py       # Web scraping for recipes
├── menu_generator.py         # AI menu generation
├── init.py                   # Database initialization
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway deployment config
├── railway.toml             # Railway settings
├── .cursorrules             # Cursor AI editor rules
├── .env.example             # Environment template
├── templates/
│   ├── index.html           # Admin interface
│   └── tv_display.html      # TV kitchen display
└── static/
    └── js/
        └── app.js           # Frontend logic
```

## 🧪 Testing

El proyecto incluye un sistema completo de testing automático:

### Ejecutar Tests

```bash
# Todos los tests
python run_tests.py

# Solo backend (18 tests)
pytest tests/ -v

# Solo frontend (7 tests)
node tests/test_frontend.js

# Con cobertura de código
pytest tests/ --cov=. --cov-report=html
```

### Cobertura

- ✅ **Backend**: 18 tests (base de datos, API endpoints, generador de menús)
- ✅ **Frontend**: 7 tests (API mocks, utilidades)
- ✅ **CI/CD**: Tests automáticos en GitHub Actions

Los tests se ejecutan automáticamente en cada push y pull request.

Ver [TESTING.md](TESTING.md) para documentación completa.

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | ✅ | - | Claude API key for menu generation |
| `SECRET_KEY` | ✅ | random | Flask session secret |
| `DATABASE_URL` | ❌ | SQLite | PostgreSQL URL (Railway auto-sets) |
| `PORT` | ❌ | 5000 | Server port (Railway auto-sets) |
| `FLASK_ENV` | ❌ | development | Environment (development/production) |
| `CLERK_SECRET_KEY` | ❌ | - | Clerk authentication |
| `RESEND_API_KEY` | ❌ | - | Email service |

### Database

**Development**: Uses SQLite (automatic, no setup)

**Production (Railway)**: Uses PostgreSQL
- Automatically provisioned when added in Railway
- Connection string auto-set in `DATABASE_URL`
- Migration from SQLite handled automatically

## 🎯 Usage

### 1. Configure Family Profiles

Navigate to "Familia" tab:
- Add adult profiles with dietary preferences
- Add children profiles with pickiness levels
- Specify allergies and intolerances

### 2. Extract Recipes (Optional)

Navigate to "Recetas" tab:
- Paste recipe URLs from cooking websites
- System extracts ingredients and instructions
- Supports batch extraction

### 3. Generate Weekly Menu

Navigate to "Menú Semanal" tab:
- Click "Generate Menu with AI"
- Wait 15-30 seconds
- Review generated menu considering all preferences
- Get shopping list automatically

### 4. Display on Kitchen TV

Navigate to "Vista TV" tab:
- Copy the TV URL
- Open on your kitchen TV browser
- Use full screen mode (F11)
- Auto-refreshes every 5 minutes

**Finding your PC's IP** (for TV access):
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig

# Then use: http://YOUR-IP:5000/tv
```

## 🎨 Customization

### TV Display Colors

Edit `templates/tv_display.html`:

```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Change these hex colors */
}
```

### AI Menu Prompts

Edit `menu_generator.py`, method `_build_menu_prompt()`:

```python
# Add custom constraints
prompt += "- Maximum 3 new ingredients per week\n"
prompt += "- Include at least one pasta dish\n"
```

## 🐛 Troubleshooting

### Menu generation fails

**Issue**: "ANTHROPIC_API_KEY not found"

**Solution**:
1. Check `.env` file exists
2. Verify `ANTHROPIC_API_KEY=sk-ant-...` is set
3. Restart server

### Recipe extraction fails

**Issue**: Some websites not supported

**Solution**:
- Try different recipe websites
- Popular blogs work best
- Sites with Schema.org markup work best

### TV display not accessible

**Issue**: Can't reach from TV

**Solution**:
1. Use PC's IP address, not `localhost`
2. Ensure same WiFi network
3. Check firewall settings
4. Format: `http://192.168.1.X:5000/tv`

### Database errors on Railway

**Issue**: SQLite not supported in production

**Solution**:
- Railway requires PostgreSQL
- Add PostgreSQL plugin in Railway dashboard
- Restart deployment

## 🔐 Security

- Never commit `.env` files
- Use strong `SECRET_KEY` (32+ random chars)
- Keep API keys private
- Use HTTPS in production (Railway provides this)
- Implement rate limiting for public deployments

## 📊 Performance

**Expected Response Times**:
- Profile operations: < 100ms
- Recipe extraction: 2-5 seconds
- Menu generation: 15-30 seconds
- Page loads: < 500ms

**Optimization Tips**:
- Use PostgreSQL in production (not SQLite)
- Enable caching for recipe extractions
- Consider Redis for sessions (high traffic)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 Development with Cursor

This project includes `.cursorrules` for [Cursor](https://cursor.sh/) AI editor:

- Automatic code style enforcement
- Context-aware suggestions
- Security best practices
- Railway deployment helpers

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Meal prep mode (batch cooking)
- [ ] Nutritional analysis
- [ ] Recipe ratings and favorites
- [ ] Calendar integration (Google Calendar, iCal)
- [ ] Multiple household support (with Clerk)
- [ ] Email reminders (with Resend)
- [ ] Shopping list export (Todoist, etc.)

## 📄 License

MIT License - feel free to use for personal or commercial projects

## 🙏 Credits

- **Anthropic** for Claude AI
- **Railway** for hosting platform
- **Flask** community
- All recipe websites that share their content

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/family-kitchen-menu/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/family-kitchen-menu/discussions)
- **Documentation**: Check README and inline comments

## 🌟 Show Your Support

If this project helps you, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting features
- 🔀 Contributing code

---

**Made with ❤️ for families who want to eat better with less stress**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)
