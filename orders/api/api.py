# api.py
from datetime import datetime
from http import HTTPStatus          
from uuid import UUID, uuid4

from starlette.responses import Response
from starlette import status
from orders.app import app
from fastapi import APIRouter
from orders.api.schemas import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
    )
from fastapi import HTTPException
from typing import Optional

router = APIRouter()

ORDERS = []
order = {
    'id': 'ff0f1355-e821-4178-9567-550dec27a373',
    'status': 'delivered',
    'created': datetime.utcnow(),
    'updated': datetime.utcnow(),
    'order': [
        {
            'product': 'cappuccino',
            'size': 'medium',
            'quantity': 1
        }
    ]
}

@app.get('/orders', response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int] = None):
    if cancelled is None and limit is None:
        return {'orders': ORDERS}
    
    query_set = [order for order in ORDERS]
    
    if cancelled is not None:
        if cancelled:
            query_set = [
                order
                for order in query_set
                if order['status'] == 'cancelled'
            ]
        
        else: 
            query_set = [
                order
                for order in query_set
                if order['status'] != 'cancelled'
            ]
            
    if limit is not None and len(query_set) > limit:
        return {'orders': query_set[:limit]}
    return {'orders': query_set}


@app.post('/orders', 
          status_code=status.HTTP_201_CREATED,
          response_model=GetOrderSchema,
          )
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order['id'] = uuid4()
    order['created'] = datetime.utcnow()
    order['status'] = 'created'
    ORDERS.append(order)
    return order                     

@app.get('/orders/{order_id}')
def get_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            return order
        
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@app.put('/orders/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            return Response(status_code=HTTPStatus.NO_CONTENT.value) 
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order     
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )
    
@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )