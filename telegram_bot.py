import asyncio
import os
from telethon import TelegramClient, events
from aiohttp import web

# Environment variables
API_ID = int(os.environ.get('API_ID', '34564214'))
API_HASH = os.environ.get('API_HASH', 'f3366498b42504fe7ef2198ebf2e0434')
TARGET_BOT = os.environ.get('TARGET_BOT', '@Tgnumberrrr_bot')
PORT = int(os.environ.get('PORT', 10000))  # Render default PORT

client = TelegramClient('user_master', API_ID, API_HASH)

async def handle_search(request):
    query = request.query.get('q', '')
    if not query:
        return web.json_response({"error": "No query provided"}, status=400)
    
    try:
        if not client.is_connected():
            await client.connect()
            
        async with client.conversation(TARGET_BOT, timeout=30) as conv:
            await conv.send_message(query)
            resp = await conv.get_response()
            
            final_text = ""
            if resp.buttons:
                for row in resp.buttons:
                    for button in row:
                        if 'Telegram' in button.text:
                            await button.click()
                            final_resp = await conv.get_response()
                            final_text = final_resp.text
            else:
                final_text = resp.text

            branded_result = f"{final_text}\n\n--- BY @RAJPUTTEAM101 ---"
            
            return web.json_response({
                "status": "success",
                "data": branded_result
            })
            
    except asyncio.TimeoutError:
        return web.json_response({"error": "Bot response timeout"}, status=504)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def health_check(request):
    return web.json_response({"status": "healthy"})

async def start_server():
    # Pehle client start karo
    await client.start()
    print("✅ Telegram client started!")
    
    # Web app banao
    app = web.Application()
    app.router.add_get('/search', handle_search)
    app.router.add_get('/health', health_check)  # Render ke liye health check
    app.router.add_get('/', lambda r: web.json_response({
        "message": "Telegram Number Bot API - BY @RAJPUTTEAM101",
        "usage": "/search?q=@username",
        "status": "running"
    }))
    
    # Server start karo
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', PORT).start()
    print(f"🚀 API LIVE on port {PORT}")
    print(f"📡 Health check: /health")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_server())
