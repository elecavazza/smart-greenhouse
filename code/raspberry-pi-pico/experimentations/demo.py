message1 = "SENSOR:TEMP:24.6"
message2 = "RELAY:LED:ON"

message = message2
parts = message.split(":")

if parts[0] == "SENSOR":
    print(f"my sensor reading is {parts[2]} for {parts[1]}")
elif parts[0] == "RELAY":
    print(f"my relay {parts[1]} changed to {parts[2]}")