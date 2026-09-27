"""Shared MCP metadata: server instructions and tool safety annotations.

`ToolAnnotations` are MCP protocol hints (readOnlyHint, destructiveHint,
idempotentHint, openWorldHint) that tell MCP clients (Claude, ChatGPT, etc.)
which tools are safe to call autonomously and which need user confirmation.
"""

from mcp.types import ToolAnnotations

SERVER_INSTRUCTIONS = (
    "Use these tools to inspect and modify the user's Anki collection. "
    "Before adding a note, identify the target deck, note type, and required "
    "fields with get_deck_names, get_model_names, and get_model_field_names. "
    "If no existing note type fits, create one with create_model (fields plus "
    "Front/Back templates), or adjust an existing model with "
    "model_add_field / model_rename_field / model_reposition_field / "
    "model_remove_field — field removal loses that field's data in all notes, "
    "and template edits must keep at least one field replacement on the "
    "front. To edit card content, inspect its current fields and note ID with "
    "find_notes / get_notes_info, then call update_note_fields with only the "
    "fields the user requested; note edits affect all sibling cards, preserve "
    "supplied text and HTML verbatim, and remain local until sync is called. "
    "Store new binary media before referencing its filename in a field. The "
    "sync tool synchronizes collection data with AnkiWeb; wait for its final "
    "result before claiming synchronization completed. Full conflicts always "
    "download from AnkiWeb. Only perform state-changing operations when the "
    "user has requested them, and report returned IDs and failures. Import, "
    "export, and AnkiWeb sync interact with resources outside the collection; "
    "verify their paths, scope, and intended direction first."
)

READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

ADDITIVE_WRITE = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=False,
    openWorldHint=False,
)

IDEMPOTENT_WRITE = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

DESTRUCTIVE_WRITE = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=True,
    idempotentHint=False,
    openWorldHint=False,
)

DESTRUCTIVE_IDEMPOTENT_WRITE = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=True,
    idempotentHint=True,
    openWorldHint=False,
)

DESTRUCTIVE_OPEN_WORLD_WRITE = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=True,
    idempotentHint=False,
    openWorldHint=True,
)
