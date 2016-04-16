"""
Play with trust:

for player in game:
    if current player:
        send move
    else:
        listen for move
        receive move
decide winner


Play trusting no one:

Swap hashes:
    for player in game:
        if current player:
            send hasher(move + salt)
        else:
            listen for hash
            receive hash

Swap salts:
    for player in game:
        if current player:
            send move + salt
        else:
            listen for move + salt
            receive move + salt
            verify hasher(move + salt) == hash

decide winner
"""
