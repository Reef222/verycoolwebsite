#netstat -ano|findstr 8080
#tskill
from website import create_app
from waitress import serve

if __name__ == "__main__":
    app = create_app()
    #serve(app, host='192.168.68.101', port=8080, threads=10000)
    app.run(port=8080, debug=True)
