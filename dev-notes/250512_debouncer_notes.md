
# examples of how to handle the various button actions:

while True:
    switch.update()
    if switch.short_count == 1:
        print("Short Press Activate!")
        enablePaSystemNormal()
    if switch.long_press:
        print("Long Press")
    if switch.short_count != 0:
        print("Short Press Count =", switch.short_count)
    if switch.long_press and switch.short_count == 1:
        print("That's a long double press !")