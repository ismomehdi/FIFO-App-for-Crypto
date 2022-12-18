import inspect

if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

from invoke import task

@task
def build(ctx):
    try:
        ctx.run('psql < db/schema/schema.sql', pty=True)
        ctx.run('psql < db/views/buy_amounts.sql', pty=True)
        ctx.run('psql < db/views/sell_amounts.sql', pty=True)
        ctx.run('psql < db/views/cumulative_sell_cost.sql', pty=True)
        ctx.run('psql < db/views/profit_and_loss.sql', pty=True)
        ctx.run('psql < db/indexes/portfolio_id.sql', pty=True)
    except:
        raise Exception('Failed to build database. Make sure you are in the root directory of the project.')

@task
def buildfly(ctx):
    try:
        ctx.run('fly postgres connect -a tsoha-fifo-db < db/schema/schema.sql', pty=True)
        ctx.run('fly postgres connect -a tsoha-fifo-db < db/views/buy_amounts.sql', pty=True)
        ctx.run('fly postgres connect -a tsoha-fifo-db < db/views/sell_amounts.sql', pty=True)
        ctx.run('fly postgres connect -a tsoha-fifo-db < db/views/cumulative_sell_cost.sql', pty=True)
        ctx.run('fly postgres connect -a tsoha-fifo-db < db/views/profit_and_loss.sql', pty=True)
        ctx.run('fly postgres connect -a tsoha-fifo-db < db/indexes/portfolio_id.sql', pty=True)
    except:
        raise Exception('Failed to build database. Make sure you are in the root directory of the project.')

@task
def destroy(ctx):
    try:
        ctx.run('psql < db/for_dev/destroy.sql', pty=True)
    except:
        raise Exception('Failed to destroy database. Make sure you are in the root directory of the project.')