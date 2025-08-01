#!/usr/bin/env python3
"""
Update Supabase Connection String
"""

import os

def update_nightscout_env():
    """Update Nightscout .env file with Supabase connection string"""
    
    # Your Supabase connection string
    supabase_connection = "postgresql://postgres:$Glywatch@2103@db.kkxlmjfmjrtgiqyomzks.supabase.co:5432/postgres"
    
    # Nightscout .env file path
    env_file_path = "./nightscout/.env"
    
    if not os.path.exists(env_file_path):
        print("❌ Nightscout .env file not found!")
        print("   Please run the setup script first: python setup_complete_system.py")
        return False
    
    # Read the current .env file
    with open(env_file_path, "r") as f:
        env_content = f.read()
    
    # Update the connection string
    if "MONGO_CONNECTION=" in env_content:
        # Replace existing connection string
        env_content = env_content.replace(
            "MONGO_CONNECTION=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres",
            f"MONGO_CONNECTION={supabase_connection}"
        )
    elif "CUSTOMCONNSTR_mongo=" in env_content:
        # Replace MongoDB connection with PostgreSQL
        env_content = env_content.replace(
            "CUSTOMCONNSTR_mongo=mongodb://....",
            f"MONGO_CONNECTION={supabase_connection}"
        )
    else:
        # Add the connection string if not found
        env_content = f"MONGO_CONNECTION={supabase_connection}\n" + env_content
    
    # Write the updated content
    with open(env_file_path, "w") as f:
        f.write(env_content)
    
    print("✅ Updated Nightscout .env file with your Supabase connection string!")
    print(f"   Connection: {supabase_connection}")
    
    return True

if __name__ == "__main__":
    print("🔧 Updating Supabase Connection String")
    print("This will update the Nightscout .env file with your Supabase connection...")
    
    if update_nightscout_env():
        print("\n🎉 Connection string updated successfully!")
        print("\n📋 Next Steps:")
        print("1. Start Nightscout: cd nightscout && npm start")
        print("2. Start GlyWatch API: python main.py")
        print("3. Test the connection: curl http://localhost:1337/api/v1/status.json")
    else:
        print("\n❌ Failed to update connection string.") 