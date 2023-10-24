from fastapi import FastAPI, Request, Response, HTTPException
import httpx
from starlette.responses import Response

app = FastAPI()

@app.post("/api/{destination:path}/checkUser")
async def proxy_request(destination: str, request: Request):
    try:
        destination_url = f'http://{destination}/checkUser'

        content_length = int(request.headers.get('content-length', 0))
        post_data = await request.body()

        async with httpx.AsyncClient() as client:
            response = await client.post(destination_url, data=post_data, headers=dict(request.headers))

        return Response(content=response.content, status_code=response.status_code, headers=response.headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")     

@app.get("/api/{destination:path}")
async def redirect_request(destination: str, request: Request):
    try:
        destination_url = f'http://{destination}'

        async with httpx.AsyncClient() as client:
            response = await client.get(destination_url, params=request.query_params)

        return Response(content=response.content, status_code=response.status_code, headers=response.headers)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)