"""
Quick reset script for LearnMate system.
Run this if you encounter redirect loops or session issues.
"""
import os
import sys

def reset_system():
    """Reset database and clear Python cache."""
    print("Resetting LearnMate system...")
    
    # Remove database
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("✓ Database removed")
    
    # Remove Python cache
    import shutil
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            print(f"✓ Removed {os.path.join(root, '__pycache__')}")
    
    print("\n✓ System reset complete!")
    print("\nNext steps:")
    print("1. Run: python manage.py migrate")
    print("2. Run: python manage.py createsuperuser (optional)")
    print("3. Run: python manage.py runserver")
    print("4. Clear your browser cookies/cache")
    print("5. Open http://127.0.0.1:8000/ in a new incognito window")

if __name__ == '__main__':
    reset_system()

