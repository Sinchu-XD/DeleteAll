from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

api_id = 22680309
api_hash = "0c4c469a75fa545063a0b3207efedfd2"
session_string = "BQFaEvUAlAy3bWP3U6arzYzsJQIEcWwetja6YEC--k8HvZ0tPAFp_YUu-CrvZoZN2gYaCgR7GCEN2oQXiLDyXhT6XB6QhdhogVffUgVbNKiwUv_mMl0cmJ_GkgpuH-cvdkFXm0Ab9yK6rWVUe8Vi8MUU8vYb2KvUsNvWSGTs-dZ0LGyLoJlixdyrKPYwszAHjM4v6o8Jj4u4WedNNhBFqvQav5S1hoRulVW0fOGQjniEcnYbSGykMgWV-KRjQoiOxnAtlFVat4jvcbMGitFJ0hiA500sJ8wqz7s0saGFu5d2xoLihCud4Hz-QN4Q-cX7IHlwAxsLjfec-ZjmrP0mP6QsBDYqcwAAAAHBtt-bAA"

app = Client(
    name="Purge", api_id=api_id, api_hash=api_hash, session_string=session_string
)

SUDO_USERS = [7862043458, 8091116698, 7544954779]  


@app.on_message(filters.command("purgeall"))
async def purge_all(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if user is authorized
    if user_id not in SUDO_USERS:
        return await message.reply("🚫 **Only Rex Bhadwa And Abhi Randi Use This Command**")

    if len(message.command) < 2:
        return await message.reply("❌ Please give a Chat ID or username.\nUsage: `/purgeall -1001234567890`", quote=True)

    chat_id = message.command[1]
    try:
        chat_id = int(chat_id)
    except ValueError:
        return await message.reply("❌ Invalid Chat ID.")

    await message.reply(f"🧹 Purging chat: `{chat_id}`...")

    deleted = 0
    failed = 0
    batch = []

    async for msg in client.get_chat_history(chat_id):
        batch.append(msg.id)
        if len(batch) == 100:
            try:
                await client.delete_messages(chat_id, batch)
                deleted += len(batch)
            except Exception as e:
                print(f"❌ Failed deleting batch: {e}")
                failed += len(batch)
            batch = []
            await asyncio.sleep(0.5)  # Reduce flood risk

    # Delete any remaining messages
    if batch:
        try:
            await client.delete_messages(chat_id, batch)
            deleted += len(batch)
        except Exception as e:
            print(f"❌ Final batch error: {e}")
            failed += len(batch)

    await message.reply(f"✅ Done!\nDeleted: {deleted}\nFailed: {failed}")

    # ✅ Console log with bot username
    me = await client.get_me()
    print(f"✅ Purged {deleted} messages from chat {chat_id} as @{me.username}")

print("✅ UserBot started...")

app.run()
