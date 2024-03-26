from enigma.machine import EnigmaMachine

# setup machine according to specs from a real Enigma Machine
machine = EnigmaMachine.from_key_sheet(
       rotors='II IV V',
       reflector='B',
       ring_settings=[1, 20, 11],
       plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')

# set machine initial starting position
machine.set_display('WXC')

# encrypt the message key
msg_key = machine.process_text('KCH')

# decrypt the message key
machine.set_display('WXC')
decoded_msg_key = machine.process_text(msg_key)

print(f"Encoded message key: {msg_key}")
print(f"Decoded message key: {decoded_msg_key}")

# Assuming the message key is now set to the encoded message key for both sender and receiver
# Set the Enigma machine to the initial position for the actual message encoding/decoding
machine.set_display(msg_key)

# Encrypt a message
message = "HELLO WORLD"
encrypted_message = machine.process_text(message)

# To decrypt, the machine should be reset to the same state as when it started encrypting
machine.set_display(msg_key)
decrypted_message = machine.process_text(encrypted_message)

print(f"Original Message: {message}")
print(f"Encrypted Message: {encrypted_message}")
print(f"Decrypted Message: {decrypted_message}")
