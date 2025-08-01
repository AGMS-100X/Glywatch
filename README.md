# 🌙 GlyWatch Complete System

A comprehensive diabetes management platform that combines **GlyWatch** (your custom application) with **Nightscout** (open-source CGM monitoring) and **Supabase** (database) for multi-user support.

## 🎯 **What This System Does**

✅ **Multi-User Support** - Each user gets their own Nightscout instance  
✅ **Local Deployment** - Everything runs on your machine  
✅ **Supabase Database** - Better than MongoDB, easier to manage  
✅ **Complete API** - All endpoints for glucose, device status, treatments  
✅ **Simple Setup** - One command to get everything running  

## 🏗️ **Project Structure**

```
glywatch-complete/
├── glywatch-fullstack/          # Your GlyWatch application
│   ├── backend/                 # FastAPI backend
│   │   ├── services/           # Nightscout & Supabase services
│   │   ├── routers/            # API endpoints
│   │   └── setup_scripts/      # Installation scripts
│   └── frontend/               # React frontend (if you have one)
├── nightscout/                  # Nightscout CGM monitoring
│   ├── lib/                    # Nightscout libraries
│   ├── views/                  # Web interface
│   └── .env                    # Configuration
├── docs/                       # Documentation
├── setup/                      # Setup scripts
└── README.md                   # This file
```

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Node.js 16+
- Git

### **Installation**

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/glywatch-complete.git
cd glywatch-complete
```

2. **Run the setup script:**
```bash
cd glywatch-fullstack/backend
python manual_setup.py
```

3. **Start the services:**
```bash
# Terminal 1: Start Nightscout
cd nightscout
npm start

# Terminal 2: Start GlyWatch API
cd glywatch-fullstack/backend
python main.py
```

4. **Test the system:**
```bash
# Test Nightscout
curl http://localhost:1337/api/v1/status.json

# Test GlyWatch API
curl http://localhost:8000/health

# Register a user
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_123",
    "user_email": "test@example.com",
    "cgm_type": "Dexcom G6"
  }'
```

## 📱 **For Your Users**

When someone registers on GlyWatch:
1. **User provides**: Email, CGM device type
2. **GlyWatch creates**: Their own Nightscout instance
3. **User gets**: Unique Nightscout URL and API secret
4. **Data flows**: CGM → Nightscout → GlyWatch → User's dashboard

## 🔧 **API Endpoints**

### **User Management:**
- `POST /users/register` - Register new user
- `GET /users/{user_id}/status` - Get user status
- `POST /users/{user_id}/start-nightscout` - Start user's Nightscout

### **Glucose Data (per user):**
- `GET /cgm/latest/{user_id}` - Latest glucose for user
- `GET /cgm/history/{user_id}` - Glucose history for user
- `GET /cgm/device-status/{user_id}` - Device status for user

## 🛠️ **Configuration**

### **Supabase Setup**
1. Create a Supabase project at https://supabase.com
2. Run the SQL from `glywatch-fullstack/backend/supabase_tables.sql`
3. Update the connection string in `nightscout/.env`

### **Environment Variables**
```env
# Nightscout Configuration
MONGO_CONNECTION=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
API_SECRET=glywatch_secret_123
DISPLAY_UNITS=mg/dl
PORT=1337

# GlyWatch Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 📚 **Documentation**

- [Complete Setup Guide](docs/COMPLETE_SETUP_GUIDE.md)
- [API Documentation](http://localhost:8000/docs)
- [Nightscout Interface](http://localhost:1337)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 **License**

This project combines:
- **GlyWatch**: Your custom application
- **Nightscout**: MIT License (https://github.com/nightscout/cgm-remote-monitor)
- **Supabase**: Open source

## 🆘 **Support**

- **Issues**: Create an issue on GitHub
- **Documentation**: Check the docs folder
- **Nightscout Help**: https://nightscout.github.io/

---

**🎉 Built with ❤️ for the diabetes community** 