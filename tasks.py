import inspect
from invoke import task

if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec


@task
def build(ctx):
    try:
        ctx.run('psql < db/schema/schema.sql', pty=True)
        ctx.run('psql < db/views/buy_amounts.sql', pty=True)
        ctx.run('psql < db/views/sell_amounts.sql', pty=True)
        ctx.run('psql < db/views/cumulative_sell_cost.sql', pty=True)
        ctx.run('psql < db/views/profit_and_loss.sql', pty=True)
        ctx.run('psql < db/indexes/portfolio_id.sql', pty=True)
    except Exception as exc:
        raise Exception(
            'Failed to build database. Make sure you are in the root \
                directory of the project.') from exc


@task
def destroy(ctx):
    try:
        ctx.run('psql < db/for_dev/destroy.sql', pty=True)
    except Exception as exc:
        raise Exception(
            'Failed to destroy database. Make sure you are in the root \
                directory of the project.') from exc
