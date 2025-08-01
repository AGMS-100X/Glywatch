# 🚀 Quick Start Guide

This guide will get you up and running with GlyWatch + Nightscout + Supabase in 10 minutes.

## ⚡ **Quick Setup (5 minutes)**

### **Step 1: Set up Supabase**
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to SQL Editor and run the contents of `supabase_tables.sql`
4. Go to Settings → Database and copy your connection string

### **Step 2: Run the Setup Script**
```bash
cd glywatch-fullstack/backend
python setup_complete_system.py
```

### **Step 3: Update Database Connection**
Edit `nightscout/.env` and replace:
```
MONGO_CONNECTION=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
```
With your actual Supabase connection string.

### **Step 4: Start Services**
```bash
# Terminal 1: Start Nightscout
cd nightscout
npm start

# Terminal 2: Start GlyWatch API
cd glywatch-fullstack/backend
python main.py
```

## 🧪 **Quick Test**

### **Test 1: Check if everything is running**
```bash
# Test Nightscout
curl http://localhost:1337/api/v1/status.json

# Test GlyWatch API
curl http://localhost:8000/health
```

### **Test 2: Register a user**
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_123",
    "user_email": "test@example.com",
    "cgm_type": "Dexcom G6"
  }'
```

### **Test 3: Get user's glucose data**
```bash
curl http://localhost:8000/cgm/latest/test_user_123
```

## 🎯 **What You Get**

✅ **Local Nightscout** running on `http://localhost:1337`  
✅ **GlyWatch API** running on `http://localhost:8000`  
✅ **Supabase Database** storing all data  
✅ **Multi-user support** - each user gets their own Nightscout instance  
✅ **Complete API** with all endpoints  

## 📱 **For Your Users**

When someone registers on GlyWatch:
1. **User provides**: Email, CGM device type
2. **GlyWatch creates**: Their own Nightscout instance
3. **User gets**: Unique Nightscout URL and API secret
4. **Data flows**: CGM → Nightscout → GlyWatch → User's dashboard

## 🔧 **API Endpoints**

- `POST /users/register` - Register new user
- `GET /users/{user_id}/status` - Get user status
- `GET /cgm/latest/{user_id}` - Latest glucose for user
- `GET /cgm/history/{user_id}` - Glucose history for user
- `GET /cgm/device-status/{user_id}` - Device status for user

## 🐛 **Common Issues**

### **"Nightscout not responding"**
- Check if Nightscout is running: `npm start` in nightscout directory
- Make sure you updated the database connection string in `.env`

### **"Supabase connection failed"**
- Verify your Supabase URL and API keys
- Check if tables are created in Supabase

### **"User registration failed"**
- Check if Supabase is configured correctly
- Verify the `user_nightscout_config` table exists

## 📚 **Next Steps**

1. **Test the system** with the provided endpoints
2. **Integrate with your frontend** using the API
3. **Add user authentication** to secure the system
4. **Deploy to production** when ready

---

**🎉 You now have a complete GlyWatch system running locally!** 