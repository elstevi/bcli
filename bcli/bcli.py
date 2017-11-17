import click
from collections import OrderedDict
from libbhyve.vm import VM
from libbhyve.disk import Disk
from libbhyve.nic import Nic
from libbhyve.config import VM_DIR
from os import listdir
from tabulate import tabulate

@click.group()
def cli():
    """ Manages libbhyve vm's """

@cli.command('list')
@click.option('--tablefmt', prompt=False, required=False, default='grid')
def list(tablefmt):
    """ Lists all virtual machines and their status """
    all_vms = listdir(VM_DIR)
    vms = [] 
    i = 0
    for vm_name in all_vms:
        thisvm = VM(vm_name)
        vms.append(OrderedDict([
                ('name', thisvm.name),
                ('status', thisvm.status()),
                ('ncpus', thisvm.ncpus),
                ('memory', thisvm.memory),
                ]))
        i = i+1
    click.echo(tabulate(vms, headers='keys', tablefmt=tablefmt))

@cli.command('create')
@click.option('--com1', default='stdio')
@click.option('--com2', default=None)
@click.option('--disk', multiple=True, prompt=True)
@click.option('--iso', default=None)
@click.option('--memory', default=1024)
@click.option('--name', prompt=True)
@click.option('--ncpus', default=1)
@click.option('--network', prompt=True, multiple=True)
@click.option('--onboot/--offboot', prompt=True, default=False)
def create(name, onboot, com1, com2, disk, iso, memory, ncpus, network):
    """ Creates a VM """
    myvm = VM(None)
    myvm.name = name
    myvm.auto_start = onboot
    myvm.com1 = com1
    myvm.com2 = com2
    myvm.iso  = iso
    myvm.memory  = memory
    myvm.ncpus  = ncpus
    for disc in disk:
        myvm.disk.append(Disk(disc, 'ahci-hd'))
    for nic in network:
        myvm.network.append(Nic(nic, 'virtio-net'))
    myvm.save()
    click.echo("VM Created")


@cli.command('destroy')
@click.argument('vm_name')
@click.confirmation_option(help='Are you sure you want to destroy this VM?')
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
