# Complete GlyWatch Setup & Testing Guide

This comprehensive guide covers the complete setup of GlyWatch with Nightscout integration and Supabase database persistence, including testing of all endpoints.

## 📋 Overview

The updated GlyWatch system now includes:
- ✅ Nightscout integration for real-time CGM data
- ✅ Supabase database for data persistence
- ✅ Automatic data synchronization
- ✅ Comprehensive API endpoints
- ✅ Complete testing suite

## 🚀 Step-by-Step Setup

### Step 1: Install Dependencies

```bash
cd glywatch-fullstack/backend
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Run the interactive setup script:
```bash
python setup_env.py
```

This will guide you through configuring:
- Nightscout URL and API secret
- Supabase URL and API keys
- Connection timeouts

### Step 3: Set Up Supabase Database

1. **Create a Supabase project:**
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Note your project URL and API keys

2. **Create the database tables:**
   - Open your Supabase dashboard
   - Go to SQL Editor
   - Copy and paste the contents of `supabase_tables.sql`
   - Run the SQL commands

3. **Get your API keys:**
   - Go to Settings → API
   - Copy your project URL and anon key
   - Optionally copy your service key for admin operations

### Step 4: Test Connections

Test both Nightscout and Supabase connections:
```bash
python test_nightscout.py
```

Expected output:
```
✅ Connection Successful!
   Nightscout Version: 14.2.6
   Server Time: 2024-01-01T10:15:00.000Z

🔬 Testing Glucose Data Retrieval...
✅ Glucose Data Retrieved Successfully!
   Glucose: 125 mg/dL
   Trend: stable
   Status: normal

📱 Testing Device Status...
✅ Device Status Retrieved Successfully!
   Device Connected: True
   Device Name: Dexcom G6
```

### Step 5: Start the API Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### Step 6: Test All API Endpoints

Run the comprehensive test suite:
```bash
python test_all_endpoints.py
```

This will test all endpoints and provide detailed results.

## 🔧 Available API Endpoints

### Connection Testing
- `GET /health` - Basic health check
- `GET /cgm/test-connection` - Test Nightscout connection
- `GET /cgm/test-db-connection` - Test Supabase connection
- `GET /cgm/test-all-connections` - Test both connections

### Glucose Data
- `GET /cgm/latest/{patient_id}` - Get latest glucose from Nightscout + store in DB
- `GET /cgm/latest-db/{patient_id}` - Get latest glucose from database only
- `GET /cgm/history/{patient_id}?hours=24` - Get glucose history from Nightscout + store in DB
- `GET /cgm/history-db/{patient_id}?hours=24` - Get glucose history from database only

### Device Status
- `GET /cgm/device-status/{patient_id}` - Get device status from Nightscout + store in DB
- `GET /cgm/device-status` - Get general device status

### Treatments
- `GET /cgm/treatments/{patient_id}?hours=24` - Get treatments from Nightscout + store in DB

### Other Endpoints
- `GET /cgm/readings` - General glucose readings
- `GET /cgm/current` - Current reading
- `GET /cgm/history?days=7` - General history
- `POST /cgm/calibrate` - Sensor calibration

## 🧪 Testing Each Endpoint

### 1. Test Connection Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Test Nightscout connection
curl http://localhost:8000/cgm/test-connection

# Test Supabase connection
curl http://localhost:8000/cgm/test-db-connection

# Test all connections
curl http://localhost:8000/cgm/test-all-connections
```

### 2. Test Glucose Endpoints

```bash
# Get latest glucose (stores in DB)
curl http://localhost:8000/cgm/latest/test_patient_123

# Get latest glucose from database only
curl http://localhost:8000/cgm/latest-db/test_patient_123

# Get glucose history (stores in DB)
curl http://localhost:8000/cgm/history/test_patient_123?hours=24

# Get glucose history from database only
curl http://localhost:8000/cgm/history-db/test_patient_123?hours=24
```

### 3. Test Device Status Endpoints

```bash
# Get device status (stores in DB)
curl http://localhost:8000/cgm/device-status/test_patient_123

# Get general device status
curl http://localhost:8000/cgm/device-status
```

### 4. Test Treatment Endpoints

```bash
# Get treatments (stores in DB)
curl http://localhost:8000/cgm/treatments/test_patient_123?hours=24
```

### 5. Test Other Endpoints

```bash
# General readings
curl http://localhost:8000/cgm/readings

# Current reading
curl http://localhost:8000/cgm/current

# General history
curl http://localhost:8000/cgm/history?days=7

# Calibrate sensor
curl -X POST http://localhost:8000/cgm/calibrate
```

## 📊 Database Schema

### Glucose Readings Table
```sql
CREATE TABLE glucose_readings (
    id BIGSERIAL PRIMARY KEY,
    patient_id VARCHAR(255) NOT NULL,
    glucose INTEGER NOT NULL,
    timestamp TIMESTAMPTZ,
    trend VARCHAR(50),
    status VARCHAR(50),
    raw INTEGER,
    filtered INTEGER,
    noise INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Device Status Table
```sql
CREATE TABLE device_status (
    id BIGSERIAL PRIMARY KEY,
    patient_id VARCHAR(255) NOT NULL,
    device_connected BOOLEAN DEFAULT FALSE,
    battery_level INTEGER,
    signal_strength VARCHAR(50),
    device_name VARCHAR(255),
    last_communication TIMESTAMPTZ,
    pump_status JSONB,
    loop_status JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Treatments Table
```sql
CREATE TABLE treatments (
    id BIGSERIAL PRIMARY KEY,
    patient_id VARCHAR(255) NOT NULL,
    treatment_type VARCHAR(100),
    timestamp TIMESTAMPTZ,
    insulin DECIMAL(5,2),
    carbs INTEGER,
    notes TEXT,
    entered_by VARCHAR(255),
    raw_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🔍 Expected API Responses

### Successful Glucose Response
```json
{
  "patient_id": "test_patient_123",
  "glucose": 125,
  "timestamp": "2024-01-01T10:15:00.000Z",
  "trend": "stable",
  "status": "normal",
  "raw": 125000,
  "filtered": 125000,
  "noise": 1,
  "storage_result": {
    "success": true,
    "id": 1,
    "message": "Glucose reading stored successfully"
  }
}
```

### Successful Device Status Response
```json
{
  "patient_id": "test_patient_123",
  "device_connected": true,
  "battery_level": 85,
  "signal_strength": "strong",
  "device_name": "Dexcom G6",
  "last_communication": "2024-01-01T10:15:00.000Z",
  "pump_status": {},
  "loop_status": {},
  "storage_result": {
    "success": true,
    "id": 1,
    "message": "Device status stored successfully"
  }
}
```

### Connection Test Response
```json
{
  "connected": true,
  "status": "success",
  "nightscout_version": "14.2.6",
  "server_time": "2024-01-01T10:15:00.000Z",
  "base_url": "https://your-nightscout.herokuapp.com"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **"Connection refused"**
   - Make sure the server is running: `python main.py`
   - Check if port 8000 is available

2. **"Nightscout connection failed"**
   - Verify your Nightscout URL is correct
   - Check if your Nightscout instance is running
   - Verify API secret if required

3. **"Supabase connection failed"**
   - Check your Supabase URL and API keys
   - Ensure tables are created in Supabase
   - Verify your Supabase project is active

4. **"No data available"**
   - Check if your CGM device is connected
   - Verify Nightscout is receiving data
   - Check your CGM uploader is working

### Debugging Steps

1. **Check environment variables:**
   ```bash
   python -c "import os; print('NIGHTSCOUT_URL:', os.getenv('NIGHTSCOUT_URL')); print('SUPABASE_URL:', os.getenv('SUPABASE_URL'))"
   ```

2. **Test individual services:**
   ```bash
   python test_nightscout.py
   ```

3. **Check server logs:**
   - Look for error messages in the console
   - Check the detailed test results: `api_test_results.json`

4. **Verify database tables:**
   - Go to your Supabase dashboard
   - Check if tables exist and have data

## 📈 Performance Monitoring

The system includes performance monitoring:

- Response time tracking
- Success/failure rates
- Data storage statistics
- Connection status monitoring

Check the test results for performance metrics:
```bash
python test_all_endpoints.py
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` files to version control
2. **API Keys**: Keep your Supabase keys secure
3. **Row Level Security**: Consider enabling RLS in Supabase for production
4. **HTTPS**: Always use HTTPS in production
5. **Rate Limiting**: Be mindful of API rate limits

## 🚀 Production Deployment

For production deployment:

1. **Set up proper environment variables**
2. **Enable Row Level Security in Supabase**
3. **Use HTTPS endpoints**
4. **Set up monitoring and logging**
5. **Configure backup strategies**
6. **Set up proper error handling**

## 📚 Additional Resources

- [Nightscout Documentation](https://nightscout.github.io/)
- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**🎉 Your GlyWatch API is now fully set up with Nightscout integration and Supabase persistence!** 