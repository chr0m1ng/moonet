# Moonet — minimal backend to play YouTube audio on Raspberry Pi via mpv

## API Endpoints

- `GET /health` — liveness check
- `GET /status` — mpv status (pause, volume, time, duration, title)
- `POST /control/play` — body: `{ "url": "https://..." }` or `{ "query": "white noise" }` (optional `volume`)
- `POST /control/pause` — pause playback
- `POST /control/resume` — resume playback
- `POST /control/stop` — stop playback
- `POST /control/volume` — `{ "value": 0..100 }` or `{ "delta": +/-5 }`
- `GET /search?q=...` — YouTube search via yt-dlp

## Notes

- mpv is controlled via IPC UNIX socket at `/tmp/moonet-mpv.sock`.
- Bluetooth auto-reconnect planned in `services/bluetooth.py` (stub).

## Activation

```sh
sudo systemctl daemon-reload
sudo systemctl enable bt-auto-connect.service
sudo systemctl enable moonet.service
sudo systemctl start bt-auto-connect.service
sudo systemctl start moonet.service
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh
hostname -I
```
