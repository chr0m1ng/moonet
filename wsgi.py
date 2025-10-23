from moonet import create_app

app = create_app()


def main():
  app.run(
    host=app.config.get("HOST", "0.0.0.0"),
    port=app.config.get("PORT", 8080),
    debug=app.config.get("DEBUG", False),
  )


if __name__ == "__main__":
  main()
