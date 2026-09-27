"""Tests for MCP server functionality."""

import os
import tempfile

import pytest


@pytest.fixture
def api_wrapper():
    """Create an AnkiWrapper for API testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        collection_path = os.path.join(tmpdir, "test.anki2")
        media_path = collection_path + "-media"
        os.makedirs(media_path, exist_ok=True)

        from anki_connect_server.anki_wrapper import AnkiWrapper

        wrapper = AnkiWrapper(collection_path)

        yield wrapper

        wrapper.close()


@pytest.fixture(autouse=True)
def patch_api_wrapper(api_wrapper):
    """Patch the MCP server's internal wrapper for each test."""
    from anki_connect_server import mcp_server

    original = mcp_server.set_wrapper_for_test(api_wrapper)
    yield api_wrapper
    mcp_server.set_wrapper_for_test(original)


class TestMCPWrapper:
    """Test MCP wrapper functions using AnkiWrapper directly."""

    def test_get_deck_names(self):
        """Test get_deck_names MCP tool."""
        from anki_connect_server.mcp_server import get_deck_names

        result = get_deck_names()
        assert "Default" in result

    def test_get_deck_names_and_ids(self):
        """Test get_deck_names_and_ids MCP tool."""
        from anki_connect_server.mcp_server import get_deck_names_and_ids

        result = get_deck_names_and_ids()
        assert "Default" in result

    def test_create_deck(self):
        """Test create_deck MCP tool."""
        from anki_connect_server.mcp_server import create_deck

        deck_id = create_deck("MCPTestDeck")
        assert deck_id > 0

    def test_delete_decks(self):
        """Test delete_decks MCP tool."""
        from anki_connect_server.mcp_server import create_deck, delete_decks

        create_deck("ToDeleteMCP")
        result = delete_decks(["ToDeleteMCP"])
        assert result is True

    def test_get_model_names(self):
        """Test get_model_names MCP tool."""
        from anki_connect_server.mcp_server import get_model_names

        result = get_model_names()
        assert "Basic" in result

    def test_get_model_field_names(self):
        """Test get_model_field_names MCP tool."""
        from anki_connect_server.mcp_server import get_model_field_names

        result = get_model_field_names("Basic")
        assert "Front" in result
        assert "Back" in result

    def test_add_note(self):
        """Test add_note MCP tool."""
        from anki_connect_server.mcp_server import add_note

        note_id = add_note("Default", "Basic", {"Front": "Test", "Back": "Answer"})
        assert note_id is not None

    def test_find_notes(self):
        """Test find_notes MCP tool."""
        from anki_connect_server.mcp_server import add_note, find_notes

        add_note("Default", "Basic", {"Front": "FindMe", "Back": "Test"})
        result = find_notes("FindMe")
        assert len(result) > 0

    def test_get_notes_info(self):
        """Test get_notes_info MCP tool."""
        from anki_connect_server.mcp_server import add_note, get_notes_info

        note_id = add_note("Default", "Basic", {"Front": "Test", "Back": "Test"})
        assert note_id is not None
        result = get_notes_info([note_id])
        assert len(result) == 1
        assert result[0]["noteId"] == note_id

    def test_delete_notes(self):
        """Test delete_notes MCP tool."""
        from anki_connect_server.mcp_server import add_note, delete_notes

        note_id = add_note("Default", "Basic", {"Front": "ToDelete", "Back": "Test"})
        assert note_id is not None
        result = delete_notes([note_id])
        assert result is True

    def test_find_cards(self):
        """Test find_cards MCP tool."""
        from anki_connect_server.mcp_server import add_note, find_cards

        add_note("Default", "Basic", {"Front": "CardTest", "Back": "Test"})
        result = find_cards("CardTest")
        assert len(result) > 0

    def test_get_cards_info(self):
        """Test get_cards_info MCP tool."""
        from anki_connect_server.mcp_server import add_note, find_cards, get_cards_info

        add_note("Default", "Basic", {"Front": "Test", "Back": "Test"})
        card_ids = find_cards("Test")
        result = get_cards_info(card_ids)
        assert len(result) > 0

    def test_suspend_cards(self):
        """Test suspend_cards MCP tool."""
        from anki_connect_server.mcp_server import add_note, find_cards, suspend_cards

        add_note("Default", "Basic", {"Front": "SuspendMe", "Back": "Test"})
        card_ids = find_cards("SuspendMe")
        result = suspend_cards(card_ids)
        assert result is True

    def test_unsuspend_cards(self):
        """Test unsuspend_cards MCP tool."""
        from anki_connect_server.mcp_server import (
            add_note,
            find_cards,
            suspend_cards,
            unsuspend_cards,
        )

        add_note("Default", "Basic", {"Front": "UnsuspendMe", "Back": "Test"})
        card_ids = find_cards("UnsuspendMe")
        suspend_cards(card_ids)
        result = unsuspend_cards(card_ids)
        assert result is True

    def test_are_suspended(self):
        """Test are_suspended MCP tool."""
        from anki_connect_server.mcp_server import (
            add_note,
            are_suspended,
            find_cards,
            suspend_cards,
        )

        add_note("Default", "Basic", {"Front": "SuspendedCheck", "Back": "Test"})
        card_ids = find_cards("SuspendedCheck")
        suspend_cards(card_ids)
        result = are_suspended(card_ids)
        assert result[0] is True

    def test_are_due(self):
        """Test are_due MCP tool."""
        from anki_connect_server.mcp_server import add_note, are_due, find_cards

        add_note("Default", "Basic", {"Front": "DueCheck", "Back": "Test"})
        card_ids = find_cards("DueCheck")
        result = are_due(card_ids)
        assert len(result) == 1

    def test_get_card_intervals(self):
        """Test get_card_intervals MCP tool."""
        from anki_connect_server.mcp_server import add_note, find_cards, get_card_intervals

        add_note("Default", "Basic", {"Front": "IntervalTest", "Back": "Test"})
        card_ids = find_cards("IntervalTest")
        result = get_card_intervals(card_ids)
        assert len(result) == 1

    def test_get_all_tags(self):
        """Test get_all_tags MCP tool."""
        from anki_connect_server.mcp_server import get_all_tags

        result = get_all_tags()
        assert isinstance(result, list)

    def test_get_media_dir_path(self):
        """Test get_media_dir_path MCP tool."""
        from anki_connect_server.mcp_server import get_media_dir_path

        result = get_media_dir_path()
        assert result is not None

    def test_cards_to_notes(self):
        """Test cards_to_notes MCP tool."""
        from anki_connect_server.mcp_server import add_note, cards_to_notes, find_cards

        note_id = add_note("Default", "Basic", {"Front": "CardsToNotes", "Back": "Test"})
        card_ids = find_cards("CardsToNotes")
        result = cards_to_notes(card_ids)
        assert note_id in result

    def test_change_deck(self):
        """Test change_deck MCP tool."""
        from anki_connect_server.mcp_server import add_note, change_deck, create_deck, find_cards

        create_deck("MCPNewDeck")
        add_note("Default", "Basic", {"Front": "MoveMe", "Back": "Test"})
        card_ids = find_cards("MoveMe")
        result = change_deck(card_ids, "MCPNewDeck")
        assert result is True

    def test_get_deck_config(self):
        """Test get_deck_config MCP tool."""
        from anki_connect_server.mcp_server import get_deck_config

        result = get_deck_config("Default")
        assert isinstance(result, dict)

    def test_get_model_templates(self):
        """Test get_model_templates MCP tool."""
        from anki_connect_server.mcp_server import get_model_templates

        result = get_model_templates("Basic")
        assert "Card 1" in result

    def test_get_model_styling(self):
        """Test get_model_styling MCP tool."""
        from anki_connect_server.mcp_server import get_model_styling

        result = get_model_styling("Basic")
        assert "css" in result

    def test_create_model(self):
        """Test create_model MCP tool."""
        from anki_connect_server.mcp_server import (
            create_model,
            get_model_field_names,
            get_model_templates,
        )

        result = create_model(
            "MCPTestModel",
            ["Front", "Back", "Extra"],
            {"Card 1": {"Front": "{{Front}}", "Back": "{{Back}}"}},
            css=".card { color: blue; }",
        )
        assert result is True
        assert get_model_field_names("MCPTestModel") == ["Front", "Back", "Extra"]
        templates = get_model_templates("MCPTestModel")
        assert templates["Card 1"]["Front"] == "{{Front}}"

    def test_create_model_cloze(self):
        """Test create_model MCP tool with a cloze model."""
        from anki_connect_server.mcp_server import create_model

        result = create_model(
            "MCPClozeModel",
            ["Text"],
            {"Cloze": {"Front": "{{cloze:Text}}", "Back": "{{cloze:Text}}"}},
            is_cloze=True,
        )
        assert result is True

    def test_model_field_management(self):
        """Test model_add_field / model_rename_field / model_reposition_field /
        model_remove_field MCP tools."""
        from anki_connect_server.mcp_server import (
            get_model_field_names,
            model_add_field,
            model_remove_field,
            model_rename_field,
            model_reposition_field,
        )

        assert model_add_field("Basic", "MCPExtra") is True
        names = get_model_field_names("Basic")
        assert names[-1] == "MCPExtra"

        assert model_reposition_field("Basic", "MCPExtra", 0) is True
        assert get_model_field_names("Basic")[0] == "MCPExtra"

        assert model_rename_field("Basic", "MCPExtra", "MCPRenamed") is True
        names = get_model_field_names("Basic")
        assert "MCPRenamed" in names and "MCPExtra" not in names

        assert model_remove_field("Basic", "MCPRenamed") is True
        assert "MCPRenamed" not in get_model_field_names("Basic")

    def test_model_field_errors(self):
        """Field operations raise for unknown model/field or duplicate field."""
        import pytest

        from anki_connect_server.mcp_server import (
            model_add_field,
            model_remove_field,
        )

        with pytest.raises(ValueError, match="Model not found"):
            model_add_field("NoSuchModelMCP", "F")
        with pytest.raises(ValueError, match="Field already exists"):
            model_add_field("Basic", "Front")
        with pytest.raises(ValueError, match="Field not found"):
            model_remove_field("Basic", "NoSuchFieldMCP")

    def test_update_note_fields(self):
        """Test update_note_fields MCP tool."""
        from anki_connect_server.mcp_server import (
            add_note,
            get_notes_info,
            update_note_fields,
        )

        note_id = add_note("Default", "Basic", {"Front": "Old", "Back": "B"})
        assert note_id is not None
        assert update_note_fields(note_id, {"Front": "New"}) is True
        info = get_notes_info([note_id])[0]
        assert info["fields"]["Front"]["value"] == "New"
        assert info["fields"]["Back"]["value"] == "B"

    def test_update_model_templates_and_styling(self):
        """Test update_model_templates / update_model_styling MCP tools."""
        from anki_connect_server.mcp_server import (
            get_model_styling,
            get_model_templates,
            update_model_styling,
            update_model_templates,
        )

        assert update_model_templates("Basic", {"Card 1": {"Front": "Q: {{Front}}"}}) is True
        assert get_model_templates("Basic")["Card 1"]["Front"] == "Q: {{Front}}"

        css = ".card { font-family: mono; }"
        assert update_model_styling("Basic", css) is True
        assert get_model_styling("Basic")["css"] == css

    def test_get_api_version(self):
        """Test get_api_version MCP tool."""
        from anki_connect_server.mcp_server import get_api_version

        result = get_api_version()
        assert result == 6

    def test_retrieve_media_file_not_found(self):
        """Test retrieve_media_file returns None for missing file."""
        from anki_connect_server.mcp_server import retrieve_media_file

        result = retrieve_media_file("nonexistent_mcp.txt")
        assert result is None
