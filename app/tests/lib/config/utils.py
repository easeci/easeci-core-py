from app.lib.io.io_file import File


def generate_fake_config():
    path = '/tmp/general.yml'
    content = "main:\n" \
              "  paths:\n" \
              "    temp: /tmp/ease\n" \
              "    home: /usr/local/ease\n" \
              "\n" \
              "output:\n" \
              "  queue:\n" \
              "    max-size: 100\n" \
              "  autopublishing: False\n" \
              ""
    return File(path, content)
