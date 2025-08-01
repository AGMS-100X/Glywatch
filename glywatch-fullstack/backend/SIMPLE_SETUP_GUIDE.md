# 🌙 Simple GlyWatch Setup Guide

This guide will help you set up GlyWatch with **local Nightscout** and **Supabase** for multi-user support.

## 🎯 **Why This Approach?**

✅ **Full Control**: Run everything locally  
✅ **No Heroku/Atlas Complexity**: Use Supabase instead  
✅ **Multi-User Support**: Each user gets their own Nightscout instance  
✅ **Simple Deployment**: Everything runs on your machine  
✅ **Cost Effective**: Free Supabase tier is generous  

## 🚀 **Step-by-Step Setup**

### **Step 1: Install Prerequisites**

```bash
# Install Node.js (if not already installed)
# Download from: https://nodejs.org/

# Install Python dependencies
cd glywatch-fullstack/backend
pip install -r requirements.txt
```

### **Step 2: Set Up Supabase**

1. **Create Supabase Project:**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Note your project URL and API keys

2. **Create Database Tables:**
   - Go to SQL Editor in Supabase
   - Copy and paste contents of `supabase_tables.sql`
   - Run the SQL commands

3. **Get PostgreSQL Connection String:**
   - Go to Settings → Database
   - Copy the connection string
   - Replace `[YOUR-PASSWORD]` with your database password

### **Step 3: Run Complete Setup Script**

```bash
python setup_complete_system.py
```

This script will:
- ✅ Check dependencies
- ✅ Download and set up Nightscout
- ✅ Configure environment variables
- ✅ Test the complete system

### **Step 4: Manual Configuration (if needed)**

If the automatic setup doesn't work, do this manually:

#### **A. Set up Nightscout:**
```bash
# Clone Nightscout
git clone https://github.com/nightscout/cgm-remote-monitor.git nightscout
cd nightscout

# Install dependencies
npm install

# Create environment file
cp sample.env .env
```

Edit `nightscout/.env`:
```env
MONGO_CONNECTION=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
API_SECRET=glywatch_secret_123
DISPLAY_UNITS=mg/dl
ENABLE=careportal basal dbsize rawbg iob maker cob bwp cage sage boluscalc pushover treatmentnotify loop pump profile food openaps bage iage weight heartrate
PORT=1337
```

#### **B. Set up GlyWatch:**
```bash
cd glywatch-fullstack/backend
python setup_env.py
```

When prompted:
- **Nightscout URL**: `http://localhost:1337`
- **API Secret**: `glywatch_secret_123`
- **Supabase URL**: Your Supabase project URL
- **Supabase Key**: Your Supabase anon key

### **Step 5: Start the System**

```bash
# Terminal 1: Start Nightscout
cd nightscout
npm start

# Terminal 2: Start GlyWatch API
cd glywatch-fullstack/backend
python main.py
```

## 🧪 **Testing the System**

### **Test 1: Check Services**
```bash
# Test Nightscout
curl http://localhost:1337/api/v1/status.json

# Test GlyWatch API
curl http://localhost:8000/health
```

### **Test 2: Register a User**
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_123",
    "user_email": "test@example.com",
    "cgm_type": "Dexcom G6"
  }'
```

### **Test 3: Get User Status**
```bash
curl http://localhost:8000/users/test_user_123/status
```

### **Test 4: Get Glucose Data**
```bash
curl http://localhost:8000/cgm/latest/test_user_123
```

## 📱 **For Your Users**

### **User Registration Flow:**

1. **User visits GlyWatch**
2. **User registers with:**
   - Email
   - CGM device type (Dexcom G6, Medtronic, etc.)
   - Device ID (optional)

3. **GlyWatch automatically:**
   - Creates Nightscout instance for user
   - Generates unique API secret
   - Stores configuration in Supabase

4. **User gets:**
   - Nightscout URL: `http://localhost:1337/user_123`
   - API Secret for their instance
   - Instructions to set up CGM uploader

### **User Data Flow:**

```
User's CGM Device → Nightscout Instance → GlyWatch API → GlyWatch Frontend
```

## 🔧 **API Endpoints for Multi-User Support**

### **User Management:**
- `POST /users/register` - Register new user
- `GET /users/{user_id}/status` - Get user status
- `POST /users/{user_id}/start-nightscout` - Start user's Nightscout
- `GET /users/{user_id}/nightscout-config` - Get user's config

### **Glucose Data (per user):**
- `GET /cgm/latest/{user_id}` - Latest glucose for user
- `GET /cgm/history/{user_id}` - Glucose history for user
- `GET /cgm/device-status/{user_id}` - Device status for user

## 🎯 **Example User Journey**

### **1. User Registration:**
```javascript
// Frontend registration
const userData = {
  user_id: "john_doe_123",
  user_email: "john@example.com",
  cgm_type: "Dexcom G6",
  cgm_device_id: "DEXCOM123"
};

// Register user
const response = await fetch('/users/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(userData)
});

const result = await response.json();
// Result: { nightscout_url: "http://localhost:1337/john_doe_123", api_secret: "..." }
```

### **2. User Gets Their Data:**
```javascript
// Get user's glucose data
const glucoseData = await fetch(`/cgm/latest/john_doe_123`);
const data = await glucoseData.json();
// Data: { glucose: 125, trend: "stable", status: "normal" }
```

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **"Nightscout not responding"**
   - Check if Nightscout is running: `npm start` in nightscout directory
   - Check port 1337 is available

2. **"Supabase connection failed"**
   - Verify your Supabase URL and API keys
   - Check if tables are created in Supabase

3. **"User registration failed"**
   - Check if Supabase is configured correctly
   - Verify the user_nightscout_config table exists

### **Debug Commands:**
```bash
# Test Nightscout connection
curl http://localhost:1337/api/v1/status.json

# Test GlyWatch API
curl http://localhost:8000/health

# Test Supabase connection
python test_nightscout.py

# Test all endpoints
python test_all_endpoints.py
```

## 🚀 **Production Deployment**

For production, you'll want to:

1. **Deploy Nightscout instances** to a cloud service
2. **Use a proper database** (Supabase is fine)
3. **Set up proper authentication**
4. **Use HTTPS everywhere**
5. **Set up monitoring and logging**

## 📚 **Next Steps**

1. **Test the system** with the provided endpoints
2. **Integrate with your frontend** using the API
3. **Add user authentication** to secure the system
4. **Deploy to production** when ready

---

**🎉 You now have a complete GlyWatch system with local Nightscout and Supabase!**

Your users can register, get their own Nightscout instances, and access their CGM data through your GlyWatch application. 