"""Pasarela clásica hacia el detector cuántico: pertenece a App A, NO a la plataforma."""
import os
import httpx
from fastapi import FastAPI, HTTPException, Request
from qos_faults import FaultProfile
fault_profile = FaultProfile()
app = FastAPI(title='Hybrid application gateway')
QPU_URL = os.getenv('QPU_URL', 'http://groveralg0:8080').rstrip('/')
@app.get('/health')
def health(): return {'status': 'ok'}
@app.get('/metrics')
def metrics(): return fault_profile.decorate({'status': 'ok', 'execution_time': 10, 'response_time_ms': 70, 'availability': 24, 'reliability': 0.08, 'cost': 0.12})
@app.post('/detect')
async def detect(request: Request):
    try:
        async with httpx.AsyncClient(timeout=120, trust_env=False) as client:
            response = await client.post(QPU_URL + '/detect', content=await request.body(), headers={'Content-Type':'application/json'})
        if response.is_error:
            raise HTTPException(503, f'Quantum component: {response.status_code}')
        return response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(503, str(exc)) from exc


@app.post('/admin/simulate')
def inject_qos_fault(payload: dict):
    """Modifica TEMPORALMENTE métricas expuestas por este contenedor real."""
    from fastapi import HTTPException
    try:
        return fault_profile.inject(payload)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
