"""Restless main entry point."""

import click
from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from click import Context
from tabulate import tabulate


def get_host_from_inventory(
    inventory_manager: InventoryManager, host: str
) -> Host | None:
    """
    Get a host object from the inventory.

    Args:
        inventory_manager: InventoryManager object.
        host: Host to get from inventory.

    Returns:
        Host object if host exists in inventory, else None.
    """
    try:
        return inventory_manager.get_host(host)
    except KeyError:
        click.echo(f'Host "{host}" does not exist in inventory.')
        return None


@click.group()
@click.option(
    "--inventory-file",
    "-i",
    default="/etc/ansible/hosts",
    help="Path to inventory file",
)
@click.pass_context
def cli(ctx: Context, inventory_file: str) -> None:
    """
    Ansible inventory reader.
    """
    ctx.ensure_object(dict)
    ctx.obj["inventory_file"] = inventory_file
    ctx.obj["inventory_manager"] = InventoryManager(
        loader=DataLoader(), sources=inventory_file
    )
    ctx.obj["variable_manager"] = VariableManager(
        loader=DataLoader(), inventory=ctx.obj["inventory_manager"]
    )


@cli.command()
@click.pass_context
def list_hosts(ctx: Context) -> None:
    """
    List all hosts in the inventory.
    """
    inventory_manager: InventoryManager = ctx.obj["inventory_manager"]
    hosts = inventory_manager.get_hosts()
    for host in hosts:
        click.echo(host.name)


@cli.command()
@click.pass_context
def list_groups(ctx: Context) -> None:
    """
    List all groups in the inventory.
    """
    inventory_manager: InventoryManager = ctx.obj["inventory_manager"]
    groups = inventory_manager.get_groups_dict()
    if not groups:
        click.echo("No groups exist in inventory.")
        return
    for group in groups:
        click.echo(group)


@cli.command()
@click.argument("host")
@click.pass_context
def get_host(ctx: Context, host: str) -> None:
    """
    Get details for a specific host.
    """
    inventory_manager: InventoryManager = ctx.obj["inventory_manager"]
    host_obj = get_host_from_inventory(inventory_manager, host)
    if not host_obj:
        click.echo(f'Host "{host}" does not exist in inventory.')
        return
    click.echo(f"Name: {host_obj.name or 'None'}")
    click.echo(f"Vars: {host_obj.vars or 'None'}")
    click.echo(f"Groups: {host_obj.groups or 'None'}")


@cli.command()
@click.argument("group")
@click.pass_context
def list_group_members(ctx: Context, group: str) -> None:
    """
    List all hosts in a specific group.
    """
    inventory_manager: InventoryManager = ctx.obj["inventory_manager"]
    hosts: list[Host] = inventory_manager.get_hosts(group)
    for host in hosts:
        click.echo(host.name)


@cli.command()
@click.pass_context
def list_inventory(ctx: Context) -> None:
    """
    Show the inventory in a structured manner.
    """
    inventory_manager: InventoryManager = ctx.obj["inventory_manager"]
    inventory = inventory_manager._inventory
    groups: dict[str, str] | None = inventory.get_groups_dict()
    if not groups:
        click.echo("No groups exist in inventory.")
        return
    for group_name, group in groups.items():
        click.echo(f"[{group_name}]")
        for host in inventory_manager.get_hosts(group):
            click.echo(host.name)
        click.echo("")


@cli.command()
@click.pass_context
def display_table(ctx: Context) -> None:
    """
    Display the inventory in a table format.
    """
    inventory_manager: InventoryManager = ctx.obj["inventory_manager"]
    inventory = inventory_manager._inventory
    groups: dict[str, str] | None = inventory.get_groups_dict()
    if not groups:
        click.echo("No groups exist in inventory.")
        return
    skip_vars = ["inventory_file", "inventory_dir"]
    table = []
    for group_name, group in groups.items():
        for host in inventory_manager.get_hosts(group):
            vars: dict[str, str] = {
                k: v for (k, v) in host.vars.items() if k not in skip_vars
            }
            table.append([host.name, group_name, vars or ""])
    click.echo(tabulate(table, headers=["Host", "Group", "Vars"]))
