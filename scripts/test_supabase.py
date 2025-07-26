
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

def test_supabase_connection():
    """Test Supabase connection and storage access"""
    
    print("Testing Supabase connection...")
    print(f"URL: {SUPABASE_URL}")
    print(f"Key: {SUPABASE_KEY[:20]}...")
    
    try:
        # Initialize client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Client initialized successfully")
        
        # Test storage access
        buckets = supabase.storage.list_buckets()
        print(f"✅ Storage accessible, buckets: {buckets}")
        
        # Test if 'public' bucket exists
        public_bucket = None
        for bucket in buckets:
            if bucket.name == 'public':
                public_bucket = bucket
                break
        
        if public_bucket:
            print("✅ Public bucket found")
        else:
            print("❌ Public bucket not found, creating it...")
            # Try to create bucket
            try:
                result = supabase.storage.create_bucket('public', {'public': True})
                print(f"✅ Public bucket created: {result}")
            except Exception as e:
                print(f"❌ Failed to create bucket: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_supabase_connection()
