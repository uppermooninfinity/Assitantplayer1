#!/usr/bin/env python3
"""
Generate Pyrogram String Session
Run this script to generate a string session for the assistant account.
"""

from pyrogram import Client

print("Welcome to String Session Generator")
print("=" * 50)

API_ID = input("Enter your API_ID: ")
API_HASH = input("Enter your API_HASH: ")

if not API_ID or not API_HASH:
    print("Error: API_ID and API_HASH are required!")
    exit(1)

try:
    with Client(
        name="session_generator",
        api_id=int(API_ID),
        api_hash=API_HASH,
        in_memory=True
    ) as app:
        session_string = app.export_session_string()

        print("\n" + "=" * 50)
        print("Your String Session:")
        print("=" * 50)
        print(session_string)
        print("=" * 50)
        print("\nSave this string session in your .env file as STRING_SESSION")
        print("Keep it secure and never share it with anyone!")

except Exception as e:
    print(f"\nError: {e}")
    print("\nMake sure you:")
    print("1. Entered correct API_ID and API_HASH")
    print("2. Have pyrogram installed (pip install pyrogram TgCrypto)")
    print("3. Have a stable internet connection")
