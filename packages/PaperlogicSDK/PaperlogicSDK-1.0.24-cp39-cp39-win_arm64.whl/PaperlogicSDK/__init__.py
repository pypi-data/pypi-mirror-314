import click
import sys
from .sign import sign_pplg
from .timestamp import timestamp_pplg

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)

CLI_VERSION = '1.0.24'
@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', is_flag=True, help="Show version and exit.")
@click.pass_context
def cli(ctx, version):
    if version:
        click.echo(f"pplg version {CLI_VERSION}")
        ctx.exit()

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option('-pki', '--pki', type=int, required=True, default=0, 
    help='''
        Certificate type to sign \n
        0: Paperlogic certificate \n
        1: JCAN certificate \n
        2: Company seal certificate \n
        3: NRA-PKI certificate \n
        4: E-Seal HSM	 \n
    '''
)
@click.option('-uid', '--user_id', type=int, help='UserID')
@click.option('-e', '--email', type=str, help='Email')
@click.option('-pwd', '--pdf_password', type=str, help='PDF File Password')
@click.option(
    '-env', '--environment',
    type=click.Choice(['dev', 'stg', 'prod'], case_sensitive=False),
    default='stg',
    help='Environment to run the SDK (dev/stg/prod)'
)
def sign(input_file, output_file, api_token, tenant_id, pki, user_id=None, email=None, environment='stg', pdf_password=None):
    """Sign document"""
    if environment == 'dev':
        click.echo("Development mode activated")
    elif environment == 'stg':
        click.echo("Staging mode activated")
    elif environment == 'prod':
        click.echo("Production mode activated")

    click.echo("Start Signing")

    kwargs = {'pdf_password': pdf_password} if pdf_password else {}
    res, msg = sign_pplg(input_file, output_file, api_token, tenant_id, pki, user_id, email, environment, **kwargs)

    if res:
        click.echo(f"Status: success")
        sys.exit(0)
    else:
        if msg == 'error.password.required':
            click.echo(f'''
                    Status: failure. \n 
                    Error: error.password.incorrect \n
                    ErrorMessage: PDF file's password is not correct. Please provide correct password.''', 
                err=True
            )
        elif msg == 'error.pki.user_id.required':
            click.echo(f'''
                    Status: failure. \n 
                    Error: error.pki.user_id.required \n
                    ErrorMessage: Sign by company seal requires user_id (group_id).''', 
                err=True
            )
        elif msg == 'error.wrong_tenant':
            click.echo(f'''
                    Status: failure. \n 
                    Error: error.wrong_tenant \n
                    ErrorMessage: You don't have permission on this tenant.''', 
                err=True
            )
        elif msg == 'error.sdk_permission':
            click.echo(f'''
                    Status: failure. \n 
                    Error: error.sdk_permission \n
                    ErrorMessage: Your tenant does not have permission on this sdk function.''', 
                err=True
            )
        elif msg == 'message.errors.certificate.not-exists':
            click.echo(f'''
                    Status: failure. \n 
                    Error: message.errors.certificate.not-exists \n
                    ErrorMessage: Certificate file is not exists.''', 
                err=True
            )
        elif msg == 'message.errors.users.not-permission':
            click.echo(f'''
                    Status: failure. \n 
                    Error: message.errors.users.not-permission \n
                    ErrorMessage: User does not have permission.''', 
                err=True
            )
        else:
            click.echo(f'''
                    Status: failure. \n 
                    Error: error.other
                    ErrorMessage: {msg}
                ''', 
                err=True
            )
        sys.exit(1)

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option('-pwd', '--pdf_password', type=str, help='PDF File Password')
@click.option(
    '-env', '--environment',
    type=click.Choice(['dev', 'stg', 'prod'], case_sensitive=False),
    default='stg',
    help='Environment to run the SDK (dev/stg/prod)'
)
def timestamp(input_file, output_file, api_token, tenant_id, environment='stg', pdf_password=None):
    """Timestamp document"""
    if environment == 'dev':
        click.echo("Development mode activated")
    elif environment == 'stg':
        click.echo("Staging mode activated")
    elif environment == 'prod':
        click.echo("Production mode activated")

    click.echo(f"Start Timestamp")

    kwargs = {'pdf_password': pdf_password} if pdf_password else {}
    res, msg = timestamp_pplg(input_file, output_file, api_token, tenant_id, environment, **kwargs)

    if res:
        click.echo(f"Status: success")
        sys.exit(0)
    else:
        if msg == 'error.password.required':
            click.echo(f'''
                    Status: failure. \n 
                    Error: error.password.incorrect \n
                    ErrorMessage: PDF file's password is not correct. Please provide correct password.''', 
                err=True
            )
        else:
            click.echo(f'''
                Status: failure''', 
            err=True)
        sys.exit(1)
