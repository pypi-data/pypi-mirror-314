from __future__ import annotations

from collections.abc import Sequence  # noqa: TC003
from typing import TYPE_CHECKING, Any, Literal

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from llmling.config.models import (
    CallableResource,
    CLIResource,
    ImageResource,
    PathResource,
    Resource,
    SourceResource,
    TextResource,
    ToolConfig,
)
from py2openai import OpenAIFunctionTool  # noqa: TC002
from pydantic import BaseModel
from pydantic.fields import Field

from mcp_server_llmling.log import get_logger
from mcp_server_llmling.transports.stdio import StdioServer


if TYPE_CHECKING:
    from mcp_server_llmling.server import LLMLingServer

# from mcp_server_llmling.ui import create_ui_app


logger = get_logger(__name__)


ComponentType = Literal["resource", "tool", "prompt"]


def create_app() -> FastAPI:
    """Create FastAPI application for config injection."""
    return FastAPI(
        title="LLMling Config Injection API",
        description="""
        API for hot-injecting configuration into running LLMling server.

        ## Features
        * Inject new resources
        * Update existing tools
        * Real-time configuration updates
        * WebSocket support for live updates

        ## WebSocket Interface
        Connect to `/ws` for real-time updates. The WebSocket interface supports:

        ### Message Types
        * update: Update components in real-time
        * query: Query current component status
        * error: Error reporting from client

        ### Message Format
        ```json
        {
            "type": "update|query|error",
            "data": {
                "resources": {...},
                "tools": {...}
            },
            "request_id": "optional-correlation-id"
        }
        ```

        ### Response Format
        ```json
        {
            "type": "success|error|update",
            "data": {...},
            "request_id": "correlation-id",
            "message": "optional status message"
        }
        ```
        """,
        version="1.0.0",
        openapi_tags=[
            {
                "name": "components",
                "description": "Server component operations (resources/tools/prompts)",
            },
            {"name": "config", "description": "Configuration management endpoints"},
        ],
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )


class ComponentResponse(BaseModel):
    """Response model for component operations."""

    status: Literal["success", "error"]
    message: str
    component_type: ComponentType
    name: str


class ConfigUpdate(BaseModel):
    """Model for config updates."""

    resources: dict[str, Resource] | None = Field(
        default=None, description="Resource updates"
    )
    tools: dict[str, ToolConfig] | None = Field(default=None, description="Tool updates")


class BulkUpdateResponse(BaseModel):
    """Response model for bulk updates."""

    results: list[ComponentResponse]
    summary: dict[str, int] = Field(default_factory=lambda: {"success": 0, "error": 0})


class ConfigUpdateRequest(BaseModel):
    """Request model for config updates."""

    resources: dict[str, Resource] | None = None
    tools: dict[str, ToolConfig] | None = None
    replace_existing: bool = Field(
        default=True, description="Whether to replace existing components"
    )


class WebSocketMessage(BaseModel):
    """Message format for WebSocket communication."""

    type: Literal["update", "query", "error"]
    data: ConfigUpdateRequest | dict[str, Any]
    request_id: str | None = None


class WebSocketResponse(BaseModel):
    """Response format for WebSocket communication."""

    type: Literal["success", "error", "update"]
    data: ComponentResponse | list[ComponentResponse] | dict[str, Any]
    request_id: str | None = None
    message: str | None = None


class ConfigInjectionServer:
    """FastAPI server for hot config injection."""

    def __init__(
        self,
        llm_server: LLMLingServer,
        host: str = "localhost",
        port: int = 8765,
    ) -> None:
        """Initialize server.

        Args:
            llm_server: The LLMling server instance
            host: Host to bind to
            port: Port to listen on
        """
        self.llm_server = llm_server
        self.host = host
        self.port = port
        self.app = create_app()
        # create_ui_app(self.app)
        self._setup_routes()
        self._server: Any = None  # uvicorn server instance

    def _setup_routes(self) -> None:
        """Set up API routes."""

        @self.app.post(
            "/inject-config",
            response_model=ComponentResponse,
            tags=["config"],
            summary="Inject new configuration",
            description="Inject new configuration into the running server.",
            responses={
                200: {
                    "description": "Configuration successfully injected",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "success",
                                "message": "Config injected successfully",
                                "component_type": "resource",
                                "name": "example_resource",
                            }
                        }
                    },
                },
                400: {"description": "Invalid configuration"},
            },
        )
        async def inject_config(config: dict[str, Any]) -> ComponentResponse:
            """Inject raw YAML configuration."""
            logger.debug("Received config: %s", config)
            try:
                # Update resources
                if resources := config.get("resources"):
                    logger.debug("Processing resources: %s", resources)
                    for name, resource in resources.items():
                        # Validate based on resource type
                        resource_type = resource.get("type")
                        logger.debug(
                            "Processing resource %s of type %s", name, resource_type
                        )
                        match resource_type:
                            case "path":
                                validated = PathResource.model_validate(resource)
                            case "text":
                                validated = TextResource.model_validate(resource)
                            case "cli":
                                validated = CLIResource.model_validate(resource)
                            case "source":
                                validated = SourceResource.model_validate(resource)
                            case "callable":
                                validated = CallableResource.model_validate(resource)
                            case "image":
                                validated = ImageResource.model_validate(resource)
                            case _:
                                msg = f"Unknown resource type: {resource_type}"
                                raise ValueError(msg)  # noqa: TRY301

                        self.llm_server.runtime.register_resource(
                            name, validated, replace=True
                        )
                        logger.debug("Resource %s registered", name)

                # Update tools
                if tools := config.get("tools"):
                    logger.debug("Processing tools: %s", tools)
                    for name, tool in tools.items():
                        logger.debug("Processing tool: %s", name)
                        validated = ToolConfig.model_validate(tool)
                        self.llm_server.runtime._tool_registry.register(
                            name, validated, replace=True
                        )
                        logger.debug("Tool %s registered", name)

                result = ComponentResponse(
                    status="success",
                    message="Config injected successfully",
                    component_type="tool",
                    name="yaml_injection",
                )
                logger.debug("Returning response: %s", result.model_dump())
            except Exception as e:
                logger.exception("Failed to inject config")
                raise HTTPException(status_code=400, detail=str(e)) from e
            else:
                return result

        @self.app.get(
            "/components",
            tags=["components"],
            summary="List all components",
            description="Get a list of all registered components grouped by type.",
            response_description="Dictionary containing arrays of component names",
            responses={
                200: {
                    "description": "List of all components",
                    "content": {
                        "application/json": {
                            "example": {
                                "resources": ["resource1", "resource2"],
                                "tools": ["tool1", "tool2"],
                                "prompts": ["prompt1", "prompt2"],
                            }
                        }
                    },
                }
            },
        )
        async def list_components() -> dict[str, Sequence[str]]:
            """List all registered components."""
            return {
                "resources": self.llm_server.runtime.list_resource_names(),
                "tools": self.llm_server.runtime.list_tool_names(),
                "prompts": self.llm_server.runtime.list_prompt_names(),
            }

        # Resource endpoints
        @self.app.post(
            "/resources/{name}",
            response_model=ComponentResponse,
            tags=["components"],
            summary="Add or update resource",
            description="""
            Register a new resource or update an existing one.
            Supports various resource types including path, text, CLI, source,
            callable, and image.
            """,
            responses={
                200: {"description": "Resource successfully registered"},
                400: {"description": "Invalid resource configuration"},
            },
        )
        async def add_resource(name: str, resource: Resource) -> ComponentResponse:
            """Add or update a resource."""
            try:
                self.llm_server.runtime.register_resource(name, resource, replace=True)
                return ComponentResponse(
                    status="success",
                    message=f"Resource {name} registered",
                    component_type="resource",
                    name=name,
                )
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e)) from e

        @self.app.get(
            "/resources",
            tags=["components"],
            summary="List all resources",
            description="Get a list of all registered resources with their full config.",
            responses={
                200: {
                    "description": "Dictionary of resources",
                    "content": {
                        "application/json": {
                            "example": {
                                "resource1": {
                                    "type": "text",
                                    "content": "Example content",
                                },
                                "resource2": {"type": "path", "path": "/example/path"},
                            }
                        }
                    },
                }
            },
        )
        async def list_resources() -> dict[str, Resource]:
            """List all resources with their configuration."""
            return {
                name: self.llm_server.runtime._resource_registry[name]
                for name in self.llm_server.runtime.list_resource_names()
            }

        @self.app.delete(
            "/resources/{name}",
            response_model=ComponentResponse,
            tags=["components"],
            summary="Remove resource",
            description="Remove a registered resource by name.",
            responses={
                200: {"description": "Resource successfully removed"},
                404: {"description": "Resource not found"},
            },
        )
        async def remove_resource(name: str) -> ComponentResponse:
            """Remove a resource."""
            try:
                del self.llm_server.runtime._resource_registry[name]
                return ComponentResponse(
                    status="success",
                    message=f"Resource {name} removed",
                    component_type="resource",
                    name=name,
                )
            except KeyError as e:
                raise HTTPException(
                    status_code=404, detail=f"Resource {name} not found"
                ) from e

        # Tool endpoints
        @self.app.post(
            "/tools/{name}",
            response_model=ComponentResponse,
            tags=["components"],
            summary="Add or update tool",
            description="Register a new tool or update an existing one.",
            responses={
                200: {"description": "Tool successfully registered"},
                400: {"description": "Invalid tool configuration"},
            },
        )
        async def add_tool(name: str, tool: ToolConfig) -> ComponentResponse:
            """Add or update a tool."""
            try:
                self.llm_server.runtime._tool_registry.register(name, tool, replace=True)
                return ComponentResponse(
                    status="success",
                    message=f"Tool {name} registered",
                    component_type="tool",
                    name=name,
                )
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e)) from e

        @self.app.get(
            "/tools",
            tags=["components"],
            summary="List all tools",
            description="Get a list of all registered tools with their OpenAPI schemas.",
            responses={
                200: {
                    "description": "Dictionary of tools with their schemas",
                    "content": {
                        "application/json": {
                            "example": {
                                "tool1": {
                                    "name": "tool1",
                                    "description": "Example tool",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {},
                                    },
                                }
                            }
                        }
                    },
                },
                500: {"description": "Failed to get tool schemas"},
            },
        )
        async def list_tools() -> dict[str, OpenAIFunctionTool]:
            """List all tools with their OpenAPI schemas."""
            try:
                return {
                    name: tool.get_schema()
                    for name, tool in self.llm_server.runtime.tools.items()
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Failed to get tool schemas: {e}"
                ) from e

        @self.app.delete(
            "/tools/{name}",
            response_model=ComponentResponse,
            tags=["components"],
            summary="Remove tool",
            description="Remove a registered tool by name.",
            responses={
                200: {"description": "Tool successfully removed"},
                404: {"description": "Tool not found"},
            },
        )
        async def remove_tool(name: str) -> ComponentResponse:
            """Remove a tool."""
            try:
                del self.llm_server.runtime._tool_registry[name]
                return ComponentResponse(
                    status="success",
                    message=f"Tool {name} removed",
                    component_type="tool",
                    name=name,
                )
            except KeyError as e:
                raise HTTPException(
                    status_code=404, detail=f"Tool {name} not found"
                ) from e

        # Bulk update endpoint
        @self.app.post(
            "/bulk-update",
            response_model=BulkUpdateResponse,
            tags=["config"],
            summary="Bulk update components",
            description="""
            Update multiple components in a single request.

            This endpoint allows you to register multiple resources and tools at once.
            Failed operations will be reported in the response but won't affect others.
            """,
            responses={
                200: {
                    "description": "Bulk update results",
                    "content": {
                        "application/json": {
                            "example": {
                                "results": [
                                    {
                                        "status": "success",
                                        "message": "Resource registered",
                                        "component_type": "resource",
                                        "name": "example",
                                    }
                                ],
                                "summary": {"success": 1, "error": 0},
                            }
                        }
                    },
                },
            },
        )
        async def bulk_update(request: ConfigUpdateRequest) -> BulkUpdateResponse:
            """Update multiple components at once."""
            responses: list[ComponentResponse] = []
            summary = {"success": 0, "error": 0}

            if request.resources:
                for name, resource in request.resources.items():
                    try:
                        self.llm_server.runtime.register_resource(
                            name, resource, replace=request.replace_existing
                        )
                        response = ComponentResponse(
                            status="success",
                            message=f"Resource {name} registered",
                            component_type="resource",
                            name=name,
                        )
                        responses.append(response)
                        summary["success"] += 1
                    except Exception as e:  # noqa: BLE001
                        response = ComponentResponse(
                            status="error",
                            message=str(e),
                            component_type="resource",
                            name=name,
                        )
                        responses.append(response)
                        summary["error"] += 1

            if request.tools:
                for name, tool in request.tools.items():
                    try:
                        self.llm_server.runtime._tool_registry.register(
                            name, tool, replace=request.replace_existing
                        )
                        response = ComponentResponse(
                            status="success",
                            message=f"Tool {name} registered",
                            component_type="tool",
                            name=name,
                        )
                        responses.append(response)
                        summary["success"] += 1
                    except Exception as e:  # noqa: BLE001
                        response = ComponentResponse(
                            status="error",
                            message=str(e),
                            component_type="tool",
                            name=name,
                        )
                        responses.append(response)
                        summary["error"] += 1

            return BulkUpdateResponse(results=responses, summary=summary)

        # WebSocket endpoint
        @self.app.websocket(
            "/ws",
            name="component_updates",
            dependencies=None,
        )
        async def websocket_endpoint(websocket: WebSocket) -> None:
            """Handle WebSocket connections."""
            await websocket.accept()
            try:
                while True:
                    raw_data = await websocket.receive_json()
                    try:
                        message = WebSocketMessage.model_validate(raw_data)
                        match message.type:
                            case "update":
                                if isinstance(message.data, dict):
                                    request = ConfigUpdateRequest.model_validate(
                                        message.data
                                    )
                                    response = await bulk_update(request)
                                    await websocket.send_json(
                                        WebSocketResponse(
                                            type="success",
                                            data=response.results,
                                            request_id=message.request_id,
                                            message="Components updated successfully",
                                        ).model_dump()
                                    )
                            case "query":
                                # Handle component queries
                                components = await list_components()
                                await websocket.send_json(
                                    WebSocketResponse(
                                        type="success",
                                        data=components,
                                        request_id=message.request_id,
                                    ).model_dump()
                                )
                            case "error":
                                logger.error("Client error: %s", message.data)
                    except Exception:
                        error_msg = "Operation failed"
                        logger.exception(error_msg)
                        await websocket.send_json(
                            WebSocketResponse(
                                type="error",
                                data={},
                                message=error_msg,
                                request_id=getattr(message, "request_id", None),
                            ).model_dump()
                        )
            except WebSocketDisconnect:
                logger.debug("WebSocket client disconnected")

    async def start(self) -> None:
        """Start FastAPI server in the same event loop."""
        if not isinstance(self.llm_server.transport, StdioServer):
            msg = "Config injection requires stdio transport"
            raise RuntimeError(msg)  # noqa: TRY004

        import uvicorn

        config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
        )
        self._server = uvicorn.Server(config)
        # Run in same event loop
        await self._server.serve()

    async def stop(self) -> None:
        """Stop FastAPI server."""
        if self._server:
            self._server.should_exit = True
            await self._server.shutdown()
            self._server = None


if __name__ == "__main__":

    async def main() -> None:
        import httpx

        async with httpx.AsyncClient() as client:
            # Add a single resource
            response = await client.post(
                "http://localhost:8765/resources/my_resource",
                json={"type": "text", "content": "Dynamic content"},
            )
            print(response.json())

            # Add a tool
            url = "http://localhost:8765/tools/my_tool"
            response = await client.post(url, json={"import_path": "myapp.tools.analyze"})
            print(response.json())

            # List all components
            components = await client.get("http://localhost:8765/components")
            print(components.json())

            # Bulk update
            response = await client.post(
                "http://localhost:8765/bulk-update",
                json={
                    "resources": {
                        "resource1": {"type": "text", "content": "Content 1"},
                        "resource2": {"type": "text", "content": "Content 2"},
                    },
                    "tools": {
                        "tool1": {"import_path": "myapp.tools.tool1"},
                        "tool2": {"import_path": "myapp.tools.tool2"},
                    },
                },
            )
            print(response.json())


if __name__ == "__main__":
    import asyncio

    from llmling import Config, RuntimeConfig

    from mcp_server_llmling.server import LLMLingServer

    async def main() -> None:
        # Create minimal config
        config = Config.model_validate({
            "global_settings": {},
            "resources": {"initial": {"type": "text", "content": "Initial resource"}},
        })

        async with RuntimeConfig.from_config(config) as runtime:
            server = LLMLingServer(
                runtime,
                transport="stdio",
                enable_injection=True,  # Enable our injection server
                injection_port=8765,
            )
            print("Starting server with injection endpoint at http://localhost:8765")
            await server.start(raise_exceptions=True)

    asyncio.run(main())
