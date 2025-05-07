from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

api_id = 20429011
api_hash = "a090311053eeed80fa3c62ab10999fb3"
session_string = "BQE3uNMAIzBxpbMjCofMHKoiSy2sS6WHqegGNOXbGWJAeZolBWeQl0pnnDX1Yam9Ym4XOi-IecEX0O2bupf5R6JVOJNEifsItgS9u726JOyG4rM2El5wqLL60IGGK4tZJR0rAUxtDeTtdaWaUAnbUedustBPPVcD6XR_uib5y4dAB2bu9zyNkQdWAlDBKVVSPeHVC5smUedDvl2nJic5UwWPqKNwnXtCi2iHcv5Rfpoq28nFWJCEYLE5ytYa9yBvY6Sjh1wc5qb7qAPG6auygdqD_ZSWdVX6W5tqfAFt0mcMOOy2Q33uL54OZXQcSMbTyAFJk8AcVFUvV9CEWa4zGl37RRgXdQAAAAHAZhJ9AA"

app = Client(
    name="Purge", api_id=api_id, api_hash=api_hash, session_string=session_string
)

SUDO_USERS = [7862043458, 8091116698]  


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
