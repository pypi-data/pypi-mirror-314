import base64
import csv
from pathlib import Path
import click
import yaml
import tableauserverclient as TSC
import psycopg
from psycopg import sql

CONFIG_FILE = str(Path.home().joinpath(".tableau_toolkit", "tableau.yaml"))


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
    server.add_http_options({"verify": False})
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


@cli.command()
def init():
    """Initialize the tableau_toolkit configuration."""
    home_dir = Path.home()
    config_dir = home_dir / ".tableau_toolkit"
    config_file = config_dir / "tableau.yaml"

    if config_file.exists():
        click.echo("Configuration file already exists. Do you want to overwrite it?")
        if not click.confirm("Overwrite?"):
            click.echo("Initialization cancelled.")
            return

    config_dir.mkdir(exist_ok=True)

    default_config = {
        "tableau_server": {"url": "https://hostname"},
        "authentication": {"type": "tableau_auth"},
        "personal_access_token": {"name": "name", "secret": "secret"},
        "tableau_auth": {"username": "username", "password": "password"},
        "site": {"content_url": ""},
        "api": {"version": "3.24"},
        "postgres": {
            "host": "host",
            "port": 8060,
            "database": "workgroup",
            "user": "readonly",
            "password": "password",
        },
    }

    with config_file.open("w") as f:
        yaml.dump(default_config, f, default_flow_style=False)

    click.echo(f"Configuration file created at {config_file}")


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
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--min_usage_date", default=None, help="Minimum usage date in yyyy-mm-dd format"
)
@click.option(
    "--max_usage_date", default=None, help="Maximum usage date in yyyy-mm-dd format"
)
@click.option(
    "--min_update_date", default=None, help="Minimum update date in yyyy-mm-dd format"
)
@click.option(
    "--max_update_date", default=None, help="Maximum update date in yyyy-mm-dd format"
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--owner_email", default=None, help="Filter by owner email")
@click.option("--min_size", default=None, type=float, help="Minimum size in MB")
@click.option("--max_size", default=None, type=float, help="Maximum size in MB")
@click.option("--min_views", default=None, type=int, help="Minimum number of views")
@click.option("--max_views", default=None, type=int, help="Maximum number of views")
@click.option(
    "--min_users", default=None, type=int, help="Minimum number of unique users"
)
@click.option(
    "--max_users", default=None, type=int, help="Maximum number of unique users"
)
@click.pass_context
def largest_workbooks(
    ctx,
    limit,
    min_usage_date,
    max_usage_date,
    min_update_date,
    max_update_date,
    headers,
    owner_email,
    min_size,
    max_size,
    min_views,
    max_views,
    min_users,
    max_users,
):
    """Find largest workbooks with usage data from historical events"""
    config = load_config(ctx.obj["config"])
    query = sql.SQL(
        """
        WITH date_range AS (
            SELECT COALESCE(%s::date, MIN(time)::date) AS min_usage_date,
                   COALESCE(%s::date, MAX(time)::date) AS max_usage_date
            FROM views_stats
        ),
        workbook_usage AS (
            SELECT
                v.workbook_id,
                v.site_id,
                COUNT(DISTINCT d.user_id) AS unique_users,
                sum(nviews) AS total_views,
                max(time) last_accessed_at
            FROM views_stats d
            join views v
            on v.id = d.view_id
            and v.site_id = d.site_id
            cross join date_range dr
            WHERE d.time::date BETWEEN dr.min_usage_date AND dr.max_usage_date
            GROUP BY v.workbook_id, v.site_id
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
                    (p.name || ' >> ' || ph.path)::character varying
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
            s.luid as site_luid,
            w.name AS workbook_name,
            w.luid as workbook_luid,
            w.size / 1048576.0 AS size_mb,
            COALESCE(wu.unique_users, 0) AS unique_users,
            COALESCE(wu.total_views, 0) AS total_views,
            w.created_at,
            w.updated_at,
            COALESCE(pp.full_project_path, 'Top Level') AS project_path,
            su.name AS owner_id,
            su.friendly_name owner_name,
            su.email owner_email,
            dr.min_usage_date,
            dr.max_usage_date,
            wu.last_accessed_at
        FROM workbooks w
        JOIN sites s ON w.site_id = s.id
        JOIN workbook_usage wu ON w.id = wu.workbook_id and w.site_id = wu.site_id
        LEFT JOIN project_path pp ON w.id = pp.content_id
        LEFT JOIN users o ON w.owner_id = o.id
        left join system_users su on su.id = o.system_user_id
        cross join date_range dr
        WHERE (%s::text IS NULL OR su.email = %s::text)
        AND (%s::float IS NULL OR w.size / 1048576.0 >= %s::float)
        AND (%s::float IS NULL OR w.size / 1048576.0 <= %s::float)
        AND (%s::int IS NULL OR COALESCE(wu.total_views, 0) >= %s::int)
        AND (%s::int IS NULL OR COALESCE(wu.total_views, 0) <= %s::int)
        AND (%s::int IS NULL OR COALESCE(wu.unique_users, 0) >= %s::int)
        AND (%s::int IS NULL OR COALESCE(wu.unique_users, 0) <= %s::int)
        AND (%s::date IS NULL OR w.updated_at::date >= %s::date)
        AND (%s::date IS NULL OR w.updated_at::date <= %s::date)
        ORDER BY w.size DESC
        LIMIT %s
        """
    )

    results = execute_query(
        config,
        query,
        (
            min_usage_date,
            max_usage_date,
            owner_email,
            owner_email,
            min_size,
            min_size,
            max_size,
            max_size,
            min_views,
            min_views,
            max_views,
            max_views,
            min_users,
            min_users,
            max_users,
            max_users,
            min_update_date,
            min_update_date,
            max_update_date,
            max_update_date,
            limit,
        ),
    )

    if headers:
        click.echo(
            "Site Name\tSite ID\t"
            "Workbook Name\tWorkbook ID\t"
            "Size (MB)\tUnique Users\t"
            "Total Views\tCreated At\t"
            "Updated At\tProject Path\t"
            "Owner ID\tOwner Name\t"
            "Owner Email\tUsage Start Date\t"
            "Usage End Date\tLast Accessed At"
        )

    for row in results:
        click.echo(
            f"{row[0] or 'Unknown'}\t{row[1] or 'Unknown'}\t"
            f"{row[2] or 'Unknown'}\t{row[3] or 'Unknown'}\t"
            f"{row[4]:.2f}\t{row[5]}\t"
            f"{row[6]}\t{row[7]}\t"
            f"{row[8]}\t{row[9] or 'Top Level'}\t"
            f"{row[10] or 'Unknown'}\t{row[11] or 'Unknown'}\t"
            f"{row[12] or 'Unknown'}\t{row[13] or 'Unknown'}\t"
            f"{row[14] or 'Unknown'}\t{row[15] or 'Unknown'}"
        )


@find.command()
@click.option("--limit", default=10, help="Number of results to return")
@click.option(
    "--min_usage_date", default=None, help="Minimum usage date in yyyy-mm-dd format"
)
@click.option(
    "--max_usage_date", default=None, help="Maximum usage date in yyyy-mm-dd format"
)
@click.option(
    "--min_update_date", default=None, help="Minimum update date in yyyy-mm-dd format"
)
@click.option(
    "--max_update_date", default=None, help="Maximum update date in yyyy-mm-dd format"
)
@click.option(
    "--headers/--no-headers", default=True, help="Display headers (default: on)"
)
@click.option("--owner_email", default=None, help="Filter by owner email")
@click.option("--min_size", default=None, type=float, help="Minimum size in MB")
@click.option("--max_size", default=None, type=float, help="Maximum size in MB")
@click.option("--min_views", default=None, type=int, help="Minimum number of views")
@click.option("--max_views", default=None, type=int, help="Maximum number of views")
@click.pass_context
def largest_datasources(
    ctx,
    limit,
    min_usage_date,
    max_usage_date,
    min_update_date,
    max_update_date,
    headers,
    owner_email,
    min_size,
    max_size,
    min_views,
    max_views,
):
    """Find largest datasources with usage data"""
    config = load_config(ctx.obj["config"])
    query = sql.SQL(
        """
        WITH date_range AS (
            SELECT COALESCE(%s::date, MIN(last_access_time)::date) AS min_usage_date, 
                   COALESCE(%s::date, MAX(last_access_time)::date) AS max_usage_date
            FROM _datasources_stats
        ),
        datasource_usage AS (
            SELECT 
                d.datasource_id,
                d.site_id,
                sum(nviews) AS total_views,
                max(last_access_time) last_accessed_at
            FROM _datasources_stats d
            join datasources v
              on v.id = d.datasource_id
             and v.site_id = d.site_id
            cross join date_range dr
            WHERE 
              v.connectable
                and
              d.last_access_time::date BETWEEN dr.min_usage_date AND dr.max_usage_date
            GROUP BY d.datasource_id, d.site_id
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
                WHERE pc.content_type = 'datasource'
                
                UNION ALL
                
                SELECT
                    ph.content_id,
                    p.id,
                    p.name,
                    p.parent_project_id,
                    ph.level + 1,
                    (p.name || ' >> ' || ph.path)::character varying
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
            s.luid as site_luid,
            d.name AS datasource_name,
            d.luid as datasource_luid,
            d.size / 1048576.0 AS size_mb,
            COALESCE(du.total_views, 0) AS total_views,
            d.created_at,
            d.updated_at,
            COALESCE(pp.full_project_path, 'Top Level') AS project_path,
            su.name AS owner_id,
            su.friendly_name owner_name,
            su.email owner_email,
            dr.min_usage_date,
            dr.max_usage_date,
            du.last_accessed_at
        FROM datasources d
        JOIN sites s ON d.site_id = s.id
        JOIN datasource_usage du 
          ON d.id = du.datasource_id and d.site_id = du.site_id
        LEFT JOIN project_path pp ON d.id = pp.content_id
        LEFT JOIN users o ON d.owner_id = o.id
        left join system_users su on su.id = o.system_user_id
        cross join date_range dr
        WHERE (%s::text IS NULL OR su.email = %s::text)
          AND (%s::float IS NULL OR d.size / 1048576.0 >= %s::float)
          AND (%s::float IS NULL OR d.size / 1048576.0 <= %s::float)
          AND (%s::int IS NULL OR COALESCE(du.total_views, 0) >= %s::int)
          AND (%s::int IS NULL OR COALESCE(du.total_views, 0) <= %s::int)
          AND (%s::date IS NULL OR d.updated_at::date >= %s::date)
          AND (%s::date IS NULL OR d.updated_at::date <= %s::date)
          AND d.connectable
        ORDER BY d.size DESC
        LIMIT %s
    """
    )

    results = execute_query(
        config,
        query,
        (
            min_usage_date,
            max_usage_date,
            owner_email,
            owner_email,
            min_size,
            min_size,
            max_size,
            max_size,
            min_views,
            min_views,
            max_views,
            max_views,
            min_update_date,
            min_update_date,
            max_update_date,
            max_update_date,
            limit,
        ),
    )

    if headers:
        click.echo(
            "Site Name\tSite ID\t"
            "Datasource Name\tDatasource ID\t"
            "Size (MB)\t"
            "Total Views\tCreated At\t"
            "Updated At\tProject Path\t"
            "Owner ID\tOwner Name\t"
            "Owner Email\tUsage Start Date\t"
            "Usage End Date\tLast Accessed At"
        )

    for row in results:
        click.echo(
            f"{row[0] or 'Unknown'}\t{row[1] or 'Unknown'}\t"
            f"{row[2] or 'Unknown'}\t{row[3] or 'Unknown'}\t"
            f"{row[4]:.2f}\t"
            f"{row[5]}\t{row[6]}\t"
            f"{row[7]}\t{row[8] or 'Top Level'}\t"
            f"{row[9] or 'Unknown'}\t{row[10] or 'Unknown'}\t"
            f"{row[11] or 'Unknown'}\t{row[12] or 'Unknown'}\t"
            f"{row[13] or 'Unknown'}\t{row[14] or 'Unknown'}"
        )


@cli.group()
def delete():
    """Delete various Tableau resources"""


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site ID", help="Column name for Site ID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option(
    "--workbook-id-col", default="Workbook ID", help="Column name for Workbook ID"
)
@click.option(
    "--workbook-name-col", default="Workbook Name", help="Column name for Workbook Name"
)
@click.option(
    "--owner-email-col", default="Owner Email", help="Column name for Owner Email"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def workbooks(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    workbook_id_col,
    workbook_name_col,
    owner_email_col,
    owner_name_col,
):
    """Delete Tableau workbooks specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}

    if stdin:
        import sys

        csv_data = sys.stdin
    elif file:
        csv_data = open(file, "r", encoding="utf-8", newline="")
    else:
        raise click.UsageError("Either --file or --stdin must be provided")

    reader = csv.DictReader(csv_data, delimiter=delimiter)

    for row in reader:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        workbook_id = row[workbook_id_col]
        workbook_name = row[workbook_name_col]
        site_name = row[site_name_col]
        owner_name = row[owner_name_col]
        owner_email = row[owner_email_col]

        try:
            server.auth.switch_site(site)
            server.workbooks.delete(workbook_id)
            click.echo(
                f"Successfully deleted workbook: {workbook_name} "
                f"(ID: {workbook_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Owner: {owner_name} ({owner_email})")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting workbook {workbook_name} "
                f"(ID: {workbook_id}): {str(e)}",
                err=True,
            )
        except Exception as e:
            click.echo(f"Unexpected error: {str(e)}", err=True)

    if not stdin:
        csv_data.close()

    server.auth.sign_out()


@delete.command()
@click.option("--file", type=click.Path(exists=True), help="Path to the CSV file")
@click.option("--stdin", is_flag=True, help="Read from stdin instead of a file")
@click.option("--delimiter", default="\t", help="Delimiter used in the CSV file")
@click.option("--site-id-col", default="Site ID", help="Column name for Site ID")
@click.option("--site-name-col", default="Site Name", help="Column name for Site Name")
@click.option(
    "--datasource-id-col", default="Datasource ID", help="Column name for Datasource ID"
)
@click.option(
    "--datasource-name-col",
    default="Datasource Name",
    help="Column name for Datasource Name",
)
@click.option(
    "--owner-email-col", default="Owner Email", help="Column name for Owner Email"
)
@click.option(
    "--owner-name-col", default="Owner Name", help="Column name for Owner Name"
)
@click.pass_context
def datasources(
    ctx,
    file,
    stdin,
    delimiter,
    site_id_col,
    site_name_col,
    datasource_id_col,
    datasource_name_col,
    owner_email_col,
    owner_name_col,
):
    """Delete Tableau datasources specified in a CSV file or from stdin."""
    config = load_config(ctx.obj["config"])
    server = authenticate(config)

    # Get all sites to create a mapping of site LUID to site object
    all_sites, _ = server.sites.get()
    site_luid_to_site = {site.id: site for site in all_sites}

    if stdin:
        import sys

        csv_data = sys.stdin
    elif file:
        csv_data = open(file, "r", encoding="utf-8", newline="")
    else:
        raise click.UsageError("Either --file or --stdin must be provided")

    reader = csv.DictReader(csv_data, delimiter=delimiter)

    for row in reader:
        site_luid = row[site_id_col]
        site = site_luid_to_site.get(site_luid)
        datasource_id = row[datasource_id_col]
        datasource_name = row[datasource_name_col]
        site_name = row[site_name_col]
        owner_name = row[owner_name_col]
        owner_email = row[owner_email_col]

        try:
            server.auth.switch_site(site)
            server.datasources.delete(datasource_id)
            click.echo(
                f"Successfully deleted datasource: {datasource_name} "
                f"(ID: {datasource_id}) from site: {site_name} (ID: {site_luid})"
            )
            click.echo(f"Owner: {owner_name} ({owner_email})")
        except TSC.ServerResponseError as e:
            click.echo(
                f"Error deleting datasource {datasource_name} "
                f"(ID: {datasource_id}): {str(e)}",
                err=True,
            )
        except Exception as e:
            click.echo(f"Unexpected error: {str(e)}", err=True)

    if not stdin:
        csv_data.close()

    server.auth.sign_out()


if __name__ == "__main__":
    cli(ctx={}, config=get_default_config_path())
