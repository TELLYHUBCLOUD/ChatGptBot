from aiohttp import web
from .route import routes

async def web_server():
    """
    Creates and configures a web server application.
    """
    try:
        # Define the maximum client request size (30 MB for file uploads or payloads)
        max_request_size = 30 * 1024 * 1024  # 30 MB
        web_app = web.Application(client_max_size=max_request_size)

        # Validate and add routes to the application
        if not isinstance(routes, (list, web.RouteTableDef)):
            raise TypeError("`routes` must be a list of aiohttp routes or an instance of web.RouteTableDef.")

        web_app.add_routes(routes)
        return web_app

    except Exception as e:
        # Log the error and re-raise it
        print(f"Error initializing web server: {e}")
        raise
