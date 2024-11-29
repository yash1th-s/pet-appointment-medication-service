import logging
from fastapi import HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import httpx

AUTH_SERVICE_URL = "http://a487d8b00bc6542ca91c2dd298684952-1223040857.us-east-1.elb.amazonaws.com/verify-token"  

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        open_routes = ["/docs", "/openapi.json", "/redoc"]
        if any(request.url.path.startswith(route) for route in open_routes):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                content='{"detail": "Missing or invalid token"}',
                status_code=401,
                media_type="application/json"
            )

        token = auth_header.split(" ")[1]
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(AUTH_SERVICE_URL, json={"token": token})
                if response.status_code != 200:
                    return Response(
                        content='{"detail": "Unauthorized"}',
                        status_code=401,
                        media_type="application/json"
                    )
                
                user_data = response.json()  # Optional if user info is needed
                request.state.user = user_data  # Store the user info if required
        except httpx.RequestError as e:
            return Response(
                content=f'{{"detail": "Auth service unreachable: {e}"}}',
                status_code=500,
                media_type="application/json"
            )
        except Exception as e:
            return Response(
                content='{"detail": "Error validating token"}',
                status_code=500,
                media_type="application/json"
            )

        return await call_next(request)
