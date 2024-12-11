import os
import sys
import asyncio
import traceback
import aiohttp

MCP_HOST = os.getenv("MCP_HOST", "localhost")
MCP_PORT = os.getenv("MCP_PORT", "3000")
BASE_URL = f"http://{MCP_HOST}:{MCP_PORT}"
BACKEND_URL_SSE = f"{BASE_URL}/api/v1/mcp/sse"
BACKEND_URL_MSG = f"{BASE_URL}/api/v1/mcp/"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def debug(message):
    """Output debug messages to stderr."""
    if DEBUG:
        print(message, file=sys.stderr)

async def connect_sse_backend():
    """Establish persistent SSE connection to MCP server."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BACKEND_URL_SSE) as response:
                if response.status != 200:
                    raise Exception(f"SSE connection failed with status {response.status}")

                debug("--- SSE backend connected")

                # Read and process SSE messages
                async for line in response.content:
                    if line:
                        message = line.decode().strip()
                        debug(f"<-- {message}")
                        
                        if message.startswith("event: endpoint"):
                            # Next line will contain the endpoint data
                            continue
                        elif message.startswith("data: ") and message_endpoint is None:
                            # This is the endpoint data following "event: endpoint"
                            endpoint = message[6:]  # Strip "data: " prefix
                            message_endpoint = f"{BASE_URL}{endpoint}"
                            debug(f"Set message endpoint to: {message_endpoint}")
                        elif message.startswith("data: "):
                            data = message[6:]  # Strip "data: " prefix
                            print(data)  # Forward just the data portion
    except Exception as e:
        debug(f"--- SSE backend disc./error: {str(e)}")
        raise


async def process_message(session, message):
    """Forward received message to the MCP server."""
    if not message_endpoint:
        debug("No message endpoint set yet, dropping message")
        return
        
    debug(f"-->{message.strip()}")
    try:
        async with session.post(message_endpoint, data=message, headers={"Content-Type": "application/json"}) as resp:
            if resp.status != 202:
                debug(f"Unexpected response status: {resp.status}")
    except Exception as e:
        debug(f"fetch error: {e}")

async def run_bridge():
    """Run the bridge."""
    try:
        # Start the SSE connection in a background task
        asyncio.create_task(connect_sse_backend())

        async with aiohttp.ClientSession() as session:
            debug("-- MCP stdio to SSE gw running")

            # Read stdin synchronously using a ThreadPoolExecutor
            loop = asyncio.get_running_loop()

            def read_stdin_sync():
                return sys.stdin.read()

            while True:
                # Read a line synchronously from stdin
                message = await loop.run_in_executor(None, sys.stdin.readline)
                if not message:  # End of input
                    break
                await process_message(session, message.strip())
    except Exception as error:
        debug(f"Fatal error running server: {error}")
        trace = traceback.format_exc()
        debug(f"Traceback: {trace}")
        sys.exit(1)

def app():
    asyncio.run(run_bridge())

if __name__ == "__main__":
    asyncio.run(app())

