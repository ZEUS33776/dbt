from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
from database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text  
app = FastAPI()

class QueryParams(BaseModel):
    metrics: List[str]
    dimensions: List[str]
    filters: Dict[str, str]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/query")
async def query_data(params: QueryParams, db: Session = Depends(get_db)):
    try:
        # Generate the SQL query
        dimension_clause = ", ".join(params.dimensions)
        metric_clause = ", ".join(params.metrics)
        
        # Create filter clause with proper SQL Server syntax
        filter_pairs = []
        for key, value in params.filters.items():
            if value.isdigit():
                filter_pairs.append(f"{key} = {value}")
            else:
                filter_pairs.append(f"{key} = '{value}'")
        
        filter_clause = " AND ".join(filter_pairs)

        # Construct the SQL query with schema specification
        query = text(f"""
        SELECT 
            {dimension_clause},
            {metric_clause}
        FROM 
            dbo.FactInternetSales isales
        JOIN 
            dbo.DimSalesTerritory st ON isales.SalesTerritoryKey = st.SalesTerritoryKey
        JOIN 
            dbo.DimProduct p ON isales.ProductKey = p.ProductKey
        JOIN 
            dbo.DimProductSubcategory psc ON p.ProductSubcategoryKey = psc.ProductSubcategoryKey
        JOIN 
            dbo.DimProductCategory pc ON psc.ProductCategoryKey = pc.ProductCategoryKey
        JOIN 
            dbo.DimDate d ON isales.OrderDateKey = d.DateKey
        WHERE 
            {filter_clause}
        GROUP BY 
            {dimension_clause}
        """)

        # Execute the query
        result = db.execute(query)
        
        # Convert result to list of dictionaries
        columns = result.keys()
        data = [dict(zip(columns, row)) for row in result.fetchall()]
        
        # Handle decimal serialization
        for row in data:
            for key, value in row.items():
                if hasattr(value, 'to_decimal'):
                    row[key] = float(value)
        
        return {"status": "success", "data": data}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing query: {str(e)}")