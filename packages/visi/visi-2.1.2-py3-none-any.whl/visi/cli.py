import click
import requests


@click.group()
def cli():
    pass


@cli.command()
def hello():
    click.echo("Hello, World!")


@cli.command()
@click.option(
    "--option", type=click.Choice(["luggage", "cat", "option3"]), help="Pick an option"
)
@click.option("--width", type=int, help="Specify the width")
@click.option("--height", type=int, help="Specify the height")
def mock(option, width, height):
    name = "mock_"
    name += option
    import random

    name += str(random.randint(1, 10000))
    if not option or option == "luggage":
        from .luggage import conveyor_belt

        conveyor_data_uri = conveyor_belt
        import base64

        if "data:image/jpeg;base64," in conveyor_data_uri:
            conveyor_data_uri = conveyor_data_uri.replace("data:image/jpeg;base64,", "")
        conveyor_data_uri = base64.b64decode(conveyor_data_uri)
        with open(name + ".jpg", "wb") as f:
            f.write(conveyor_data_uri)
        pass
    width = width or 200
    height = height or 200

    if option == "cat" or not option:
        response = requests.get(
            "https://cataas.com/cat?width=" + str(width) + "&height=" + str(height)
        )
        import random

        opts = ["full", "blaze", "act", "inst", "woo"]
        opts2 = ["box", "way", "play", "tune"]
        name = random.choice(opts) + random.choice(opts2)
        with open(f"{name}.jpg", "wb") as f:
            f.write(response.content)
        click.echo(f"Downloaded image to {name}.jpg")

    if width and height:
        click.echo(f"Width: {width}, Height: {height}")


@cli.command()
@click.option("--norm", type=click.Path(exists=True), help="Path to the image file")
def bbox(norm):
    click.echo(f"Processing image: {norm}")


if __name__ == "__main__":
    cli()
