from app.server import app

def main():
    from uvicorn import run
    run(app.app, host="0.0.0.0", port=8000)
    
if __name__ == "__main__":
    main()