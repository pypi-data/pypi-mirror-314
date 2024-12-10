import base64
from pathlib import Path
import click
import yaml
import tableauserverclient as TSC
import psycopg
from psycopg import sql

CONFIG_FILE = "tableau.yaml"


def get_default_config_path():
    return str(Path.home() / CONFIG_FILE)


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def decode_secret(encoded_secret):
    decoded_bytes = base64.b64decode(encoded_secret.split(":")[0])
    return decoded_bytes.decode("utf-8")


def authenticate(config):
    server_url = config["tableau_server"]["url"]
    site_content_url = config["site"]["content_url"]
    api_version = config["api"]["version"]

    if config["authentication"]["type"] == "personal_access_token":
        token_name = config["personal_access_token"]["name"]
        token_secret = decode_secret(config["personal_access_token"]["secret"])
        tableau_auth = TSC.PersonalAccessTokenAuth(
            token_name, token_secret, site_id=site_content_url
        )
    else:
        username = config["tableau_auth"]["username"]
        password = decode_secret(config["tableau_auth"]["password"])
        tableau_auth = TSC.TableauAuth(username, password, site_id=site_content_url)

    server = TSC.Server(server_url, use_server_version=False)
    server.version = api_version
    server.auth.sign_in(tableau_auth)
    return server


@click.group()
@click.option(
    "--config", default=get_default_config_path(), help="Path to the configuration file"
)
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj["config"] = config


@cli.group()
def ls():
    """List various Tableau resources"""


@ls.command()
@click.pass_context
def users(ctx):
    """List users"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)
    all_users, _ = server.users.get()
    for user in all_users:
        click.echo(f"User: {user.name}, ID: {user.id}")
    server.auth.sign_out()


@ls.command()
@click.pass_context
def groups(ctx):
    """List groups"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)
    all_groups, _ = server.groups.get()
    for group in all_groups:
        click.echo(f"Group: {group.name}, ID: {group.id}")
    server.auth.sign_out()


@ls.command()
@click.pass_context
def workbooks(ctx):
    """List workbooks"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)
    all_workbooks, _ = server.workbooks.get()
    for workbook in all_workbooks:
        click.echo(f"Workbook: {workbook.name}, ID: {workbook.id}")
    server.auth.sign_out()


@ls.command()
@click.pass_context
def datasources(ctx):
    """List datasources"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)
    all_datasources, _ = server.datasources.get()
    for datasource in all_datasources:
        click.echo(f"Datasource: {datasource.name}, ID: {datasource.id}")
    server.auth.sign_out()


@ls.command()
@click.pass_context
def projects(ctx):
    """List projects"""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)
    all_projects, _ = server.projects.get()
    for project in all_projects:
        click.echo(f"Project: {project.name}, ID: {project.id}")
    server.auth.sign_out()


@cli.command()
@click.argument("string")
def encode(string):
    """Encode a string using Base64 encoding."""
    encoded_bytes = base64.b64encode(string.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")
    click.echo(encoded_str)


@cli.command()
@click.argument("encoded_string")
def decode(encoded_string):
    """Decode a Base64 encoded string."""
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_str = decoded_bytes.decode("utf-8")
        click.echo(decoded_str)
    except UnicodeDecodeError as e:
        click.echo(f"Error decoding string: {e}")


def execute_query(config, query, params=None):
    # pylint: disable=not-context-manager
    with psycopg.connect(
        host=config["postgres"]["host"],
        port=config["postgres"]["port"],
        dbname=config["postgres"]["database"],
        user=config["postgres"]["user"],
        password=decode_secret(config["postgres"]["password"]),
    ) as conn:
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            results = cur.fetchall()
    return results


@cli.group()
def find():
    """Find various Tableau resources"""


@find.command()
@click.option("-limit", default=10, help="Number of results to return")
@click.option("-min_date", default=None, help="Minimum date in yyyy-mm-dd format")
@click.option("-max_date", default=None, help="Maximum date in yyyy-mm-dd format")
@click.option(
    "-headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.pass_context
def slowest_views(ctx, limit, min_date, max_date, headers):
    """Find slowest views"""
    config = load_config(ctx.obj["config"])
    query = sql.SQL(
        """
        WITH date_range AS (
            SELECT MIN(created_at) AS min_date, MAX(created_at) AS max_date
            FROM http_requests
            WHERE action = 'bootstrapSession'
        )
        SELECT 
            s.name AS site_name,
            SPLIT_PART(hr.currentsheet, '/', 1) AS workbook_name,
            SPLIT_PART(hr.currentsheet, '/', 2) AS view_name,
            AVG(EXTRACT(EPOCH FROM (hr.completed_at - hr.created_at))) AS avg_duration,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(
                EPOCH FROM (hr.completed_at - hr.created_at))) AS median_duration,
            MIN(hr.created_at) AS min_date,
            MAX(hr.created_at) AS max_date
        FROM http_requests hr
        JOIN sites s ON hr.site_id = s.id
        WHERE hr.action = 'bootstrapSession'
        AND hr.created_at >= COALESCE(%s, (SELECT min_date FROM date_range))
        AND hr.created_at <= COALESCE(%s, (SELECT max_date FROM date_range))
        GROUP BY s.name, hr.currentsheet
        ORDER BY avg_duration DESC
        LIMIT %s
    """
    )

    results = execute_query(config, query, (min_date, max_date, limit))

    if headers:
        click.echo(
            "Site\tWorkbook\tView\tAvg Duration (s)\tMedian Duration (s)"
            "\tMin Date\tMax Date"
        )

    for row in results:
        click.echo(
            f"{row[0] or 'Unknown'}\t{row[1] or 'Unknown'}\t{row[2] or 'Unknown'}"
            f"\t{row[3]:.2f}\t{row[4]:.2f}\t{row[5]}\t{row[6]}"
        )


@find.command()
@click.option("-limit", default=10, help="Number of results to return")
@click.option("-min_date", default=None, help="Minimum date in yyyy-mm-dd format")
@click.option("-max_date", default=None, help="Maximum date in yyyy-mm-dd format")
@click.option(
    "-headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.pass_context
def largest_workbooks(ctx, limit, min_date, max_date, headers):
    """Find largest workbooks with usage data from historical events"""
    config = load_config(ctx.obj["config"])
    query = sql.SQL(
        """
        WITH date_range AS (
            SELECT COALESCE(%s::date, MIN(created_at)::date) AS min_date, 
                   COALESCE(%s::date, MAX(created_at)::date) AS max_date
            FROM workbooks
        ),
        workbook_usage AS (
            SELECT 
                workbook_id,
                COUNT(DISTINCT hist_actor_user_id) AS unique_users,
                COUNT(*) AS total_views
            FROM historical_events he
            join historical_event_types et
              on et.type_id = he.historical_event_type_id
            join hist_workbooks hw
              on he.hist_workbook_id = hw.id
            join workbooks w
              on w.id = hw.workbook_id
            WHERE et.action_type = 'Access'
            AND workbook_id IS NOT NULL
            GROUP BY workbook_id
        ),
        project_path AS (
            WITH RECURSIVE project_hierarchy AS (
                SELECT 
                    pc.content_id,
                    p.id AS project_id,
                    p.name AS project_name,
                    p.parent_project_id,
                    1 AS level,
                    p.name::character varying AS path
                FROM projects_contents pc
                JOIN projects p ON pc.project_id = p.id
                WHERE pc.content_type = 'workbook'
                
                UNION ALL
                
                SELECT
                    ph.content_id,
                    p.id,
                    p.name,
                    p.parent_project_id,
                    ph.level + 1,
                    (p.name || ' > ' || ph.path)::character varying
                FROM project_hierarchy ph
                JOIN projects p ON ph.parent_project_id = p.id
            )
            SELECT 
                content_id,
                path AS full_project_path
            FROM project_hierarchy
            WHERE parent_project_id IS NULL
        )
        SELECT 
            s.name AS site_name,
            w.name AS workbook_name,
            w.size / 1048576.0 AS size_mb,
            COALESCE(wu.unique_users, 0) AS unique_users,
            COALESCE(wu.total_views, 0) AS total_views,
            w.created_at,
            w.updated_at,
            COALESCE(pp.full_project_path, 'Top Level') AS project_path,
            su.friendly_name AS owner_name
        FROM workbooks w
        JOIN sites s ON w.site_id = s.id
        LEFT JOIN workbook_usage wu ON w.id = wu.workbook_id
        LEFT JOIN project_path pp ON w.id = pp.content_id
        LEFT JOIN users o ON w.owner_id = o.id
        left join system_users su on su.id = o.system_user_id
        CROSS JOIN date_range dr
        WHERE w.created_at::date BETWEEN dr.min_date AND dr.max_date
        ORDER BY w.size DESC
        LIMIT %s
    """
    )

    results = execute_query(config, query, (min_date, max_date, limit))

    if headers:
        click.echo(
            "Site\tWorkbook\tSize (MB)\tUnique Users\tTotal Views\tCreated At"
            "\tUpdated At\tProject Path\tOwner"
        )

    for row in results:
        click.echo(
            f"{row[0] or 'Unknown'}\t{row[1] or 'Unknown'}\t{row[2]:.2f}"
            f"\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}\t{row[7] or 'Top Level'}"
            f"\t{row[8] or 'Unknown'}"
        )


@find.command()
@click.option("-limit", default=10, help="Number of results to return")
@click.option("-min_date", default=None, help="Minimum date in yyyy-mm-dd format")
@click.option("-max_date", default=None, help="Maximum date in yyyy-mm-dd format")
@click.option(
    "-headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.pass_context
def largest_datasources(ctx, limit, min_date, max_date, headers):
    """Find largest datasources"""
    config = load_config(ctx.obj["config"])
    query = sql.SQL(
        """
        WITH date_range AS (
            SELECT MIN(created_at) AS min_date, MAX(created_at) AS max_date
            FROM datasources
        )
        SELECT 
            s.name AS site_name,
            d.name AS datasource_name,
            d.size / 1048576.0 AS size_mb,
            d.created_at,
            d.updated_at
        FROM datasources d
        JOIN sites s ON d.site_id = s.id
        WHERE d.created_at >= COALESCE(%s, (SELECT min_date FROM date_range))
        AND d.created_at <= COALESCE(%s, (SELECT max_date FROM date_range))
        ORDER BY d.size DESC
        LIMIT %s
    """
    )

    results = execute_query(config, query, (min_date, max_date, limit))

    if headers:
        click.echo("Site\tDatasource\tSize (MB)\tCreated At\tUpdated At")

    for row in results:
        click.echo(
            f"{row[0] or 'Unknown'}\t{row[1] or 'Unknown'}\t{row[2]:.2f}"
            f"\t{row[3]}\t{row[4]}"
        )


if __name__ == "__main__":
    cli(ctx={}, config=get_default_config_path())
