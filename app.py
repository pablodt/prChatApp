from chatapp import create_app

if __name__ == '__main__':
    chatapp = create_app()
    chatapp.run(debug=True)