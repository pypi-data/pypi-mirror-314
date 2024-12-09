#!/usr/bin/env python3
import os
import sys
import asyncio
import argparse
from pathlib import Path
from .api_client import PromptGeneratorClient
import click
import functools
import logging
import json
import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def async_command(f):
    """Decorator to run async click commands."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context
def cli(ctx):
    """CLI for managing templates and generating prompts."""
    ctx.ensure_object(dict)
    ctx.obj['client'] = PromptGeneratorClient()

@cli.command()
@click.option('-t', '--type', type=click.Choice(['template', 'guidance', 'questions']), help='Type of item')
@click.option('-s', '--section', help='Name of section')
@click.option('-d', '--doc-type', help='Type of document')
@click.option('-a', '--archive', is_flag=True, help='Include archived items')
@click.pass_context
@async_command
async def list(ctx, type, section, doc_type, archive):
    """List items matching the specified filters"""
    try:
        items = await ctx.obj['client'].list_items(type, section, doc_type, archive)
        
        # Display filters if any were applied
        filters = []
        if type:
            filters.append(f"Type: {type}")
        if section:
            filters.append(f"Section: {section}")
        if doc_type:
            filters.append(f"DocType: {doc_type}")
        if filters:
            click.echo(f"\nFilters applied: {', '.join(filters)}")
        
        click.echo("\nItems found:")
        for item in items:
            properties = item.get('properties', {})
            name = properties.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unnamed')
            item_type = properties.get('Type', {}).get('select', {}).get('name', '')
            doc_type = properties.get('DocType', {}).get('select', {}).get('name', '')
            section = properties.get('Section', {}).get('select', {}).get('name', '')
            status = properties.get('Status', {}).get('select', {}).get('name', 'Active')
            click.echo(f"- {name} [Type: {item_type}] [Section: {section}] [DocType: {doc_type}] [Status: {status}]")
            
    except Exception as e:
        click.echo(f"\nError listing items: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('-t', '--type', type=click.Choice(['template', 'guidance', 'questions']), required=True, help='Type of item')
@click.option('-s', '--section', required=True, help='Name of section')
@click.option('-d', '--doc-type', required=True, help='Type of document')
@click.pass_context
@async_command
async def get(ctx, type, section, doc_type):
    """Get content of a specific item"""
    try:
        item = await ctx.obj['client'].get_item(type, doc_type, section)
        
        if not item:
            click.echo(f"\nNo {type} found with section '{section}' and doc-type '{doc_type}'")
            return
            
        properties = item.get('properties', {})
        section = properties.get('Section', {}).get('select', {}).get('name', '')
        item_type = properties.get('Type', {}).get('select', {}).get('name', '')
        doc_type = properties.get('DocType', {}).get('select', {}).get('name', '')
        status = properties.get('Status', {}).get('select', {}).get('name', '')
        last_modified = properties.get('Last Modified', {}).get('last_edited_time', '')
        if last_modified:
            last_modified = datetime.datetime.fromisoformat(last_modified.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Header section
        click.echo(f"\nSection: {section}")
        click.echo(f"Type: {item_type}")
        click.echo(f"DocType: {doc_type}")
        click.echo(f"Status: {status}")
        click.echo(f"Last Modified: {last_modified}")
        click.echo("\n" + "="*50 + "\n")
        
        # Content section
        click.echo(item.get('content', ''))
        
    except Exception as e:
        click.echo(f"\nError getting {type}: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('-t', '--type', type=click.Choice(['template', 'guidance', 'questions']), required=True, help='Type of item')
@click.option('-s', '--section', required=True, help='Name of section')
@click.option('-d', '--doc-type', required=True, help='Type of document')
@click.option('-c', '--content', help='Content to create')
@click.option('-f', '--file', type=click.Path(exists=True), help='File containing content')
@click.pass_context
@async_command
async def create(ctx, type, section, doc_type, content, file):
    """Create a new item in Notion (template, guidance, or your own questions)"""
    if bool(content) == bool(file):
        raise click.UsageError("Exactly one of --content or --file must be provided")
    
    try:
        if file:
            with open(file, 'r') as f:
                content = f.read()
        
        result = await ctx.obj['client'].create_item(type, section, content, doc_type)
        click.echo("\nSuccessfully created " + type)
    except Exception as e:
        click.echo(f"\nError creating {type}: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('-t', '--type', type=click.Choice(['template', 'guidance', 'questions']), help='Type of item')
@click.option('-s', '--section', help='Name of section')
@click.option('-d', '--doc-type', help='Type of document')
@click.option('-a', '--archive', is_flag=True, help='Delete archived items only')
@click.option('-y', '--yes', is_flag=True, help='Skip confirmation')
@click.pass_context
@async_command
async def delete(ctx, type, section, doc_type, archive, yes):
    """Delete items matching the specified filters"""
    try:
        # Get items to delete first
        items = await ctx.obj['client'].list_items(type, section, doc_type, include_archived=True if archive else False)
        
        if not items:
            click.echo("\nNo items found matching the criteria.")
            return
            
        # Filter items based on type and archive flag
        items_to_delete = []
        for item in items:
            properties = item.get('properties', {})
            item_type = properties.get('Type', {}).get('select', {}).get('name', '')
            is_archived = properties.get('Status', {}).get('select', {}).get('name', '') == 'Archived'
            
            # Only include items that match the type and archive status
            if type and item_type != type:
                continue
            if archive != is_archived:
                continue
                
            items_to_delete.append(item)
            
        if not items_to_delete:
            click.echo("\nNo items found matching the criteria.")
            return
        
        # Show items to be deleted
        click.echo("\nThe following items will be deleted:")
        for item in items_to_delete:
            properties = item.get('properties', {})
            name = properties.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unnamed')
            item_type = properties.get('Type', {}).get('select', {}).get('name', '')
            doc_type = properties.get('DocType', {}).get('select', {}).get('name', '')
            section = properties.get('Section', {}).get('select', {}).get('name', '')
            status = properties.get('Status', {}).get('select', {}).get('name', 'Active')
            click.echo(f"- {name} [Type: {item_type}] [Section: {section}] [DocType: {doc_type}] [Status: {status}]")
        
        # Confirm deletion
        if not yes and not click.confirm("\nDo you want to proceed?"):
            click.echo("Operation cancelled.")
            return
            
        # Delete items
        result = await ctx.obj['client'].delete_items(type=type, section=section, doc_type=doc_type, archive_only=archive)
        click.echo(f"\nDeleted {result['deleted_count']} items.")
        
    except Exception as e:
        click.echo(f"\nError deleting items: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('-s', '--section', required=True, help='Name of section')
@click.option('-d', '--doc-type', required=True, help='Type of document')
@click.pass_context
@async_command
async def generate(ctx, section, doc_type):
    """Generate curious questions automatically based on guidance in Notion"""
    try:
        # Get the guidance content for this section/doc-type
        guidance = await ctx.obj['client'].get_item('guidance', doc_type, section)
        if not guidance:
            raise click.UsageError(f"No guidance found for section '{section}' and doc-type '{doc_type}'")

        # Get the template 
        template = await ctx.obj['client'].get_item('template', doc_type, section)
        if not template:
            raise click.UsageError(f"No template found for section '{section}' and doc-type '{doc_type}'")

        guidance_content = guidance.get('content', '')
        template_content = template.get('content', '')
        
        # Generate questions
        response = await ctx.obj['client'].generate_questions(guidance_content, template_content)
        questions = response['markdown'].replace('# Generated Questions\n\n', '')
        
        try:
            # Try to update existing questions
            await ctx.obj['client'].update_item(
                type='questions',
                section=section,
                content=questions,
                doc_type=doc_type
            )
        except ValueError as e:
            if 'No questions found' in str(e):
                # Create new questions if they don't exist
                await ctx.obj['client'].create_item(
                    type='questions',
                    section=section,
                    content=questions,
                    doc_type=doc_type
                )
            else:
                raise
        
        click.echo("\nGenerated and stored questions:")
        click.echo(questions)
    except Exception as e:
        click.echo(f"\nError generating questions: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('-s', '--section', required=True, help='Name of section')
@click.option('-d', '--doc-type', required=True, help='Type of document')
@click.option('-c', '--content', help='Questions to append')
@click.option('-f', '--file', type=click.Path(exists=True), help='File containing questions to append')
@click.pass_context
@async_command
async def update(ctx, section, doc_type, content, file):
    """Append new questions to existing ones in Notion"""
    if bool(content) == bool(file):
        raise click.UsageError("Exactly one of --content or --file must be provided")
    
    try:
        if file:
            with open(file, 'r') as f:
                content = f.read()
        
        result = await ctx.obj['client'].update_questions(section, content, doc_type)
        click.echo("\nSuccessfully updated questions")
    except Exception as e:
        click.echo(f"\nError updating questions: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('-k', '--key', required=True, help='API key for authentication')
@click.pass_context
def config(ctx, key):
    """Configure API key and other settings"""
    try:
        # Get the directory where the CLI is installed
        cli_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(cli_dir, '..', '.env')
        
        # Create or update .env file
        with open(env_path, 'w') as f:
            f.write(f'PROMPT_GENERATOR_API_KEY={key}\n')
        
        click.echo(f"\nAPI key configured successfully in {env_path}")
        click.echo("You can now use other qg commands")
        
    except Exception as e:
        click.echo(f"\nError configuring API key: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
