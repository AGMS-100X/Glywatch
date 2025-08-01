-- Supabase Tables for GlyWatch Nightscout Integration
-- Run these SQL commands in your Supabase SQL Editor

-- Enable Row Level Security (RLS)
-- Note: You may want to customize RLS policies based on your security requirements

-- 1. Glucose Readings Table
CREATE TABLE IF NOT EXISTS glucose_readings (
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

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_glucose_readings_patient_id ON glucose_readings(patient_id);
CREATE INDEX IF NOT EXISTS idx_glucose_readings_created_at ON glucose_readings(created_at);
CREATE INDEX IF NOT EXISTS idx_glucose_readings_timestamp ON glucose_readings(timestamp);

-- 2. Device Status Table
CREATE TABLE IF NOT EXISTS device_status (
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

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_device_status_patient_id ON device_status(patient_id);
CREATE INDEX IF NOT EXISTS idx_device_status_created_at ON device_status(created_at);

-- 3. Treatments Table
CREATE TABLE IF NOT EXISTS treatments (
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

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_treatments_patient_id ON treatments(patient_id);
CREATE INDEX IF NOT EXISTS idx_treatments_created_at ON treatments(created_at);
CREATE INDEX IF NOT EXISTS idx_treatments_timestamp ON treatments(timestamp);

-- 4. User Nightscout Configuration Table
CREATE TABLE IF NOT EXISTS user_nightscout_config (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    nightscout_url VARCHAR(500),
    api_secret VARCHAR(255),
    cgm_type VARCHAR(100),
    cgm_device_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for user config
CREATE INDEX IF NOT EXISTS idx_user_nightscout_config_user_id ON user_nightscout_config(user_id);
CREATE INDEX IF NOT EXISTS idx_user_nightscout_config_status ON user_nightscout_config(status);

-- 5. Connection Logs Table (for debugging)
CREATE TABLE IF NOT EXISTS connection_logs (
    id BIGSERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL, -- 'nightscout' or 'supabase'
    status VARCHAR(50) NOT NULL, -- 'success', 'error', 'timeout'
    message TEXT,
    response_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for connection logs
CREATE INDEX IF NOT EXISTS idx_connection_logs_service_name ON connection_logs(service_name);
CREATE INDEX IF NOT EXISTS idx_connection_logs_created_at ON connection_logs(created_at);

-- 6. Data Sync Status Table
CREATE TABLE IF NOT EXISTS data_sync_status (
    id BIGSERIAL PRIMARY KEY,
    patient_id VARCHAR(255) NOT NULL,
    data_type VARCHAR(50) NOT NULL, -- 'glucose', 'device_status', 'treatments'
    last_sync_at TIMESTAMPTZ DEFAULT NOW(),
    records_synced INTEGER DEFAULT 0,
    sync_status VARCHAR(50) DEFAULT 'success', -- 'success', 'error', 'partial'
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for sync status
CREATE INDEX IF NOT EXISTS idx_data_sync_status_patient_id ON data_sync_status(patient_id);
CREATE INDEX IF NOT EXISTS idx_data_sync_status_data_type ON data_sync_status(data_type);

-- Enable Row Level Security (RLS) - Optional
-- Uncomment the following lines if you want to enable RLS

-- ALTER TABLE glucose_readings ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE device_status ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE treatments ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE user_nightscout_config ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE connection_logs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE data_sync_status ENABLE ROW LEVEL SECURITY;

-- Example RLS policies (customize based on your needs)
-- CREATE POLICY "Users can view their own glucose readings" ON glucose_readings
--     FOR SELECT USING (auth.uid()::text = patient_id);

-- CREATE POLICY "Users can insert their own glucose readings" ON glucose_readings
--     FOR INSERT WITH CHECK (auth.uid()::text = patient_id);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_glucose_readings_updated_at 
    BEFORE UPDATE ON glucose_readings 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_device_status_updated_at 
    BEFORE UPDATE ON device_status 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_treatments_updated_at 
    BEFORE UPDATE ON treatments 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_nightscout_config_updated_at 
    BEFORE UPDATE ON user_nightscout_config 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_data_sync_status_updated_at 
    BEFORE UPDATE ON data_sync_status 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing (optional)
-- INSERT INTO glucose_readings (patient_id, glucose, timestamp, trend, status) VALUES
-- ('test_patient', 125, NOW(), 'stable', 'normal'),
-- ('test_patient', 130, NOW() - INTERVAL '5 minutes', 'rising', 'normal'),
-- ('test_patient', 120, NOW() - INTERVAL '10 minutes', 'falling', 'normal');

-- INSERT INTO device_status (patient_id, device_connected, battery_level, device_name) VALUES
-- ('test_patient', true, 85, 'Dexcom G6');

-- INSERT INTO treatments (patient_id, treatment_type, insulin, carbs, notes) VALUES
-- ('test_patient', 'Meal Bolus', 5.0, 45, 'Lunch bolus');

-- INSERT INTO user_nightscout_config (user_id, user_email, nightscout_url, api_secret, cgm_type) VALUES
-- ('user_123', 'user@example.com', 'http://localhost:1337/user_123', 'glywatch_user_123_secret', 'Dexcom G6'); 