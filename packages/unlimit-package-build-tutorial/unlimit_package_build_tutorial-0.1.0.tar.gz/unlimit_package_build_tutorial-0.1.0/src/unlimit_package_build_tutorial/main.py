from jinja2 import Environment, FileSystemLoader
import os

def render_template(template_name, **context):
    """
    Renders a template from the `templates` folder with the given context.
    """
    # Get the directory of the current file
    current_dir = os.path.dirname(__file__)
    templates_dir = os.path.join(current_dir, "templates")

    # Initialize the Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Load the template
    template = env.get_template(template_name)

    # Render the template with the given context
    return template.render(**context)

def main():
    # Example context
    context = {
        "store_name": "Example Store",
        "message": "Welcome to our online store!"
    }

    # Render and print the template
    output = render_template("store.html", **context)
    print(output)

if __name__ == "__main__":
    main()