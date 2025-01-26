from website import create_app

if __name__ == '__main__':
    # Create the app using the __init__.py file
    app = create_app()
    # Run the app
    app.run(debug=True, host='0.0.0.0')