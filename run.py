from flaskblog import create_app

app = create_app() 

# run the app with: python flaskblog.py
if __name__ == '__main__':
    app.run(debug=True)
