# Nightscout Integration Setup Guide

This guide will help you set up and test the Nightscout integration for your GlyWatch application.

## 🌙 What is Nightscout?

Nightscout is an open-source web application that allows real-time access to CGM (Continuous Glucose Monitor) data. It provides a REST API that your application can use to retrieve glucose readings, device status, and treatment data.

## 📋 Prerequisites

1. **Nightscout Instance**: You need a running Nightscout instance
2. **API Access**: Your Nightscout instance must allow API access
3. **API Secret** (optional): Some Nightscout instances require authentication

## 🚀 Step-by-Step Setup

### Step 1: Get Your Nightscout URL

1. **If you already have a Nightscout instance:**
   - Your URL will be something like: `https://your-nightscout.herokuapp.com`
   - Or: `https://your-nightscout.netlify.app`
   - Or: `https://your-nightscout.azurewebsites.net`

2. **If you don't have a Nightscout instance:**
   - Visit [Nightscout Foundation](https://nightscout.github.io/)
   - Follow their setup guide to create your own instance
   - Common hosting options: Heroku, Netlify, Azure, or self-hosted

### Step 2: Get Your API Secret (if required)

1. **Check if your Nightscout requires authentication:**
   - Visit your Nightscout URL in a browser
   - If it asks for a password, you'll need an API secret

2. **Find your API secret:**
   - In your Nightscout configuration (usually in environment variables)
   - Common variable names: `API_SECRET`, `NIGHTSCOUT_API_SECRET`
   - If you set up Nightscout yourself, you should know this value

3. **Test API access:**
   - Try visiting: `https://your-nightscout-url.herokuapp.com/api/v1/status.json`
   - If it returns JSON data, no authentication is needed
   - If it returns an error, you need to include the API secret

### Step 3: Configure Environment Variables

1. **Create a `.env` file in the backend directory:**
   ```bash
   cd glywatch-fullstack/backend
   ```

2. **Add your Nightscout configuration:**
   ```env
   # Required: Your Nightscout URL
   NIGHTSCOUT_URL=https://your-nightscout-instance.herokuapp.com
   
   # Optional: API Secret (if your instance requires it)
   NIGHTSCOUT_API_SECRET=your_api_secret_here
   
   # Optional: Timeout in seconds (default: 30)
   NIGHTSCOUT_TIMEOUT=30
   ```

3. **Load the environment variables:**
   ```bash
   # On Windows (PowerShell):
   $env:NIGHTSCOUT_URL="https://your-nightscout-instance.herokuapp.com"
   $env:NIGHTSCOUT_API_SECRET="your_api_secret_here"
   
   # On Windows (Command Prompt):
   set NIGHTSCOUT_URL=https://your-nightscout-instance.herokuapp.com
   set NIGHTSCOUT_API_SECRET=your_api_secret_here
   
   # On Linux/Mac:
   export NIGHTSCOUT_URL=https://your-nightscout-instance.herokuapp.com
   export NIGHTSCOUT_API_SECRET=your_api_secret_here
   ```

### Step 4: Test the Connection

1. **Run the test script:**
   ```bash
   cd glywatch-fullstack/backend
   python test_nightscout.py
   ```

2. **Expected output if successful:**
   ```
   🌙 Nightscout Connection Test
   ==================================================
   
   🔍 Testing Nightscout Connection...
   ==================================================
   📋 Configuration Status:
      Base URL: https://your-nightscout-instance.herokuapp.com
      API Secret Configured: True
      Timeout: 30 seconds
      Properly Configured: True
   
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
   
   ==================================================
   🎉 All tests completed successfully!
      Your Nightscout integration is working properly.
   ```

### Step 5: Start Your API Server

1. **Install dependencies (if not already done):**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server:**
   ```bash
   python main.py
   ```

3. **Test the API endpoints:**
   - Open your browser to: `http://localhost:8000/docs`
   - This will show the interactive API documentation
   - Test the `/cgm/test-connection` endpoint first

## 🔧 API Endpoints

Once your server is running, you can test these endpoints:

### Test Connection
```bash
curl http://localhost:8000/cgm/test-connection
```

### Get Latest Glucose
```bash
curl http://localhost:8000/cgm/latest/patient123
```

### Get Glucose History
```bash
curl http://localhost:8000/cgm/history/patient123?hours=24
```

### Get Device Status
```bash
curl http://localhost:8000/cgm/device-status/patient123
```

### Get Treatments
```bash
curl http://localhost:8000/cgm/treatments/patient123?hours=24
```

## 🐛 Troubleshooting

### Connection Issues

1. **"Unable to connect to Nightscout server"**
   - Check your Nightscout URL is correct
   - Verify your Nightscout instance is running
   - Try accessing the URL in your browser

2. **"HTTP error: 401"**
   - Your Nightscout requires authentication
   - Set the `NIGHTSCOUT_API_SECRET` environment variable

3. **"HTTP error: 403"**
   - API access might be disabled on your Nightscout instance
   - Check your Nightscout configuration

4. **"Connection timeout"**
   - Your Nightscout instance might be slow
   - Increase the timeout: `NIGHTSCOUT_TIMEOUT=60`

### Data Issues

1. **"No glucose data available"**
   - Your CGM device might not be connected
   - Check if your Nightscout is receiving data
   - Verify your CGM uploader is working

2. **"No device status available"**
   - Your pump/CGM might not be reporting status
   - This is normal for some setups

## 📊 Understanding the Data

### Glucose Readings
- `glucose`: Current glucose value in mg/dL
- `trend`: Direction of glucose change (rising, falling, stable, etc.)
- `status`: Categorized as low (<70), normal (70-180), or high (>180)
- `raw`: Raw sensor value
- `filtered`: Filtered sensor value
- `noise`: Noise level indicator

### Device Status
- `device_connected`: Whether the device is connected
- `battery_level`: Battery percentage
- `device_name`: Name of the connected device
- `last_communication`: Last time device reported

### Treatments
- Insulin doses
- Carbohydrate intake
- Exercise events
- Other diabetes-related events

## 🔒 Security Notes

1. **API Secret**: Keep your API secret secure and don't commit it to version control
2. **HTTPS**: Always use HTTPS URLs for production
3. **Rate Limiting**: Be mindful of API rate limits
4. **Data Privacy**: Ensure you have permission to access the Nightscout data

## 📚 Additional Resources

- [Nightscout Documentation](https://nightscout.github.io/)
- [Nightscout API Reference](https://nightscout.github.io/api/)
- [Nightscout Setup Guide](https://nightscout.github.io/website/)

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your Nightscout instance is working in a browser
3. Test the API directly: `https://your-nightscout-url/api/v1/status.json`
4. Check your Nightscout logs for errors
5. Ensure your environment variables are set correctly

---

**Happy coding! 🌙✨** 