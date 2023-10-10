# Picture Frame

A web-app to update the photograph on a [Pimoroni Inky Impression 5.7"](https://shop.pimoroni.com/products/inky-impression-5-7?variant=32298701324371).

Controlled with a Raspberry Pi Zero W.

## Local Setup Reqs:

- Python3
- Flask
- Pillow

## Run local sever

```python
flask --app application --debug run
```

## Deployment

- Install `gunicorn` and `nginx`
- Edit and Use the external config to set up a systemd daemon to run gunicorn
- Edit and Use the external config to set up an nginx reverse proxy