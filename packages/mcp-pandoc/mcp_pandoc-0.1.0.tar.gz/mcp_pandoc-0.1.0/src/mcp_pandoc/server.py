import asyncio
import pandoc
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

server = Server("mcp-pandoc")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available note resources.
    Each note is exposed as a resource with a custom note:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"note://internal/{name}"),
            name=f"Note: {name}",
            description=f"A simple note named {name}",
            mimeType="text/plain",
        )
        for name in notes
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific note's content by its URI.
    The note name is extracted from the URI host component.
    """
    if uri.scheme != "note":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    name = uri.path
    if name is not None:
        name = name.lstrip("/")
        return notes[name]
    raise ValueError(f"Note not found: {name}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="summarize-notes",
            description="Creates a summary of all notes",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="Style of the summary (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    The prompt includes all current notes and can be customized via arguments.
    """
    if name != "summarize-notes":
        raise ValueError(f"Unknown prompt: {name}")

    style = (arguments or {}).get("style", "brief")
    detail_prompt = " Give extensive details." if style == "detailed" else ""

    return types.GetPromptResult(
        description="Summarize the current notes",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                    + "\n".join(
                        f"- {name}: {content}"
                        for name, content in notes.items()
                    ),
                ),
            )
        ],
    )

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        # types.Tool(
        #     name="add-note",
        #     description="Add a new note",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "name": {"type": "string"},
        #             "content": {"type": "string"},
        #         },
        #         "required": ["name", "content"],
        #     },
        # ),
        # types.Tool(
        #     name="get-note",
        #     description="get existing note",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "name": {"type": "string"},
        #         },
        #         "required": ["name"],
        #     },
        # ),
        # types.Tool(
        #     name="convert-note-content",
        #     description="convert note content from text to given output format",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "name": {"type": "string"},
        #             "output_format": {"type": "string"},
        #         },
        #         "required": ["name", "output_format"],
        #     },
        # )
        types.Tool(
            name="convert-contents",
            description="Converts content between different formats. Transforms input content from any supported format into the specified output format. Supported output formats include HTML, Markdown, and PDF. Use this tool to seamlessly convert between different document and content representations while preserving formatting and structure.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contents": {"type": "string"},
                    "output_format": {"type": "string"},
                },
                "required": ["contents", "output_format"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:    
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name not in ["convert-contents"]:
        raise ValueError(f"Unknown tool: {name}")
    
    print(arguments)

    if not arguments:
        raise ValueError("Missing arguments")
    

    contents = arguments.get("contents")
    output_format = arguments.get("output_format", "").lower()
    
    # Validate required parameters
    if not contents:
        raise ValueError("Missing required parameter: 'contents'")
    if not output_format:
        raise ValueError("Missing required parameter: 'output_format'")
    
    # Validate supported output formats
    SUPPORTED_FORMATS = {'html', 'markdown'}
    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported output format: '{output_format}'. Supported formats are: {', '.join(SUPPORTED_FORMATS)}")
    
    try:
        # Convert content using Pandoc
        doc = pandoc.read(contents, format="markdown")
        converted_output = pandoc.write(doc, format=output_format)
        
        if not converted_output:
            raise ValueError(f"Conversion resulted in empty output")
        
        return [
            types.TextContent(
                type="text",
                text=converted_output
            )
        ]
        
    except Exception as e:
        # Handle Pandoc conversion errors
        error_msg = f"Error converting contents: '{contents}' to {output_format}: {str(e)}"
        raise ValueError(error_msg)

    # """
    # Handle tool execution requests.
    # Tools can modify server state and notify clients of changes.
    # """
    # if name not in ["add-note", "get-note", "convert-note-content"]:
    #     raise ValueError(f"Unknown tool: {name}")
    
    # # print(arguments)

    # if not arguments:
    #     raise ValueError("Missing arguments")


    
    # if name == "add-note":
    #     note_name = arguments.get("name")
    #     content = arguments.get("content") 
        
    #     if not note_name or not content:
    #         raise ValueError("Missing name or content")
        
    #     # Update server state
    #     notes[note_name] = content


    #     # Notify clients that resources have changed
    #     await server.request_context.session.send_resource_list_changed()
        
    #     return [
    #     types.TextContent(
    #         type="text",
    #         text=f"Added note '{note_name}' with content: {content}",
    #     )
    # ]
    # elif name == "get-note":
    #     note_name = arguments.get("name")

    #     if not note_name:
    #         raise ValueError("Missing name")
        
    #     content = notes.get(note_name, None) 
        
    #     if not content:
    #         raise ValueError(f'Could not get note for note name: {note_name}')
        
    #     return [
    #         types.TextContent(
    #             type="text",
    #             text=f"Got note '{note_name}' with content: {content}",
    #         )
    #     ]
    # elif name == "convert-note-content":
    #     note_name = arguments.get("name")
    #     output_format = arguments.get("output_format")

    #     if not (note_name or output_format):
    #         raise ValueError("Missing name or Output format")
        
    #     content = notes.get(note_name, None) 
    

    #     # Markdown text to convert
    #     markdown_text = content

    #     # Convert Markdown to a Pandoc document
    #     doc = pandoc.read(markdown_text, format="markdown")

    #     # Convert the document to HTML and print
    #     html_output = pandoc.write(doc, format=output_format)
    #     print(html_output)

        
    #     if not html_output:
    #         raise ValueError(f'Could not convert to html note: {note_name}, content: {content}')
        
    #     return [
    #         types.TextContent(
    #             type="text",
    #             text=f"Converted contents for note: {note_name} to html: {html_output}",
    #         )
    #     ]



async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-pandoc",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )