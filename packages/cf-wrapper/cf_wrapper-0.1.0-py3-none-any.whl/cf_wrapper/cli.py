"""Cloud Fix Wrapper CLI."""

import click
from . import sdk
import json
import os

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Cloud Fix Wrapper CLI for managing and querying cloud resources."""
    pass

@cli.group(context_settings=CONTEXT_SETTINGS)
def list():
    """List available options (accounts, regions, services, finders)."""
    pass

@list.command(context_settings=CONTEXT_SETTINGS)
@click.option('-l', '--limit', type=int, default=100, help='Number of results to return (default: 100)')
@click.option('-o', '--offset', type=int, default=0, help='Offset for pagination (default: 0)')
def accounts():
    """List all available accounts."""
    result = sdk.list_options('accounts', limit=limit, offset=offset)
    if result and 'accounts' in result:
        click.echo("\nAvailable Accounts:")
        click.echo("==================")
        for account in result['accounts']:
            name = account.get('account_name', 'N/A')
            click.echo(f"{account['account']} - {name}")
        
        # Show pagination info
        total = result.get('total', 0)
        remaining = max(0, total - (offset + limit))
        if remaining > 0:
            click.echo(f"\nShowing {min(limit, len(result['accounts']))} of {total} accounts. {remaining} more available.")
            click.echo(f"Use --offset {offset + limit} to see more.")

@list.command(context_settings=CONTEXT_SETTINGS)
@click.option('-l', '--limit', type=int, default=100, help='Number of results to return (default: 100)')
@click.option('-o', '--offset', type=int, default=0, help='Offset for pagination (default: 0)')
def regions():
    """List all available regions."""
    result = sdk.list_options('regions', limit=limit, offset=offset)
    if result and 'regions' in result:
        click.echo("\nAvailable Regions:")
        click.echo("=================")
        for region in result['regions']:
            click.echo(region['region'])
            
        # Show pagination info
        total = result.get('total', 0)
        remaining = max(0, total - (offset + limit))
        if remaining > 0:
            click.echo(f"\nShowing {min(limit, len(result['regions']))} of {total} regions. {remaining} more available.")
            click.echo(f"Use --offset {offset + limit} to see more.")

@list.command(context_settings=CONTEXT_SETTINGS)
@click.option('-l', '--limit', type=int, default=100, help='Number of results to return (default: 100)')
@click.option('-o', '--offset', type=int, default=0, help='Offset for pagination (default: 0)')
def services():
    """List all available AWS services."""
    result = sdk.list_options('services', limit=limit, offset=offset)
    if result and 'services' in result:
        click.echo("\nAvailable Services:")
        click.echo("==================")
        for service in result['services']:
            click.echo(service['service'])
            
        # Show pagination info
        total = result.get('total', 0)
        remaining = max(0, total - (offset + limit))
        if remaining > 0:
            click.echo(f"\nShowing {min(limit, len(result['services']))} of {total} services. {remaining} more available.")
            click.echo(f"Use --offset {offset + limit} to see more.")

@list.command(context_settings=CONTEXT_SETTINGS)
@click.option('-l', '--limit', type=int, default=100, help='Number of results to return (default: 100)')
@click.option('-o', '--offset', type=int, default=0, help='Offset for pagination (default: 0)')
def finders():
    """List all available finders."""
    result = sdk.list_options('finders', limit=limit, offset=offset)
    if result and 'finders' in result:
        click.echo("\nAvailable Finders:")
        click.echo("=================")
        for finder in result['finders']:
            click.echo(f"{finder['service']} - {finder['finder']}")
            
        # Show pagination info
        total = result.get('total', 0)
        remaining = max(0, total - (offset + limit))
        if remaining > 0:
            click.echo(f"\nShowing {min(limit, len(result['finders']))} of {total} finders. {remaining} more available.")
            click.echo(f"Use --offset {offset + limit} to see more.")

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-a', '--account', help='Account ID')
@click.option('-r', '--region', help='AWS region')
@click.option('-s', '--service', help='AWS service')
@click.option('-f', '--finder', help='Finder name')
@click.option('-l', '--limit', type=int, default=100, help='Number of results to return (default: 100)')
@click.option('-o', '--offset', type=int, default=0, help='Offset for pagination (default: 0)')
def get(account, region, service, finder, limit, offset):
    """Get records filtered by account, region, service, or finder."""
    if not any([account, region, service, finder]):
        click.echo("Error: At least one filter option is required (-a, -r, -s, or -f)", err=True)
        return

    result = sdk.get_records(account, region, service, finder, limit, offset)
    if not result or not result.get('records'):
        click.echo("No records found", err=True)
        return

    # Print records with proper formatting
    records = result['records']
    for record in records:
        # Print record header
        click.echo("\nRecord Details:")
        click.echo("=" * 50)
        
        # Basic information
        click.echo(f"ID:              {record['id']}")
        click.echo(f"Account:         {record['account']}")
        click.echo(f"Region:          {record['region']}")
        click.echo(f"Finder:          {record['finder_id']}")
        click.echo(f"Status:          {record['status']}")
        
        # Resource details
        click.echo(f"\nResource:")
        click.echo(f"  ID:            {record['resource_id']}")
        click.echo(f"  Name:          {record['resource_name']}")
        click.echo(f"  ARN:           {record.get('resource_arn', 'N/A')}")
        click.echo(f"  URL:           {record.get('resource_url', 'N/A')}")
        
        # Cost information
        if record.get('annual_cost') or record.get('annual_savings'):
            click.echo(f"\nCost Information:")
            click.echo(f"  Annual Cost:    ${record.get('annual_cost', 0):,.2f}")
            click.echo(f"  Annual Savings: ${record.get('annual_savings', 0):,.2f}")
        
        # Change request information if present
        if record.get('change_request_id'):
            click.echo(f"\nChange Request:")
            click.echo(f"  ID:            {record['change_request_id']}")
            click.echo(f"  Status:        {record.get('change_request_status', 'N/A')}")
            if record.get('change_request_failure'):
                click.echo(f"  Failure:       {record['change_request_failure']}")
        
        # Finder report
        finder_report = record.get('finder_report')
        if finder_report and finder_report.strip():  # Only show if non-empty
            click.echo("\nFinder Report:")
            click.echo("==================================================")
            try:
                # Try to parse as JSON first
                report_json = json.loads(finder_report)
                click.echo(json.dumps(report_json, indent=2))
            except json.JSONDecodeError:
                # If not valid JSON, show as plain text
                click.echo(finder_report)

        # Timestamps
        click.echo(f"\nTimestamps:")
        click.echo(f"  Created:        {record['created_at']}")
        click.echo(f"  Updated:        {record['updated_at']}")
        if record.get('completed_at'):
            click.echo(f"  Completed:      {record['completed_at']}")
        if record.get('scheduled_at'):
            click.echo(f"  Scheduled:      {record['scheduled_at']}")

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', '--table', required=True, help='Name of the table to describe')
def describe(table):
    """Describe the structure of a database table."""
    try:
        result = sdk.describe_table(table)
        if not result or 'error' in result:
            click.echo(f"Error: {result.get('error', 'No table description found')}", err=True)
            return

        # Print table name
        click.echo(f"\nTable: {result['table_name']}")
        click.echo("=" * (len(result['table_name']) + 7))
        
        # Print column details
        click.echo("\nColumns:")
        click.echo("-" * 80)
        
        # Format and print each column
        for col in result['columns']:
            # Format the column header
            header = f"{col['name']} ({col['type']})"
            if col['key'] == 'PRI':
                header += " [PRIMARY KEY]"
            elif col['key'] == 'MUL':
                header += " [INDEXED]"
            elif col['key'] == 'UNI':
                header += " [UNIQUE]"
            
            click.echo(header)
            
            # Format column attributes
            attrs = []
            if col['nullable'] == 'NO':
                attrs.append("NOT NULL")
            if col['extra']:
                attrs.append(col['extra'])
            
            if attrs:
                click.echo(f"  Attributes: {', '.join(attrs)}")
            
            # Print description if available
            if col.get('description'):
                # Wrap description at 70 characters
                desc_lines = [col['description'][i:i+70] for i in range(0, len(col['description']), 70)]
                for line in desc_lines:
                    click.echo(f"  {line}")
            
            click.echo("")  # Empty line between columns
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-k', '--key', help='API key for authentication')
def config(key):
    """Configure the CloudFix CLI."""
    if key:
        # Store the key in user's home directory
        config_dir = os.path.expanduser('~/.cloudfix')
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, 'config.json')
        
        config_data = {}
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        
        config_data['api_key'] = key
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        click.echo("API key configured successfully")
    else:
        click.echo("Please provide an API key using the -k option")

if __name__ == '__main__':
    cli()
