# Mosquitto MQTT Broker Setup

## Initial Password Configuration

Before starting Mosquitto, you MUST create a password file:

```bash
# Create password file for MQTT user
docker run --rm -it -v $(pwd)/docker/mosquitto:/mosquitto/config eclipse-mosquitto mosquitto_passwd -c /mosquitto/config/passwd mqtt

# Or if docker/mosquitto is in current directory:
docker run --rm -it -v ./docker/mosquitto:/mosquitto/config eclipse-mosquitto mosquitto_passwd -c /mosquitto/config/passwd mqtt
```

Enter a strong password when prompted.

## Add Additional Users

```bash
# Add another user (without -c flag to append)
docker run --rm -it -v ./docker/mosquitto:/mosquitto/config eclipse-mosquitto mosquitto_passwd /mosquitto/config/passwd homeassistant
```

## File Permissions

The `passwd` file must be readable by the mosquitto container:

```bash
chmod 644 docker/mosquitto/passwd
```

## Testing Connection

```bash
# Subscribe to test topic
mosquitto_sub -h localhost -p 1883 -u mqtt -P your-password -t test/#

# Publish test message
mosquitto_pub -h localhost -p 1883 -u mqtt -P your-password -t test/message -m "Hello MQTT"
```
