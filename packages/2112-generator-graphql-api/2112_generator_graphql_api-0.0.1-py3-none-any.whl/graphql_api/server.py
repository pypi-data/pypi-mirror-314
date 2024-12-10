from fastapi import FastAPI
from graphql import build_schema
from graphql.execution.executors.asyncio import AsyncioExecutor
from strawberry.fastapi import GraphQLRouter

# Import the GraphQL schema
from generated.schema import schema_str

# Build the schema
schema = build_schema(schema_str)

# FastAPI app
app = FastAPI()

# GraphQL endpoint
graphql_app = GraphQLRouter(schema, executor_class=AsyncioExecutor)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "GraphQL Python API is running"}