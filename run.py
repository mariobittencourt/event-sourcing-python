from src.ui.console.commands.manage_customer_payment_projection import *

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(import_stream())
    except KeyboardInterrupt:
        print('Bye')