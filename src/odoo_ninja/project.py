"""Project task operations for Odoo Ninja."""

from typing import Any

from odoo_ninja.base import (
    add_comment as base_add_comment,
)
from odoo_ninja.base import (
    add_note as base_add_note,
)
from odoo_ninja.base import (
    add_tag_to_record,
    display_record_detail,
    display_records,
    display_tags,
    download_record_attachments,
    get_record,
    get_record_url,
    list_attachments,
    list_fields,
    list_messages,
    list_records,
    list_tags,
    set_record_fields,
)
from odoo_ninja.base import (
    create_attachment as base_create_attachment,
)
from odoo_ninja.client import OdooClient

# Model name constant
MODEL = "project.task"
TAG_MODEL = "project.tags"


def list_tasks(
    client: OdooClient,
    domain: list[Any] | None = None,
    limit: int | None = 50,
    fields: list[str] | None = None,
) -> list[dict[str, Any]]:
    """List project tasks.

    Args:
        client: Odoo client
        domain: Search domain filters
        limit: Maximum number of tasks
        fields: List of fields to fetch (None = default fields)

    Returns:
        List of task dictionaries

    """
    if fields is None:
        fields = [
            "id",
            "name",
            "partner_id",
            "project_id",
            "stage_id",
            "user_ids",
            "priority",
            "tag_ids",
            "create_date",
        ]

    return list_records(client, MODEL, domain=domain, limit=limit, fields=fields)


def display_tasks(tasks: list[dict[str, Any]]) -> None:
    """Display tasks in a rich table.

    Args:
        tasks: List of task dictionaries

    """
    display_records(tasks, title="Project Tasks")


def get_task(
    client: OdooClient,
    task_id: int,
    fields: list[str] | None = None,
) -> dict[str, Any]:
    """Get detailed task information.

    Args:
        client: Odoo client
        task_id: Task ID
        fields: List of field names to read (None = all fields)

    Returns:
        Task dictionary

    Raises:
        ValueError: If task not found

    """
    return get_record(client, MODEL, task_id, fields=fields)


def list_task_fields(client: OdooClient) -> dict[str, Any]:
    """Get all available fields for project tasks.

    Args:
        client: Odoo client

    Returns:
        Dictionary of field definitions with field names as keys

    """
    return list_fields(client, MODEL)


def set_task_fields(
    client: OdooClient,
    task_id: int,
    values: dict[str, Any],
) -> bool:
    """Update fields on a task.

    Args:
        client: Odoo client
        task_id: Task ID
        values: Dictionary of field names and values to update

    Returns:
        True if successful

    Examples:
        >>> set_task_fields(client, 42, {"name": "New title", "priority": "1"})
        >>> set_task_fields(client, 42, {"user_ids": [(6, 0, [5])], "stage_id": 3})

    """
    return set_record_fields(client, MODEL, task_id, values)


def display_task_detail(task: dict[str, Any], show_html: bool = False) -> None:
    """Display detailed task information.

    Args:
        task: Task dictionary
        show_html: If True, show raw HTML description, else convert to markdown

    """
    display_record_detail(task, MODEL, show_html=show_html, record_type="Task")


def add_comment(
    client: OdooClient,
    task_id: int,
    message: str,
    user_id: int | None = None,
    markdown: bool = False,
) -> bool:
    """Add a comment to a task (visible to followers).

    Args:
        client: Odoo client
        task_id: Task ID
        message: Comment message (plain text or markdown)
        user_id: User ID to post as (uses default if None)
        markdown: If True, convert markdown to HTML

    Returns:
        True if successful

    """
    return base_add_comment(client, MODEL, task_id, message, user_id=user_id, markdown=markdown)


def add_note(
    client: OdooClient,
    task_id: int,
    message: str,
    user_id: int | None = None,
    markdown: bool = False,
) -> bool:
    """Add an internal note to a task.

    Args:
        client: Odoo client
        task_id: Task ID
        message: Note message (plain text or markdown)
        user_id: User ID to post as (uses default if None)
        markdown: If True, convert markdown to HTML

    Returns:
        True if successful

    """
    return base_add_note(client, MODEL, task_id, message, user_id=user_id, markdown=markdown)


def list_task_tags(client: OdooClient) -> list[dict[str, Any]]:
    """List available project tags.

    Args:
        client: Odoo client

    Returns:
        List of tag dictionaries

    """
    return list_tags(client, TAG_MODEL)


def display_task_tags(tags: list[dict[str, Any]]) -> None:
    """Display project tags in a rich table.

    Args:
        tags: List of tag dictionaries

    """
    display_tags(tags, title="Project Tags")


def add_tag_to_task(
    client: OdooClient,
    task_id: int,
    tag_id: int,
) -> bool:
    """Add a tag to a task.

    Args:
        client: Odoo client
        task_id: Task ID
        tag_id: Tag ID

    Returns:
        True if successful

    """
    return add_tag_to_record(client, MODEL, task_id, tag_id)


def list_task_messages(
    client: OdooClient,
    task_id: int,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """List messages/chatter for a task.

    Args:
        client: Odoo client
        task_id: Task ID
        limit: Maximum number of messages (None = all)

    Returns:
        List of message dictionaries

    """
    return list_messages(client, MODEL, task_id, limit=limit)


def list_task_attachments(
    client: OdooClient,
    task_id: int,
) -> list[dict[str, Any]]:
    """List attachments for a task.

    Args:
        client: Odoo client
        task_id: Task ID

    Returns:
        List of attachment dictionaries

    """
    return list_attachments(client, MODEL, task_id)


def download_task_attachments(
    client: OdooClient,
    task_id: int,
    output_dir: Any = None,
    extension: str | None = None,
) -> list[Any]:
    """Download all attachments from a task.

    Args:
        client: Odoo client
        task_id: Task ID
        output_dir: Output directory (defaults to current directory)
        extension: File extension filter (e.g., 'pdf', 'jpg')

    Returns:
        List of paths to downloaded files

    """
    return download_record_attachments(client, MODEL, task_id, output_dir, extension=extension)


def create_task_attachment(
    client: OdooClient,
    task_id: int,
    file_path: Any,
    name: str | None = None,
) -> int:
    """Create an attachment for a task.

    Args:
        client: Odoo client
        task_id: Task ID
        file_path: Path to file to attach
        name: Attachment name (defaults to filename)

    Returns:
        ID of created attachment

    """
    return base_create_attachment(client, MODEL, task_id, file_path, name=name)


def get_task_url(client: OdooClient, task_id: int) -> str:
    """Get the web URL for a task.

    Args:
        client: Odoo client
        task_id: Task ID

    Returns:
        URL to view the task in Odoo web interface

    """
    return get_record_url(client, MODEL, task_id)
