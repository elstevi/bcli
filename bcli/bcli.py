import click
from libbhyve.vm import VM

@click.group()
def cli():
    """ Manages libbhyve vm's """

@cli.command('create')
@click.argument('vm_name')
def create(vm_name):
    """ Creates a VM """
    myvm = VM('base.conf')
    myvm.name = vm_name
    myvm.save()
    click.echo("VM Created")

@cli.command('destroy')
@click.argument('vm_name')
def destroy(vm_name):
    """ Destroys a VM """
    myvm = VM(vm_name)
    myvm.delete()

@cli.command('restart')
@click.argument('vm_name')
def restart(vm_name):
    """ Restart a VM """
    myvm = VM(vm_name)
    myvm.restart()

@cli.command('start')
@click.argument('vm_name')
def start(vm_name):
    """ Start a VM """
    myvm = VM(vm_name)
    myvm.start()

@cli.command('stop')
@click.argument('vm_name')
def stop(vm_name):
    """ Stop a VM """
    myvm = VM(vm_name)
    myvm.stop()

@cli.command('status')
@click.argument('vm_name')
def status(vm_name):
    """ Status a VM """
    myvm = VM(vm_name)
    click.echo(myvm.status())


if __name__ == '__main__':
        cli()
