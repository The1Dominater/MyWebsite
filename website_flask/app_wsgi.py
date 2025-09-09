from website import create_app

# Create the app using the __init__.py file
# Must be outside if statement for gunicorn to access app obj
app = create_app()

# Run the app
if __name__ == '__main__':
    app.run()